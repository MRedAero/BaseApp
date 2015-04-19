__author__ = 'Michael Redmond'


from base_app.application.core.logic import logic_core


class BaseAppLogicController(object):
    def __init__(self, adaptor):
        super(BaseAppLogicController, self).__init__()

        self._adaptor = adaptor
        """:type: base_app.application.adaptor.BaseAppAdaptor"""

    def open_file(self, filename):
        return logic_core.open_file(filename)