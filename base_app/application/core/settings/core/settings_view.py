__author__ = 'Michael Redmond'

from PyQt4 import QtGui

from base_app.application.core.settings.core.settings_ui import Ui_Settings


class BaseAppSettingsView(QtGui.QWidget):
    def __init__(self):
        super(BaseAppSettingsView, self).__init__()

        self.ui = Ui_Settings()
        self.ui.setupUi(self)
