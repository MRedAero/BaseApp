__author__ = 'Michael Redmond'

from PyQt4 import QtGui, QtCore

from base_app.simple_pubsub import pub


class MDIController(object):
    def __init__(self, view):
        self._view = view
        """:type: base_app.application.core.view.view_core.BaseAppViewCore"""

        self._tab_widget = QtGui.QTabWidget(self._view.central_widget)
        self._tab_widget.setObjectName("tab_widget")

        self._view.grid_layout.addWidget(self._tab_widget, 0, 0, 1, 1)

        self._current_index = -1
        self._active_document = None
        self._skip = 0

        self._tab_widget.currentChanged.connect(self._update_current_document)

    def add_document(self, name):
        new_tab = QtGui.QWidget()
        new_tab.setObjectName(name)
        new_tab.grid_layout = QtGui.QGridLayout(new_tab)

        self._skip = 1  # why is this needed to prevent infinite recursion?  probably should fix
        self._tab_widget.addTab(new_tab, name)
        self._tab_widget.setCurrentIndex(self._tab_widget.count()-1)
        self._current_index = self._tab_widget.count() - 1
        self._active_document = self._tab_widget.widget(self._current_index)

    def close_document(self, index):
        self._tab_widget.removeTab(index)

    def set_active_document(self, index):
        self._current_index = index
        self._active_document = self._tab_widget.widget(index)
        self._tab_widget.setCurrentIndex(index)

    def get_current_index(self):
        return self._current_index

    def get_active_document(self):
        return self._active_document

    def _update_current_document(self, index):
        if self._skip:  # why is this needed to prevent infinite recursion?  probably should fix
            self._skip -= 1
            return

        if self._current_index == -1:
            pub.publish('program.new_file')
            return

        pub.publish('program.set_active_document', index=index)



