# -*- coding: utf-8 -*-
"""
Copyright (C) ООО "Системная интеграция" 2012

Эта программа является свободным программным обеспечением.
Вы можете использовать, распространять и/или модифицировать её согласно
условиям GNU GPL версии 3 или любой более поздней версии.
"""

from PyQt4.QtGui import QStandardItem

from itnovPackages.PrintDebug.TemplateDataShowTableView import TemplateDataShowTableView, VARIABLE_NAME_ROLE, \
    VARIABLE_VALUE_ROLE


class DebugPrintData:
    """Класс для передачи параметров шаблона печати в окно отладки."""
    def __init__(self):
        self.context = None
        self.code = None
        self.name = None
        self.groupName = None
        self.data = None
        self.template = None
        self.pageFormat = None


def createChildRow(variableName, variableValue):
    # type: (str, Any) -> List[QStandardItem]
    """Возвращает строку с представлением переменной для дерева переменных (TemplateDataShowTableView)."""
    childItem = QStandardItem(variableName)
    childItem.setData(variableName, VARIABLE_NAME_ROLE)
    childItem.setData(variableValue, VARIABLE_VALUE_ROLE)
    valueView = TemplateDataShowTableView.getTypeView(variableValue)
    childRow = [childItem, QStandardItem(valueView.getType()), QStandardItem(valueView.toString())]
    return childRow
