class EufyCloudError(Exception):
    """Base error."""


class EufyAuthError(EufyCloudError):
    """Login rejected or token no longer valid."""


class EufyConnectionError(EufyCloudError):
    """Network / HTTP-level failure."""


class EufyRateLimited(EufyConnectionError):
    """The cloud answered HTTP 429; back off before logging in again."""
