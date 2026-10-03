"""Base client for WFRMLS API."""

import os
from typing import Any, Dict, List, Optional, Union

import requests
from dotenv import load_dotenv

from .exceptions import (
    AuthenticationError,
    NetworkError,
    NotFoundError,
    RateLimitError,
    ServerError,
    ValidationError,
    WFRMLSError,
)

load_dotenv()


class BaseClient:
    """Shared authenticated HTTP client for the resource interfaces.

    Each instance owns a Requests session. Shared resource requests do not set
    an explicit timeout or implement automatic retries, backoff, or token refresh.
    The separate WFRMLSClient metadata request has different behavior.
    """

    def __init__(
        self, bearer_token: Optional[str] = None, base_url: Optional[str] = None
    ) -> None:
        """Initialize a service client and resolve its credentials.

        Args:
            bearer_token: Explicit token, or None to use WFRMLS_BEARER_TOKEN.
            base_url: OData service root, or None for the package default.

        Raises:
            AuthenticationError: If neither an explicit nor environment token exists.
        """
        self.bearer_token = bearer_token or os.getenv("WFRMLS_BEARER_TOKEN")
        if not self.bearer_token:
            raise AuthenticationError(
                "Bearer token is required. Set WFRMLS_BEARER_TOKEN environment "
                "variable or pass bearer_token parameter."
            )

        self.base_url = base_url or "https://resoapi.utahrealestate.com/reso/odata"
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {self.bearer_token}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
        )

    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """Handle HTTP response and raise appropriate exceptions.

        Args:
            response: The HTTP response object to process

        Returns:
            Parsed JSON response data

        Raises:
            ValidationError: For 400 Bad Request responses
            AuthenticationError: For 401 Unauthorized responses
            NotFoundError: For 404 Not Found responses
            RateLimitError: For 429 Too Many Requests responses
            ServerError: For 5xx server error responses
            WFRMLSError: For other unexpected error responses
        """
        try:
            response_data = response.json() if response.content else {}
        except ValueError:
            # If response is not JSON, create a simple dict with the text
            response_data = {"message": response.text}

        # Helper function to extract error message
        def get_error_message(data: Dict[str, Any], default: str) -> str:
            """Extract error message from response data, handling nested error structures."""
            # First try direct message
            if "message" in data:
                return str(data["message"])
            # Then try nested error.message
            if (
                "error" in data
                and isinstance(data["error"], dict)
                and "message" in data["error"]
            ):
                return str(data["error"]["message"])
            # Finally return default
            return default

        if response.status_code in (200, 201):
            return response_data
        elif response.status_code == 204:
            # No content - return empty dict
            return {}
        elif response.status_code == 400:
            raise ValidationError(
                f"Bad request: {get_error_message(response_data, 'Invalid request')}",
                status_code=400,
                response_data=response_data,
            )
        elif response.status_code == 401:
            raise AuthenticationError(
                f"Authentication failed: {get_error_message(response_data, 'Invalid credentials')}",
                status_code=401,
                response_data=response_data,
            )
        elif response.status_code == 404:
            raise NotFoundError(
                f"Resource not found: {get_error_message(response_data, 'Not found')}",
                status_code=404,
                response_data=response_data,
            )
        elif response.status_code == 429:
            raise RateLimitError(
                f"Rate limit exceeded: {get_error_message(response_data, 'Too many requests')}",
                status_code=429,
                response_data=response_data,
            )
        elif 500 <= response.status_code < 600:
            raise ServerError(
                f"Server error: {get_error_message(response_data, 'Internal server error')}",
                status_code=response.status_code,
                response_data=response_data,
            )
        else:
            raise WFRMLSError(
                f"Unexpected error: {get_error_message(response_data, 'Unknown error')}",
                status_code=response.status_code,
                response_data=response_data,
            )

    def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        json_data: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
        files: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Make HTTP request to API.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE, etc.)
            endpoint: API endpoint path (relative to base_url)
            data: Form data to send in request body
            json_data: JSON data to send in request body
            files: Files to upload
            params: Query parameters

        Returns:
            Parsed JSON response data

        Raises:
            NetworkError: If network connection fails
            WFRMLSError: For various API error conditions
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        try:
            response = self.session.request(
                method=method,
                url=url,
                json=json_data,
                data=data,
                files=files,
                params=params,
            )
            return self._handle_response(response)

        except requests.exceptions.RequestException as e:
            raise NetworkError(f"Network error: {str(e)}")

    def get(
        self, endpoint: str, params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Send a GET request to a path relative to the configured service root.

        Args:
            endpoint: Relative path; leading slashes are removed before URL assembly.
            params: Raw query dictionary, including $ prefixes for OData parameters.

        Returns:
            Handled JSON response. No query clamping or response schema validation occurs.

        Raises:
            WFRMLSError: For mapped HTTP failures or a wrapped transport failure.
        """
        return self._request("GET", endpoint, params=params)
