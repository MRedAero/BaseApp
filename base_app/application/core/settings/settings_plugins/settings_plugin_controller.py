__author__ = 'Michael Redmond'

from PyQt4 import QtGui

from base_app.plugin_manager import PluginManager
from base_app.simple_pubsub import pub
from base_app import config

from settings_plugin_view import PluginsView


class SettingsPluginController(object):
    def __init__(self, layout, plugin_controller):

        self._layout = layout
        """:type: PyQt4.QtGui.QGridLayout.QGridLayout"""

        self._plugin_controller = plugin_controller
        """:type: base_app.application.core.plugins.plugin_controller.BaseAppPluginController"""

        self._view = PluginsView()

        self._view.ui.listView.clicked.connect(self._clicked)

        self._pm = PluginManager()
        self._pm.add_plugin_folder(config.program_path + '/external_plugins')

        self._model = QtGui.QStandardItemModel()

        self._changes = {}
        self._items = []

        self.update_available_plugins()

        self._canceling = False

        self._model.itemChanged.connect(self._item_changed)

    def show(self):
        self._layout.addWidget(self._view)
        self._view.show()

    def hide(self):
        self._layout.removeWidget(self._view)
        self._view.hide()

    def update_available_plugins(self):
        self._pm.collect_plugins()

        plugins = self._pm.get_plugins()

        self._model.clear()
        self._items = []
        self._changes = {}

        for category in plugins.keys():
            for name in plugins[category].keys():
                plugin = plugins[category][name]

                item = QtGui.QStandardItem('%s - %s' % (category, name))
                item.setCheckable(True)
                item.plugin_category = category
                item.plugin_name = name
                item.old_state = False

                if plugin.is_loaded():
                    item.setCheckState(True)

                self._model.appendRow(item)
                self._items.append(item)

        self._view.ui.listView.setModel(self._model)

    def _clicked(self, index):
        """

        :param index: PyQt4.QtGui.QStandardItem.QStandardItem
        :return:
        """
        model = self._view.ui.listView.model()
        """:type: PyQt4.QtGui.QStandardItemModel.QStandardItemModel"""
        item = model.item(index.row(), index.column())

        plugin = self._pm.get_plugins()[item.plugin_category][item.plugin_name]
        info = plugin.get_info()

        self._view.ui.textBrowser.setText("%s\n%s" % (info['Core'], info['Description']))

    def _item_changed(self, item):
        if self._canceling:
            return

        if item.checkState() != item.old_state:
            self._changes[item] = item.checkState()

    def update(self):
        plugins = self._pm.get_plugins()

        for item in self._items:
            plugin = plugins[item.plugin_category][item.plugin_name]
            if item.checkState():
                if not plugin.is_loaded():
                    self._plugin_controller.load_plugin(plugin)
            else:
                self._plugin_controller.unload_plugin(plugin)

            item.old_state = item.checkState()

        self._changes = {}

    def cancel(self):
        self._canceling = True
        for item in self._changes.keys():
            if item.checkState():
                item.setCheckState(False)
            else:
                item.setCheckState(2)
        self._canceling = False

        self._changes = {}