__author__ = 'Michael Redmond'

from base_app.simple_pubsub import pub
from base_app.utilities.misc import new_name

from model import BaseAppModelController
from view import BaseAppViewController
from plugins import BaseAppPluginController
from settings import BaseAppSettingsController
from utilities import file_utilities


class BaseAppProgramController(object):
    def __init__(self, app):
        super(BaseAppProgramController, self).__init__()

        self._app = app
        """:type: base_app.application.BaseQApplication"""

        self._model_controller = self.create_model_controller_object()
        self._view_controller = self.create_view_controller_object(self._app)
        self._plugin_controller = self.create_plugin_controller_object()
        self._settings_controller = self.create_settings_controller_object(self._plugin_controller)

        pub.subscribe(self.new_file, 'program.new_file')
        pub.subscribe(self.set_active_document, 'program.set_active_document')
        pub.subscribe(self.open_file, 'program.open_file')
        pub.subscribe(self.close_file, 'program.close_file')
        pub.subscribe(self.settings, 'program.settings')

    def create_model_controller_object(self):
        return BaseAppModelController()

    def create_view_controller_object(self, app):
        return BaseAppViewController(app)

    def create_plugin_controller_object(self):
        return BaseAppPluginController(self)

    def create_settings_controller_object(self, plugin_controller):
        return BaseAppSettingsController(plugin_controller)

    def show_view(self):
        self._view_controller.show()

    def new_file(self):
        name = new_name(self._model_controller.get_model_names())
        pub.publish("view.new_view", name=name)
        pub.publish("model.new_model", name=name)

        index = self.get_model_controller().get_model_names().index(name)
        self.set_active_document(index)

    def set_active_document(self, index):
        pub.publish("view.set_active_view", index=index)
        pub.publish("model.set_active_model", index=index)

    def open_file(self, filename):
        file_ = file_utilities.open_file(filename)

        if file_:
            pub.publish("view.set_file", file_=file_)
            pub.publish("model.set_file", file_=file_)

    def close_file(self, index):
        pub.publish("view.close_view", index=index)
        pub.publish("model.close_model", index=index)

        last_index = len(self._model_controller.get_model_names()) - 1

        if index > last_index:
            index -= 1

        if index < 0:
            return

        self.set_active_document(index)

    def get_view_controller(self):
        return self._view_controller

    def get_model_controller(self):
        return self._model_controller

    def settings(self):
        self._settings_controller.show()