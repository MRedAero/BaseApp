__author__ = 'Michael Redmond'

from PyQt4 import QtGui, QtCore

from base_app.simple_pubsub import pub

from mdi_subwindow import MdiSubWindow

from base_app.utilities.menus import MenuController


class MDIController(object):
    def __init__(self, view):
        self._view = view
        """:type: base_app.application.core.view.view_core.BaseAppViewCore"""


        #Optional Image Background
        # Uncomment either image or None option
        #
        #1.:
        #background_img = QtGui.QPixmap(r'D:\DELETEME\BaseApp\base_app\application\core\document\background.png')
        #2.:
        background_img=None

        if background_img:
            self._mdiarea = MdiArea(parent = self._view.central_widget, pixmap=background_img, pixmap_position='bottom_right')
        else:
            self._mdiarea = MdiArea(parent = self._view.central_widget)

            # Can customize the Background with Brush
            brush = QtGui.QBrush()
            brush.setStyle(QtCore.Qt.Dense4Pattern)
            color = QtGui.QColor('#000')
            brush.setColor(color)
            self._mdiarea.setBackground(brush)


        self._mdiarea.setTabsClosable(False)
        self._mdiarea.setTabsMovable(True)

        self._mdiarea.setViewMode(QtGui.QMdiArea.TabbedView)
        self._view.grid_layout.addWidget(self._mdiarea, 0, 0, 1, 1)
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
        pub.subscribe(self.show_window_tabs, "mdi.show_window_tabs")

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

        # Check the tab_height 1st..  If it was 0.. we will setup the tabBar
        last_tab_height = self.get_tab_height()

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

        if last_tab_height == 0:
            self.setup_tabbar()

        # I don't think this is needed
        #self._mdiarea.setActiveSubWindow(subwindow)


        self.build_window_menu(len(self._mdiarea_subwindows))

    def remove_subwindow(self, index):
        subwindow = self._mdiarea_subwindows[index]

        if subwindow not in self._mdiarea.subWindowList():
            return

        # Do not need to .removeSubWindow
        #self._mdiarea.removeSubWindow(subwindow)

        # Remove it from our list
        self._mdiarea_subwindows.remove(subwindow)

        if index == len(self._mdiarea_subwindows):
            self._next_window()

        self._update_window_view()
        self.build_window_menu(index)

    def _update_window_view(self):

        # This maintains the state on window close.. default QT behavior on close is to show tiled, but un-organized
        if self._window_mode == "maximized":
            if self._mdiarea.activeSubWindow():
                self._mdiarea.activeSubWindow().showMaximized()
            else:
                if len(self._mdiarea_subwindows) > 0:
                    self._mdiarea.setActiveSubWindow(self._mdiarea_subwindows[0])
                    self._mdiarea.activeSubWindow().showMaximized()
        elif self._window_mode == "horizontal_tile":
            self.tile_windows_horizontally()
        elif self._window_mode == "vertical_tile":
            self.tile_windows_vertically()
        elif self._window_mode == "cascade":
            self.cascade_windows()

    def build_window_menu(self, index):

        # If the window_menu was created... Delete it and clear the menuBar
        if hasattr(self,'window_menu'):
            self._view.menu_controller.delete_item(self.window_menu)

        self.window_menu = self._view.menu_controller.add_menu('Window')

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
        self.action_window_showtabs= self.window_menu.add_action('Show Tabs').get_action()
        """:type: QtGui.QAction"""
        self.action_window_showtabs.setCheckable(True)
        self.action_window_showtabs.setChecked(True)

        # why are the separators named?
        self.window_menu.add_separator('3')

        self.action_window_new.triggered.connect(self._file_new)
        self.action_window_close.triggered.connect(self._file_close)
        self.action_window_htile.triggered.connect(self.tile_windows_horizontally)
        self.action_window_vtile.triggered.connect(self.tile_windows_vertically)
        self.action_window_cascade.triggered.connect(self.cascade_windows)
        self.action_window_showtabs.triggered.connect(self.show_window_tabs)

        # Move Window to Last - 1
        # todo: is this standard, or should the MDI_Controller be told where to place the Window Menu
        self._view.menu_controller.move_item(len(self._view.menu_controller._items)-1,len(self._view.menu_controller._items)-2)
        self._view.menu_controller.reorganize()

        # Add Open Documents Window Menu Actions
        #   after .reorganize() since the action group not within the MenuController class
        menu = self.window_menu.get_menu()
        self.wdw_action_group = QtGui.QActionGroup(self._mdiarea,exclusive=True)
        self.wdw_action_group.setExclusive(True)
        self.wdw_action_group.checkedAction()
        for wdw in self._mdiarea_subwindows:
            action_wdw_item = self.wdw_action_group.addAction(QtGui.QAction(wdw.windowTitle(),self._mdiarea, checkable=True))
            """:type: QtGui.QAction"""
            action_wdw_item.setCheckable(True)
            if wdw == self._mdiarea.currentSubWindow(): ## note: active is old
                action_wdw_item.setChecked(True)
            action_wdw_item.triggered.connect(self._select_window_from_menu)
            menu.addAction(action_wdw_item)


    def _select_window_from_menu(self,wdw):
        actions = self.wdw_action_group.actions()
        for action in self.wdw_action_group.actions():
            if action.isChecked():
                index = actions.index(action)

        self._set_active_document(index)

    def _update_window_actions(self):
        """ Update the checked item in the window menu.

        .. note:: This fires before the window_menu is rebuilt.  Therefore must check for the action_group attribute and
                  also if the index is valid.
        """
        index = self.get_current_index()
        if index == -1: return

        if hasattr(self, 'wdw_action_group'):
            if index > len(self.wdw_action_group.actions())-1:return
            self.wdw_action_group.actions()[index].setChecked(True)

    def _subwindow_activated(self, subwindow):
        index = self.get_subwindow_index(subwindow)
        #print 'subwindow activated = %d' % index
        if subwindow in self._mdiarea.subWindowList():
            print('subwindow activated: index = {0} : title = {1}'.format(index, subwindow.windowTitle()))
        else:
            print('subwindow activated: index = {0}'.format(index))

        pub.publish("program.set_active_document", index=index)

        self._update_window_actions()

    def _set_active_document(self, index):

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

    def tile_windows_horizontally(self):
        self._window_mode = "horizontal_tile"

        # todo:  investigate: an mdiarea attribute is adjusted on cascadeSubWindows and tileSubWindows
        # currently execute cascadeSubWindows first before custom tiling ...
        # if not, I miss some mdiarea attribute and doesn't display properly
        self._mdiarea.cascadeSubWindows()

        position = QtCore.QPoint(0, 0)
        for subwindow in self._mdiarea.subWindowList():
            if self.action_window_showtabs.isChecked():
                tab_height = self.tab_height
            else:
                tab_height = 0
            print('tab_height = {0}'.format(self.tab_height))
            new_width = self._mdiarea.size().width() / (len(self._mdiarea.subWindowList()))
            new_height = self._mdiarea.size().height() - tab_height

            # Note:  setGeometry does not override wdw Minimum Size.... have to reset Minimum Size
            subwindow.setMinimumSize(0, 0)
            rect = QtCore.QRect(0, 0, new_width, new_height)
            subwindow.setGeometry(rect)
            subwindow.move(position)
            position.setX(position.x() + subwindow.width())

    def tile_windows_vertically(self):
        self._window_mode = "vertical_tile"

        # todo:  investigate: some mdiarea attribute is adjusted on cascadeSubWindows and tileSubWindows
        # currently execute cascadeSubWindows first before custom tiling ...
        # if not, I miss some mdiarea attribute and doesn't display properly
        self._mdiarea.cascadeSubWindows()

        if self.action_window_showtabs.isChecked():
            #tab_height = self._mdiarea.findChild(QtGui.QTabBar).height()
            tab_height = self.tab_height
        else:
            tab_height = 0
        print('tab_height = {0}'.format(self.tab_height))
        position = QtCore.QPoint(0, 0)
        for subwindow in self._mdiarea.subWindowList():
            new_width = self._mdiarea.size().width()
            new_height = (self._mdiarea.size().height() - tab_height) / (len(self._mdiarea.subWindowList()))

            # Note:  setGeometry does not override wdw Minimum Size.... have to reset Minimum Size
            subwindow.setMinimumSize(0, 0)
            rect = QtCore.QRect(0, 0, new_width, new_height)
            subwindow.setGeometry(rect)
            subwindow.move(position)
            position.setY(position.y() + subwindow.height())

    def get_tab_height(self):
        tab_bar = self._mdiarea.findChild(QtGui.QTabBar)
        if tab_bar != None:
            tab_height =  self._mdiarea.findChild(QtGui.QTabBar).height()
        else:
            tab_height = 0

        return tab_height

    def cascade_windows(self):
        self._window_mode = "cascade"
        w_min = self._mdiarea.size().width() * 0.6
        h_min = self._mdiarea.size().height() * 0.6

        for subwindow in self._mdiarea.subWindowList():
            subwindow.setMinimumSize(w_min, h_min)
        self._mdiarea.cascadeSubWindows()

    def show_window_tabs(self):

        if self.action_window_showtabs.isChecked():
            print("true")
            self._mdiarea.setViewMode(QtGui.QMdiArea.TabbedView)

            self.setup_tabbar()

            # Have to find the QTabBar again.....
            # @ Nick: do you only need to find the tab bar once and then store it as an attribute?
            # @ Mike: unfortunately seems to be destroyed on view change
            #
            #self._mdiarea.findChild(QtGui.QTabBar).setExpanding(False)
        else:
            self._mdiarea.setViewMode(QtGui.QMdiArea.SubWindowView)

            # Note .SubWindowView changed to a tiled un_organized window, so update the state
            self._update_window_view()

    def setup_tabbar(self):
        """Configure the TabBar.

        """
        # tabbar destroyed on tab view changed
        self._mdiarea_tabbar = self._mdiarea.findChild(QtGui.QTabBar)
        self._mdiarea_tabbar.setExpanding(False)
        #self._mdiarea_tabbar.setSelectionBehaviorOnRemove(2)
        self._mdiarea_tabbar.setUsesScrollButtons(False)
        self.tab_height = self.get_tab_height()

        # Add Widget to TabBar
        _gridLayout = QtGui.QGridLayout(self._mdiarea_tabbar)
        _gridLayout.setAlignment(QtCore.Qt.AlignVCenter)
        _gridLayout.setMargin(0)
        _gridLayout.setHorizontalSpacing(0)
        _spacerItem = QtGui.QSpacerItem(self.tab_height, self.tab_height, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        _spacerItem.setAlignment(QtCore.Qt.AlignVCenter)
        _gridLayout.addItem(_spacerItem,0,0,1,1)

        # TabBar Nav Buttons
        _closebtn = QtGui.QPushButton()
        _leftbtn = QtGui.QPushButton()
        _rightbtn = QtGui.QPushButton()
        _sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        _closebtn.setSizePolicy(_sizePolicy)
        _leftbtn.setSizePolicy(_sizePolicy)
        _rightbtn.setSizePolicy(_sizePolicy)
        _closebtn.setFixedSize(QtCore.QSize(self.tab_height, self.tab_height))
        _leftbtn.setFixedSize(QtCore.QSize(self.tab_height, self.tab_height))
        _rightbtn.setFixedSize(QtCore.QSize(self.tab_height, self.tab_height))
        _closebtn.setText("")
        _leftbtn.setText("")
        _rightbtn.setText("")

        #todo:  move this out for customization
        _tab_button_style = 'QPushButton {border: 0px;} QPushButton::hover {border-style: solid; border-width: 1px; background-color: #E0F0FF; border-color: #bbb;}'
        _closebtn.setStyleSheet(_tab_button_style)
        _leftbtn.setStyleSheet(_tab_button_style)
        _rightbtn.setStyleSheet(_tab_button_style)

        # Default Icons for now
        _closebtn.setIcon(QtGui.qApp.style().standardIcon(QtGui.QStyle.SP_DockWidgetCloseButton))
        _leftbtn.setIcon(QtGui.qApp.style().standardIcon(QtGui.QStyle.SP_ArrowBack))
        _rightbtn.setIcon(QtGui.qApp.style().standardIcon(QtGui.QStyle.SP_ArrowRight))

        _gridLayout.addWidget(_leftbtn,0,1,QtCore.Qt.AlignTop)
        _gridLayout.addWidget(_rightbtn,0,2,QtCore.Qt.AlignTop)
        _gridLayout.addWidget(_closebtn,0,3,QtCore.Qt.AlignTop)

        _closebtn.pressed.connect(self._file_close)
        _rightbtn.pressed.connect(self._next_window)
        _leftbtn.pressed.connect(self._previous_window)

    def _file_close(self):
        pub.publish('program.close_file', index=self._mdiarea.subWindowList().index(self._mdiarea.currentSubWindow()))

    def _file_new(self):
        pub.publish('program.new_file')

    def _next_window(self):
        self._mdiarea.activateNextSubWindow()

    def _previous_window(self):
        self._mdiarea.activatePreviousSubWindow()



# Provision for MdiArea subclass... Not yet used
class MdiArea(QtGui.QMdiArea):
    def __init__(self, parent=None, pixmap=None, pixmap_position='centered'):
        super(MdiArea, self).__init__()

        self.background_pixmap = pixmap
        self.background_position = pixmap_position
        self.centered = False

    def paintEvent(self, event):

        print('painting')
        if self.background_pixmap:
            painter = QtGui.QPainter()
            painter.begin(self.viewport())
            painter.fillRect(event.rect(), self.palette().color(QtGui.QPalette.Window))
            if self.background_position == 'bottom_right':
                painter.drawPixmap(self.width()-self.background_pixmap.width(), self.height()-self.background_pixmap.height(), self.background_pixmap.width(), self.background_pixmap.height(), self.background_pixmap)
            elif self.background_position == 'top_right':
                painter.drawPixmap(self.width()-self.background_pixmap.width(), 0, self.background_pixmap.width(), self.background_pixmap.height(), self.background_pixmap)
            elif self.background_position == 'bottom_left':
                painter.drawPixmap(0, self.height()-self.background_pixmap.height(), self.background_pixmap.width(), self.background_pixmap.height(), self.background_pixmap)
            elif self.background_position == 'top_left':
                painter.drawPixmap(0, 0, self.background_pixmap.width(), self.background_pixmap.height(), self.background_pixmap)
            elif self.background_position == 'center_scale_to_fit':
                x = (self.width() - self.display_pixmap.width())/2
                y = (self.height() - self.display_pixmap.height())/2
                painter.drawPixmap(x, y, self.display_pixmap)
            elif self.background_position == 'center_stretch_to_fit':
                painter.drawPixmap(0, 0, self.width(), self.height(), self.background_pixmap)
            elif self.background_position == 'centered':
                x = (self.width() - self.background_pixmap.width())/2
                y = (self.height() - self.background_pixmap.height())/2
                painter.drawPixmap(x, y, self.background_pixmap.width(), self.background_pixmap.height(), self.background_pixmap)

            painter.end()
        else:
            return super(MdiArea,self).paintEvent(event)

    def resizeEvent(self, event):
        if self.background_pixmap:
            self.display_pixmap = self.background_pixmap.scaled(event.size(), QtCore.Qt.KeepAspectRatio)
        return super(MdiArea,self).resizeEvent(event)