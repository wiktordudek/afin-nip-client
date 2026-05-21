class NipLengthError(Exception):
    pass


class NipChecksumError(Exception):
    pass


class AfinError(Exception):
    pass


class EmptyResponse(AfinError):
    pass


class InvalidResponse(AfinError):
    pass


class InvalidNipError(AfinError):
    pass


class AfinApiError(AfinError):
    pass
