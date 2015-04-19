__author__ = 'Michael Redmond'


class BaseAppModelCore(object):
    def __init__(self, name):
        super(BaseAppModelCore, self).__init__()

        self._name = name
        """:type: str"""

        self._file = None

    def set_name(self, name):
        self._name = name

    def get_name(self):
        return self._name

    def set_file(self, file):
        self._file = file

    def get_file(self):
        return self._file