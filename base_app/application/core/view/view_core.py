__author__ = 'Michael Redmond'

from PyQt4 import QtGui, QtCore

from base_app.utilities.menus import MenuController


class BaseAppViewCore(QtGui.QMainWindow):
    def __init__(self):
        super(BaseAppViewCore, self).__init__()

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

        #todo: remove... deprecated to support mdi
        #self.tab_widget = QtGui.QTabWidget(self.central_widget)
        #self.tab_widget.setObjectName("tab_widget")
        #self.grid_layout.addWidget(self.tab_widget, 0, 0, 1, 1)

        self.mdiarea = QtGui.QMdiArea(self.central_widget)
        #self.mdiarea.setDocumentMode(True)
        self.mdiarea.setTabsClosable(True)
        self.mdiarea.setTabsMovable(True)
        self.mdiarea.setViewMode(QtGui.QMdiArea.TabbedView)
        self.grid_layout.addWidget(self.mdiarea, 0, 0, 1, 1)


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

    #todo: remove... deprecated to support mdi
    def add_tab(self, tab, name):

        self.tab_widget.addTab(tab, name)
        self.tab_widget.setCurrentIndex(self.tab_widget.count()-1)

        return True

    def add_subwindow(self, window):


        newwin = self.mdiarea.addSubWindow(window)

        # Define minimum size...
        golden_ratio = 1.618
        if self.width() > 500.:
            minwidth = 350.
        else:
            minwidth = 100.

        newwin.setMinimumSize(minwidth,minwidth / golden_ratio)
        newwin.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        newwin.setOption(QtGui.QMdiSubWindow.RubberBandResize)
        newwin.setOption(QtGui.QMdiSubWindow.RubberBandMove)

        newwin.show()

        return True

    #todo: remove... deprecated to support mdi
    def remove_tab(self, index):

        self.tab_widget.removeTab(index)

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

        self.file_settings = self.file_menu.add_menu('Settings')
        """:type: QtGui.QMenu"""
        self.action_file_settings_plugins = self.file_settings.add_action('Plugins...').get_action()
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

    def _build_help_menu(self):

        self.help_menu = self.menu_controller.add_menu('Help')
        self.action_help_about = self.help_menu.add_action('About...').get_action()
        """:type: QtGui.QAction"""

    def _build_window_menu(self):

        self.window_menu = self.menu_controller.add_menu('Window')
        """:type: QtGui.QMenu"""
        self.action_window_htile = self.window_menu.add_action('Tile Horizontally').get_action()
        """:type: QtGui.QAction"""
        self.action_window_vtile = self.window_menu.add_action('Tile Vertically').get_action()
        """:type: QtGui.QAction"""
        self.action_window_cascade = self.window_menu.add_action('Cascade').get_action()
        """:type: QtGui.QAction"""



if __name__ == '__main__':
    import sys

    app = QtGui.QApplication(sys.argv)

    main_window = BaseMainWindow()

    main_window.show()

    app.exec_()

