__author__ = 'Michael Redmond'

from PyQt4 import QtCore, QtGui

from base_app.simple_pubsub import pub
from view_core import BaseAppViewCore
from base_app.application.core.document.mdi_controller import MDIController


class BaseAppViewController(object):
    def __init__(self, app):
        super(BaseAppViewController, self).__init__()

        self._app = app
        """:type: base_app.application.BaseQApplication"""

        self._view = self.create_view()
        """:type: BaseAppViewCore"""

        self._connect_signals()

        # todo: move to mdi_controller.. delete here
        self._connect_window_menu()

    def get_view(self):
        return self._view

    def create_view(self):
        return BaseAppViewCore()

    def _connect_signals(self):
        self._view.action_file_new.triggered.connect(self._file_new)
        self._view.action_file_open.triggered.connect(self._file_open)
        self._view.action_file_save.triggered.connect(self._file_save)
        self._view.action_file_save_as.triggered.connect(self._file_save_as)
        self._view.action_file_close.triggered.connect(self._file_close)

        self._view.action_file_settings.triggered.connect(self._file_settings)
        self._view.action_file_exit.triggered.connect(self._file_exit)

    # todo: move to mdi_controller.. delete here
    def _connect_window_menu(self):

        self._view.action_window_new.triggered.connect(self._file_new)
        self._view.action_window_close.triggered.connect(self._file_close)

        self._view.action_window_htile.triggered.connect(self._tile_windows_horizontally)
        self._view.action_window_vtile.triggered.connect(self._tile_windows_vertically)
        self._view.action_window_cascade.triggered.connect(self._cascade_windows)
        self._view.action_window_showtabs.triggered.connect(self._show_window_tabs)

    def show(self):
        self._view.show()

    def _file_new(self):
        pub.publish('program.new_file')

    def _file_close(self):
        pub.publish('program.close_file', index=None)

    def _file_open(self):
        # noinspection PyCallByClass
        filename = QtGui.QFileDialog.getOpenFileName(self._view, 'Open File', "",
                                                     "All Files (*.txt)")

        if isinstance(filename, list):
            filename = filename[0]

        if filename == '':
            return

        filename = str(filename)

        self._app.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        try:
            pub.publish('program.open_file', filename=filename)
        finally:
            self._app.restoreOverrideCursor()

    def _set_file(self, file_):
        pass

    def _file_save(self):
        print 'file save'

    def _file_save_as(self):
        print 'file save as'

    def _file_settings(self):
        pub.publish('program.settings')

    def _file_exit(self):
        print 'file exit'

    def add_dock_widget(self, dock_area, dock_widget):
        self._view.addDockWidget(dock_area, dock_widget)

    def remove_dock_widget(self, dock_widget):
        self._view.removeDockWidget(dock_widget)

    def _tile_windows_horizontally(self):
        pub.publish("mdi.tile_windows_horizontally")

    def _tile_windows_vertically(self):
        pub.publish("mdi.tile_windows_vertically")

    def _cascade_windows(self):
        pub.publish("mdi.cascade_windows")

    def _show_window_tabs(self):
        pub.publish("mdi.show_window_tabs")
