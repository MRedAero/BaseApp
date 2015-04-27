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

        self._view.action_window_htile.triggered.connect(self._window_horz_tile)
        self._view.action_window_vtile.triggered.connect(self._window_vert_tile)
        self._view.action_window_cascade.triggered.connect(self._window_cascade)

        #todo: remove for MDI
        #self._view.tab_widget.currentChanged.connect(self._update_current_tab)

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

        #todo: remove  deprecated for MDI
        # new_tab = QtGui.QWidget()
        # new_tab.setObjectName(_new_name)
        # new_tab.grid_layout = QtGui.QGridLayout(new_tab)
        # self._view.add_tab(new_tab, _new_name)


        # MDI
        new_subwindow = QtGui.QMdiSubWindow()
        new_subwindow.setWindowTitle(_new_name)
        # looks like will have to subclass the subwindow to install an event filter to handle window maximize
        #new_subwindow.windowStateChanged.connect(lambda: self.window_state(new_subwindow))
        self._view.add_subwindow(new_subwindow)

    def window_state(self,wdw):

        # on window state change... if wdw is maximized, switch mdiarea to subwindow view
        # may have to be done by subclasssing mdisubwindow
        #
        print("running")
        print("{0}".format(str(wdw.windowTitle())))
        print("{0}".format(str(wdw.windowState())))

        # if wdw.windowState() & QtCore.Qt.WindowMaximized:
        #     self._view.mdiarea.setViewMode(QtGui.QMdiArea.TabbedView)
        #     print("maximized: {0}".format(str(wdw.windowTitle())))
        # else:
        #     self._view.mdiarea.setViewMode(QtGui.QMdiArea.SubWindowView)
        #     print("minimized: {0}".format(str(wdw.windowTitle())))


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

    def _window_horz_tile(self):

        # todo:  investigate: some mdiarea attribute is adjusted on cascadeSubWindows and tileSubWindows
        #   currently execute cascadeSubWindows first before custom tiling ... if not, I miss some mdiarea attribute and doesn't display properly
        self._view.mdiarea.cascadeSubWindows()

        position = QtCore.QPoint(0,0)

        for wdw in self._view.mdiarea.subWindowList():

            new_width = self._view.mdiarea.size().width() / (len(self._view.mdiarea.subWindowList()))
            new_height = self._view.mdiarea.size().height()

            #todo:  new_height includes tabbed height... need it to be height of mdi content area

            #print("width = {0} / height = {1}".format(self._view.mdiarea.size().width(),self._view.mdiarea.size().height()))
            #print("new_width = {0} / new_height = {1}".format(new_width,new_height))

            # Note:  setGeometry does not override wdw Minimum Size.... have to reset Minimum Size
            wdw.setMinimumSize(0,0)
            rect = QtCore.QRect(0,0,new_width,new_height)
            wdw.setGeometry(rect)
            #print("wdw.w = {0} / wdw.h = {1}".format(wdw.width(),wdw.height()))

            wdw.move(position)
            position.setX(position.x() + wdw.width())

    def _window_vert_tile(self):

        # todo:  investigate: some mdiarea attribute is adjusted on cascadeSubWindows and tileSubWindows
        #   currently execute cascadeSubWindows first before custom tiling ... if not, I miss some mdiarea attribute and doesn't display properly
        self._view.mdiarea.cascadeSubWindows()


        # Note:  subwindow maximize event needs to change mdiarea to tabbed view
        #self._view.mdiarea.setViewMode(QtGui.QMdiArea.SubWindowView)

        position = QtCore.QPoint(0,0)

        for wdw in self._view.mdiarea.subWindowList():

            new_width = self._view.mdiarea.size().width()
            new_height = self._view.mdiarea.size().height() / (len(self._view.mdiarea.subWindowList()))

            #todo:  new_height includes tabbed height... need it to be height of mdi content area
            #   --- IF staying in TabbedView Mode
            #   --- ELSE... over-ride the tab maximize event to switch back to tabbed view



            #print("width = {0} / height = {1}".format(self._view.mdiarea.size().width(),self._view.mdiarea.size().height()))
            #print("new_width = {0} / new_height = {1}".format(new_width,new_height))

            # Note:  setGeometry does not override wdw Minimum Size.... have to reset Minimum Size
            wdw.setMinimumSize(0,0)
            rect = QtCore.QRect(0,0,new_width,new_height)
            wdw.setGeometry(rect)
            #print("wdw.w = {0} / wdw.h = {1}".format(wdw.width(),wdw.height()))

            wdw.move(position)
            position.setY(position.y() + wdw.height())


    def _window_cascade(self):

        # Set cascading window size related to mdiarea size
        w_min = self._view.mdiarea.size().width() * 0.6
        h_min = self._view.mdiarea.size().height() * 0.6

        for wdw in self._view.mdiarea.subWindowList():
            wdw.setMinimumSize(w_min,h_min)
        self._view.mdiarea.cascadeSubWindows()
