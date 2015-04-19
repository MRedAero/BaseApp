from PyQt4 import QtGui
from collections import OrderedDict


class SeparatorController(object):
    def __init__(self, name):

        self._name = name

    def get_name(self):
        return self._name