__author__ = 'Michael Redmond'

# put this at the top of all files to check for license (where needed)
from base_app.license_manager import license_manager
license_manager.check_license()

from PySide import QtGui
import sys

from base_app.utilities import RepeatedTimer

from .model import Model
from .view import View
from .controller import Controller


class BaseQApplication(QtGui.QApplication):
    def __init__(self, *args, **kwargs):
        super(BaseQApplication, self).__init__(*args, **kwargs)

        self._timer = RepeatedTimer(15*60, license_manager.check_license)

    def exec_(self):
        self._timer.start()

        super(BaseQApplication, self).exec_()


class BaseApplication(object):
    def __init__(self, *args, **kwargs):
        super(BaseApplication, self).__init__()

        self._app = BaseQApplication(*args, **kwargs)

        self._model = None
        self._view = None
        self._controller = None

    def build(self, controller=None):

        if controller is None:
            controller = Controller(self._app, Model(), View())

        self._model = controller.get_model()
        self._view = controller.get_view()
        self._controller = controller

    def start(self):
        sys.exit(self._app.exec_())

    def get_qapp(self):
        return self._app
