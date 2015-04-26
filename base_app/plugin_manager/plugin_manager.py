__author__ = 'Michael Redmond'

import os
import glob
import imp
from collections import OrderedDict


#TODO: convert print statements into signals and/or logs


class Plugin(object):
    def __init__(self, info):
        super(Plugin, self).__init__()

        self._info = info
        self._class = None
        self._object = None

    def set_plugin_class(self, class_):
        self._class = class_
        self._object = None

    def get_plugin_class(self):
        return self._class

    def get_info(self):
        return self._info

    def load_plugin(self, *args, **kwargs):
        if self._object is None:
            self._object = self._class(*args, **kwargs)

        return self._object

    def is_loaded(self):
        return self._object is not None

    def new_plugin(self):
        return self._class()

    def unload(self):
        try:
            self._object.unload()
        except AttributeError:
            pass

        self._object = None


class PluginManager(object):
    def __init__(self):
        super(PluginManager, self).__init__()

        self._plugins = None

        self._plugin_folders = []

    def get_plugin_folders(self):
        return self._plugin_folders

    def add_plugin_folder(self, folder):
        if os.path.exists(folder):
            if folder not in self._plugin_folders:
                self._plugin_folders.append(folder)
        else:
            print "%s doesn't exist!\n" % folder

    def remove_plugin_folder(self, folder):
        try:
            index = self._plugin_folders.index(folder)
            del self._plugin_folders[index]
        except Exception:
            pass

        for category in self._plugins.keys():
            for name in self._plugins[category].keys():
                info = self._plugins[category][name]

                if info['Folder'] == folder:
                    del self._plugins[category][name]

    def collect_plugins(self):
        if self._plugins is None:
            self._plugins = OrderedDict()

        for folder in self._plugin_folders:
            for file in glob.glob("%s/*.plugin" % folder):
                file = os.path.basename(file)
                self.read_plugin(folder, file)

    def get_plugins(self):
        return self._plugins

    def read_plugin(self, folder, file):

        plugin_file = "%s/%s" % (folder, file)

        if not os.path.exists(plugin_file):
            print "Plugin %s doesn't exist!\n" % plugin_file
            return

        with open(plugin_file, 'r') as f:
            lines = f.readlines()

        info = {'Core': {}, 'Description': {}, 'Folder': folder, 'File': file}

        info_ = None

        for line in lines:

            line = line.replace('\n', '').replace('\r', '')

            if line[:6] == '[Core]':
                info_ = info['Core']
                continue
            elif line[:13] == '[Description]':
                info_ = info['Description']
                continue

            data = line.split('=')

            if len(data) < 2:
                continue

            info_[data[0].strip()] = data[1].strip()

        try:
            module_name = info['Core']['Module']
        except KeyError:
            try:
                module_name = info['Core']['Package']
            except KeyError:
                print "Module name is not defined!\n"
                return

        category = info['Core']['Category']
        plugin_name = info['Core']['Name']
        mount_name = info['Core']['Mount']

        fp, pathname, description = imp.find_module(module_name, [folder])
        try:
            package = imp.load_module(module_name, fp, pathname, description)
        finally:
            if fp:
                fp.close()

        new_plugin = Plugin(info)
        new_plugin.set_plugin_class(getattr(package, mount_name))

        if category not in self._plugins.keys():
            self._plugins[category] = OrderedDict()

        if plugin_name in self._plugins[category].keys():
            plugin_info = self._plugins[category][plugin_name].get_info()

            if folder == plugin_info['Folder'] and file == plugin_info['File']:
                # same plugin already exists, just ignore
                return

            # same plugin category and name, but folder or file isn't the same
            print "Plugin %s already exists in category %s!\n" % (plugin_name, category)
            return

        self._plugins[category][plugin_name] = new_plugin


if __name__ == '__main__':
    pm = PluginManager()
    pm.add_plugin_folder('./examples')
    pm.collect_plugins()

    plugin = pm.get_plugins()['category1']['Plugin1']
    plugin.load_plugin().some_method()


