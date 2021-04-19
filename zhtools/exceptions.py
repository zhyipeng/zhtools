class ModuleRequired(Exception):

    def __init__(self, module: str, version: str = None):
        self.module = module
        self.version = version

    def __str__(self) -> str:
        module = self.module
        if self.version:
            module += f'>={self.version}'
        return (f'Module [{module}]'
                f' is required. Please use pip to install it.')


class ExternalServiceException(Exception):

    def __init__(self, error_code: str = '', error_message: str = ''):
        self.error_code = error_code
        self.error_message = error_message

    def __str__(self) -> str:
        return (f'error_code: {self.error_code}, '
                f'error_message: {self.error_message}')


class NotFoundError(ExternalServiceException):

    def __init__(self):
        super().__init__('404', '404 not found.')


class Unauthorized(ExternalServiceException):

    def __init__(self):
        super().__init__('401', 'unauthorized')


class PermissionDenied(ExternalServiceException):

    def __init__(self):
        super().__init__('403', 'permission denied.')


class UnknownServiceError(ExternalServiceException):
    pass


class ExternalServiceError(ExternalServiceException):

    def __init__(self, error_code: str = '500'):
        super().__init__(error_code, 'external service error.')


class ResponseIsNotJSONable(ExternalServiceException):

    def __init__(self, error_code: str = ''):
        super().__init__(error_code, 'response data is not jsonable')


class ParameterError(ExternalServiceException):
    pass

