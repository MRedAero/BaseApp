__author__ = 'Michael Redmond'


class BaseAppPluginController(object):
    def __init__(self, program_controller):
        super(BaseAppPluginController, self).__init__()

        self._program_controller = program_controller
        """:type: base_app.application.core.program_controller.BaseAppProgramController"""

        self._view_controller = self._program_controller.get_view_controller()

        self._external_plugins = []

    def load_plugin(self, plugin):
        """

        :param plugin: base_app.plugin_manager.plugin_manager.Plugin
        :return:
        """

        new_plugin = plugin.load_plugin(self._program_controller)

        if new_plugin not in self._external_plugins:
            self._external_plugins.append(new_plugin)

    def unload_plugin(self, plugin):
        """

        :param plugin: base_app.plugin_manager.plugin_manager.Plugin
        :return:
        """

        if not plugin.is_loaded():
            return

        old_plugin = plugin.load_plugin()

        if old_plugin in self._external_plugins:
            index = self._external_plugins.index(old_plugin)
            del self._external_plugins[index]

        plugin.unload()