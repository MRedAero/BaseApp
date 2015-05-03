__author__ = 'Michael Redmond'

from PyQt4 import QtGui, QtCore

from base_app.simple_pubsub import pub

from mdi_subwindow import MdiSubWindow


class MDIController(object):
    def __init__(self, view):
        self._view = view
        """:type: base_app.application.core.view.view_core.BaseAppViewCore"""

        self._mdiarea = QtGui.QMdiArea(self._view.central_widget)
        self._mdiarea.setTabsClosable(True)
        self._mdiarea.setTabsMovable(True)
        self._mdiarea.setViewMode(QtGui.QMdiArea.TabbedView)
        self._mdiarea_tabbar = self._mdiarea.findChild(QtGui.QTabBar)
        self._mdiarea_tabbar.setExpanding(False)

        #self._mdiarea.subWindowActivated.connect(self._update_current_document)

        self._view.grid_layout.addWidget(self._mdiarea, 0, 0, 1, 1)

        ###  Issue with this signal...  Migrate to add signal: aboutToActivate to the subwindow when created
        self._mdiarea.subWindowActivated.connect(self._subwindow_activated)

        self._window_mode = "maximized"
        self._show_tabs = True

        # List of active subwindows in order of creation (append on add, remove on close)
        # Allows windows/tabs to be moved and still retain their index
        self._mdiarea_subwindows = []

        self._subscribe_to_pub()

    def _subscribe_to_pub(self):
        pub.subscribe(self.tile_windows_horizontally, "mdi.tile_windows_horizontally")
        pub.subscribe(self.tile_windows_vertically, "mdi.tile_windows_vertically")
        pub.subscribe(self.cascade_windows, "mdi.cascade_windows")
        pub.subscribe(self.set_tab_view, "mdi.set_tab_view")
        pub.subscribe(self.set_tab_view, "mdi.show_window_tabs")

    def get_mdi_area(self):
        return self._mdiarea

    def get_subwindow_index(self, subwindow):
        try:
            #return self._mdiarea.subWindowList().index(subwindow)
            return self._mdiarea_subwindows.index(subwindow)
        except (IndexError, ValueError):
            return -1

    def get_current_index(self):
        try:
            #return self._mdiarea.subWindowList().index(self.get_active_document())
            return self._mdiarea_subwindows.index(self.get_active_document())

        except (IndexError, ValueError):
            return -1

    def get_active_document(self):
        return self._mdiarea.activeSubWindow()

    def add_subwindow(self, subwindow):
        # Sub Class
        #new_subwindow = MdiSubWindow(self)
        #new_subwindow = QtGui.QMdiSubWindow()
        #new_subwindow.setWindowTitle(name)
        # new_subwindow.maximized.connect(lambda: self.set_tab_view(new_subwindow))
        self._mdiarea.addSubWindow(subwindow)

        self._mdiarea_subwindows.append(subwindow)

        # Define minimum size...
        golden_ratio = 1.618
        if self._view.width() > 500.:
            minwidth = 350.
        else:
            minwidth = 100.

        subwindow.setMinimumSize(minwidth, minwidth / golden_ratio)
        #new_subwindow.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        subwindow.setOption(QtGui.QMdiSubWindow.RubberBandResize)
        subwindow.setOption(QtGui.QMdiSubWindow.RubberBandMove)
        subwindow.showMaximized()
        subwindow.show()

        # I don't think this is needed
        #self._mdiarea.setActiveSubWindow(subwindow)

    def remove_subwindow(self, index):
        subwindow = self._mdiarea_subwindows[index]

        if subwindow not in self._mdiarea.subWindowList():
            return

        # Do not need to .removeSubWindow
        #self._mdiarea.removeSubWindow(subwindow)

        # Remove it from our list though
        self._mdiarea_subwindows.remove(subwindow)

        # This maintains the state on window close.. default QT behavior on close is to show tiled, but un-organized
        if self._window_mode == "maximized":
            if self._mdiarea.activeSubWindow():
                self._mdiarea.activeSubWindow().showMaximized()
            else:
                if len(self._mdiarea_subwindows) > 0:
                    self._mdiarea.setActiveSubWindow(self._mdiarea_subwindows[0])
                    self._mdiarea.activeSubWindow().showMaximized()
        elif self._window_mode == "horizontal_tile":
            self.tile_windows_horizontally(self._show_tabs)
        elif self._window_mode == "vertical_tile":
            self.tile_windows_vertically(self._show_tabs)
        elif self._window_mode == "cascade":
            self.cascade_windows()

    def _subwindow_activated(self, subwindow):
        index = self.get_subwindow_index(subwindow)
        #print 'subwindow activated = %d' % index
        if subwindow in self._mdiarea.subWindowList():
            print('subwindow activated: index = {0} : title = {1}'.format(index, subwindow.windowTitle()))
        else:
            print('subwindow activated: index = {0}'.format(index))

        pub.publish("program.set_active_document", index=index)

    def _set_active_document(self, index):

        #ubwindow = self._mdiarea.subWindowList()[index]

        if self._mdiarea_subwindows[index] in self._mdiarea.subWindowList():
            subwindow = self._mdiarea_subwindows[index]
        else:
            subwindow = self._mdiarea.subWindowList()[0]

        self._skip = 1
        self._mdiarea.setActiveSubWindow(subwindow)
        self._skip = 0

        print "%d = %d" % (index, self.get_current_index())

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
            print("true")
            self._mdiarea.setViewMode(QtGui.QMdiArea.TabbedView)
            # Have to find the QTabBar again.....
            # @ Nick: do you only need to find the tab bar once and then store it as an attribute?
            self._mdiarea.findChild(QtGui.QTabBar).setExpanding(False)
        elif show_tabs == False:
            self._mdiarea.setViewMode(QtGui.QMdiArea.SubWindowView)
            self.cascade_windows()








