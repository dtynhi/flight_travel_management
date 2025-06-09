from utils.utils import object_to_dict


class ApiResponse:
    def __init__(self, success=True, message="Success"):
        self.success = success
        self.message = message
        self.data = None

    def to_dict(self):
        return object_to_dict(self)


class SuccessApiResponse(ApiResponse):
    def __init__(self, data=None):
        super().__init__(success=True, message="Success")
        self.data = data

    def to_dict(self):
        return object_to_dict(self)


class ErrorApiResponse(ApiResponse):
    def __init__(self, message="Error", error=None):
        super().__init__(success=False, message=message)
        self.error = error

    def to_dict(self):
        return object_to_dict(self)
