# WFRMLS API Wrapper Development Guide

A comprehensive template for building the WFRMLS (Wasatch Front Regional MLS) Python API wrapper, based on professional API wrapper architecture and best practices.

## Table of Contents

1. [Overview](#overview)
2. [Architecture Patterns](#architecture-patterns)
3. [Project Structure](#project-structure)
4. [Setup & Configuration](#setup--configuration)
5. [Implementation Guide](#implementation-guide)
6. [Code Patterns](#code-patterns)
7. [Testing Strategy](#testing-strategy)
8. [Documentation Standards](#documentation-standards)
9. [Development Workflow](#development-workflow)
10. [Task Management](#task-management)

## Overview

This template provides a blueprint for creating the WFRMLS Python API wrapper that is:

- **Type-safe** with comprehensive type hints
- **Well-tested** with 100% code coverage
- **Well-documented** with examples and workflows
- **Maintainable** with clear architecture patterns
- **Production-ready** with proper error handling and configuration

### Key Features

- ✅ Modular client architecture with service separation
- ✅ Comprehensive error handling with custom exceptions
- ✅ Flexible parameter handling (enums, unions, optional types)
- ✅ 100% test coverage with mocked responses
- ✅ Google-style docstrings with examples
- ✅ Modern Python packaging with pyproject.toml
- ✅ Full development tooling (linting, formatting, type checking)
- ✅ Task-driven development with progress tracking

## Architecture Patterns

### Core Architecture

```
Main Client (WFRMLSClient)
├── Property Client (PropertyClient) → BaseClient
├── Member Client (MemberClient) → BaseClient
├── Office Client (OfficeClient) → BaseClient
├── OpenHouse Client (OpenHouseClient) → BaseClient
├── Media Client (MediaClient) → BaseClient
├── History Transactional Client (HistoryTransactionalClient) → BaseClient
├── Data System Client (DataSystemClient) → BaseClient
├── Resource Client (ResourceClient) → BaseClient
├── Lookup Client (LookupClient) → BaseClient
├── Property Green Verification Client (PropertyGreenVerificationClient) → BaseClient
├── Property Unit Types Client (PropertyUnitTypesClient) → BaseClient
├── ADU Client (ADUClient) → BaseClient
├── Deleted Client (DeletedClient) → BaseClient
└── Service Discovery Client (ServiceDiscoveryClient) → BaseClient

BaseClient
├── HTTP methods (get only - API is read-only)
├── Bearer token authentication
├── Error handling & response processing
├── Rate limiting support (200 records per request)
├── NextLink pagination support
├── Geolocation query support
└── Common utilities
```

### Key Design Patterns

1. **Composition over Inheritance**: Main client composes service clients
2. **Lazy Initialization**: Service clients created on first access
3. **Flexible Parameters**: Union types for enums and strings
4. **Error Hierarchy**: Specific exceptions for different error types
5. **Type Safety**: Comprehensive type hints throughout

## Project Structure

```
wfrmls/
├── .github/workflows/           # CI/CD pipelines
├── docs/                        # Documentation
│   ├── api-reference/          # Auto-generated API docs
│   ├── workflows/              # Workflow examples
│   └── README.md               # Main documentation
├── tasks/                       # Implementation tracking
│   ├── endpoints.md   # Endpoints to implement
├── tests/                       # Test suite
├── wfrmls/                       # Main package
│   ├── __init__.py             # Package exports
│   ├── base_client.py          # Base HTTP client
│   ├── client.py               # Main WFRMLS client
│   ├── exceptions.py           # Custom exceptions
│   ├── property.py             # Property client
│   ├── member.py               # Member client
│   ├── office.py               # Office client
│   ├── openhouse.py            # OpenHouse client
│   ├── media.py                # Media client
│   ├── history_transactional.py # History transactional client
│   ├── data_system.py          # Data system client
│   ├── resource.py             # Resource client
│   ├── lookup.py               # Lookup client
│   ├── property_green_verification.py # Property green verification client
│   ├── property_unit_types.py  # Property unit types client
│   ├── adu.py                  # ADU client
│   ├── deleted.py              # Deleted records client
│   ├── service_discovery.py    # Service discovery client
│   └── py.typed                # Type hint marker
├── api_docs/                    # Existing API documentation
├── .env                        # Environment variables (not committed)
├── .gitignore                  # Git ignore patterns
├── LICENSE                     # License file
├── MANIFEST.in                 # Package manifest
├── pyproject.toml              # Project configuration
├── README.md                   # Project README
├── requirements.txt            # Runtime dependencies
├── requirements-dev.txt        # Development dependencies
└──  STYLE_GUIDE.md              # Coding standards
```

## Setup & Configuration

### 1. Initialize Project

```bash
# Navigate to project directory
cd wfrmls

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

### 2. Create pyproject.toml

```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "wfrmls"
version = "1.0.0"
description = "Python wrapper for Wasatch Front Regional MLS API"
readme = "README.md"
license = {text = "MIT"}
authors = [
    {name = "Your Name", email = "your.email@example.com"}
]
keywords = ["wfrmls", "mls", "real-estate", "api", "wrapper", "reso"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Office/Business :: Financial :: Investment",
    "Typing :: Typed"
]
requires-python = ">=3.8"
dependencies = [
    "requests>=2.25.0",
    "python-dotenv>=0.19.0",
    "pydantic>=2.0.0"
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "pytest-mock>=3.10.0",
    "responses>=0.23.0",
    "black>=23.0.0",
    "flake8>=6.0.0",
    "mypy>=1.0.0",
    "isort>=5.12.0",
    "pylint>=2.17.0",
    "types-requests>=2.25.0"
]

[tool.black]
line-length = 88
target-version = ['py38']

[tool.isort]
profile = "black"
multi_line_output = 3
line_length = 88

[tool.mypy]
python_version = "3.8"
warn_return_any = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
strict_equality = true

[tool.pytest.ini_options]
addopts = "-ra -q --strict-markers --cov=wfrmls --cov-report=term-missing --cov-report=html"
testpaths = ["tests"]
```

### 3. Install Dependencies

```bash
pip install -e .[dev]
```

## Implementation Guide

### Step 1: Define Custom Exceptions

Create `wfrmls/exceptions.py`:

```python
"""Custom exceptions for WFRMLS API wrapper."""

from typing import Any, Dict, Optional


class WFRMLSError(Exception):
    """Base exception for all WFRMLS API errors."""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response_data: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Initialize the exception.

        Args:
            message: Error message
            status_code: HTTP status code
            response_data: Raw response data
        """
        super().__init__(message)
        self.status_code = status_code
        self.response_data = response_data


class AuthenticationError(WFRMLSError):
    """Raised when authentication fails."""


class ValidationError(WFRMLSError):
    """Raised when request validation fails."""


class NotFoundError(WFRMLSError):
    """Raised when a resource is not found."""


class RateLimitError(WFRMLSError):
    """Raised when rate limit is exceeded."""


class ServerError(WFRMLSError):
    """Raised when server returns 5xx error."""


class NetworkError(WFRMLSError):
    """Raised when network connection fails."""
```

### Step 2: Create Base Client

Create `wfrmls/base_client.py`:

```python
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
    """Base client with common functionality."""

    def __init__(
        self, bearer_token: Optional[str] = None, base_url: Optional[str] = None
    ) -> None:
        """Initialize the base client.

        Args:
            bearer_token: Bearer token for authentication
            base_url: Base URL for the API
        """
        self.bearer_token = bearer_token or os.getenv("WFRMLS_BEARER_TOKEN")
        if not self.bearer_token:
            raise AuthenticationError(
                "Bearer token is required. Set WFRMLS_BEARER_TOKEN environment variable or pass bearer_token parameter."
            )

        self.base_url = base_url or "https://resoapi.utahrealestate.com/reso/odata"
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.bearer_token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        })

    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """Handle HTTP response and raise appropriate exceptions."""
        try:
            response_data = response.json() if response.content else {}
        except ValueError:
            response_data = {"message": response.text}

        if response.status_code in (200, 201):
            return response_data
        elif response.status_code == 204:
            return {}
        elif response.status_code == 400:
            raise ValidationError(
                f"Bad request: {response_data.get('message', 'Invalid request')}",
                status_code=400,
                response_data=response_data,
            )
        elif response.status_code == 401:
            raise AuthenticationError(
                f"Authentication failed: {response_data.get('message', 'Invalid credentials')}",
                status_code=401,
                response_data=response_data,
            )
        elif response.status_code == 404:
            raise NotFoundError(
                f"Resource not found: {response_data.get('message', 'Not found')}",
                status_code=404,
                response_data=response_data,
            )
        elif response.status_code == 429:
            raise RateLimitError(
                f"Rate limit exceeded: {response_data.get('message', 'Too many requests')}",
                status_code=429,
                response_data=response_data,
            )
        elif 500 <= response.status_code < 600:
            raise ServerError(
                f"Server error: {response_data.get('message', 'Internal server error')}",
                status_code=response.status_code,
                response_data=response_data,
            )
        else:
            raise WFRMLSError(
                f"Unexpected error: {response_data.get('message', 'Unknown error')}",
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
        """Make HTTP request to API."""
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

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make GET request."""
        return self._request("GET", endpoint, params=params)
```

### Step 3: Create Service Clients

Create service-specific clients, e.g., `wfrmls/property.py`:

```python
"""Property client for WFRMLS API."""

from datetime import date
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from .base_client import BaseClient


class PropertyStatus(Enum):
    """Property status options."""

    ACTIVE = "Active"
    PENDING = "Pending"
    SOLD = "Sold"
    EXPIRED = "Expired"


class PropertyType(Enum):
    """Property type options."""

    RESIDENTIAL = "Residential"
    COMMERCIAL = "Commercial"
    LAND = "Land"


class PropertyClient(BaseClient):
    """Client for property API endpoints."""

    def __init__(
        self, bearer_token: Optional[str] = None, base_url: Optional[str] = None
    ) -> None:
        """Initialize the property client.

        Args:
            bearer_token: Bearer token for authentication
            base_url: Base URL for the API
        """
        super().__init__(bearer_token=bearer_token, base_url=base_url)

    def get_properties(
        self,
        top: Optional[int] = None,
        skip: Optional[int] = None,
        filter_query: Optional[str] = None,
        select: Optional[Union[List[str], str]] = None,
        orderby: Optional[str] = None,
        expand: Optional[Union[List[str], str]] = None,
        count: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """Get properties with optional OData filtering.

        Args:
            top: Number of results to return (OData $top, max 200)
            skip: Number of results to skip (OData $skip) - use with caution for large datasets
            filter_query: OData filter query
            select: Fields to select (OData $select)
            orderby: Order by clause (OData $orderby)
            expand: Related resources to include (OData $expand)
            count: Include total count in results (OData $count)

        Returns:
            Dictionary containing property data

        Example:
            ```python
            # Get first 10 active properties
            properties = client.property.get_properties(
                top=10,
                filter_query="StandardStatus eq 'Active'"
            )

            # Get properties with photos and agent info
            properties = client.property.get_properties(
                expand=["Media", "Member"],
                top=50
            )

            # Get properties with geolocation filtering (within 5 miles of coordinates)
            properties = client.property.get_properties(
                filter_query="geo.distance(Latitude, Longitude, 40.7128, -74.0060) le 5",
                top=100
            )

            # Get properties with multi-lookup filtering
            properties = client.property.get_properties(
                filter_query="ExteriorFeatures has Odata.Models.ExteriorFeatures'Patio'",
                top=50
            )
            ```
        """
        params: Dict[str, Any] = {}

        if top is not None:
            # Enforce 200 record limit as per API specification
            params["$top"] = min(top, 200)
        if skip is not None:
            params["$skip"] = skip
        if filter_query is not None:
            params["$filter"] = filter_query
        if orderby is not None:
            params["$orderby"] = orderby
        if count is not None:
            params["$count"] = "true" if count else "false"

        if select is not None:
            if isinstance(select, list):
                params["$select"] = ",".join(select)
            else:
                params["$select"] = select

        if expand is not None:
            if isinstance(expand, list):
                params["$expand"] = ",".join(expand)
            else:
                params["$expand"] = expand

        return self.get("Property", params=params)

    def get_property(self, listing_id: str) -> Dict[str, Any]:
        """Get property by listing ID.

        Args:
            listing_id: Listing ID to retrieve

        Returns:
            Dictionary containing property data

        Example:
            ```python
            property = client.property.get_property("12345678")
            ```
        """
        return self.get(f"Property('{listing_id}')")

    def search_properties_by_radius(
        self,
        latitude: float,
        longitude: float,
        radius_miles: float,
        additional_filters: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Search properties within a radius of given coordinates.

        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate  
            radius_miles: Search radius in miles
            additional_filters: Additional OData filter query
            **kwargs: Additional OData parameters (top, select, etc.)

        Returns:
            Dictionary containing property data

        Example:
            ```python
            # Find properties within 10 miles of Salt Lake City
            properties = client.property.search_properties_by_radius(
                latitude=40.7608,
                longitude=-111.8910,
                radius_miles=10,
                additional_filters="StandardStatus eq 'Active'",
                top=50
            )
            ```
        """
        geo_filter = f"geo.distance(Latitude, Longitude, {latitude}, {longitude}) le {radius_miles}"
        
        if additional_filters:
            filter_query = f"{geo_filter} and {additional_filters}"
        else:
            filter_query = geo_filter
            
        return self.get_properties(filter_query=filter_query, **kwargs)

    def search_properties_by_polygon(
        self,
        polygon_coordinates: List[Dict[str, float]],
        additional_filters: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Search properties within a polygon area.

        Args:
            polygon_coordinates: List of coordinate dicts with 'lat' and 'lng' keys
            additional_filters: Additional OData filter query  
            **kwargs: Additional OData parameters (top, select, etc.)

        Returns:
            Dictionary containing property data

        Example:
            ```python
            # Define polygon around downtown area
            polygon = [
                {"lat": 40.7608, "lng": -111.8910},
                {"lat": 40.7708, "lng": -111.8810},
                {"lat": 40.7508, "lng": -111.8710},
                {"lat": 40.7608, "lng": -111.8910}  # Close polygon
            ]
            
            properties = client.property.search_properties_by_polygon(
                polygon_coordinates=polygon,
                additional_filters="PropertyType eq 'Residential'",
                top=100
            )
            ```
        """
        # Build polygon string for geo.intersects function
        coords_str = ",".join([f"{coord['lat']} {coord['lng']}" for coord in polygon_coordinates])
        geo_filter = f"geo.intersects(Latitude, Longitude, geography'POLYGON(({coords_str}))')"
        
        if additional_filters:
            filter_query = f"{geo_filter} and {additional_filters}"
        else:
            filter_query = geo_filter
            
        return self.get_properties(filter_query=filter_query, **kwargs)

    def get_properties_with_media(
        self,
        **kwargs
    ) -> Dict[str, Any]:
        """Get properties with their associated media/photos.

        Args:
            **kwargs: OData parameters (top, filter_query, etc.)

        Returns:
            Dictionary containing property data with media

        Example:
            ```python
            # Get active properties with photos
            properties = client.property.get_properties_with_media(
                filter_query="StandardStatus eq 'Active'",
                top=25
            )
            ```
        """
        return self.get_properties(expand="Media", **kwargs)
```

### Step 4: Create Main Client

Create `wfrmls/client.py`:

```python
"""Main WFRMLS client."""

from typing import Optional

from .property import PropertyClient
from .member import MemberClient
from .office import OfficeClient
from .openhouse import OpenHouseClient
from .media import MediaClient
from .history_transactional import HistoryTransactionalClient
from .data_system import DataSystemClient
from .resource import ResourceClient
from .lookup import LookupClient
from .property_green_verification import PropertyGreenVerificationClient
from .property_unit_types import PropertyUnitTypesClient
from .adu import ADUClient
from .deleted import DeletedClient
from .service_discovery import ServiceDiscoveryClient


class WFRMLSClient:
    """Main client for WFRMLS API.

    Example:
        ```python
        from wfrmls import WFRMLSClient

        # Initialize with bearer token from environment variable
        client = WFRMLSClient()

        # Or provide bearer token directly
        client = WFRMLSClient(bearer_token="your_bearer_token_here")

        # Use service endpoints
        properties = client.property.get_properties(top=10)
        property_detail = client.property.get_property("12345678")
        ```
    """

    def __init__(
        self, bearer_token: Optional[str] = None, base_url: Optional[str] = None
    ) -> None:
        """Initialize the client.

        Args:
            bearer_token: Bearer token for authentication
            base_url: Base URL for the API
        """
        self._bearer_token = bearer_token
        self._base_url = base_url
        self._property: Optional[PropertyClient] = None
        self._member: Optional[MemberClient] = None
        self._office: Optional[OfficeClient] = None
        self._openhouse: Optional[OpenHouseClient] = None
        self._media: Optional[MediaClient] = None
        self._history_transactional: Optional[HistoryTransactionalClient] = None
        self._data_system: Optional[DataSystemClient] = None
        self._resource: Optional[ResourceClient] = None
        self._lookup: Optional[LookupClient] = None
        self._property_green_verification: Optional[PropertyGreenVerificationClient] = None
        self._property_unit_types: Optional[PropertyUnitTypesClient] = None
        self._adu: Optional[ADUClient] = None
        self._deleted: Optional[DeletedClient] = None
        self._service_discovery: Optional[ServiceDiscoveryClient] = None

    @property
    def property(self) -> PropertyClient:
        """Access to property endpoints.

        Returns:
            PropertyClient instance
        """
        if self._property is None:
            self._property = PropertyClient(
                bearer_token=self._bearer_token, base_url=self._base_url
            )
        return self._property

    @property
    def member(self) -> MemberClient:
        """Access to member endpoints.

        Returns:
            MemberClient instance
        """
        if self._member is None:
            self._member = MemberClient(
                bearer_token=self._bearer_token, base_url=self._base_url
            )
        return self._member

    @property
    def office(self) -> OfficeClient:
        """Access to office endpoints.

        Returns:
            OfficeClient instance
        """
        if self._office is None:
            self._office = OfficeClient(
                bearer_token=self._bearer_token, base_url=self._base_url
            )
        return self._office

    @property
    def openhouse(self) -> OpenHouseClient:
        """Access to openhouse endpoints.

        Returns:
            OpenHouseClient instance
        """
        if self._openhouse is None:
            self._openhouse = OpenHouseClient(
                bearer_token=self._bearer_token, base_url=self._base_url
            )
        return self._openhouse

    @property
    def media(self) -> MediaClient:
        """Access to media endpoints.

        Returns:
            MediaClient instance
        """
        if self._media is None:
            self._media = MediaClient(
                bearer_token=self._bearer_token, base_url=self._base_url
            )
        return self._media

    @property
    def history_transactional(self) -> HistoryTransactionalClient:
        """Access to history transactional endpoints.

        Returns:
            HistoryTransactionalClient instance
        """
        if self._history_transactional is None:
            self._history_transactional = HistoryTransactionalClient(
                bearer_token=self._bearer_token, base_url=self._base_url
            )
        return self._history_transactional

    @property
    def data_system(self) -> DataSystemClient:
        """Access to data system endpoints.

        Returns:
            DataSystemClient instance
        """
        if self._data_system is None:
            self._data_system = DataSystemClient(
                bearer_token=self._bearer_token, base_url=self._base_url
            )
        return self._data_system

    @property
    def resource(self) -> ResourceClient:
        """Access to resource endpoints.

        Returns:
            ResourceClient instance
        """
        if self._resource is None:
            self._resource = ResourceClient(
                bearer_token=self._bearer_token, base_url=self._base_url
            )
        return self._resource

    @property
    def lookup(self) -> LookupClient:
        """Access to lookup endpoints.

        Returns:
            LookupClient instance
        """
        if self._lookup is None:
            self._lookup = LookupClient(
                bearer_token=self._bearer_token, base_url=self._base_url
            )
        return self._lookup

    @property
    def property_green_verification(self) -> PropertyGreenVerificationClient:
        """Access to property green verification endpoints.

        Returns:
            PropertyGreenVerificationClient instance
        """
        if self._property_green_verification is None:
            self._property_green_verification = PropertyGreenVerificationClient(
                bearer_token=self._bearer_token, base_url=self._base_url
            )
        return self._property_green_verification

    @property
    def property_unit_types(self) -> PropertyUnitTypesClient:
        """Access to property unit types endpoints.

        Returns:
            PropertyUnitTypesClient instance
        """
        if self._property_unit_types is None:
            self._property_unit_types = PropertyUnitTypesClient(
                bearer_token=self._bearer_token, base_url=self._base_url
            )
        return self._property_unit_types

    @property
    def adu(self) -> ADUClient:
        """Access to ADU (Accessory Dwelling Unit) endpoints.

        Returns:
            ADUClient instance
        """
        if self._adu is None:
            self._adu = ADUClient(
                bearer_token=self._bearer_token, base_url=self._base_url
            )
        return self._adu

    @property
    def deleted(self) -> DeletedClient:
        """Access to deleted records endpoints.

        Returns:
            DeletedClient instance
        """
        if self._deleted is None:
            self._deleted = DeletedClient(
                bearer_token=self._bearer_token, base_url=self._base_url
            )
        return self._deleted

    @property
    def service_discovery(self) -> ServiceDiscoveryClient:
        """Access to service discovery endpoints.

        Returns:
            ServiceDiscoveryClient instance
        """
        if self._service_discovery is None:
            self._service_discovery = ServiceDiscoveryClient(
                bearer_token=self._bearer_token, base_url=self._base_url
            )
        return self._service_discovery
```

### Step 5: Create Package Init

Create `wfrmls/__init__.py`:

```python
"""WFRMLS Python Client."""

from .client import WFRMLSClient
from .exceptions import (
    AuthenticationError,
    NetworkError,
    NotFoundError,
    RateLimitError,
    ServerError,
    ValidationError,
    WFRMLSError,
)
from .property import PropertyClient, PropertyStatus, PropertyType
from .member import MemberClient
from .office import OfficeClient
from .openhouse import OpenHouseClient
from .media import MediaClient
from .history_transactional import HistoryTransactionalClient
from .data_system import DataSystemClient
from .resource import ResourceClient
from .lookup import LookupClient
from .property_green_verification import PropertyGreenVerificationClient
from .property_unit_types import PropertyUnitTypesClient
from .adu import ADUClient
from .deleted import DeletedClient
from .service_discovery import ServiceDiscoveryClient

__version__ = "1.0.0"
__all__ = [
    "WFRMLSClient",
    "PropertyClient",
    "MemberClient", 
    "OfficeClient",
    "OpenHouseClient",
    "MediaClient",
    "HistoryTransactionalClient",
    "DataSystemClient",
    "ResourceClient",
    "LookupClient",
    "PropertyGreenVerificationClient",
    "PropertyUnitTypesClient",
    "ADUClient",
    "DeletedClient",
    "ServiceDiscoveryClient",
    "PropertyStatus",
    "PropertyType",
    "WFRMLSError",
    "AuthenticationError",
    "ValidationError",
    "NotFoundError",
    "RateLimitError",
    "ServerError",
    "NetworkError",
]
```

## Code Patterns

### Follow STYLE_GUIDE.md

Always check `./STYLE_GUIDE.md` for project-specific coding standards before implementing any endpoint.

### OData Parameter Handling

```python
# Support OData query parameters
def method(self, top: Optional[int] = None, filter_query: Optional[str] = None):
    params = {}
    if top is not None:
        params["$top"] = top
    if filter_query is not None:
        params["$filter"] = filter_query
```

### Enum Parameter Handling

```python
# Support both enum and string values
def method(self, status: Optional[Union[PropertyStatus, str]] = None):
    if status is not None:
        if isinstance(status, PropertyStatus):
            params["status"] = status.value
        else:
            params["status"] = status
```

### Date Parameter Handling

```python
# Support both date objects and ISO strings
def method(self, date_filter: Optional[Union[date, str]] = None):
    if date_filter is not None:
        if isinstance(date_filter, date):
            params["date"] = date_filter.isoformat()
        else:
            params["date"] = date_filter
```

### List Parameter Handling

```python
# Support both single items and lists
def method(self, fields: Optional[Union[List[str], str]] = None):
    if fields is not None:
        if isinstance(fields, list):
            params["$select"] = ",".join(fields)
        else:
            params["$select"] = fields
```

### NextLink Pagination Support

```python
# Implement efficient pagination using @odata.nextLink
def get_all_properties_paginated(self, **kwargs):
    """Get all properties using NextLink pagination (more efficient than $skip)."""
    all_results = []
    response = self.get_properties(**kwargs)
    
    while True:
        if 'value' in response:
            all_results.extend(response['value'])
        
        # Check for next page
        if '@odata.nextLink' not in response:
            break
            
        # Extract continuation URL and make next request
        next_url = response['@odata.nextLink']
        # Parse and make request to continuation URL
        # ... implementation details
        
    return {"value": all_results}
```

### Geolocation Query Patterns

```python
# Utah grid address system support
def format_utah_address(street_number: str, street_dir_prefix: str, 
                       cross_street: str, street_dir_suffix: str):
    """Format Utah grid system addresses (e.g., '1300 E 9400 S')."""
    return f"{street_number} {street_dir_prefix} {cross_street} {street_dir_suffix}"

# SRID=3956 distance calculations
def build_geo_distance_filter(lat: float, lng: float, radius_miles: float):
    """Build geographic distance filter with proper SRID."""
    return f"geo.distance(Latitude, Longitude, {lat}, {lng}) le {radius_miles}"
```

### Multi-Lookup Value Handling

```python
# Handle multi-lookup fields with 'has' operator
def build_multi_lookup_filter(field: str, value: str, namespace: str = "Odata.Models"):
    """Build filter for multi-lookup fields like ExteriorFeatures."""
    return f"{field} has {namespace}.{field}'{value}'"

# Example usage
filter_query = build_multi_lookup_filter("ExteriorFeatures", "Patio")
# Results in: "ExteriorFeatures has Odata.Models.ExteriorFeatures'Patio'"
```

### Rate Limiting and Error Handling

```python
# Implement rate limiting awareness
def safe_request_with_retry(self, method_func, max_retries=3, delay=1):
    """Make request with exponential backoff for rate limiting."""
    for attempt in range(max_retries):
        try:
            return method_func()
        except RateLimitError:
            if attempt == max_retries - 1:
                raise
            time.sleep(delay * (2 ** attempt))  # Exponential backoff
```

### Docstring Template

```python
def method_name(
    self,
    required_param: str,
    optional_param: Optional[int] = None,
    enum_param: Optional[Union[PropertyStatus, str]] = None,
) -> Dict[str, Any]:
    """Brief description of what the method does.

    Longer description with more details about the method's purpose
    and behavior if needed.

    Args:
        required_param: Description of required parameter
        optional_param: Description of optional parameter (default: None)
        enum_param: Description of enum parameter (Active, Pending, etc.)

    Returns:
        Dictionary containing response data with structure description

    Raises:
        WFRMLSError: If the API request fails
        ValidationError: If parameters are invalid

    Example:
        ```python
        # Basic usage
        result = client.property.method_name("required_value")

        # With optional parameters
        result = client.property.method_name(
            required_param="value",
            optional_param=42,
            enum_param=PropertyStatus.ACTIVE
        )
        ```
    """
```

## Testing Strategy

### Test File Structure

Create `tests/test_property.py`:

```python
"""Tests for property client."""

import pytest
import responses
from datetime import date

from wfrmls.property import PropertyClient, PropertyStatus, PropertyType
from wfrmls.exceptions import NotFoundError, ValidationError


class TestPropertyClient:
    """Test cases for PropertyClient."""

    def setup_method(self) -> None:
        """Set up test client."""
        self.client = PropertyClient(bearer_token="test_bearer_token")

    @responses.activate
    def test_get_properties_success(self) -> None:
        """Test successful get properties request."""
        mock_response = {
            "@odata.context": "https://resoapi.utahrealestate.com/reso/odata/$metadata#Property",
            "value": [
                {"ListingId": "12345678", "ListPrice": 250000, "StandardStatus": "Active"},
                {"ListingId": "87654321", "ListPrice": 300000, "StandardStatus": "Pending"}
            ]
        }

        responses.add(
            responses.GET,
            "https://resoapi.utahrealestate.com/reso/odata/Property",
            json=mock_response,
            status=200,
        )

        result = self.client.get_properties()
        assert result == mock_response
        assert len(responses.calls) == 1

    @responses.activate
    def test_get_properties_with_odata_params(self) -> None:
        """Test get properties with OData parameters."""
        mock_response = {"@odata.context": "test", "value": []}

        responses.add(
            responses.GET,
            "https://resoapi.utahrealestate.com/reso/odata/Property",
            json=mock_response,
            status=200,
        )

        result = self.client.get_properties(
            top=10,
            skip=20,
            filter_query="StandardStatus eq 'Active'",
            select=["ListingId", "ListPrice"],
            orderby="ListPrice desc"
        )

        assert result == mock_response

        # Verify query parameters
        request = responses.calls[0].request
        assert "$top=10" in request.url
        assert "$skip=20" in request.url
        assert "$filter=StandardStatus+eq+%27Active%27" in request.url
        assert "$select=ListingId%2CListPrice" in request.url
        assert "$orderby=ListPrice+desc" in request.url

    @responses.activate
    def test_get_property_not_found(self) -> None:
        """Test get property not found error."""
        responses.add(
            responses.GET,
            "https://resoapi.utahrealestate.com/reso/odata/Property('nonexistent')",
            json={"error": {"message": "Property not found"}},
            status=404,
        )

        with pytest.raises(NotFoundError, match="Resource not found"):
            self.client.get_property("nonexistent")

    def test_enum_values(self) -> None:
        """Test enum values are correct."""
        assert PropertyStatus.ACTIVE.value == "Active"
        assert PropertyStatus.PENDING.value == "Pending"
        assert PropertyType.RESIDENTIAL.value == "Residential"
        assert PropertyType.COMMERCIAL.value == "Commercial"
```

### Running Tests

```bash
# Run tests with coverage (must achieve 100%)
pytest --cov=wfrmls --cov-report=html

# Run specific test file
pytest tests/test_property.py

# Run with verbose output
pytest -v
```

## Documentation Standards

### README.md Template

```markdown
# WFRMLS Python Client

A comprehensive Python wrapper for the Wasatch Front Regional MLS API, providing easy access to all RESO-certified endpoints.

## Quick Start

```python
from wfrmls import WFRMLSClient

# Initialize client
client = WFRMLSClient(bearer_token="your_bearer_token")

# Get properties
properties = client.property.get_properties(
    top=10,
    filter_query="StandardStatus eq 'Active'"
)
```

## Installation

```bash
pip install wfrmls
```

## Documentation

- [API Reference](docs/api-reference/)
- [Workflows](docs/workflows/)

## Features

- ✅ Type-safe with comprehensive type hints
- ✅ 100% test coverage
- ✅ Complete documentation with examples
- ✅ Robust error handling
- ✅ OData query support
```

### Workflow Documentation

Create workflow guides in `docs/workflows/`, e.g., `docs/workflows/property-search.md`:

```markdown
# Property Search Workflows

## Basic Property Search

### Get All Properties
```python
properties = client.property.get_properties()
```

### Filter Active Properties
```python
active_properties = client.property.get_properties(
    filter_query="StandardStatus eq 'Active'"
)
```

### Pagination
```python
# First page
page_1 = client.property.get_properties(top=50, skip=0)

# Second page  
page_2 = client.property.get_properties(top=50, skip=50)
```

## Advanced Filtering

### Price Range
```python
properties = client.property.get_properties(
    filter_query="ListPrice ge 200000 and ListPrice le 500000"
)
```

### Multiple Criteria
```python
properties = client.property.get_properties(
    filter_query="StandardStatus eq 'Active' and PropertyType eq 'Residential' and ListPrice le 400000"
)
```

## Advanced Features

### Geolocation Search
```python
# Search within radius
properties = client.property.search_properties_by_radius(
    latitude=40.7608,  # Salt Lake City
    longitude=-111.8910,
    radius_miles=10,
    additional_filters="StandardStatus eq 'Active'"
)

# Search within polygon
polygon = [
    {"lat": 40.7608, "lng": -111.8910},
    {"lat": 40.7708, "lng": -111.8810},
    {"lat": 40.7508, "lng": -111.8710},
    {"lat": 40.7608, "lng": -111.8910}
]
properties = client.property.search_properties_by_polygon(polygon)
```

### Service Discovery
```python
# Get available endpoints
services = client.service_discovery.get_service_document()

# Get metadata schema
metadata = client.service_discovery.get_metadata()
```

### Data Synchronization
```python
# Get incremental updates (recommended every 15 minutes)
from datetime import datetime, timedelta
cutoff_time = datetime.utcnow() - timedelta(minutes=15)
updates = client.property.get_properties(
    filter_query=f"ModificationTimestamp gt {cutoff_time.isoformat()}Z"
)

# Track deletions
deleted_records = client.deleted.get_deleted(
    filter_query="ResourceName eq 'Property'"
)
```

## Error Handling

```python
try:
    property = client.property.get_property("12345678")
except NotFoundError:
    print("Property not found")
except RateLimitError:
    print("Rate limit exceeded - wait before retrying")
except ValidationError as e:
    print(f"Invalid request: {e}")
```
```

## Development Workflow

### Implementation Process

For each endpoint documented in `api_docs/` and tracked in `tasks/*.md`:

1. **Read API Documentation**: Check `api_docs/` for endpoint details
2. **Reference Type Information**: Use `./api_docs/metadata.xml` for field types, enumerations, and entity relationships
3. **Reference wfrmls_api.json**: Use for detailed API specifications
4. **Implement Client Method**: Add method to appropriate service client in `wfrmls/`
5. **Write Tests**: Create comprehensive tests in `tests/`
6. **Test Implementation**: Run tests to ensure functionality
7. **Update Documentation**: Update relevant docs in `docs/`
8. **Check Off Task**: Mark endpoint as complete in task file

### Quality Assurance

```bash
# Format code according to STYLE_GUIDE.md
black wfrmls tests
isort wfrmls tests

# Lint code
flake8 wfrmls tests
pylint wfrmls

# Type checking
mypy wfrmls

# Run tests with 100% coverage requirement
pytest --cov=wfrmls --cov-report=term-missing

# Test actual endpoint
python -c "
from wfrmls import WFRMLSClient
client = WFRMLSClient()
print(client.property.get_properties(top=1))
"
```

### GitHub Actions CI

Create `.github/workflows/ci.yml`:

```yaml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, "3.10", "3.11", "3.12"]

    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -e .[dev]

    - name: Lint with flake8
      run: flake8 wfrmls tests

    - name: Type check with mypy
      run: mypy wfrmls

    - name: Test with pytest
      run: pytest --cov=wfrmls --cov-report=xml

    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
```

## Task Management

### Progress Tracking

Use checkbox format to track completion:
- `- [ ]` for incomplete tasks 
- `- [x]` for completed tasks

Example task tracking:
```markdown
- [x] Implement PropertyClient base structure
- [x] Add get_properties() method with OData support  
- [ ] Add get_property() method for single property lookup
- [ ] Add search_properties_by_radius() geolocation method
- [ ] Write comprehensive tests with 100% coverage
- [ ] Update documentation with examples
```

## Specialized Implementation Requirements

### Data Replication & Synchronization

- **15-minute Update Cycle**: Recommended frequency for incremental updates
- **UTC Timestamps**: All timestamp handling must use UTC format
- **ResourceRecordKey**: Handle as string type (2020-11-09 API update)
- **Deletion Tracking**: Implement via Deleted resource for data integrity
- **Primary Key Pagination**: Use key-based pagination over $skip for large datasets

### Utah-Specific Features

- **Grid Address System**: Support both standard and Utah grid addressing
- **Geographic Calculations**: Use SRID=3956 for distance calculations
- **Local MLS Requirements**: Follow WFRMLS/Utah Real Estate Commission standards

### API Rate Limiting & Performance

- **200 Record Limit**: Enforce per-request maximum
- **NextLink Optimization**: Prefer NextLink pagination over $skip
- **Batch Processing**: Design for large dataset synchronization
- **Error Recovery**: Implement robust retry mechanisms

### Service Discovery Implementation

```python
# Service Discovery Client for metadata and available endpoints
class ServiceDiscoveryClient(BaseClient):
    def get_service_document(self) -> Dict[str, Any]:
        """Get service document with all available resources.
        
        Returns all available resources for the authenticated vendor,
        including resource names and URLs.
        
        Returns:
            Dictionary containing service document with available endpoints
            
        Example:
            ```python
            services = client.service_discovery.get_service_document()
            print([resource['name'] for resource in services.get('value', [])])
            ```
        """
        return self.get("")  # Base endpoint
    
    def get_metadata(self) -> Dict[str, Any]:
        """Get OData metadata XML schema.
        
        Returns XML schema with all resources, fields, enumerations,
        entity relationships and data types. Essential for understanding
        the complete API structure.
        
        Note: A local copy of this metadata is available at `./api_docs/metadata.xml`
        for development reference and type information.
        
        Returns:
            Dictionary containing metadata schema information
            
        Example:
            ```python
            metadata = client.service_discovery.get_metadata()
            # Process XML schema for field definitions
            ```
        """
        return self.get("$metadata")
```

## Best Practices Summary

1. **Follow STYLE_GUIDE.md**: Always check coding standards before implementation
2. **Reference API Documentation**: Use `api_docs/` specifications
3. **OData Support**: Implement full OData v4.0 query capabilities
4. **Type Safety**: Use comprehensive type hints with Union types for flexibility
5. **Error Handling**: Create specific exception types for different error scenarios
6. **Documentation**: Include examples in all docstrings with real estate context
7. **Testing**: Aim for 100% coverage with both success and error path testing
8. **Environment**: Use WFRMLS_BEARER_TOKEN for authentication
9. **Task Tracking**: Mark completion only after successful testing
10. **Real Estate Focus**: Use MLS-appropriate examples and naming conventions
11. **Utah Compliance**: Follow Utah grid system and local MLS requirements
12. **Rate Limiting**: Respect 200-record limits and implement proper pagination
13. **UTC Handling**: All timestamps must be processed in UTC format
14. **Data Sync**: Support incremental updates with 15-minute cycles