__author__ = 'Michael Redmond'

from PyQt4 import QtCore, QtGui

from base_app.simple_pubsub import pub
from view_core import BaseAppViewCore
from mdi_controller import MDIController


class BaseAppViewController(object):
    def __init__(self, app):
        super(BaseAppViewController, self).__init__()

        self._app = app
        """:type: base_app.application.BaseQApplication"""

        self._view = self.create_view_object()
        """:type: BaseAppViewCore"""

        self._mdi_controller = MDIController(self._view)

        self._connect_signals()
        self._subscribe_to_pub()

    def get_view(self):
        return self._view

    def create_view_object(self):
        return BaseAppViewCore()

    def _subscribe_to_pub(self):
        pub.subscribe(self._set_file, "view.set_file")

    def _connect_signals(self):
        self._view.action_file_new.triggered.connect(self._file_new)
        self._view.action_file_open.triggered.connect(self._file_open)
        self._view.action_file_save.triggered.connect(self._file_save)
        self._view.action_file_save_as.triggered.connect(self._file_save_as)
        self._view.action_file_close.triggered.connect(self._file_close)

        self._view.action_file_settings.triggered.connect(self._file_settings)
        self._view.action_file_exit.triggered.connect(self._file_exit)

        self._view.action_window_htile.triggered.connect(self._tile_windows_horizontally)
        self._view.action_window_vtile.triggered.connect(self._tile_windows_vertically)
        self._view.action_window_cascade.triggered.connect(self._cascade_windows)

    def show(self):
        self._view.show()

    def _file_new(self):
        pub.publish('program.new_file')

    def _file_close(self):
        index = self._mdi_controller.get_current_index()
        if index < 0:
            return
        pub.publish('program.close_file', index)

    def get_active_view(self):
        return self._mdi_controller.get_active_document()

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
        self._mdi_controller.tile_windows_horizontally()

    def _tile_windows_vertically(self):
        self._mdi_controller.tile_windows_vertically()

    def _cascade_windows(self):
        self._mdi_controller.cascade_windows()
