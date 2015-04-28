__author__ = 'Michael Redmond'

from PyQt4 import QtCore

QtCore.Signal = QtCore.pyqtSignal

if __name__ == '__main__':
    from base_app.base_app import main
    main()