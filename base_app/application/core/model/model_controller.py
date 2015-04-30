__author__ = 'Michael Redmond'

from base_app.simple_pubsub import pub

from model_core import BaseAppModelCore


class BaseAppModelController(object):
    def __init__(self):
        super(BaseAppModelController, self).__init__()

        self._models = []
        """:type: list [BaseAppModelCore]"""

        self._active_model = None
        """:type: BaseAppModelCore"""

        self._subscribe_to_pub()

    def _subscribe_to_pub(self):
        pub.subscribe(self._set_active_model, "model.set_active_model")
        pub.subscribe(self._close_model, "model.close_model")
        pub.subscribe(self._new_model, "model.new_model")
        pub.subscribe(self._set_file, "model.set_file")

    def get_model_names(self):
        return [model.get_name() for model in self._models]

    def create_model_object(self, name):
        return BaseAppModelCore(name)

    def _new_model(self, name):
        if name in self.get_model_names():
            print "Model name %s already exists!" % name
            return False

        new_model = self.create_model_object(name)

        self._models.append(new_model)

        self._active_model = new_model

        return True

    def _close_model(self, index):
        try:
            del self._models[index]
        except IndexError:
            pass

    def _set_active_model(self, index):
        self._active_model = self._models[index]

    def _set_file(self, file_):
        if self._active_model.get_file() is not None:
            print 'active model file is not None!'
            return

        self._active_model.set_file(file_)