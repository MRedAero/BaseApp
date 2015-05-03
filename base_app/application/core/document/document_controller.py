__author__ = 'Michael Redmond'

import gc

from base_app.simple_pubsub import pub
from base_app.utilities.misc import new_name

from mdi_controller import MDIController
from document import BaseAppDocument


class BaseAppDocumentController(object):
    def __init__(self, view_controller):
        super(BaseAppDocumentController, self).__init__()

        self._view_controller = view_controller
        """:type: base_app.application.core.view.view_controller.BaseAppViewController"""

        self._view = self._view_controller.get_view()

        self._mdi_controller = MDIController(self._view)

        self._active_document = None
        """:type: BaseAppDocument"""

        self._documents = []
        """:type: list [BaseAppDocument]"""

        self._subscribe_to_pub()

        self._skip = 0

    def _subscribe_to_pub(self):
        pub.subscribe(self._set_active_document, 'document.set_active_document')
        pub.subscribe(self._set_file, 'document.set_file')
        pub.subscribe(self._new_document, 'document.new_document')
        pub.subscribe(self._close_document, 'document.close_document')

    def get_document_names(self):
        return [doc.get_document_name() for doc in self._documents]

    def get_active_document(self):
        return self._active_document

    def get_active_subwindow(self):
        if self._active_document:
            return self._active_document.get_subwindow()
        else:
            return None

    def get_active_model(self):
        if self._active_document:
            return self._active_document.get_model()
        else:
            return None

    def get_current_index(self):
        try:
            return self._documents.index(self._active_document)
        except (IndexError, ValueError):
            return -1

    def _create_document(self, document_name, mdi_controller):
        return BaseAppDocument(document_name, mdi_controller)

    def _new_document(self, document_name=None):
        doc_names = self.get_document_names()

        if document_name:
            if document_name in doc_names:
                print 'document name %s already exists!' % document_name
                return
        else:
            document_name = new_name(doc_names)

        # need to skip the _set_active_document call here because the document is not yet added to self._documents
        # just set it manually
        self._skip = 1
        new_doc = self._create_document(document_name, self._mdi_controller)
        self._documents.append(new_doc)

        self._active_document = new_doc
        print 'set document = %d' % self.get_current_index()

        # this should be activated when the subwindow receives focus
        #self._set_active_document(self.get_current_index())

    def _close_document(self, index=None):
        if not index:
            index = self.get_current_index()

        doc = self._documents[index]
        del self._documents[index]
        doc.unload(index)
        doc = None
        gc.collect()

    def _set_active_document(self, index):
        if self._skip:
            self._skip = 0
            return

        if index < 0:
            self._active_document = None
            return

        self._active_document = self._documents[index]

    def _set_file(self, file_):
        if self._active_document:
            self._active_document.set_file(file_)

