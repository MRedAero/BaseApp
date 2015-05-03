__author__ = 'Michael Redmond'

import traceback

from PyQt4 import QtGui

from base_app.simple_pubsub import pub


class MdiSubWindow(QtGui.QMdiSubWindow):
    def __init__(self, window_title, mdi_controller):
        super(MdiSubWindow, self).__init__()

        self.setWindowTitle(window_title)

        self._mdi_controller = mdi_controller
        """:type: base_app.application.core.document.mdi_controller.MDIController"""

        self._mdi_controller.add_subwindow(self)

    def get_index(self):
        return self._mdi_controller.get_subwindow_index(self)

    def closeEvent(self, event):
        event.ignore()  # the subwindow should never close here, so ignore the event
        index = self.get_index()
        pub.publish('program.close_file', index=index)  # the window should only be closed like this

    #def focusInEvent(self, event):
    #    # the subwindow has gained focus, likely from the user clicking on it
    #    # regardless, its corresponding doc should be activated
    #    index = self.get_index()
    #    print 'focus in %s = %d' % (self.windowTitle(), index)
    #    print traceback.print_stack()
    #    pub.publish('program.set_active_document', index=index)  # the only ways docs should be activated

    def __del__(self):
        print 'deleting %s' % self.windowTitle()

    def clear_layout(self):  # might not need this anymore
        layout = self.layout()

        while True:
            child = layout.takeAt(0)
            if not child:
                break
            widget = child.widget()
            layout.removeWidget(widget)
            del child