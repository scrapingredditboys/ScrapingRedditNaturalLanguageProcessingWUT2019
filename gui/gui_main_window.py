# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer/main_window.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(640, 400)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../resources/icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget.setUsesScrollButtons(True)
        self.tabWidget.setDocumentMode(False)
        self.tabWidget.setTabBarAutoHide(False)
        self.tabWidget.setObjectName("tabWidget")
        self.subredditTab = QtWidgets.QWidget()
        self.subredditTab.setObjectName("subredditTab")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.subredditTab)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.subredditGuessField = QtWidgets.QPlainTextEdit(self.subredditTab)
        self.subredditGuessField.setObjectName("subredditGuessField")
        self.verticalLayout_8.addWidget(self.subredditGuessField)
        self.verticalLayout_9 = QtWidgets.QVBoxLayout()
        self.verticalLayout_9.setContentsMargins(-1, 10, -1, -1)
        self.verticalLayout_9.setSpacing(20)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.subredditGuessResultLabel = QtWidgets.QLabel(self.subredditTab)
        self.subredditGuessResultLabel.setEnabled(False)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.subredditGuessResultLabel.setFont(font)
        self.subredditGuessResultLabel.setText("")
        self.subredditGuessResultLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.subredditGuessResultLabel.setWordWrap(True)
        self.subredditGuessResultLabel.setObjectName("subredditGuessResultLabel")
        self.verticalLayout_9.addWidget(self.subredditGuessResultLabel)
        self.subredditGuessButton = QtWidgets.QPushButton(self.subredditTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.subredditGuessButton.sizePolicy().hasHeightForWidth())
        self.subredditGuessButton.setSizePolicy(sizePolicy)
        self.subredditGuessButton.setObjectName("subredditGuessButton")
        self.verticalLayout_9.addWidget(self.subredditGuessButton)
        self.verticalLayout_8.addLayout(self.verticalLayout_9)
        self.tabWidget.addTab(self.subredditTab, "")
        self.lengthTab = QtWidgets.QWidget()
        self.lengthTab.setObjectName("lengthTab")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.lengthTab)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setContentsMargins(50, 10, 50, 10)
        self.formLayout_2.setHorizontalSpacing(10)
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_4 = QtWidgets.QLabel(self.lengthTab)
        self.label_4.setObjectName("label_4")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.lengthSpinBox = QtWidgets.QSpinBox(self.lengthTab)
        self.lengthSpinBox.setMaximum(999999)
        self.lengthSpinBox.setObjectName("lengthSpinBox")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lengthSpinBox)
        self.lengthSubNameComboBox = QtWidgets.QComboBox(self.lengthTab)
        self.lengthSubNameComboBox.setObjectName("lengthSubNameComboBox")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lengthSubNameComboBox)
        self.label_5 = QtWidgets.QLabel(self.lengthTab)
        self.label_5.setObjectName("label_5")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.verticalLayout_11.addLayout(self.formLayout_2)
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.horizontalLayout_6.setContentsMargins(50, 10, 50, 10)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.lengthRawDataCheckBox = QtWidgets.QCheckBox(self.lengthTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lengthRawDataCheckBox.sizePolicy().hasHeightForWidth())
        self.lengthRawDataCheckBox.setSizePolicy(sizePolicy)
        self.lengthRawDataCheckBox.setObjectName("lengthRawDataCheckBox")
        self.horizontalLayout_6.addWidget(self.lengthRawDataCheckBox)
        self.verticalLayout_10.addLayout(self.horizontalLayout_6)
        self.lengthResultLabel = QtWidgets.QLabel(self.lengthTab)
        self.lengthResultLabel.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lengthResultLabel.sizePolicy().hasHeightForWidth())
        self.lengthResultLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.lengthResultLabel.setFont(font)
        self.lengthResultLabel.setText("")
        self.lengthResultLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.lengthResultLabel.setWordWrap(True)
        self.lengthResultLabel.setObjectName("lengthResultLabel")
        self.verticalLayout_10.addWidget(self.lengthResultLabel)
        self.verticalLayout_11.addLayout(self.verticalLayout_10)
        self.tabWidget.addTab(self.lengthTab, "")
        self.timeTab = QtWidgets.QWidget()
        self.timeTab.setObjectName("timeTab")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.timeTab)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setContentsMargins(50, 10, 50, 10)
        self.formLayout.setHorizontalSpacing(10)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.timeTab)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.karmaTimeSubNameComboBox = QtWidgets.QComboBox(self.timeTab)
        self.karmaTimeSubNameComboBox.setObjectName("karmaTimeSubNameComboBox")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.karmaTimeSubNameComboBox)
        self.label_2 = QtWidgets.QLabel(self.timeTab)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.karmaWeekdayComboBox = QtWidgets.QComboBox(self.timeTab)
        self.karmaWeekdayComboBox.setObjectName("karmaWeekdayComboBox")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.karmaWeekdayComboBox)
        self.label_3 = QtWidgets.QLabel(self.timeTab)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.karmaTimeEdit = QtWidgets.QTimeEdit(self.timeTab)
        self.karmaTimeEdit.setObjectName("karmaTimeEdit")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.karmaTimeEdit)
        self.verticalLayout_3.addLayout(self.formLayout)
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.horizontalLayout_5.setContentsMargins(50, 10, 50, 10)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.karmaTimeCombineDaysCheckBox = QtWidgets.QCheckBox(self.timeTab)
        self.karmaTimeCombineDaysCheckBox.setObjectName("karmaTimeCombineDaysCheckBox")
        self.horizontalLayout_5.addWidget(self.karmaTimeCombineDaysCheckBox)
        self.karmaTimeRawDataCheckBox = QtWidgets.QCheckBox(self.timeTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.karmaTimeRawDataCheckBox.sizePolicy().hasHeightForWidth())
        self.karmaTimeRawDataCheckBox.setSizePolicy(sizePolicy)
        self.karmaTimeRawDataCheckBox.setObjectName("karmaTimeRawDataCheckBox")
        self.horizontalLayout_5.addWidget(self.karmaTimeRawDataCheckBox)
        self.verticalLayout_7.addLayout(self.horizontalLayout_5)
        self.karmaTimeResultLabel = QtWidgets.QLabel(self.timeTab)
        self.karmaTimeResultLabel.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.karmaTimeResultLabel.sizePolicy().hasHeightForWidth())
        self.karmaTimeResultLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.karmaTimeResultLabel.setFont(font)
        self.karmaTimeResultLabel.setText("")
        self.karmaTimeResultLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.karmaTimeResultLabel.setWordWrap(True)
        self.karmaTimeResultLabel.setObjectName("karmaTimeResultLabel")
        self.verticalLayout_7.addWidget(self.karmaTimeResultLabel)
        self.verticalLayout_3.addLayout(self.verticalLayout_7)
        self.tabWidget.addTab(self.timeTab, "")
        self.upvoteTab = QtWidgets.QWidget()
        self.upvoteTab.setObjectName("upvoteTab")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.upvoteTab)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.formLayout_3 = QtWidgets.QFormLayout()
        self.formLayout_3.setContentsMargins(50, 10, 50, 10)
        self.formLayout_3.setHorizontalSpacing(10)
        self.formLayout_3.setObjectName("formLayout_3")
        self.label_6 = QtWidgets.QLabel(self.upvoteTab)
        self.label_6.setObjectName("label_6")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.upvoteSpinBox = QtWidgets.QSpinBox(self.upvoteTab)
        self.upvoteSpinBox.setSuffix("%")
        self.upvoteSpinBox.setMinimum(60)
        self.upvoteSpinBox.setMaximum(100)
        self.upvoteSpinBox.setProperty("value", 60)
        self.upvoteSpinBox.setDisplayIntegerBase(10)
        self.upvoteSpinBox.setObjectName("upvoteSpinBox")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.upvoteSpinBox)
        self.label_7 = QtWidgets.QLabel(self.upvoteTab)
        self.label_7.setObjectName("label_7")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_7)
        self.upvoteSubNameComboBox = QtWidgets.QComboBox(self.upvoteTab)
        self.upvoteSubNameComboBox.setObjectName("upvoteSubNameComboBox")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.upvoteSubNameComboBox)
        self.verticalLayout_4.addLayout(self.formLayout_3)
        self.verticalLayout_12 = QtWidgets.QVBoxLayout()
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.horizontalLayout_7.setContentsMargins(50, 10, 50, 10)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.upvoteRawDataCheckBox = QtWidgets.QCheckBox(self.upvoteTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.upvoteRawDataCheckBox.sizePolicy().hasHeightForWidth())
        self.upvoteRawDataCheckBox.setSizePolicy(sizePolicy)
        self.upvoteRawDataCheckBox.setObjectName("upvoteRawDataCheckBox")
        self.horizontalLayout_7.addWidget(self.upvoteRawDataCheckBox)
        self.verticalLayout_12.addLayout(self.horizontalLayout_7)
        self.upvoteResultLabel = QtWidgets.QLabel(self.upvoteTab)
        self.upvoteResultLabel.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.upvoteResultLabel.sizePolicy().hasHeightForWidth())
        self.upvoteResultLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.upvoteResultLabel.setFont(font)
        self.upvoteResultLabel.setText("")
        self.upvoteResultLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.upvoteResultLabel.setWordWrap(True)
        self.upvoteResultLabel.setObjectName("upvoteResultLabel")
        self.verticalLayout_12.addWidget(self.upvoteResultLabel)
        self.verticalLayout_4.addLayout(self.verticalLayout_12)
        self.tabWidget.addTab(self.upvoteTab, "")
        self.commentsTimeTab = QtWidgets.QWidget()
        self.commentsTimeTab.setObjectName("commentsTimeTab")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.commentsTimeTab)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.formLayout_4 = QtWidgets.QFormLayout()
        self.formLayout_4.setContentsMargins(50, 10, 50, 10)
        self.formLayout_4.setHorizontalSpacing(10)
        self.formLayout_4.setObjectName("formLayout_4")
        self.label_8 = QtWidgets.QLabel(self.commentsTimeTab)
        self.label_8.setObjectName("label_8")
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_8)
        self.commentsTimeSubNameComboBox = QtWidgets.QComboBox(self.commentsTimeTab)
        self.commentsTimeSubNameComboBox.setObjectName("commentsTimeSubNameComboBox")
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.commentsTimeSubNameComboBox)
        self.label_9 = QtWidgets.QLabel(self.commentsTimeTab)
        self.label_9.setObjectName("label_9")
        self.formLayout_4.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_9)
        self.commentsWeekdayComboBox = QtWidgets.QComboBox(self.commentsTimeTab)
        self.commentsWeekdayComboBox.setObjectName("commentsWeekdayComboBox")
        self.formLayout_4.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.commentsWeekdayComboBox)
        self.label_10 = QtWidgets.QLabel(self.commentsTimeTab)
        self.label_10.setObjectName("label_10")
        self.formLayout_4.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_10)
        self.commentsTimeEdit = QtWidgets.QTimeEdit(self.commentsTimeTab)
        self.commentsTimeEdit.setObjectName("commentsTimeEdit")
        self.formLayout_4.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.commentsTimeEdit)
        self.verticalLayout_5.addLayout(self.formLayout_4)
        self.verticalLayout_13 = QtWidgets.QVBoxLayout()
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.horizontalLayout_8.setContentsMargins(50, 10, 50, 10)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.commentsTimeCombineDaysCheckBox = QtWidgets.QCheckBox(self.commentsTimeTab)
        self.commentsTimeCombineDaysCheckBox.setObjectName("commentsTimeCombineDaysCheckBox")
        self.horizontalLayout_8.addWidget(self.commentsTimeCombineDaysCheckBox)
        self.commentsTimeRawDataCheckBox = QtWidgets.QCheckBox(self.commentsTimeTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.commentsTimeRawDataCheckBox.sizePolicy().hasHeightForWidth())
        self.commentsTimeRawDataCheckBox.setSizePolicy(sizePolicy)
        self.commentsTimeRawDataCheckBox.setObjectName("commentsTimeRawDataCheckBox")
        self.horizontalLayout_8.addWidget(self.commentsTimeRawDataCheckBox)
        self.verticalLayout_13.addLayout(self.horizontalLayout_8)
        self.commentsTimeResultLabel = QtWidgets.QLabel(self.commentsTimeTab)
        self.commentsTimeResultLabel.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.commentsTimeResultLabel.sizePolicy().hasHeightForWidth())
        self.commentsTimeResultLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.commentsTimeResultLabel.setFont(font)
        self.commentsTimeResultLabel.setText("")
        self.commentsTimeResultLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.commentsTimeResultLabel.setWordWrap(True)
        self.commentsTimeResultLabel.setObjectName("commentsTimeResultLabel")
        self.verticalLayout_13.addWidget(self.commentsTimeResultLabel)
        self.verticalLayout_5.addLayout(self.verticalLayout_13)
        self.tabWidget.addTab(self.commentsTimeTab, "")
        self.meanSentimentsTab = QtWidgets.QWidget()
        self.meanSentimentsTab.setObjectName("meanSentimentsTab")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.meanSentimentsTab)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.formLayout_5 = QtWidgets.QFormLayout()
        self.formLayout_5.setContentsMargins(50, 10, 50, 10)
        self.formLayout_5.setHorizontalSpacing(10)
        self.formLayout_5.setObjectName("formLayout_5")
        self.label_11 = QtWidgets.QLabel(self.meanSentimentsTab)
        self.label_11.setObjectName("label_11")
        self.formLayout_5.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_11)
        self.meanSentimentSubNameComboBox = QtWidgets.QComboBox(self.meanSentimentsTab)
        self.meanSentimentSubNameComboBox.setObjectName("meanSentimentSubNameComboBox")
        self.formLayout_5.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.meanSentimentSubNameComboBox)
        self.label_12 = QtWidgets.QLabel(self.meanSentimentsTab)
        self.label_12.setObjectName("label_12")
        self.formLayout_5.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_12)
        self.meanSentimentWeekdayComboBox = QtWidgets.QComboBox(self.meanSentimentsTab)
        self.meanSentimentWeekdayComboBox.setObjectName("meanSentimentWeekdayComboBox")
        self.formLayout_5.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.meanSentimentWeekdayComboBox)
        self.label_13 = QtWidgets.QLabel(self.meanSentimentsTab)
        self.label_13.setObjectName("label_13")
        self.formLayout_5.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_13)
        self.meanSentimentTimeEdit = QtWidgets.QTimeEdit(self.meanSentimentsTab)
        self.meanSentimentTimeEdit.setObjectName("meanSentimentTimeEdit")
        self.formLayout_5.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.meanSentimentTimeEdit)
        self.verticalLayout_6.addLayout(self.formLayout_5)
        self.verticalLayout_14 = QtWidgets.QVBoxLayout()
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.horizontalLayout_9.setContentsMargins(50, 10, 50, 10)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.meanSentimentCombineDaysCheckBox = QtWidgets.QCheckBox(self.meanSentimentsTab)
        self.meanSentimentCombineDaysCheckBox.setObjectName("meanSentimentCombineDaysCheckBox")
        self.horizontalLayout_9.addWidget(self.meanSentimentCombineDaysCheckBox)
        self.meanSentimentRawDataCheckBox = QtWidgets.QCheckBox(self.meanSentimentsTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.meanSentimentRawDataCheckBox.sizePolicy().hasHeightForWidth())
        self.meanSentimentRawDataCheckBox.setSizePolicy(sizePolicy)
        self.meanSentimentRawDataCheckBox.setObjectName("meanSentimentRawDataCheckBox")
        self.horizontalLayout_9.addWidget(self.meanSentimentRawDataCheckBox)
        self.verticalLayout_14.addLayout(self.horizontalLayout_9)
        self.meanSentimentResultLabel = QtWidgets.QLabel(self.meanSentimentsTab)
        self.meanSentimentResultLabel.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.meanSentimentResultLabel.sizePolicy().hasHeightForWidth())
        self.meanSentimentResultLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.meanSentimentResultLabel.setFont(font)
        self.meanSentimentResultLabel.setText("")
        self.meanSentimentResultLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.meanSentimentResultLabel.setWordWrap(True)
        self.meanSentimentResultLabel.setObjectName("meanSentimentResultLabel")
        self.verticalLayout_14.addWidget(self.meanSentimentResultLabel)
        self.verticalLayout_6.addLayout(self.verticalLayout_14)
        self.tabWidget.addTab(self.meanSentimentsTab, "")
        self.verticalLayout.addWidget(self.tabWidget)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 640, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.subredditGuessButton.setText(_translate("MainWindow", "Let\'s see!"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.subredditTab), _translate("MainWindow", "Subreddit Guess"))
        self.label_4.setText(_translate("MainWindow", "comment length"))
        self.label_5.setText(_translate("MainWindow", "subreddit name"))
        self.lengthRawDataCheckBox.setText(_translate("MainWindow", "raw data"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.lengthTab), _translate("MainWindow", "Karma based on length"))
        self.label.setText(_translate("MainWindow", "subreddit name"))
        self.label_2.setText(_translate("MainWindow", "weekday"))
        self.label_3.setText(_translate("MainWindow", "time of day"))
        self.karmaTimeEdit.setDisplayFormat(_translate("MainWindow", "HH:mm"))
        self.karmaTimeCombineDaysCheckBox.setText(_translate("MainWindow", "combine days of week"))
        self.karmaTimeRawDataCheckBox.setText(_translate("MainWindow", "raw data"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.timeTab), _translate("MainWindow", "Karma based on time"))
        self.label_6.setText(_translate("MainWindow", "upvote ratio"))
        self.label_7.setText(_translate("MainWindow", "subreddit name"))
        self.upvoteRawDataCheckBox.setText(_translate("MainWindow", "raw data"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.upvoteTab), _translate("MainWindow", "Sentiments and upvotes"))
        self.label_8.setText(_translate("MainWindow", "subreddit name"))
        self.label_9.setText(_translate("MainWindow", "weekday"))
        self.label_10.setText(_translate("MainWindow", "time of day"))
        self.commentsTimeEdit.setDisplayFormat(_translate("MainWindow", "HH:mm"))
        self.commentsTimeCombineDaysCheckBox.setText(_translate("MainWindow", "combine days of week"))
        self.commentsTimeRawDataCheckBox.setText(_translate("MainWindow", "raw data"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.commentsTimeTab), _translate("MainWindow", "Comments based on time"))
        self.label_11.setText(_translate("MainWindow", "subreddit name"))
        self.label_12.setText(_translate("MainWindow", "weekday"))
        self.label_13.setText(_translate("MainWindow", "time of day"))
        self.meanSentimentTimeEdit.setDisplayFormat(_translate("MainWindow", "HH:mm"))
        self.meanSentimentCombineDaysCheckBox.setText(_translate("MainWindow", "combine days of week"))
        self.meanSentimentRawDataCheckBox.setText(_translate("MainWindow", "raw data"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.meanSentimentsTab), _translate("MainWindow", "Mean sentiments"))

