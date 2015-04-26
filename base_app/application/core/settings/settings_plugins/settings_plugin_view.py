__author__ = 'Michael Redmond'

from PyQt4 import QtCore, QtGui

from settings_plugin_ui import Ui_Form


class PluginsView(QtGui.QWidget):
    def __init__(self):
        super(PluginsView, self).__init__()

        self.ui = Ui_Form()
        self.ui.setupUi(self)