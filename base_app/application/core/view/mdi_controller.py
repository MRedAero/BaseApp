__author__ = 'Michael Redmond'

from PyQt4 import QtGui, QtCore

from base_app.simple_pubsub import pub


class MDIController(object):
    def __init__(self, view):
        self._view = view
        """:type: base_app.application.core.view.view_core.BaseAppViewCore"""

        #MDI
        self._mdiarea = MdiArea(self._view.central_widget)
        #self._mdiarea = QtGui.QMdiArea(self._view.central_widget)
        #self._mdiarea.setDocumentMode(True)
        self._mdiarea.setTabsClosable(True)
        self._mdiarea.setTabsMovable(True)
        self._mdiarea.setViewMode(QtGui.QMdiArea.TabbedView)
        #self._mdiarea.setViewMode(QtGui.QMdiArea.SubWindowView)
        self._mdiarea_tabbar = self._mdiarea.findChild(QtGui.QTabBar)
        self._mdiarea_tabbar.setExpanding(False)

        self._view.grid_layout.addWidget(self._mdiarea, 0, 0, 1, 1)

        ###  Issue with this signal...  Migrate to add signal: aboutToActivate to the subwindow when created
        #self._mdiarea.subWindowActivated.connect(self._update_current_document)

        self._current_index = -1
        self._active_document = None
        self._skip = 0

    def add_document(self, window):

        # Sub Class
        #new_subwindow = SubWindow()
        new_subwindow = QtGui.QMdiSubWindow()
        new_subwindow.setWindowTitle(window)
        #new_subwindow.maximized.connect(lambda: self.set_tab_view(new_subwindow))
        self._mdiarea.addSubWindow(new_subwindow)

        new_subwindow.aboutToActivate.connect(self._update_current_document)

        # Define minimum size...
        golden_ratio = 1.618
        if self._view.width() > 500.:
            minwidth = 350.
        else:
            minwidth = 100.

        new_subwindow.setMinimumSize(minwidth,minwidth / golden_ratio)
        new_subwindow.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        new_subwindow.setOption(QtGui.QMdiSubWindow.RubberBandResize)
        new_subwindow.setOption(QtGui.QMdiSubWindow.RubberBandMove)
        new_subwindow.showMaximized()
        new_subwindow.show()

        self._current_index = len(self._mdiarea.subWindowList()) - 1
        self._active_document = self._mdiarea.subWindowList()[-1]

        return True

    def close_document(self, index):
        self._mdiarea.removeSubWindow(self._mdiarea.subWindowList()[index])

    def set_active_document(self, index):
        #print("Set Active Document = {0}".format(index))
        self._current_index = index
        self._active_document = self._mdiarea.setActiveSubWindow(self._mdiarea.subWindowList()[index])


    def get_current_index(self):
        return self._current_index

    def get_active_document(self):
        return self._active_document

    def _update_current_document(self):
        if self._skip:  # why is this needed to prevent infinite recursion?  probably should fix
            self._skip -= 1
            return

        if self._current_index == -1:
            pub.publish('program.new_file')
            return

        sub_windows = self._mdiarea.subWindowList()
        active_sub = self._mdiarea.activeSubWindow()
        #print("mdi_controller.py sub_windows:{0} / active_sub = {1}".format(sub_windows,active_sub))
        if active_sub:
            index = sub_windows.index(active_sub)
            #print("mdi_controller.py _update_current_document index = {0}".format(index))
            pub.publish('program.set_active_document', index=index)
            return

    def set_tab_view(self,wdw):
        wdw.showMaximized()
        self._mdiarea.setViewMode(QtGui.QMdiArea.TabbedView)

class MdiArea(QtGui.QMdiArea):
    def __init__(self, parent=None):
        QtGui.QMdiArea.__init__(self)
        pass

    # def closeEvent(self):
    #     pass

class SubWindow(QtGui.QMdiSubWindow):

    maximized = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        QtGui.QMdiSubWindow.__init__(self)


    def changeEvent(self, event):
        if event.type() == QtCore.QEvent.WindowStateChange:
            if self.windowState() & QtCore.Qt.WindowMaximized:
                print("triggered")
                self.showMaximized()
                pass
                self.maximized.emit()


