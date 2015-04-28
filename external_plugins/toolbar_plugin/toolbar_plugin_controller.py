__author__ = 'Michael Redmond'

from PyQt4 import QtCore

from toolbar_plugin_view import ToolbarPluginView


class ToolbarPluginController(object):
    def __init__(self, program_controller):
        self._program_controller = program_controller
        """:type: base_app.application.core.program_controller.BaseAppProgramController"""

        self._program_view_controller = self._program_controller.get_view_controller()

        self._view = ToolbarPluginView()
        self._program_view_controller.add_dock_widget(QtCore.Qt.RightDockWidgetArea, self._view)

        self.show()

    def show(self):
        self._view.show()

    def hide(self):
        self._view.hide()

    def unload(self):
        self._program_view_controller.remove_dock_widget(self._view)
        self._program_view_controller = None
        self._program_controller = None
        self._view.setParent(None)