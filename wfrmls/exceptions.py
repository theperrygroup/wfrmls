"""Custom exceptions for WFRMLS API wrapper."""

from typing import Any, Dict, Optional


class WFRMLSError(Exception):
    """Base custom exception with optional status_code and response_data attributes.

    Local failures may omit both attributes. Python argument errors and direct
    metadata transport errors are not necessarily wrapped in this hierarchy.
    """

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response_data: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Initialize the exception.

        Args:
            message: Error message describing what went wrong
            status_code: HTTP status code from the API response
            response_data: Raw response data from the API for debugging
        """
        super().__init__(message)
        self.status_code = status_code
        self.response_data = response_data


class AuthenticationError(WFRMLSError):
    """Raised for missing service credentials or a shared HTTP 401 response.

    The facade defers missing-credential errors until service construction.
    """


class ValidationError(WFRMLSError):
    """Raised for shared HTTP 400 responses or explicit local input checks.

    Examples include nonnumeric property keys and disabled geospatial methods.
    """


class NotFoundError(WFRMLSError):
    """Raised for shared HTTP 404 responses or an empty wrapped property lookup."""


class RateLimitError(WFRMLSError):
    """Raised for a shared HTTP 429 response.

    The package does not automatically retry or schedule requests after this error.
    """


class ServerError(WFRMLSError):
    """Raised for shared HTTP responses with status codes from 500 through 599."""


class NetworkError(WFRMLSError):
    """Raised when a shared request catches a Requests transport exception.

    The separate metadata request propagates its Requests exceptions directly.
    """
