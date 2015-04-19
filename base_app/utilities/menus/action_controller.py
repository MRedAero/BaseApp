from PyQt4 import QtGui
from collections import OrderedDict


class ActionController(object):
    def __init__(self, action, action_name):

        self._action = action

        self._action_name = action_name

        self._action.setText(action_name)

    def get_action(self):
        return self._action

    def get_name(self):
        return self._action_name


