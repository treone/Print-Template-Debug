# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'itnovPackages/treone/PrintDebug/PrintTemplateDebugWindow.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_PrintTemplateDebug(object):
    def setupUi(self, PrintTemplateDebug):
        PrintTemplateDebug.setObjectName(_fromUtf8("PrintTemplateDebug"))
        PrintTemplateDebug.resize(1280, 800)
        self.verticalLayout = QtGui.QVBoxLayout(PrintTemplateDebug)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.groupBox = QtGui.QGroupBox(PrintTemplateDebug)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.formLayout_2 = QtGui.QFormLayout(self.groupBox)
        self.formLayout_2.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.label_10 = QtGui.QLabel(self.groupBox)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_10)
        self.lblTime = QtGui.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.lblTime.setFont(font)
        self.lblTime.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.lblTime.setObjectName(_fromUtf8("lblTime"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.FieldRole, self.lblTime)
        self.horizontalLayout.addWidget(self.groupBox)
        self.groupBox1 = QtGui.QGroupBox(PrintTemplateDebug)
        self.groupBox1.setObjectName(_fromUtf8("groupBox1"))
        self.formLayout = QtGui.QFormLayout(self.groupBox1)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label = QtGui.QLabel(self.groupBox1)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.lblContext = QtGui.QLabel(self.groupBox1)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.lblContext.setFont(font)
        self.lblContext.setObjectName(_fromUtf8("lblContext"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.lblContext)
        self.label_3 = QtGui.QLabel(self.groupBox1)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_3)
        self.lblCode = QtGui.QLabel(self.groupBox1)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.lblCode.setFont(font)
        self.lblCode.setObjectName(_fromUtf8("lblCode"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.lblCode)
        self.label_4 = QtGui.QLabel(self.groupBox1)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_4)
        self.lblName = QtGui.QLabel(self.groupBox1)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.lblName.setFont(font)
        self.lblName.setObjectName(_fromUtf8("lblName"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.lblName)
        self.label_5 = QtGui.QLabel(self.groupBox1)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_5)
        self.lblGroup = QtGui.QLabel(self.groupBox1)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.lblGroup.setFont(font)
        self.lblGroup.setObjectName(_fromUtf8("lblGroup"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.lblGroup)
        self.horizontalLayout.addWidget(self.groupBox1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.tvTemplateDataShow = TemplateDataShowTableView(PrintTemplateDebug)
        self.tvTemplateDataShow.setObjectName(_fromUtf8("tvTemplateDataShow"))
        self.verticalLayout.addWidget(self.tvTemplateDataShow)
        self.verticalLayout.setStretch(1, 1)

        self.retranslateUi(PrintTemplateDebug)
        QtCore.QMetaObject.connectSlotsByName(PrintTemplateDebug)

    def retranslateUi(self, PrintTemplateDebug):
        PrintTemplateDebug.setWindowTitle(_translate("PrintTemplateDebug", "Информация", None))
        self.groupBox.setTitle(_translate("PrintTemplateDebug", "Выполнение", None))
        self.label_10.setText(_translate("PrintTemplateDebug", "Время выполнения шаблона:", None))
        self.lblTime.setText(_translate("PrintTemplateDebug", "-----", None))
        self.groupBox1.setTitle(_translate("PrintTemplateDebug", "Параметры шаблона", None))
        self.label.setText(_translate("PrintTemplateDebug", "Контекст:", None))
        self.lblContext.setText(_translate("PrintTemplateDebug", "-----", None))
        self.label_3.setText(_translate("PrintTemplateDebug", "Код:", None))
        self.lblCode.setText(_translate("PrintTemplateDebug", "-----", None))
        self.label_4.setText(_translate("PrintTemplateDebug", "Наименование:", None))
        self.lblName.setText(_translate("PrintTemplateDebug", "-----", None))
        self.label_5.setText(_translate("PrintTemplateDebug", "Группа:", None))
        self.lblGroup.setText(_translate("PrintTemplateDebug", "-----", None))

from itnovPackages.PrintDebug.TemplateDataShowTableView import TemplateDataShowTableView

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    PrintTemplateDebug = QtGui.QWidget()
    ui = Ui_PrintTemplateDebug()
    ui.setupUi(PrintTemplateDebug)
    PrintTemplateDebug.show()
    sys.exit(app.exec_())

