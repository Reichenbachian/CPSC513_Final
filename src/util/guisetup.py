import os
from PyQt5 import QtCore, QtGui, QtWidgets
from datetime import datetime
import bisect

import config
from util.repeat import Repeat
from util.scanschedule import ScanSchedule
from counter_measures import CounterMeasures
from util.quarantinedfile import QFileList


class GUISetup(object):
    def __init__(self, main_window):
        self.mainWindow = main_window

        self.centralWidget = None
        self.scanFrame = None
        self.schedScanFrame = None
        self.viewVaultFrame = None
        self.configFrame = None
        self.actionScan = None
        self.actionSchedule_Scan = None
        self.actionConfig = None
        self.actionView_Vault = None
        self.progressBar = None

        self.hodalexIcon = None
        self.scanNowIcon = None
        self.schedScanIcon = None
        self.viewVaultIcon = None
        self.configIcon = None
        self.errorIcon = None

        self.frameFont = None

        self.scan_file_paths = None
        self.scan_schedule = []
        self.vaultList = None

        self.counter_measures = CounterMeasures(config.QUARANTINE_FOLDER)
        
        QFileList.load()
        self._setupUi()

    def _setupUi(self):
        
        self._importIcons()
        self._setupFonts()
        self._setupMainWindow()
        self._setupCentralWidget()
        self._setupScanFrame()
        self._setupSchedScanFrame()
        self._setupViewVaultFrame()
        self._setupConfigFrame()
        self._setupMenuActions()
        self._setupToolbar()

        self.viewVaultFrame.hide()
        self.configFrame.hide()
        self.schedScanFrame.hide()
        self.scanFrame.raise_()

    def _setupMainWindow(self):
        self.mainWindow.setObjectName("MainWindow")
        self.mainWindow.setWindowModality(QtCore.Qt.NonModal)
        self.mainWindow.setEnabled(True)
        self.mainWindow.resize(800, 600)
        self.mainWindow.setWindowTitle("Hodalex Antivirus")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mainWindow.sizePolicy().hasHeightForWidth())
        self.mainWindow.setSizePolicy(sizePolicy)
        self.mainWindow.setMinimumSize(QtCore.QSize(800, 600))
        self.mainWindow.setMaximumSize(QtCore.QSize(800, 600))
        self.mainWindow.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.mainWindow.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.mainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.mainWindow.setDocumentMode(False)
        self.mainWindow.setUnifiedTitleAndToolBarOnMac(False)
        self.mainWindow.setWindowIcon(self.hodalexIcon)

    def _importIcons(self):
        self.hodalexIcon = QtGui.QIcon()
        self.hodalexIcon.addPixmap(QtGui.QPixmap(".\\ui\\resources/antivirus.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        
        self.scanNowIcon = QtGui.QIcon()
        self.scanNowIcon.addPixmap(QtGui.QPixmap(".\\ui\\resources/search.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        
        self.schedScanIcon = QtGui.QIcon()
        self.schedScanIcon.addPixmap(QtGui.QPixmap(".\\ui\\resources/schedule.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        self.viewVaultIcon = QtGui.QIcon()
        self.viewVaultIcon.addPixmap(QtGui.QPixmap(".\\ui\\resources/config.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        self.configIcon = QtGui.QIcon()
        self.configIcon.addPixmap(QtGui.QPixmap(".\\ui\\resources/lock.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        self.errorIcon = QtGui.QIcon()
        self.errorIcon.addPixmap(QtGui.QPixmap(".\\ui\\resources/error.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        
    def _setupFonts(self):
        self.frameFont = QtGui.QFont()
        self.frameFont.setFamily("Avantgarde")
        self.frameFont.setPointSize(22)

    def _setupToolbar(self):
        toolBar = QtWidgets.QToolBar(self.mainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(toolBar.sizePolicy().hasHeightForWidth())
        toolBar.setSizePolicy(sizePolicy)
        toolBar.setMaximumSize(QtCore.QSize(100, 600))
        toolBar.setLayoutDirection(QtCore.Qt.LeftToRight)
        toolBar.setMovable(False)
        toolBar.setObjectName("toolBar")
        toolBar.setWindowTitle("toolBar")
        self.mainWindow.addToolBar(QtCore.Qt.LeftToolBarArea, toolBar)

        toolBar.addAction(self.actionScan)
        toolBar.addSeparator()
        toolBar.addAction(self.actionSchedule_Scan)
        toolBar.addSeparator()
        toolBar.addAction(self.actionView_Vault)
        toolBar.addSeparator()
        toolBar.addAction(self.actionConfig)    
        
    def _setupMenuActions(self):

        self.actionScan = QtWidgets.QAction(self.mainWindow)
        self.actionScan.setIcon(self.scanNowIcon)
        self.actionScan.setObjectName("actionScan")
        self.actionScan.setText("Scan")
        self.actionScan.setToolTip("Scan Files Now")

        self.actionSchedule_Scan = QtWidgets.QAction(self.mainWindow)
        self.actionSchedule_Scan.setIcon(self.schedScanIcon)
        self.actionSchedule_Scan.setObjectName("actionSchedule_Scan")
        self.actionSchedule_Scan.setText("Schedule Scan")
        self.actionSchedule_Scan.setToolTip("Schedule Scan")

        self.actionConfig = QtWidgets.QAction(self.mainWindow)
        self.actionConfig.setIcon(self.viewVaultIcon)
        self.actionConfig.setObjectName("actionConfig")
        self.actionConfig.setText("Config")
        self.actionConfig.setToolTip("Configurations")

        self.actionView_Vault = QtWidgets.QAction(self.mainWindow)
        self.actionView_Vault.setIcon(self.configIcon)
        self.actionView_Vault.setObjectName("actionView_Vault")
        self.actionView_Vault.setText("View Vault")
        self.actionView_Vault.setToolTip("View Vault")

        self.actionView_Vault.triggered.connect(self.scanFrame.hide)
        self.actionScan.triggered.connect(self.scanFrame.show)
        self.actionSchedule_Scan.triggered.connect(self.scanFrame.hide)
        self.actionConfig.triggered.connect(self.scanFrame.hide)
        self.actionView_Vault.triggered.connect(self.configFrame.hide)
        self.actionConfig.triggered.connect(self.configFrame.show)
        self.actionScan.triggered.connect(self.configFrame.hide)
        self.actionSchedule_Scan.triggered.connect(self.configFrame.hide)
        self.actionConfig.triggered.connect(self.schedScanFrame.hide)
        self.actionSchedule_Scan.triggered.connect(self.schedScanFrame.show)
        self.actionScan.triggered.connect(self.schedScanFrame.hide)
        self.actionView_Vault.triggered.connect(self.schedScanFrame.hide)
        self.actionConfig.triggered.connect(self.viewVaultFrame.hide)
        self.actionScan.triggered.connect(self.viewVaultFrame.hide)
        self.actionSchedule_Scan.triggered.connect(self.viewVaultFrame.hide)
        self.actionView_Vault.triggered.connect(self.viewVaultFrame.show)
        QtCore.QMetaObject.connectSlotsByName(self.mainWindow)
    
    def _setupCentralWidget(self):

        self.centralwidget = QtWidgets.QWidget(self.mainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.mainWindow.setCentralWidget(self.centralwidget)
    
    def _setupScanFrame(self):
        self.scanFrame = QtWidgets.QFrame(self.centralwidget)
        self.scanFrame.setGeometry(QtCore.QRect(0, 0, 700, 600))
        self.scanFrame.setMaximumSize(QtCore.QSize(700, 600))
        self.scanFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.scanFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.scanFrame.setObjectName("scanFrame")

        scanLabel = QtWidgets.QLabel(self.scanFrame)
        scanLabel.setEnabled(True)
        scanLabel.setGeometry(QtCore.QRect(0, 0, 750, 62))
        
        scanLabel.setFont(self.frameFont)
        scanLabel.setLayoutDirection(QtCore.Qt.LeftToRight)
        scanLabel.setFrameShape(QtWidgets.QFrame.Panel)
        scanLabel.setFrameShadow(QtWidgets.QFrame.Sunken)
        scanLabel.setLineWidth(1)
        scanLabel.setMidLineWidth(10)
        scanLabel.setTextFormat(QtCore.Qt.PlainText)
        scanLabel.setScaledContents(False)
        scanLabel.setObjectName("scanLabel")
        scanLabel.setText("SCAN")

        scanNowButton = QtWidgets.QPushButton(self.scanFrame)
        scanNowButton.setGeometry(QtCore.QRect(230, 300, 200, 40))
        scanNowButton.setObjectName("scanNowButton")
        scanNowButton.setText("Scan Now")
        scanNowButton.clicked.connect(lambda:self._setupScanNowDialog())

        self.progressBar = QtWidgets.QProgressBar(self.scanFrame)
        self.progressBar.setGeometry(QtCore.QRect(40, 220, 641, 31))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
    
    def _setupScanNowDialog(self):
        selectFileDialog = QtWidgets.QFileDialog(self.mainWindow)
        selectFileDialog.setFileMode(QtWidgets.QFileDialog.Directory)
        selectFileDialog.setViewMode(QtWidgets.QFileDialog.Detail)
        selectFileDialog.setWindowTitle("Select directory to scan...")
        if(selectFileDialog.exec()):
            self.scan_file_paths = selectFileDialog.selectedFiles()
        self.start_scan()


    def _setupSchedScanFrame(self):
        self.schedScanFrame = QtWidgets.QFrame(self.centralwidget)
        self.schedScanFrame.setGeometry(QtCore.QRect(0, 0, 700, 600))
        self.schedScanFrame.setMaximumSize(QtCore.QSize(700, 600))
        self.schedScanFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.schedScanFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.schedScanFrame.setObjectName("schedScanFrame")

        schedScanLabel = QtWidgets.QLabel(self.schedScanFrame)
        schedScanLabel.setEnabled(True)
        schedScanLabel.setGeometry(QtCore.QRect(0, 0, 750, 62))
        schedScanLabel.setFont(self.frameFont)
        schedScanLabel.setLayoutDirection(QtCore.Qt.LeftToRight)
        schedScanLabel.setFrameShape(QtWidgets.QFrame.Panel)
        schedScanLabel.setFrameShadow(QtWidgets.QFrame.Sunken)
        schedScanLabel.setLineWidth(1)
        schedScanLabel.setMidLineWidth(10)
        schedScanLabel.setTextFormat(QtCore.Qt.PlainText)
        schedScanLabel.setScaledContents(False)
        schedScanLabel.setObjectName("schedScanLabel")
        schedScanLabel.setText("SCHEDULE SCAN")
        
        newSchedGroup = QtWidgets.QGroupBox("Add New Schedule", self.schedScanFrame)
        newSchedGroup.setGeometry(QtCore.QRect(30, 75, 600, 220))
        newSchedGroupLayout = QtWidgets.QHBoxLayout()
        newSchedGroup.setLayout(newSchedGroupLayout)
        calendarLayout = QtWidgets.QHBoxLayout()
        newSchedGroupLayout.addLayout(calendarLayout)

        calendarInput = QtWidgets.QCalendarWidget(self.schedScanFrame)
        calendarInput.setVerticalHeaderFormat(QtWidgets.QCalendarWidget.NoVerticalHeader)
        calendarLayout.addWidget(calendarInput)
        newSchedGroupLayout.addSpacerItem(QtWidgets.QSpacerItem(30, 10))

        n2Layout = QtWidgets.QVBoxLayout()
        newSchedGroupLayout.addLayout(n2Layout)
        n3Layout = QtWidgets.QVBoxLayout()
        n2Layout.addLayout(n3Layout)
        timeInputLayout = QtWidgets.QHBoxLayout()
        n3Layout.addLayout(timeInputLayout)
        n3Layout.addSpacerItem(QtWidgets.QSpacerItem(10, 10))

        hourInput = QtWidgets.QComboBox(self.schedScanFrame)
        hourInput.addItem("12")
        for hour in range(1, 12, 1):
            hourInput.addItem(f"{hour:02}")
        minuteInput = QtWidgets.QComboBox(self.schedScanFrame)
        for minute in range(0, 60, 1):
            minuteInput.addItem(f"{minute:02}")
        ampmInput = QtWidgets.QComboBox(self.schedScanFrame)
        ampmInput.addItem("AM")
        ampmInput.addItem("PM")
        timeInputLayout.addWidget(hourInput)
        timeInputLayout.addWidget(minuteInput)
        timeInputLayout.addWidget(ampmInput)
        
        oneTimeButton = QtWidgets.QRadioButton("Once", self.schedScanFrame)
        oneTimeButton.setChecked(True)
        dailyButton = QtWidgets.QRadioButton("Daily", self.schedScanFrame)
        weeklyButton = QtWidgets.QRadioButton("Weekly", self.schedScanFrame)
        monthlyButton = QtWidgets.QRadioButton("Monthly", self.schedScanFrame)
        n3Layout.addWidget(oneTimeButton)
        n3Layout.addWidget(dailyButton)
        n3Layout.addWidget(weeklyButton)
        n3Layout.addWidget(monthlyButton)
        choiceGroup = QtWidgets.QButtonGroup(self.schedScanFrame)
        choiceGroup.addButton(oneTimeButton, int(Repeat.ONCE))
        choiceGroup.addButton(dailyButton, int(Repeat.DAILY))
        choiceGroup.addButton(weeklyButton, int(Repeat.WEEKLY))
        choiceGroup.addButton(monthlyButton, int(Repeat.MONTHLY))

        scheduleButton = QtWidgets.QPushButton(self.schedScanFrame)
        scheduleButton.setText("Schedule")
        n3Layout.addWidget(scheduleButton)

        currentScheduleGroup = QtWidgets.QGroupBox("Current Schedule", self.schedScanFrame)
        currentScheduleGroup.setGeometry(QtCore.QRect(30, 320, 600, 230))
        currSchedGroupLayout = QtWidgets.QHBoxLayout()
        currentScheduleGroup.setLayout(currSchedGroupLayout)

        schedList = QtWidgets.QListWidget(self.schedScanFrame)
        currSchedGroupLayout.addWidget(schedList)

        currSchedButtonLayout = QtWidgets.QVBoxLayout()
        currSchedGroupLayout.addLayout(currSchedButtonLayout)
        deleteSchedButton = QtWidgets.QPushButton("Delete",self.schedScanFrame)
        clearSchedButton = QtWidgets.QPushButton("Clear", self.schedScanFrame)
        currSchedButtonLayout.addSpacerItem(QtWidgets.QSpacerItem(50, 50))
        currSchedButtonLayout.addWidget(deleteSchedButton)
        currSchedButtonLayout.addWidget(clearSchedButton)
        currSchedButtonLayout.addSpacerItem(QtWidgets.QSpacerItem(50, 50))

        scheduleButton.clicked.connect(lambda:self._fetchScheduledDateAndTime(calendarInput, hourInput, minuteInput, ampmInput, schedList, choiceGroup))
        deleteSchedButton.clicked.connect(lambda:self._removeSelectedSchedule(schedList))
        clearSchedButton.clicked.connect(lambda:self._clearSchedule(schedList))

    def _fetchScheduledDateAndTime(self, calendarInput, hourInput, minuteInput, ampmInput, schedList, choiceGroup):
        date = calendarInput.selectedDate()
        year = date.year()
        month = date.month()
        day = date.day()
        hour = hourInput.currentText()
        minute = minuteInput.currentText()
        ampm = ampmInput.currentText()
        repeat = choiceGroup.checkedId()
        new_schedule = ScanSchedule(year, month, day, hour, minute, ampm, repeat)
        if (new_schedule.is_past()):
            self._displayError("Can't schedule a scan in the past!")
        elif (new_schedule not in self.scan_schedule):
            bisect.insort(self.scan_schedule, new_schedule)
            index = self.scan_schedule.index(new_schedule)
            schedList.insertItem(index, QtWidgets.QListWidgetItem(str(new_schedule)))
    
    def _removeSelectedSchedule(self, schedList):
        if (len(self.scan_schedule) > 0 and schedList.currentRow() >= 0):
            confirm = QtWidgets.QMessageBox()
            confirm.setWindowIcon(self.schedScanIcon)
            confirm.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            confirm.setText("Are you sure you want to delete scheduled scan?")
            confirm.setWindowTitle("Delete Scheduled Scan")
            retval = confirm.exec()
            if (retval == QtWidgets.QMessageBox.Yes):
                    index = schedList.currentRow()
                    item = schedList.takeItem(index)
                    schedList.removeItemWidget(item)
                    del self.scan_schedule[index]
    
    def _updateSelectedSchedule(self, schedList):
        if (len(self.scan_schedule) > 0 and schedList.currentRow() >= 0):
            index = schedList.currentRow()
            item = schedList.takeItem(index)
            schedList.removeItemWidget(item)
            schedule = self.scan_schedule[index]
            del self.scan_schedule[index]
            if(schedule.next_schedule() and schedule not in self.scan_schedule):
                bisect.insort(self.scan_schedule, schedule)
                index = self.scan_schedule.index(schedule)
                schedList.insertItem(index, QtWidgets.QListWidgetItem(str(schedule)))
    
    def _clearSchedule(self, schedList):
        if (len(self.scan_schedule) > 0):
            confirm = QtWidgets.QMessageBox()
            confirm.setWindowIcon(self.schedScanIcon)
            confirm.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            confirm.setText("Are you sure you want to remove all scheduled scans?")
            confirm.setWindowTitle("Clear Schedule")
            retval = confirm.exec()
            if (retval == QtWidgets.QMessageBox.Yes):
                for _ in range(len(self.scan_schedule)):
                    item = schedList.takeItem(0)
                    schedList.removeItemWidget(item)
                    del self.scan_schedule[0]

    def _setupViewVaultFrame(self):
        self.viewVaultFrame = QtWidgets.QFrame(self.centralwidget)
        self.viewVaultFrame.setGeometry(QtCore.QRect(0, 0, 700, 600))
        self.viewVaultFrame.setMaximumSize(QtCore.QSize(700, 600))
        self.viewVaultFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.viewVaultFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.viewVaultFrame.setObjectName("viewVaultFrame")

        viewVaultLabel = QtWidgets.QLabel(self.viewVaultFrame)
        viewVaultLabel.setEnabled(True)
        viewVaultLabel.setGeometry(QtCore.QRect(0, 0, 750, 62))
        viewVaultLabel.setFont(self.frameFont)
        viewVaultLabel.setLayoutDirection(QtCore.Qt.LeftToRight)
        viewVaultLabel.setFrameShape(QtWidgets.QFrame.Panel)
        viewVaultLabel.setFrameShadow(QtWidgets.QFrame.Sunken)
        viewVaultLabel.setLineWidth(1)
        viewVaultLabel.setMidLineWidth(10)
        viewVaultLabel.setTextFormat(QtCore.Qt.PlainText)
        viewVaultLabel.setScaledContents(False)
        viewVaultLabel.setObjectName("viewVaultLabel")
        viewVaultLabel.setText("VAULT")

        mainLayout = QtWidgets.QVBoxLayout(self.viewVaultFrame)
        mainLayout.addSpacerItem(QtWidgets.QSpacerItem(10, 55))
        listLayout = QtWidgets.QHBoxLayout()
        mainLayout.addLayout(listLayout)
        mainLayout.addSpacerItem(QtWidgets.QSpacerItem(10, 20))
        self.vaultList = QtWidgets.QTableWidget(self.viewVaultFrame)
        self.vaultList.setRowCount(0)
        self.vaultList.setColumnCount(3)
        self.vaultList.setHorizontalHeaderLabels(["Timestamp", "Name", "Location"])
        self.vaultList.setShowGrid(False)
        self.vaultList.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.vaultList.setCornerButtonEnabled(True)
        self.vaultList.horizontalHeader().setStretchLastSection(True)
        self._updateVault()

        listLayout.addWidget(self.vaultList)
        listLayout.addSpacerItem(QtWidgets.QSpacerItem(20, 10))
        buttonLayout = QtWidgets.QVBoxLayout()
        listLayout.addLayout(buttonLayout)
        listLayout.addSpacerItem(QtWidgets.QSpacerItem(50, 10))
        restoreButton = QtWidgets.QPushButton("Restore", self.viewVaultFrame)
        restoreButton.clicked.connect(lambda:self._restoreQuarantinedFile())
        deleteButton = QtWidgets.QPushButton("Delete", self.viewVaultFrame)
        deleteButton.clicked.connect(lambda:self._deleteQuarantinedFile())
        buttonLayout.addSpacerItem(QtWidgets.QSpacerItem(10, 60))
        buttonLayout.addWidget(restoreButton)
        buttonLayout.addWidget(deleteButton)
        buttonLayout.addSpacerItem(QtWidgets.QSpacerItem(10, 350))
    
    def _updateVault(self):
        self.vaultList.clear()
        for i in range(QFileList.len()):
            qfile = QFileList.get(i)
            self._addQuarantinedFile(qfile)

    def _addQuarantinedFile(self, qfile):
        timestampItem = QtWidgets.QTableWidgetItem(str(qfile.time))
        timestampItem.setFlags(timestampItem.flags() ^ QtCore.Qt.ItemIsEditable)
        timestampItem.setToolTip(str(qfile.time))
        nameItem = QtWidgets.QTableWidgetItem(qfile.name)
        nameItem.setFlags(nameItem.flags() ^ QtCore.Qt.ItemIsEditable)
        nameItem.setToolTip(qfile.name)
        locationItem = QtWidgets.QTableWidgetItem(qfile.path)
        locationItem.setFlags(locationItem.flags() ^ QtCore.Qt.ItemIsEditable)
        locationItem.setToolTip(qfile.path)
        self.vaultList.insertRow(0)
        self.vaultList.setItem(0, 0, timestampItem)
        self.vaultList.setItem(0, 1, nameItem)
        self.vaultList.setItem(0, 2, locationItem)  

    def _deleteQuarantinedFile(self, confirm = None):
        items = self.vaultList.selectedItems()
        if (len(items) > 0):
            if (confirm == None):
                confirm = QtWidgets.QMessageBox()
                confirm.setWindowIcon(self.viewVaultIcon)
                confirm.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                confirm.setText("Are you sure you want to delete selected quanrantined file(s)?")
                confirm.setWindowTitle("Delete Quaratined File")

            retval = confirm.exec()
            if (retval == QtWidgets.QMessageBox.Yes):
                for i in range(0,len(items), 3):
                    item = items[i]
                    index = self.vaultList.row(item)
                    qfile = QFileList.get(index)
                    os.remove(os.path.join(config.QUARANTINE_FOLDER, qfile.name))
                    QFileList.remove(qfile)
                    self.vaultList.removeRow(index)
                
    def _restoreQuarantinedFile(self):
        items = self.vaultList.selectedItems()
        if (len(items) > 0):
            confirm = QtWidgets.QMessageBox()
            confirm.setWindowIcon(self.viewVaultIcon)
            confirm.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            confirm.setText("Are you sure you want to restore selected quanrantined file(s)?")
            confirm.setWindowTitle("Restore Quaratined File")
            retval = confirm.exec()
            if (retval == QtWidgets.QMessageBox.Yes):
                for i in range(0,len(items), 3):
                    item = items[i]
                    index = self.vaultList.row(item)
                    qfile = QFileList.get(index)
                    file = os.path.join(config.QUARANTINE_FOLDER, qfile.name)
                    os.chmod(file, qfile.old_perm)
                    os.rename(file, qfile.path)
                    QFileList.remove(qfile)
                    self.vaultList.removeRow(index)         
    
    def _setupConfigFrame(self):
        self.configFrame = QtWidgets.QFrame(self.centralwidget)
        self.configFrame.setEnabled(True)
        self.configFrame.setGeometry(QtCore.QRect(0, 0, 700, 600))
        self.configFrame.setMaximumSize(QtCore.QSize(700, 600))
        self.configFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.configFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.configFrame.setObjectName("configFrame")

        configLabel = QtWidgets.QLabel(self.configFrame)
        configLabel.setEnabled(True)
        configLabel.setGeometry(QtCore.QRect(0, 0, 750, 62))
        configLabel.setFont(self.frameFont)
        configLabel.setLayoutDirection(QtCore.Qt.LeftToRight)
        configLabel.setFrameShape(QtWidgets.QFrame.Panel)
        configLabel.setFrameShadow(QtWidgets.QFrame.Sunken)
        configLabel.setLineWidth(1)
        configLabel.setMidLineWidth(10)
        configLabel.setTextFormat(QtCore.Qt.PlainText)
        configLabel.setScaledContents(False)
        configLabel.setObjectName("configLabel")
        configLabel.setText("CONFIG")

    def _displayError(self, message):
        error_dialog = QtWidgets.QErrorMessage()
        error_dialog.showMessage(str(message))
        error_dialog.setWindowIcon(self.errorIcon)
        error_dialog.setWindowTitle("Error")
        error_dialog.exec()
    
    def scan_now(self):
        raise NotImplementedError