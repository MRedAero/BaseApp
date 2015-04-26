# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settings_ui.ui'
#
# Created: Sun Apr 26 06:50:26 2015
#      by: PyQt4 UI code generator 4.9.6
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

class Ui_Settings(object):
    def setupUi(self, Settings):
        Settings.setObjectName(_fromUtf8("Settings"))
        Settings.resize(1087, 691)
        self.gridLayout = QtGui.QGridLayout(Settings)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.splitter = QtGui.QSplitter(Settings)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.treeWidget = QtGui.QTreeWidget(self.splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.treeWidget.sizePolicy().hasHeightForWidth())
        self.treeWidget.setSizePolicy(sizePolicy)
        self.treeWidget.setMinimumSize(QtCore.QSize(100, 0))
        self.treeWidget.setMaximumSize(QtCore.QSize(300, 16777215))
        self.treeWidget.setFrameShape(QtGui.QFrame.NoFrame)
        self.treeWidget.setObjectName(_fromUtf8("treeWidget"))
        item_0 = QtGui.QTreeWidgetItem(self.treeWidget)
        item_1 = QtGui.QTreeWidgetItem(item_0)
        item_0 = QtGui.QTreeWidgetItem(self.treeWidget)
        self.viewFrame = QtGui.QFrame(self.splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.viewFrame.sizePolicy().hasHeightForWidth())
        self.viewFrame.setSizePolicy(sizePolicy)
        self.viewFrame.setFrameShape(QtGui.QFrame.NoFrame)
        self.viewFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.viewFrame.setObjectName(_fromUtf8("viewFrame"))
        self.verticalLayout.addWidget(self.splitter)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.okButton = QtGui.QPushButton(Settings)
        self.okButton.setObjectName(_fromUtf8("okButton"))
        self.horizontalLayout.addWidget(self.okButton)
        self.cancelButton = QtGui.QPushButton(Settings)
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        self.horizontalLayout.addWidget(self.cancelButton)
        self.applyButton = QtGui.QPushButton(Settings)
        #self.applyButton.setEnabled(False)
        self.applyButton.setObjectName(_fromUtf8("applyButton"))
        self.horizontalLayout.addWidget(self.applyButton)
        self.helpButton = QtGui.QPushButton(Settings)
        self.helpButton.setEnabled(False)
        self.helpButton.setObjectName(_fromUtf8("helpButton"))
        self.horizontalLayout.addWidget(self.helpButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(Settings)
        QtCore.QMetaObject.connectSlotsByName(Settings)

    def retranslateUi(self, Settings):
        Settings.setWindowTitle(_translate("Settings", "Settings", None))
        self.treeWidget.headerItem().setText(0, _translate("Settings", "", None))
        __sortingEnabled = self.treeWidget.isSortingEnabled()
        self.treeWidget.setSortingEnabled(False)
        self.treeWidget.topLevelItem(0).setText(0, _translate("Settings", "Appearance", None))
        self.treeWidget.topLevelItem(0).child(0).setText(0, _translate("Settings", "Something", None))
        self.treeWidget.topLevelItem(1).setText(0, _translate("Settings", "Plugins", None))
        self.treeWidget.setSortingEnabled(__sortingEnabled)
        self.okButton.setText(_translate("Settings", "Ok", None))
        self.cancelButton.setText(_translate("Settings", "Cancel", None))
        self.applyButton.setText(_translate("Settings", "Apply", None))
        self.helpButton.setText(_translate("Settings", "Help", None))

