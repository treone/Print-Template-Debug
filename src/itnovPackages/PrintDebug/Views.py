# -*- coding: utf-8 -*-
"""
Copyright (C) ООО "Системная интеграция" 2012

Эта программа является свободным программным обеспечением.
Вы можете использовать, распространять и/или модифицировать её согласно
условиям GNU GPL версии 3 или любой более поздней версии.
"""
from UserList import UserList
from abc import ABCMeta, abstractmethod

from PyQt4 import QtGui
from PyQt4.QtCore import QString
from PyQt4.QtGui import QStandardItem

from Events.ActionInfo import CActionInfo
from itnovPackages.PrintDebug.TemplateDataShowTableView import TemplateDataShowTableView, VARIABLE_NAME_ROLE, \
    VARIABLE_VALUE_ROLE
from itnovPackages.PrintDebug.Utils import createChildRow
from library.PrintInfo import CInfoList
from library.Utils import forceString, formatNum, smartDict


MAX_LIST_SIZE = 20  # Максимальное количество элементов в списках. (большое значение замедлит работу)


def connectPlugins():
    """Подключение плагинов к представлению переменных.

    Порядок важен, будет использоваться первое подошедшее представление.
    """
    if not TemplateDataShowTableView.variableViewPlugins:
        TemplateDataShowTableView.registerViewPlugin(NoneView)  # Представление для None
        TemplateDataShowTableView.registerViewPlugin(CallableView)  # Представление для методов и функций
        TemplateDataShowTableView.registerViewPlugin(CustomRowsListView)  # Helper для внутренних списков

        TemplateDataShowTableView.registerViewPlugin(CInfoListView)  # Представление для объектов класса CInfoList
        TemplateDataShowTableView.registerViewPlugin(ActionInfoView)  # Представление для объектов класса CActionInfo
        TemplateDataShowTableView.registerViewPlugin(SmartDictView)  # Представление для объектов класса smartDict

        TemplateDataShowTableView.registerViewPlugin(ListView)  # Представление для списков
        TemplateDataShowTableView.registerViewPlugin(TupleView)  # Представление для кортежей
        TemplateDataShowTableView.registerViewPlugin(DictView)  # Представление для словарей
        TemplateDataShowTableView.registerViewPlugin(IntView)  # Представление для чисел
        TemplateDataShowTableView.registerViewPlugin(StringView)  # Представление для строк

        TemplateDataShowTableView.registerViewPlugin(ObjectTypeView)  # Общее представление для всех объектов


class GeneralTypeView:
    """Абстрактный класс который должен быть реализован для корректной работы класса-представления."""
    __metaclass__ = ABCMeta

    @staticmethod
    @abstractmethod
    def isApplicable(variable):
        # type: (Any) -> bool
        """Является ли это представление применимым к переменной."""
        raise NotImplementedError

    @abstractmethod
    def getType(self):
        # type: () -> unicode
        """Возвращает тип переменной."""
        raise NotImplementedError

    @abstractmethod
    def toString(self):
        # type: () -> unicode
        """Возвращает строковое значение переменной."""
        raise NotImplementedError

    def hasChildren(self):
        # type: () -> bool
        """Переменная имеет потомков?"""
        return False

    def getChildrenList(self):
        # type: () -> List[QStandardItem]
        """Возвращает список потомков или пустой список, если потомков нет."""
        return []


