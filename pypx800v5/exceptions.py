"""Exceptions for IPX800."""


class IPX800CannotConnectError(Exception):
    """Exception to indicate an error in connection."""


class IPX800InvalidAuthError(Exception):
    """Exception to indicate an error in authentication."""


class IPX800RequestError(Exception):
    """Exception to indicate an error with an API request."""
