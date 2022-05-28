# Отладчик печатных форм для МИС "Самсон"
## Демонстрация работы
https://youtu.be/OAk_T5k4z1g

## Установка:
Для установки модуля, скопируйте пакет **itnovPackages** в корень Самсона.  
Затем, внесите правки в модули **s11main**, **PrintTemplates** и **ReportView**.

## Пример установки:
Вносим правки в модуль **s11main**. Создаем в объекте приложения PyQt (QtGui.qApp) необходимые переменные.
Необходимо придумать способ, как включать отладку форм в приложении. Мы решили сделать это, добавив параметры запуска:

_s11main.main():~7494_
```python
...
    # TreOne: Кастомные аргументы
    parser.add_option(
        '--itnov_debug',
        dest='isPrintDebugEnabled',
        help='run in debug mode',
        metavar='is enable (1-true)?',
        default=0
    )
    # TreOne: END
...
```

Затем сохраним необходимые переменные в объект приложения PyQt. Для корректной работы необходимо две переменные:
 - QtGui.qApp.isPrintDebugEnabled
 - QtGui.qApp.debugPrintData

_s11main.main():~7548_
```python
...
    QtGui.qApp = app

    app.applyDecorPreferences() # надеюсь, что это поможет немного сэкономить при создании гл.окна
	
    # TreOne: Отладка печатных форм
    QtGui.qApp.isPrintDebugEnabled = bool(int(options.isPrintDebugEnabled))
    from itnovPackages.PrintDebug.Utils import DebugPrintData
    QtGui.qApp.debugPrintData = DebugPrintData()
    # TreOne: END
	
    MainWindow = CS11MainWindow(bgParams)
    app.mainWindow = MainWindow
    app.applyDecorPreferences() # применение максимизации/полноэкранного режима к главному окну
...
```

Вносим правки в **library/PrintTemplates.py** в методы **getTemplate()** и **applyTemplateInt()** для сохранения необходимой для отладки информации.

_library.PrintTemplates.getTemplate()_
```python
...
def getTemplate(templateId):
    u'''Возвращает код шаблона печати и код типа содержимого (html/exaro/svg).'''
    content = None
    record = QtGui.qApp.db.getRecord('rbPrintTemplate', '*', templateId)
    if record:
	
        # TreOne: Сохраняем данные для отладки печатной формы
        if QtGui.qApp.isPrintDebugEnabled:
            QtGui.qApp.debugPrintData.name = forceString(record.value('name'))
            QtGui.qApp.debugPrintData.context = forceString(record.value('context'))
            QtGui.qApp.debugPrintData.code = forceString(record.value('code'))
            QtGui.qApp.debugPrintData.groupName = forceString(record.value('groupName'))
        # TreOne: END
		
        name = forceString(record.value('name'))
        fileName = forceString(record.value('fileName'))
...
```

_library.PrintTemplates.applyTemplateInt()_
```python
...
def applyTemplateInt(widget, name, template, data, templateType=htmlTemplate, fromWidget=None, signAndAttachHandler=None):
    # u'''Выводит на печать шаблон печати по имени name с кодом template и данными data'''
    pageFormat = CPageFormat(pageSize=CPageFormat.A4, orientation=CPageFormat.Portrait, leftMargin=5, topMargin=5, rightMargin=5,  bottomMargin=5)
    
    # TreOne: Сохраняем данные для отладки печатной формы
    if QtGui.qApp.isPrintDebugEnabled:
        QtGui.qApp.debugPrintData.template = template
        QtGui.qApp.debugPrintData.data = data
        QtGui.qApp.debugPrintData.pageFormat = pageFormat
    # TreOne: END

    if templateType == exaroTemplate and not exaroSupport:
        templateType = htmlTemplate
        templateResult = exaroFallback()
...
```


Вносим правки в **Reports/ReportView.py** в класс **CReportViewDialog**. Нам необходимо добавить тут несколько методов.
Это необходимо, чтобы включить кнопку отладки в печатной форме, запустить отладку при нажатии кнопки, и обновлять шаблон при необходимости.

_Reports.ReportView.CReportViewDialog_
```python
...
class CReportViewDialog(QtGui.QDialog, Ui_ReportViewDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
...
        self.btnPrint.setFocus(Qt.OtherFocusReason)
        self._setFindVisible(False)
        self.txtReport.actFind.triggered.connect(self.on_actFind_triggered)

    # TreOne: Отладка печатной формы
    def enableDebugButton(self):
        from itnovPackages.PrintDebug.PrintTemplateDebugWindow import PrintTemplateDebugWindow
        self.fsWatcher = None
        self.debugView = PrintTemplateDebugWindow(self)
        self.btnPrintDebug = QtGui.QPushButton(u'Отладка', self)
        self.btnPrintDebug.setObjectName('btnPrintDebug')
        self.btnPrintDebug.setStyleSheet("QPushButton { background-color: #fff3c4 }")
        self.buttonBox.addButton(self.btnPrintDebug, QtGui.QDialogButtonBox.ActionRole)
        self.btnPrintDebug.clicked.connect(self.startPrintFormDebug)

    @QtCore.pyqtSlot()
    def startPrintFormDebug(self):
        dirPath = QtGui.QFileDialog.getExistingDirectory(
            QtGui.qApp.mainWindow,
            u'Выберите папку для сохранения шаблона:',
            QtGui.qApp.getTemplateDir(),
            QtGui.QFileDialog.ShowDirsOnly
        )
        if dirPath:
            self.debugView.showData(QtGui.qApp.debugPrintData.data)
            debugFilename = os.path.join(unicode(dirPath), u'debug_template.html')
            f = open(debugFilename, 'w')
            f.write(QtGui.qApp.debugPrintData.template.encode('utf8'))
            f.close()
            self.btnPrintDebug.setText(u'ИДЕТ ОТЛАДКА')
            self.btnPrintDebug.setStyleSheet("QPushButton { background-color: #ffcfc4 }")
            self.btnPrintDebug.setEnabled(False)
            self.fsWatcher = QtCore.QFileSystemWatcher([debugFilename])
            self.fsWatcher.connect(self.fsWatcher, QtCore.SIGNAL('fileChanged(QString)'), self.fileChanged)
            self.fileChanged(debugFilename)
            self.debugView.show()

    @QtCore.pyqtSlot(str)
    def fileChanged(self, path):
        import time
        from library.PrintTemplates import compileAndExecTemplate
        try:
            with codecs.open(path, mode='r', encoding='utf-8') as templateFile:
                template = templateFile.read()
            startTime = time.time()
            templateResult = compileAndExecTemplate(
                documentName=QtGui.qApp.debugPrintData.name,
                template=template,
                data=QtGui.qApp.debugPrintData.data,
                pageFormat=QtGui.qApp.debugPrintData.pageFormat
            )
            self.setText(templateResult.content)
            execTime = time.time() - startTime
            self.debugView.showRenderTime(execTime)
        except Exception as e:
            import traceback
            errorTemplate = u"""<h1 style='color: red;'>%s</h1><pre>%s</pre>"""
            self.setText(errorTemplate % (unicode(e), traceback.format_exc()))
    # TreOne: END

    def _setFindVisible(self, value):
        self._findVisible = value
        self.lblFind.setVisible(value)
        self.edtFind.setVisible(value)
...
```
