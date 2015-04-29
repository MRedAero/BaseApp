__author__ = 'Michael Redmond'

# put this at the top of all files to check for license (where needed)
from base_app.license_manager import license_manager
license_manager.check_license()

from PyQt4 import QtGui, QtCore
QtCore.Signal = QtCore.pyqtSignal
import sys

from base_app.application.core import BaseAppProgramController
from base_app.utilities import RepeatedTimer


class BaseQApplication(QtGui.QApplication):
    def __init__(self, *args, **kwargs):
        super(BaseQApplication, self).__init__(*args, **kwargs)

        self._timer = RepeatedTimer(15*60, license_manager.check_license)

    def exec_(self):
        self._timer.start()
        super(BaseQApplication, self).exec_()
        self._timer.stop()


class BaseApplication(object):
    def __init__(self):
        super(BaseApplication, self).__init__()

        self._app = BaseQApplication([])
        self._program_controller = self.create_program_controller_object(self._app)

    @property
    def create_program_controller_object(self):
        return BaseAppProgramController

    def show(self):
        self._program_controller.show_view()

    def start(self):
        sys.exit(self._app.exec_())


if __name__ == "__main__":
    app = BaseApplication()
    app.show()
    app.start()