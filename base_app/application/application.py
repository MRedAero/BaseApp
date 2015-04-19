__author__ = 'Michael Redmond'

# put this at the top of all files to check for license (where needed)
from base_app.license_manager import license_manager
license_manager.check_license()

from PyQt4 import QtGui, QtCore
QtCore.Signal = QtCore.pyqtSignal
import sys

from base_app.application.adaptor import BaseAppAdaptor

from base_app.utilities import RepeatedTimer


class BaseQApplication(QtGui.QApplication):
    def __init__(self, *args, **kwargs):
        super(BaseQApplication, self).__init__(*args, **kwargs)

        self._timer = RepeatedTimer(15*60, license_manager.check_license)

    def exec_(self):
        self._timer.start()

        super(BaseQApplication, self).exec_()


class BaseApplication(object):
    def __init__(self):
        super(BaseApplication, self).__init__()

        self._app = BaseQApplication([])

        self._adaptor = self.create_adaptor_object(self._app)

    @property
    def create_adaptor_object(self):
        return BaseAppAdaptor

    def show(self):
        self._adaptor.show_view()

    def start(self):
        sys.exit(self._app.exec_())



if __name__ == "__main__":
    app = BaseApplication()
    app.show()
    app.start()