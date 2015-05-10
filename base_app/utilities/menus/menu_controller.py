from PyQt4 import QtGui
from collections import OrderedDict

from action_controller import ActionController
from separator_controller import SeparatorController


class MenuController(object):
    def __init__(self, menu, menu_name):

        self._menu = menu

        self._menu_name = menu_name

        if isinstance(menu, QtGui.QMenu):
            self._menu.setTitle(menu_name)
            self._menu.setObjectName("menu_" + menu_name)
        else:
            self._menu.setObjectName("menu_bar_" + menu_name)

        self._items = OrderedDict()

    def get_name(self):
        return self._menu_name

    def get_menu(self):
        return self._menu

    def add_menu(self, menu_name, reorganize=False):

        if menu_name in self._items.keys():
            print "menu name %s already exists!" % menu_name
            return

        menu = MenuController(QtGui.QMenu(self._menu), menu_name)

        self._items[menu_name] = menu

        if reorganize:
            self.reorganize()

        return menu

    def add_action(self, action_name, reorganize=False):

        if action_name in self._items.keys():
            print "action name %s already exists!" % action_name
            return

        #action = ActionController(QtGui.QAction(self._menu), action_name)
        action = ActionController(QtGui.QAction(None), action_name)

        self._items[action_name] = action

        if reorganize:
            self.reorganize()

        return action

    def add_separator(self, name):

        if name in self._items.keys():
            print "separator name %s already exists!" % name
            return

        self._items[name] = SeparatorController(name)

    def get_item(self, item):
        if isinstance(item, int):
            item = self._items.keys()[item]

        return self._items[item]

    def get_item_index(self, item):
        if isinstance(item, int):
            return item

        return self._items.keys().index(item)

    def get_item_name(self, item):
        if isinstance(item, int):
            item = self._items.keys()[item]
        elif isinstance(item, str):
            item = self._items[item]

        return item.get_name()

    def delete_item(self, item, reorganize=False):

        item_name = self.get_item_name(item)

        del self._items[item_name]

        if reorganize:
            self.reorganize()

    def move_item(self, index, new_index, reorganize=False):
        item = self.get_item(index)

        if item is None:
            return

        del self._items[item.get_name()]

        if new_index < 0:
            new_index = 0

        item_count = len(self._items.keys())

        if new_index > item_count:
            new_index = item_count

        items = []

        for key in self._items.keys():
            items.append(self._items[key])

        items.insert(new_index, item)

        self._items = OrderedDict()

        for item in items:
            self._items[item.get_name()] = item

        if reorganize:
            self.reorganize()

    def reorganize(self):

        # @Mike... If this is a QMenuBar, clearing it once works.... otherwise it then clears the menus within
        #          the MenuBar also, which leads to a deleted wrapper item error when reorganize is ran twice
        #
        #          Not sure.... somehow IF its a QMenuBar, just need to clear the MenuBar, not the MenuBar and then its items
        #                       IF a QMenu... but not called from a QMenuBar reorganize, then should clear
        #                                         - but this would have to be done in another def, or before .reorganize

        #if isinstance(self._menu, QtGui.QMenuBar):
        self._menu.clear()

        for key in self._items.keys():
            item = self._items[key]

            if isinstance(item, MenuController):
                self._menu.addMenu(item.get_menu())
                item.reorganize()
            elif isinstance(item, ActionController):
                self._menu.addAction(item.get_action())
            elif isinstance(item, SeparatorController):
                self._menu.addSeparator()


if __name__ == '__main__':
    from base_main_window import BaseMainWindow

    import sys

    app = QtGui.QApplication(sys.argv)

    main_window = BaseMainWindow()

    main_window.menuBar().clear()

    mb = MenuController(main_window.menuBar(), 'menu_bar')

    file = mb.add_menu('File')
    tools = mb.add_menu('Tools')
    help = mb.add_menu('Help')

    file.add_action('New...')
    file.add_action('Open...')
    file.add_action('Save')
    file.add_action('Save As...')
    file.add_action('Close')
    file.add_separator('sep1')
    settings = file.add_menu('Settings...')
    file.add_separator('sep2')
    file.add_action('Exit')

    settings.add_action('Plugins...')

    help.add_action('About...')

    #file.move_item(2, 0)

    mb.reorganize()

    main_window.show()

    app.exec_()