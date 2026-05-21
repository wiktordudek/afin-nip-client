class AfinError(Exception):
    pass


class NipValidationError(AfinError):
    def __init__(self, nip: str, reason: str) -> None:
        self.nip = nip
        self.reason = reason
        super().__init__(f"Invalid NIP {nip!r}: {reason}")


class NipLengthError(NipValidationError):
    def __init__(self, nip: str) -> None:
        super().__init__(nip, f"expected 10 digits, got {len(nip)}")


class NipChecksumError(NipValidationError):
    def __init__(self, nip: str) -> None:
        super().__init__(nip, "checksum mismatch")


class AfinApiError(AfinError):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class EmptyResponse(AfinApiError):
    def __init__(self) -> None:
        super().__init__("API returned empty response")


class InvalidResponse(AfinApiError):
    def __init__(self, field_count: int | None = None) -> None:
        msg = "API returned invalid response format"
        if field_count is not None:
            msg += f": expected >= 12 fields, got {field_count}"
        super().__init__(msg)


class InvalidNipError(AfinApiError):
    def __init__(self, api_message: str) -> None:
        self.api_message = api_message
        super().__init__(f"NIP rejected by API: {api_message}")
