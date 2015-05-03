__author__ = 'Michael Redmond'

from base_app.simple_pubsub import pub
from base_app.utilities.misc import new_name

from document import BaseAppDocumentController
from view import BaseAppViewController
from plugins import BaseAppPluginController
from settings import BaseAppSettingsController
from utilities import file_utilities


class BaseAppProgramController(object):
    def __init__(self, app):
        super(BaseAppProgramController, self).__init__()

        self._app = app
        """:type: base_app.application.BaseQApplication"""

        self._view_controller = self.create_view_controller(self._app)
        self._document_controller = self.create_document_controller(self._view_controller)
        self._plugin_controller = self.create_plugin_controller()
        self._settings_controller = self.create_settings_controller(self._plugin_controller)

        self._subscribe_to_pub()

    def _subscribe_to_pub(self):
        pub.subscribe(self.new_file, 'program.new_file')
        pub.subscribe(self.set_active_document, 'program.set_active_document')
        pub.subscribe(self.open_file, 'program.open_file')
        pub.subscribe(self.close_file, 'program.close_file')
        pub.subscribe(self.show_settings, 'program.settings')

    def create_document_controller(self, view_controller):
        return BaseAppDocumentController(view_controller)

    def create_view_controller(self, app):
        return BaseAppViewController(app)

    def create_plugin_controller(self):
        return BaseAppPluginController(self)

    def create_settings_controller(self, plugin_controller):
        return BaseAppSettingsController(plugin_controller)

    def show_view(self):
        self._view_controller.show()

    def new_file(self):
        pub.publish("document.new_document")

    def set_active_document(self, index):
        pub.publish("document.set_active_document", index=index)

    def open_file(self, filename):
        file_ = file_utilities.open_file(filename)

        if file_:
            pub.publish("document.set_file", file_=file_)

    def close_file(self, index):
        pub.publish("document.close_document", index=index)

    def get_view_controller(self):
        return self._view_controller

    def get_document_controller(self):
        return self._document_controller

    def show_settings(self):
        self._settings_controller.show()