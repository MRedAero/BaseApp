# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'toolbar_plugin_ui.ui'
#
# Created: Sun Apr 26 16:21:13 2015
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

class Ui_Toolbar(object):
    def setupUi(self, Toolbar):
        Toolbar.setObjectName(_fromUtf8("Toolbar"))
        Toolbar.resize(216, 184)
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        Toolbar.setWidget(self.dockWidgetContents)

        self.retranslateUi(Toolbar)
        QtCore.QMetaObject.connectSlotsByName(Toolbar)

    def retranslateUi(self, Toolbar):
        Toolbar.setWindowTitle(_translate("Toolbar", "Toolbar", None))