class ObjectTypeView(GeneralTypeView):
    """Общее представление для всех объектов."""

    def __init__(self, variable):
        self._variable = variable

    @staticmethod
    def isApplicable(variable):
        # В Python все является объектом, даже примитивы.
        return True

    def getType(self):
        return self._variable.__class__.__name__

    def toString(self):
        return forceString(self._variable)

    def hasChildren(self):
        if hasattr(self._variable, '__dict__'):
            # Проверяем словарь пространства имен
            return bool(self._variable.__dict__)
        return False

    def getChildrenList(self):
        childrenList = []

        # Получаем поля объекта
        methods = []
        hiddenFields = []
        privateFields = []
        publicFields = []
        for fieldName in dir(self._variable):
            if not hasattr(self._variable, fieldName):
                continue
            attr = getattr(self._variable, fieldName)
            if callable(attr):
                methods.append(fieldName + '()')
                continue
            if fieldName.startswith('__'):
                hiddenFields.append(fieldName)
                continue
            if fieldName.startswith('_'):
                privateFields.append(fieldName)
                continue
            publicFields.append(fieldName)
        methods.sort()
        hiddenFields.sort()
        privateFields.sort()
        publicFields.sort()

        methodsItem = QStandardItem(u'Методы()')
        boldFont = QtGui.QFont()
        boldFont.setBold(True)
        methodsItem.setFont(boldFont)
        methodsList = CustomRowsList([])
        for methodName in methods:
            childItem = QStandardItem(methodName)
            childItem.setData(methodName, VARIABLE_NAME_ROLE)
            methodsList.append([childItem, QStandardItem(u'Метод')])
        methodsItem.setData(methodsList, VARIABLE_VALUE_ROLE)
        childrenList.append([methodsItem])

        hiddenFieldsItem = QStandardItem(u'__СкрытыеПоля')
        hiddenFieldsItem.setFont(boldFont)
        hiddenFieldsList = CustomRowsList([])
        for fieldName in hiddenFields:
            fieldValue = getattr(self._variable, fieldName)
            childRow = createChildRow(fieldName, fieldValue)
            hiddenFieldsList.append(childRow)
        hiddenFieldsItem.setData(hiddenFieldsList, VARIABLE_VALUE_ROLE)
        childrenList.append([hiddenFieldsItem])

        privateFieldsItem = QStandardItem(u'_ПриватныеПоля')
        privateFieldsItem.setFont(boldFont)
        privateFieldsList = CustomRowsList([])
        for fieldName in privateFields:
            fieldValue = getattr(self._variable, fieldName)
            childRow = createChildRow(fieldName, fieldValue)
            privateFieldsList.append(childRow)
        privateFieldsItem.setData(privateFieldsList, VARIABLE_VALUE_ROLE)
        childrenList.append([privateFieldsItem])

        for fieldName in publicFields:
            fieldValue = getattr(self._variable, fieldName)
            childRow = createChildRow(fieldName, fieldValue)
            childrenList.append(childRow)

        return childrenList


class IntView(GeneralTypeView):
    """Представление для чисел."""

    def __init__(self, variable):
        self._variable = variable

    @staticmethod
    def isApplicable(variable):
        return isinstance(variable, int)

    def getType(self):
        return u'Число'

    def toString(self):
        return unicode(self._variable)


class StringView(GeneralTypeView):
    """Представление для строк."""

    def __init__(self, variable):
        self._variable = variable

    @staticmethod
    def isApplicable(variable):
        return isinstance(variable, (unicode, str, QString))

    def getType(self):
        return u'Строка'

    def toString(self):
        return unicode(self._variable)


class CallableView(GeneralTypeView):
    """Представление для методов и функций."""

    def __init__(self, variable):
        self._variable = variable

    @staticmethod
    def isApplicable(variable):
        return callable(variable)

    def getType(self):
        return u'Метод'

    def toString(self):
        return u''


class ListView(GeneralTypeView):
    """Представление для списков."""

    def __init__(self, variable):
        self._variable = variable

    @staticmethod
    def isApplicable(variable):
        return isinstance(variable, list)

    def getType(self):
        return u'Список'

    def toString(self):
        return u'Список: {}'.format(formatNum(len(self._variable), [u'элемент', u'элемента', u'элементов']))

    def hasChildren(self):
        return True

    def getChildrenList(self):
        childrenList = []
        batch = self._variable[:MAX_LIST_SIZE]
        for idx, value in enumerate(batch):
            variableName = str(idx)  # У элементов списка нет имен переменных. Будем возвращать индекс.
            childRow = createChildRow(variableName, value)
            childrenList.append(childRow)
        hiddenElements = len(self._variable) - len(batch)
        if hiddenElements:
            childrenList.append(QStandardItem(u'Скрыто {}...'.format(
                formatNum(hiddenElements, [u'элемент', u'элемента', u'элементов']))
            ))
        return childrenList or [QStandardItem(u'Нет элементов...')]


class TupleView(ListView):
    """Представление для кортежей."""

    def __init__(self, variable):
        super(TupleView, self).__init__(variable)

    @staticmethod
    def isApplicable(variable):
        return isinstance(variable, tuple)

    def getType(self):
        return u'Кортеж'

    def toString(self):
        return forceString(self._variable)


class DictView(GeneralTypeView):
    """Представление для словарей."""

    def __init__(self, variable):
        self._variable = variable

    @staticmethod
    def isApplicable(variable):
        return isinstance(variable, dict)

    def getType(self):
        return u'Словарь'

    def toString(self):
        return u''

    def hasChildren(self):
        return True

    def getChildrenList(self):
        childrenList = []
        keys = sorted(self._variable.keys())
        for key in keys:
            value = self._variable[key]
            childRow = createChildRow(key, value)
            childrenList.append(childRow)
        return childrenList or [QStandardItem(u'Нет элементов...')]


