# -*- coding: utf-8 -*-
"""
Copyright (C) ООО "Системная интеграция" 2012

Эта программа является свободным программным обеспечением.
Вы можете использовать, распространять и/или модифицировать её согласно
условиям GNU GPL версии 3 или любой более поздней версии.
"""

from PyQt4 import QtGui
from PyQt4.QtCore import Qt, pyqtSlot
from PyQt4.QtGui import QStatusBar

from itnovPackages.PrintDebug.PrintTemplateDebugWindow_UI import Ui_PrintTemplateDebug


class PrintTemplateDebugWindow(QtGui.QDialog, Ui_PrintTemplateDebug):
    """Интерфейс для отладки печатных форм."""
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)
        self.lblContext.setText(QtGui.qApp.debugPrintData.context)
        self.lblCode.setText(QtGui.qApp.debugPrintData.code)
        self.lblName.setText(QtGui.qApp.debugPrintData.name)
        self.lblGroup.setText(QtGui.qApp.debugPrintData.groupName)

        # Добавляем статус бар программно, так как QTDesigner не может это сделать.
        self.statusBar = QStatusBar(self)
        self.statusBar.setObjectName('statusBar')
        self.verticalLayout.addWidget(self.statusBar)

    @pyqtSlot(dict)
    def showData(self, data):
        """Выводит данные в окне отладки."""
        self.tvTemplateDataShow.showData(data)

    @pyqtSlot(float)
    def showRenderTime(self, renderTime):
        """Отображает скорость рендеринга шаблона печати."""
        renderTimeStr = u"{:.2f} с.".format(renderTime)
        self.lblTime.setText(renderTimeStr)
