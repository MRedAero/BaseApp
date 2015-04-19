__author__ = 'Michael Redmond'


from base_app.application.core.model import BaseAppModelCore


class BaseAppModelController(object):
    def __init__(self, adaptor):
        super(BaseAppModelController, self).__init__()

        self._adaptor = adaptor
        """:type: base_app.application.adaptor.BaseAppAdaptor"""

        self._models = []
        """:type: list [BaseAppModelCore]"""

        self._active_model = None
        """:type: BaseAppModelCore"""

    def get_model_names(self):
        return [model.get_name() for model in self._models]

    @property
    def create_model_object(self):
        return BaseAppModelCore

    def new_model(self, model_name):
        if model_name in self.get_model_names():
            print "Model name %s already exists!" % model_name
            return False

        new_model = self.create_model_object(model_name)

        self._models.append(new_model)

        self._active_model = new_model

        return True

    def close_model(self, index):
        try:
            del self._models[index]
        except IndexError:
            pass

    def set_active_model(self, index):
        self._active_model = self._models[index]

    def set_file(self, file):
        if self._active_model.get_file() is not None:
            print 'active model file is not None!'
            return

        self._active_model.set_file(file)