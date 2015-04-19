__author__ = 'Michael Redmond'

from base_app.application.controller.model import BaseAppModelController
from base_app.application.controller.view import BaseAppViewController
from base_app.application.controller.logic import BaseAppLogicController


class BaseAppAdaptor(object):
    def __init__(self, app):
        super(BaseAppAdaptor, self).__init__()

        self._app = app
        """:type: base_app.application.BaseQApplication"""

        self._model_controller = self.create_model_controller_object(self)
        self._view_controller = self.create_view_controller_object(self, self._app)
        self._logic_controller = self.create_logic_controller_object(self)

        self._view_controller.new_document()

    @property
    def create_model_controller_object(self):
        return BaseAppModelController

    @property
    def create_view_controller_object(self):
        return BaseAppViewController

    @property
    def create_logic_controller_object(self):
        return BaseAppLogicController

    def show_view(self):
        self._view_controller.show()

    def get_model_names(self):
        return self._model_controller.get_model_names()

    def new_model(self, model_name):
        # this can only be called by the view controller
        if not self._view_controller.is_active():
            return

        return self._model_controller.new_model(model_name)

    def close_model(self, index):
        # this can only be called by the view controller
        if not self._view_controller.is_active():
            return

        return self._model_controller.close_model(index)

    def set_active_model(self, index):
        # this can only be called by the view controller
        if not self._view_controller.is_active():
            return

        return self._model_controller.set_active_model(index)

    def open_file(self, filename):
        # this can only be called by the view controller
        if not self._view_controller.is_active():
            return

        file = self._logic_controller.open_file(filename)

        if file:
            self._model_controller.set_file(file)
            self._view_controller.set_file(file)