class ActionInfoView(ObjectTypeView):
    """Представление для объектов класса Events.ActionInfo.CActionInfo"""

    def __init__(self, variable):
        super(ActionInfoView, self).__init__(variable)

    def toString(self):
        if hasattr(self._variable, 'name'):
            return u'Действие "%s"' % self._variable.name
        else:
            return super(ActionInfoView, self).toString()

    @staticmethod
    def isApplicable(variable):
        return isinstance(variable, CActionInfo)

    def getType(self):
        return u'Действие (CActionInfo)'

    def hasChildren(self):
        return True

    def getChildrenList(self):
        childrenList = super(ActionInfoView, self).getChildrenList()
        boldFont = QtGui.QFont()
        boldFont.setBold(True)
        propsList = CustomRowsList([])
        for prop in self._variable:
            childRow = createChildRow(unicode(prop), prop)
            propsList.append(childRow)
        propsFieldsItem = QStandardItem(u'СВОЙСТВА ДЕЙСТВИЯ: {}'.format(len(propsList)))
        propsFieldsItem.setFont(boldFont)
        propsFieldsItem.setData(propsList, VARIABLE_VALUE_ROLE)
        childrenList.insert(0, [propsFieldsItem])
        return childrenList


class SmartDictView(ObjectTypeView):
    """Представление для объектов класса library.Utils.smartDict"""

    def __init__(self, variable):
        super(SmartDictView, self).__init__(variable)

    @staticmethod
    def isApplicable(variable):
        return isinstance(variable, smartDict)

    def getType(self):
        return u'Словарь (smartDict)'

    def toString(self):
        return u''

    def hasChildren(self):
        return True


class CInfoListView(GeneralTypeView):
    """Представление для объектов класса library.PrintInfo.CInfoList"""

    def __init__(self, variable):
        self._variable = variable

    @staticmethod
    def isApplicable(variable):
        return isinstance(variable, CInfoList)

    def getType(self):
        return self._variable.__class__.__name__

    def toString(self):
        className = self._variable.__class__.__name__
        return u'{className}: {size}'.format(className=className, size=len(self._variable))

    def hasChildren(self):
        return True

    def getChildrenList(self):
        childrenList = []

        # Защита от зависания при обработке больших списков
        fullLen = len(self._variable)
        if hasattr(self._variable, 'idList'):
            # Fix для CClientInfoListEx и т.п. (в Самсоне "idList" используется для загрузки "Items",
            #  а это к сожалению генератор, а не итератор, так что загружается сразу весь список из 10к клиентов)
            self._variable.idList = self._variable.idList[:MAX_LIST_SIZE]
        if hasattr(self._variable, 'Items'):
            self._variable.Items = self._variable.Items[:MAX_LIST_SIZE]

        batch = self._variable[:MAX_LIST_SIZE]
        for idx, value in enumerate(batch):
            variableName = str(idx)  # У элементов списка нет имен переменных. Будем возвращать индекс.
            childRow = createChildRow(variableName, value)
            childrenList.append(childRow)
        hiddenElements = fullLen - len(batch)
        if hiddenElements:
            childrenList.append(QStandardItem(u'Скрыто {}...'.format(
                formatNum(hiddenElements, [u'элемент', u'элемента', u'элементов']))
            ))
        return childrenList or [QStandardItem(u'Нет элементов...')]


class NoneView(GeneralTypeView):
    """Представление для None."""

    def __init__(self, variable):
        self._variable = variable

    @staticmethod
    def isApplicable(variable):
        return variable is None

    def getType(self):
        return u'None'

    def toString(self):
        return u''


class CustomRowsList(UserList):
    """Кастомный список переменных. Данный тип списков создан для удобства.

    Пример использования:
        Ваш объект является итерируемым. Вы хотите вывести список методов в нем.

            methodsItem = QStandardItem(u'Методы()')
            methodsItem.setFont(boldFont)
            methodsList = CustomRowsList([])
            for methodName in methods:
                childItem = QStandardItem(methodName)
                childItem.setData(methodName, VariableNameRole)
                methodsList.append([childItem, QStandardItem(u'Метод')])
            methodsItem.setData(methodsList, VariableValueRole)
            childrenList.append([methodsItem])
    """

    def __init__(self, data):
        self.data = data


class CustomRowsListView(GeneralTypeView):
    """Вспомогательный класс для отображения внутренних списков объектов."""

    def __init__(self, variable):
        self._variable = variable  # type: CustomRowsList

    @staticmethod
    def isApplicable(variable):
        return isinstance(variable, CustomRowsList)

    def getType(self):
        return u''

    def toString(self):
        return u''

    def hasChildren(self):
        return True

    def getChildrenList(self):
        return self._variable.data
