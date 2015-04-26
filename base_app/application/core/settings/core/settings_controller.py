__author__ = 'Michael Redmond'

from PyQt4 import QtGui


from settings_view import BaseAppSettingsView

from base_app.application.core.settings.settings_plugins import SettingsPluginController


class BaseAppSettingsController(object):
    def __init__(self, plugin_controller):

        self._view = BaseAppSettingsView()
        self._grid_layout = QtGui.QGridLayout(self._view.ui.viewFrame)

        self._settings_plugin_controller = SettingsPluginController(self._grid_layout, plugin_controller)

        self._view.ui.okButton.clicked.connect(self._ok_clicked)
        self._view.ui.cancelButton.clicked.connect(self._cancel_clicked)
        self._view.ui.applyButton.clicked.connect(self._apply_clicked)
        self._view.ui.helpButton.clicked.connect(self._help_clicked)

        self._view.ui.treeWidget.itemPressed.connect(self._item_changed)

        self._active_controller = None

    def show(self):
        self._view.show()

    def hide(self):
        self._view.hide()

    def _item_changed(self, item, column):
        item_text = str(item.text(0))

        if item_text == 'Plugins':
            self._settings_plugin_controller.show()
            self._active_controller = self._settings_plugin_controller
        else:
            self._settings_plugin_controller.hide()
            self._active_controller = None

    def _ok_clicked(self):
        if self._active_controller:
            self._active_controller.update()

        self.hide()

    def _cancel_clicked(self):
        if self._active_controller:
            self._active_controller.cancel()

        self.hide()

    def _apply_clicked(self):
        if self._active_controller:
            self._active_controller.update()

    def _help_clicked(self):
        pass