class ZemfrogException(Exception):
    pass


class ZemfrogTemplateNotFound(ZemfrogException):
    pass


class ZemfrogEnvironment(ZemfrogException):
    pass


class ZemfrogModelNotFound(ZemfrogException):
    pass
