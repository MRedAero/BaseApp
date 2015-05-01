__author__ = 'Michael Redmond'

from PyQt4 import QtGui, QtCore

from base_app.utilities.menus import MenuController


class BaseAppViewCore(QtGui.QMainWindow):
    def __init__(self):
        super(BaseAppViewCore, self).__init__()

        flags = QtGui.QMainWindow.AllowNestedDocks | QtGui.QMainWindow.AllowTabbedDocks

        self.setDockOptions(flags)

        self.setObjectName("BaseMainWindow")
        self.resize(850, 600)

        self.setWindowTitle("BaseMainWindow")

        self.central_widget = QtGui.QWidget(self)
        self.central_widget.setObjectName("central_widget")
        self.setCentralWidget(self.central_widget)

        self.grid_layout = QtGui.QGridLayout(self.central_widget)
        self.grid_layout.setMargin(0)
        self.grid_layout.setSpacing(0)
        self.grid_layout.setObjectName("grid_layout")

        self.toolbar = self.addToolBar('Toolbar')

        self.menu_bar = QtGui.QMenuBar(self)
        self.menu_bar.setGeometry(0, 0, 850, 21)
        self.menu_bar.setObjectName("menu_bar")

        self.setMenuBar(self.menu_bar)

        self.status_bar = QtGui.QStatusBar(self)
        self.status_bar.setObjectName("status_bar")

        self.setStatusBar(self.status_bar)

        self.menu_controller = MenuController(self.menu_bar, "menu_bar")

        QtCore.QMetaObject.connectSlotsByName(self)

        self.build_menu()

    def build_menu(self):

        self._build_file_menu()
        self._build_edit_menu()
        self._build_tool_menu()
        self._build_window_menu()
        self._build_help_menu()

        self.menu_controller.reorganize()

    def _build_file_menu(self):

        self.file_menu = self.menu_controller.add_menu('File')
        """:type: QtGui.QMenu"""
        self.action_file_new = self.file_menu.add_action('New...').get_action()
        """:type: QtGui.QAction"""
        self.action_file_open = self.file_menu.add_action('Open...').get_action()
        """:type: QtGui.QAction"""
        self.action_file_save = self.file_menu.add_action('Save').get_action()
        """:type: QtGui.QAction"""
        self.action_file_save_as = self.file_menu.add_action('Save As...').get_action()
        """:type: QtGui.QAction"""
        self.action_file_close = self.file_menu.add_action('Close').get_action()
        """:type: QtGui.QAction"""
        self.file_menu.add_separator('sep1')

        self.action_file_settings = self.file_menu.add_action('Settings...').get_action()
        """:type: QtGui.QAction"""

        self.file_menu.add_separator('sep2')
        self.action_file_exit = self.file_menu.add_action('Exit').get_action()
        """:type: QtGui.QAction"""

    def _build_edit_menu(self):

        self.edit_menu = self.menu_controller.add_menu('Edit')
        """:type: QtGui.QMenu"""

    def _build_tool_menu(self):

        self.tool_menu = self.menu_controller.add_menu('Tools')
        """:type: QtGui.QMenu"""

    def _build_window_menu(self):

        self.window_menu = self.menu_controller.add_menu('Window')
        """:type: QtGui.QMenu"""
        self.action_window_new = self.window_menu.add_action('New Window...').get_action()
        """:type: QtGui.QAction"""
        self.action_window_close = self.window_menu.add_action('Close Window').get_action()
        """:type: QtGui.QAction"""

        # why are the separators named?
        self.window_menu.add_separator('1')
        self.action_window_htile = self.window_menu.add_action('Tile Horizontally').get_action()
        """:type: QtGui.QAction"""
        self.action_window_vtile = self.window_menu.add_action('Tile Vertically').get_action()
        """:type: QtGui.QAction"""
        self.action_window_cascade = self.window_menu.add_action('Cascade').get_action()
        """:type: QtGui.QAction"""

        # why are the separators named?
        self.window_menu.add_separator('2')
        self.action_window_tabview= self.window_menu.add_action('Show Tabs').get_action()
        """:type: QtGui.QAction"""
        self.action_window_tabview.setCheckable(True)
        self.action_window_tabview.setChecked(True)

        # why are the separators named?
        self.window_menu.add_separator('3')



    def _build_help_menu(self):

        self.help_menu = self.menu_controller.add_menu('Help')
        self.action_help_about = self.help_menu.add_action('About...').get_action()
        """:type: QtGui.QAction"""


if __name__ == '__main__':
    import sys

    app = QtGui.QApplication(sys.argv)

    main_window = BaseAppViewCore()

    main_window.show()

    app.exec_()

