__author__ = 'Michael Redmond'

from PyQt4 import QtGui, QtCore

from base_app.simple_pubsub import pub


class MDIController(object):
    def __init__(self, view):
        self._view = view
        """:type: base_app.application.core.view.view_core.BaseAppViewCore"""

        # MDI
        self._mdiarea = MdiArea(self._view.central_widget)
        # self._mdiarea = QtGui.QMdiArea(self._view.central_widget)
        #self._mdiarea.setDocumentMode(True)
        self._mdiarea.setTabsClosable(True)
        self._mdiarea.setTabsMovable(True)
        self._mdiarea.setViewMode(QtGui.QMdiArea.TabbedView)
        #self._mdiarea.setViewMode(QtGui.QMdiArea.SubWindowView)
        self._mdiarea_tabbar = self._mdiarea.findChild(QtGui.QTabBar)
        self._mdiarea_tabbar.setExpanding(False)

        self._mdiarea.subWindowActivated.connect(self._update_current_document)

        self._view.grid_layout.addWidget(self._mdiarea, 0, 0, 1, 1)

        ###  Issue with this signal...  Migrate to add signal: aboutToActivate to the subwindow when created
        #self._mdiarea.subWindowActivated.connect(self._update_current_document)

        self._skip = 0

        self._window_mode = "maximized"
        self._show_tabs = True

        self._subscribe_to_pub()


    def _subscribe_to_pub(self):
        pub.subscribe(self._set_active_document, "view.set_active_view")
        pub.subscribe(self._close_document, "view.close_view")
        pub.subscribe(self._new_document, "view.new_view")

    def get_current_index(self):
        try:
            return self._mdiarea.subWindowList().index(self.get_active_document())
        except (IndexError, ValueError):
            return -1

    def get_active_document(self):
        return self._mdiarea.activeSubWindow()

    def _new_document(self, name):
        # Sub Class
        new_subwindow = SubWindow(self._mdiarea.subWindowList, self.get_active_document)
        #new_subwindow = QtGui.QMdiSubWindow()
        new_subwindow.setWindowTitle(name)
        # new_subwindow.maximized.connect(lambda: self.set_tab_view(new_subwindow))
        self._skip = 1
        self._mdiarea.addSubWindow(new_subwindow)

        # Define minimum size...
        golden_ratio = 1.618
        if self._view.width() > 500.:
            minwidth = 350.
        else:
            minwidth = 100.

        new_subwindow.setMinimumSize(minwidth, minwidth / golden_ratio)
        #new_subwindow.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        new_subwindow.setOption(QtGui.QMdiSubWindow.RubberBandResize)
        new_subwindow.setOption(QtGui.QMdiSubWindow.RubberBandMove)
        new_subwindow.showMaximized()
        new_subwindow.show()

        self._mdiarea.setActiveSubWindow(new_subwindow)

        return True

    def _close_document(self, index):
        if not self._mdiarea.subWindowList():
            return
        self._skip = 1
        self._mdiarea.removeSubWindow(self._mdiarea.subWindowList()[index])
        self._skip = 0

        # This maintains the state on window close.. default QT behavior on close is to show tiled, but un-organized
        if self._window_mode == "maximized":
            self._mdiarea.activeSubWindow().showMaximized()
        elif self._window_mode == "horizontal_tile":
            self.tile_windows_horizontally(self._show_tabs)
        elif self._window_mode == "vertical_tile":
            self.tile_windows_vertically(self._show_tabs)
        elif self._window_mode == "cascade":
            self.cascade_windows()

    def _set_active_document(self, index):
        subwindow = self._mdiarea.subWindowList()[index]
        self._skip = 1
        self._mdiarea.setActiveSubWindow(subwindow)
        self._skip = 0

        print "%d = %d" % (index, self.get_current_index())

    def _update_current_document(self, active_doc):
        # this should only be used when the user clicks on a new subwindow, any other time it should be skipped
        # and handled by the program controller
        if self._skip:
            self._skip -= 1
            return

        if not active_doc:
            return

        if self.get_current_index() == -1:
            pub.publish('program.new_file')
            return

        if active_doc:
            index = self._mdiarea.subWindowList().index(active_doc)
            pub.publish('program.set_active_document', index=index)
            return

    def set_tab_view(self, subwindow):
        subwindow.showMaximized()
        self._mdiarea.setViewMode(QtGui.QMdiArea.TabbedView)

    def tile_windows_horizontally(self, show_tabs = True):
        self._window_mode = "horizontal_tile"

        # todo:  investigate: an mdiarea attribute is adjusted on cascadeSubWindows and tileSubWindows
        # currently execute cascadeSubWindows first before custom tiling ...
        # if not, I miss some mdiarea attribute and doesn't display properly
        self._mdiarea.cascadeSubWindows()

        position = QtCore.QPoint(0, 0)
        for subwindow in self._mdiarea.subWindowList():
            if show_tabs == True:
                tab_height = self._mdiarea.findChild(QtGui.QTabBar).height()
            else:
                tab_height = 0
            new_width = self._mdiarea.size().width() / (len(self._mdiarea.subWindowList()))
            new_height = self._mdiarea.size().height() - tab_height

            # Note:  setGeometry does not override wdw Minimum Size.... have to reset Minimum Size
            subwindow.setMinimumSize(0, 0)
            rect = QtCore.QRect(0, 0, new_width, new_height)
            subwindow.setGeometry(rect)
            subwindow.move(position)
            position.setX(position.x() + subwindow.width())

    def tile_windows_vertically(self, show_tabs=True):
        self._window_mode = "vertical_tile"

        # todo:  investigate: some mdiarea attribute is adjusted on cascadeSubWindows and tileSubWindows
        # currently execute cascadeSubWindows first before custom tiling ...
        # if not, I miss some mdiarea attribute and doesn't display properly
        self._mdiarea.cascadeSubWindows()

        position = QtCore.QPoint(0, 0)
        for subwindow in self._mdiarea.subWindowList():
            if show_tabs == True:
                tab_height = self._mdiarea.findChild(QtGui.QTabBar).height()
            else:
                tab_height = 0
            new_width = self._mdiarea.size().width()
            new_height = (self._mdiarea.size().height() - tab_height) / (len(self._mdiarea.subWindowList()))

            # Note:  setGeometry does not override wdw Minimum Size.... have to reset Minimum Size
            subwindow.setMinimumSize(0, 0)
            rect = QtCore.QRect(0, 0, new_width, new_height)
            subwindow.setGeometry(rect)
            subwindow.move(position)
            position.setY(position.y() + subwindow.height())

    def cascade_windows(self):
        self._window_mode = "cascade"

        w_min = self._mdiarea.size().width() * 0.6
        h_min = self._mdiarea.size().height() * 0.6

        for subwindow in self._mdiarea.subWindowList():
            subwindow.setMinimumSize(w_min, h_min)
        self._mdiarea.cascadeSubWindows()

    def show_window_tabs(self, show_tabs=True):
        self._show_tabs = show_tabs

        if show_tabs == True:
            self._mdiarea.setViewMode(QtGui.QMdiArea.TabbedView)
            # Have to find the QTabBar again.....
            self._mdiarea.findChild(QtGui.QTabBar).setExpanding(False)
        elif show_tabs == False:
            self._mdiarea.setViewMode(QtGui.QMdiArea.SubWindowView)
            self.cascade_windows()



