# -*- coding: utf-8 -*-
"""
Copyright (C) ООО "Системная интеграция" 2012

Эта программа является свободным программным обеспечением.
Вы можете использовать, распространять и/или модифицировать её согласно
условиям GNU GPL версии 3 или любой более поздней версии.
"""
from PyQt4.QtCore import QModelIndex, Qt, pyqtSlot
from PyQt4.QtGui import QAbstractItemView, QApplication, QHeaderView, QMessageBox, QStandardItem, QStandardItemModel, \
    QTreeView

VARIABLE_NAME_ROLE = Qt.UserRole + 501  # Роль: Название переменной
VARIABLE_VALUE_ROLE = Qt.UserRole + 502  # Роль: Значение переменной


class TemplateDataShowItemModel(QStandardItemModel):
    def hasChildren(self, index):
        variable = self.data(index, VARIABLE_VALUE_ROLE).toPyObject()
        if variable is not None:
            valueView = TemplateDataShowTableView.getTypeView(variable)
            return valueView.hasChildren()
        return super(TemplateDataShowItemModel, self).hasChildren(index)


class TemplateDataShowTableView(QTreeView):
    """QTreeView, в котором можно выводить данные шаблона печати."""

    variableViewPlugins = []

    def __init__(self, *__args):
        QTreeView.__init__(self, *__args)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.model = TemplateDataShowItemModel(self)
        self.model.invisibleRootItem()
        self.model.setHorizontalHeaderLabels([u'Переменная', u'Тип переменной', u'Значение'])
        self.setModel(self.model)
        header = self.header()
        header.setResizeMode(QHeaderView.ResizeToContents)

        self.__initViewPlugins()

        self.expanded.connect(self.expandItem)
        self.doubleClicked.connect(self.itemDoubleClicked)

    def __initViewPlugins(self):
        """Регистрируем плагины представления переменных."""
        from itnovPackages.PrintDebug.Views import connectPlugins
        connectPlugins()

    @staticmethod
    def registerViewPlugin(viewPlugin):
        # type: (Type[GeneralTypeView]) -> None
        """Регистрирует плагины представления переменных."""
        TemplateDataShowTableView.variableViewPlugins.append(viewPlugin)

    @staticmethod
    def getTypeView(variable):
        # type: (Any) -> GeneralTypeView
        """Возвращает представление на основе переменной."""
        for typeView in TemplateDataShowTableView.variableViewPlugins:  # type: Type[GeneralTypeView]
            if typeView.isApplicable(variable):
                return typeView(variable)
        raise Exception('A suitable plugin for the variable was not found.')

    @pyqtSlot(dict)
    def showData(self, data):
        """Выводит данные контекста печати."""
        for key in sorted(data.keys()):
            value = data[key]
            childItem = QStandardItem(key)
            childItem.setData(key, VARIABLE_NAME_ROLE)
            childItem.setData(value, VARIABLE_VALUE_ROLE)
            valueView = TemplateDataShowTableView.getTypeView(value)
            childRow = [childItem, QStandardItem(valueView.getType()), QStandardItem(valueView.toString())]
            self.model.appendRow(childRow)

    @pyqtSlot(QModelIndex)
    def expandItem(self, index):
        """Отображает содержимое переменной при разворачивании.

        Для ускорения работы виджета, потомки родительской переменной рассчитываются только в момент,
        когда переменная разворачивается (нажимается "плюсик").
        """
        parentItem = self.model.itemFromIndex(index)
        if not parentItem.hasChildren():
            variable = parentItem.data(VARIABLE_VALUE_ROLE).toPyObject()
            valueView = TemplateDataShowTableView.getTypeView(variable)
            childrenList = valueView.getChildrenList()
            for childrenRow in childrenList:
                parentItem.appendRow(childrenRow)

    @pyqtSlot(QModelIndex)
    def itemDoubleClicked(self, index):
        """При двойном клике на переменную, мы копируем путь к ней в буфер обмена."""
        try:
            variableName = self.getPathNode(index)
            self.parent().statusBar.showMessage(u'Скопировано в буфер обмена: "{}"'.format(variableName), 3000)
            # Пытаемся вставить в буфер обмена.
            clipboard = QApplication.clipboard()
            if clipboard is not None:
                clipboard.setText(variableName)
        except PathfindingException:
            QMessageBox.warning(self.parent(), u'Внимание!', u'Невозможно определить путь переменной.', QMessageBox.Ok)

    def getPathNode(self, index):
        """Возвращает путь до переменной, который можно использовать в шаблоне печати.

        Функция рекурсивно вызывает сама себя. Если путь до переменной определить не удастся, выбрасывается исключение,
        чтобы прервать рекурсию и сообщить о провале.
        """
        if index == self.rootIndex():
            return u''
        firstItemInRow = self.model.sibling(index.row(), 0, index)
        variableName = firstItemInRow.data(VARIABLE_NAME_ROLE).toPyObject()
        if not variableName:
            raise PathfindingException()
        variableName = str(variableName)
        # Если именем является число, значит выбран элемент из списка. Можно выдавать ошибку в таких случаях,
        #  так как списки все таки надо перебирать. Но можно вернуть элемент по индексу.
        if variableName.isdigit():
            variableName = u"__getitem__({})".format(variableName)
        parentNode = self.model.parent(firstItemInRow)
        fullPath = u'{}.{}'.format(self.getPathNode(parentNode), variableName)
        fullPath = fullPath.strip(u'.')
        return fullPath


class PathfindingException(Exception):
    """Исключение при поиске пути переменной."""
    pass
