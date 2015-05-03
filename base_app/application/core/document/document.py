__author__ = 'Michael Redmond'

from base_app.simple_pubsub import pub
from base_app.application.core.model import BaseAppModelCore

from mdi_subwindow import MdiSubWindow


class BaseAppDocument(object):
    def __init__(self, document_name, mdi_controller):
        self._document_name = document_name

        self._mdi_controller = mdi_controller
        """:type: base_app.application.core.document.mdi_controller.MDIController"""

        self._subwindow = MdiSubWindow(document_name, self._mdi_controller)
        self._subwindow.setWindowTitle(self._document_name)

        self._model = self._create_model(document_name)

        self._file = None

    def get_document_name(self):
        return self._document_name

    def get_subwindow(self):
        return self.get_subwindow

    def get_model(self):
        return self._model

    def set_file(self, file_):
        self._file = file_

    def unload(self, index):
        #self._mdi_controller.remove_subwindow(self)
        self._mdi_controller.remove_subwindow(index)
        self._subwindow.setParent(None)
        self._subwindow = None

    def _create_model(self, document_name):
        return BaseAppModelCore(document_name)