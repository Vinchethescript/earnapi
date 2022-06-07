class EarnAppError(Exception):  # in case someone wants to handle only errors from here
    pass


class IPCheckError(EarnAppError):
    pass


class RedeemError(EarnAppError):
    pass


class DeviceOperationError(EarnAppError):
    pass


class TooManyRequestsError(EarnAppError):
    pass


class AuthenticationError(EarnAppError):
    def __init__(self) -> None:
        message = "An improper oauth-refresh-token has been used."
        super().__init__(message)


class DeviceNotFoundError(DeviceOperationError):
    pass


class DeviceAlreadyAddedError(DeviceOperationError):
    pass
