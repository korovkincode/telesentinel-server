class AppError(Exception):
    code = "app_error"
    status_code = 500
    message = "Application error"

    def __init__(self, **context):
        self.context = context
        super().__init__(self.message)


class InvalidCredentialsError(AppError):
    code = "invalid_credentials"
    status_code = 401
    message = "Invalid credentials"


class UserNotFoundError(AppError):
    code = "user_not_found"
    status_code = 404
    message = "User not found"


class UserInactiveError(AppError):
    code = "user_inactive"
    status_code = 403
    message = "User is inactive"


class InvalidTokenError(AppError):
    code = "invalid_token"
    status_code = 401
    message = "Invalid token"


class InvalidTokenTypeError(InvalidTokenError):
    code = "invalid_token_type"
    status_code = 400
    message = "Invalid token type"


class NotEnoughPermissionsError(AppError):
    code = "not_enough_permissions"
    status_code = 403
    message = "Not enough permissions"


class RefreshTokenNotProvidedError(AppError):
    code = "refresh_token_not_provided"
    status_code = 400
    message = "Refresh token is not provided"
