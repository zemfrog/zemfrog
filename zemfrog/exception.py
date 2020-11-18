class ZemfrogException(Exception):
    pass


class ZemfrogTemplateNotFound(ZemfrogException):
    pass


class ZemfrogEnvironment(ZemfrogException):
    pass


class ZemfrogModelNotFound(ZemfrogException):
    pass


class ZemfrogRoleNotFound(ZemfrogException):
    pass


class ZemfrogRolePermissionNotFound(ZemfrogException):
    pass