class MdiArea(QtGui.QMdiArea):
    def __init__(self, parent=None):
        QtGui.QMdiArea.__init__(self)
        pass

        # def closeEvent(self):
        # pass


class SubWindow(QtGui.QMdiSubWindow):
    def __init__(self, window_list_getter, active_document_getter):
        super(SubWindow, self).__init__()

        self._window_list_getter = window_list_getter
        self._active_document_getter = active_document_getter

    def get_index(self):
        try:
            return self._window_list_getter().index(self)
        except IndexError:
            return -1

    def get_active_document(self):
        return self._active_document_getter()

    def closeEvent(self, event):
        index = self.get_index()

        if index < 0:
            print 'this QMdiSubWindow is no longer part of the subWindowList'
            super(SubWindow, self).closeEvent(event)
            return

        self.clear_layout()

        pub.publish('program.close_file', index=index)

        active_doc = self.get_active_document()

        # @Nick: if cascading or tiling is on, that should be updated so there's no empty space in the mdi area
        if self.isMaximized() and active_doc:
            active_doc.showMaximized()

        super(SubWindow, self).closeEvent(event)

    def clear_layout(self):
        layout = self.layout()

        while True:
            child = layout.takeAt(0)
            if not child:
                break
            widget = child.widget()
            layout.removeWidget(widget)
            del child







