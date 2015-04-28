__author__ = 'Michael Redmond'

from PyQt4 import QtGui, QtCore

from toolbar_plugin_ui import Ui_Toolbar


class ToolbarPluginView(QtGui.QDockWidget):
    def __init__(self):
        super(ToolbarPluginView, self).__init__()

        self.ui = Ui_Toolbar()
        self.ui.setupUi(self)

        self.ui.window = QtGui.QMainWindow(self)
        self.ui.window.setWindowFlags(QtCore.Qt.Widget)
        self.ui.toolbar = QtGui.QToolBar(self.ui.window)
        self.ui.window.addToolBar(self.ui.toolbar)
        self.setWidget(self.ui.window)


if __name__ == '__main__':
    import sys
    app = QtGui.QApplication([])
    dock = ToolbarPluginView()
    dock.show()
    sys.exit(app.exec_())