class EntityNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(message)


class BadRequestException(Exception):
    def __init__(self, message):
        super().__init__(message)
