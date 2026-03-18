class AppException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)
class UserExistsE(AppException):
    pass
class EmailExistsE(AppException):
    pass
class InvalidCredentialsE(AppException):
    pass
class TransactionNotFoundE(AppException):
    pass