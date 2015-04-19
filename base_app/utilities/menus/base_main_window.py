from PyQt4 import QtGui

from base_main_window_ui import Ui_MainWindow


class BaseMainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(BaseMainWindow, self).__init__()

        self.base_ui = Ui_MainWindow().setupUi(self)


if __name__ == "__main__":
    import sys

    app = QtGui.QApplication(sys.argv)

    main_window = BaseMainWindow()

    main_window.show()

    app.exec_()
