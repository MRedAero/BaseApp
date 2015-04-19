__author__ = 'Michael Redmond'

from PyQt4 import QtCore, QtGui

from base_app.utilities.misc import new_name

from base_app.application.core.view import BaseAppViewCore


class BaseAppViewController(object):
    def __init__(self, adaptor, app):

        super(BaseAppViewController, self).__init__()

        self._adaptor = adaptor
        """:type: base_app.application.adaptor.BaseAppAdaptor"""

        self._app = app
        """:type: base_app.application.BaseQApplication"""

        self._view = self.create_view_object()
        """:type: BaseAppViewCore"""

        self._is_active = False

        self._current_tab = -1

        self._connect_signals()

    @property
    def create_view_object(self):
        return BaseAppViewCore

    def _connect_signals(self):
        self._view.action_file_new.triggered.connect(self.new_document)
        self._view.action_file_open.triggered.connect(self._file_open)
        self._view.action_file_save.triggered.connect(self._file_save)
        self._view.action_file_save_as.triggered.connect(self._file_save_as)
        self._view.action_file_close.triggered.connect(self.close_document)

        self._view.action_file_settings_plugins.triggered.connect(self._file_settings_plugins)
        self._view.action_file_exit.triggered.connect(self._file_exit)

        self._view.tab_widget.currentChanged.connect(self._update_current_tab)

    def show(self):
        self._view.show()

    def is_active(self):
        return self._is_active

    def new_document(self):

        """This is where new documents will originate from.
        Either the user will click on the new document action in the File menu,
        or the user will directly call this method when using the api."""

        model_names = self._adaptor.get_model_names()

        _new_name = new_name(model_names)

        self._is_active = True
        if not self._adaptor.new_model(_new_name):
            return
        self._is_active = False

        new_tab = QtGui.QWidget()
        new_tab.setObjectName(_new_name)
        new_tab.grid_layout = QtGui.QGridLayout(new_tab)

        self._view.add_tab(new_tab, _new_name)

    def close_document(self):

        index = self._current_tab

        tab_to_close = self._view.tab_widget.getWidget(index)

        self._view.remove_tab(index)

        tab_to_close.setParent(None)

        self._is_active = True
        self._adaptor.close_model(index)
        self._is_active = False

    def _update_current_tab(self, index):

        self._current_tab = index

        self._is_active = True
        self._adaptor.set_active_model(index)
        self._is_active = False

    def _file_open(self):

        # noinspection PyCallByClass
        filename = QtGui.QFileDialog.getOpenFileName(self._view, 'Open File', "",
                                                     "All Files (*.txt)")

        if isinstance(filename, list):
            filename = filename[0]

        if filename == '':
            return

        filename = str(filename)

        if self._current_tab == -1:
            self.new_document()

        self._app.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        try:
            self._is_active = True
            success = self._adaptor.open_file(filename)
            self._is_active = False
        finally:
            self._app.restoreOverrideCursor()

    def set_file(self, file):
        pass

    def _file_save(self):
        print 'file save'

    def _file_save_as(self):
        print 'file save as'

    def _file_settings_plugins(self):
        print 'file settings plugins'

    def _file_exit(self):
        print 'file exit'
