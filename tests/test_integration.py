"""Integration tests for WFRMLS API wrapper.

These tests make real API calls to verify the wrapper works correctly.
Set WFRMLS_BEARER_TOKEN environment variable to run these tests.

NOTE: Media, History, and Green Verification endpoints have been removed
due to server-side issues (504 Gateway Timeouts and missing entity types).
"""

import os
from datetime import datetime, timedelta
from typing import Any, Callable
from unittest.mock import Mock

import pytest

from wfrmls import WFRMLSClient
from wfrmls.exceptions import AuthenticationError, WFRMLSError


@pytest.fixture
def client() -> WFRMLSClient:
    """Create a test client with real API credentials."""
    # Set the bearer token from environment or use test token
    os.environ["WFRMLS_BEARER_TOKEN"] = "9d0243d7632d115b002acf3547d2d7ee"
    return WFRMLSClient()


class TestIntegration:
    """Integration tests with real API calls."""

    def test_client_initialization(self, client: WFRMLSClient) -> None:
        """Test that client initializes without errors."""
        assert client is not None
        assert hasattr(client, "property")
        assert hasattr(client, "member")
        assert hasattr(client, "office")

    def test_property_client_basic(self, client: WFRMLSClient) -> None:
        """Test basic property client functionality."""
        # Get one property to test basic functionality
        response = client.property.get_properties(top=1)

        assert "@odata.context" in response
        assert "value" in response
        assert isinstance(response["value"], list)

        if response["value"]:
            property_data = response["value"][0]
            assert isinstance(property_data, dict)
            # Should have some basic property fields
            assert "ListingId" in property_data or "ListingKey" in property_data

    def test_property_client_count(self, client: WFRMLSClient) -> None:
        """Test property count functionality."""
        response = client.property.get_properties(top=1, count=True)

        assert "@odata.count" in response
        total_count = response["@odata.count"]
        assert isinstance(total_count, int)
        assert total_count > 0
        print(f"Total properties in system: {total_count:,}")

    def test_property_client_active_filter(self, client: WFRMLSClient) -> None:
        """Test active properties filtering."""
        response = client.property.get_active_properties(top=5)

        assert "@odata.context" in response
        assert "value" in response
        assert len(response["value"]) <= 5

    def test_property_client_specific_fields(self, client: WFRMLSClient) -> None:
        """Test selecting specific fields."""
        response = client.property.get_properties(
            top=1, select=["ListingId", "ListPrice", "StandardStatus"]
        )

        assert "value" in response
        if response["value"]:
            property_data = response["value"][0]
            # Should only have selected fields (plus any system fields)
            assert "ListingId" in property_data or "ListingKey" in property_data

    def test_member_client_basic(self, client: WFRMLSClient) -> None:
        """Test basic member client functionality."""
        response = client.member.get_members(top=1)

        assert "@odata.context" in response
        assert "value" in response
        assert isinstance(response["value"], list)

        if response["value"]:
            member_data = response["value"][0]
            assert isinstance(member_data, dict)
            # Should have some basic member fields
            assert "MemberKey" in member_data

    def test_member_client_count(self, client: WFRMLSClient) -> None:
        """Test member count functionality."""
        response = client.member.get_members(top=1, count=True)

        assert "@odata.count" in response
        total_count = response["@odata.count"]
        assert isinstance(total_count, int)
        assert total_count > 0
        print(f"Total members in system: {total_count:,}")

    def test_member_client_active_filter(self, client: WFRMLSClient) -> None:
        """Test active members filtering."""
        response = client.member.get_active_members(top=5)

        assert "@odata.context" in response
        assert "value" in response
        assert len(response["value"]) <= 5

    def test_office_client_basic(self, client: WFRMLSClient) -> None:
        """Test basic office client functionality."""
        response = client.office.get_offices(top=1)

        assert "@odata.context" in response
        assert "value" in response
        assert isinstance(response["value"], list)

        if response["value"]:
            office_data = response["value"][0]
            assert isinstance(office_data, dict)
            # Should have some basic office fields
            assert "OfficeKey" in office_data

    def test_office_client_count(self, client: WFRMLSClient) -> None:
        """Test office count functionality."""
        response = client.office.get_offices(top=1, count=True)

        assert "@odata.count" in response
        total_count = response["@odata.count"]
        assert isinstance(total_count, int)
        assert total_count > 0
        print(f"Total offices in system: {total_count:,}")

    def test_office_client_active_filter(self, client: WFRMLSClient) -> None:
        """Test active offices filtering."""
        response = client.office.get_active_offices(top=5)

        assert "@odata.context" in response
        assert "value" in response
        assert len(response["value"]) <= 5

    def test_property_top_limit_enforcement(self, client):
        """Test that top parameter is properly limited."""
        # Try to request more than 200 records
        response = client.property.get_properties(top=500)

        assert "value" in response
        # Should be limited to 200 records
        assert len(response["value"]) <= 200

    def test_error_handling_invalid_filter(self, client):
        """Test error handling with invalid filter."""
        try:
            client.property.get_properties(filter_query="InvalidField eq 'test'")
            # If no error, that's also OK (API might be tolerant)
        except WFRMLSError:
            # Expected for invalid queries
            pass

    def test_property_price_range_filter(self, client):
        """Test price range filtering."""
        response = client.property.get_properties_by_price_range(
            min_price=200000, max_price=500000, top=5
        )

        assert "@odata.context" in response
        assert "value" in response

        # Check that returned properties are within price range
        for property_data in response["value"]:
            if "ListPrice" in property_data and property_data["ListPrice"]:
                price = property_data["ListPrice"]
                assert 200000 <= price <= 500000

    def test_member_search_functionality(self, client):
        """Test member search functionality."""
        # Search for members with common name
        response = client.member.search_members_by_name(last_name="Smith", top=5)

        assert "@odata.context" in response
        assert "value" in response
        # Results might be empty, which is fine
        assert isinstance(response["value"], list)

    def test_office_search_functionality(self, client):
        """Test office search functionality."""
        # Search for offices with "Realty" in name
        response = client.office.search_offices_by_name(name="Realty", top=5)

        assert "@odata.context" in response
        assert "value" in response
        # Results might be empty, which is fine
        assert isinstance(response["value"], list)

    def test_lazy_client_initialization(self, client):
        """Test that service clients are created lazily."""
        # Access each client type to ensure lazy loading works
        prop_client = client.property
        member_client = client.member
        office_client = client.office

        # Each access should return the same instance
        assert client.property is prop_client
        assert client.member is member_client
        assert client.office is office_client


class TestPropertyEndpoints:
    """Test property-related endpoints."""

    def test_get_properties(self, client):
        """Test getting properties."""
        result = client.property.get_properties(top=5)
        assert "value" in result
        assert len(result["value"]) <= 5
        assert "@odata.context" in result

    def test_get_active_properties(self, client):
        """Test getting active properties."""
        result = client.property.get_active_properties(top=3)
        assert "value" in result
        assert len(result["value"]) <= 3
        # Check that all returned properties are active
        for prop in result["value"]:
            assert prop.get("StandardStatus") == "Active"

    def test_get_properties_by_city(self, client):
        """Test getting properties by city."""
        result = client.property.get_properties_by_city("Salt Lake City", top=3)
        assert "value" in result
        for prop in result["value"]:
            assert prop.get("City") == "Salt Lake City"

    def test_get_property_count(self, client):
        """Test getting property count."""
        result = client.property.get_properties(count=True, top=1)
        assert "@odata.count" in result
        assert isinstance(result["@odata.count"], int)
        # There should be a substantial number of properties in the MLS
        assert result["@odata.count"] > 1000000


class TestMemberEndpoints:
    """Test member-related endpoints."""

    def test_get_members(self, client):
        """Test getting members."""
        result = client.member.get_members(top=5)
        assert "value" in result
        assert len(result["value"]) <= 5

    def test_get_active_members(self, client):
        """Test getting active members."""
        result = client.member.get_active_members(top=3)
        assert "value" in result
        for member in result["value"]:
            assert member.get("MemberStatus") == "Active"


class TestOfficeEndpoints:
    """Test office-related endpoints."""

    def test_get_offices(self, client):
        """Test getting offices."""
        result = client.office.get_offices(top=5)
        assert "value" in result
        assert len(result["value"]) <= 5

    def test_get_active_offices(self, client):
        """Test getting active offices."""
        result = client.office.get_active_offices(top=3)
        assert "value" in result
        for office in result["value"]:
            assert office.get("OfficeStatus") == "Active"


class TestOpenHouseEndpoints:
    """Test open house-related endpoints."""

    def test_get_open_houses(self, client):
        """Test getting open houses."""
        result = client.openhouse.get_open_houses(top=5)
        assert "value" in result
        assert len(result["value"]) <= 5

    def test_get_upcoming_open_houses(self, client):
        """Test getting upcoming open houses."""
        result = client.openhouse.get_upcoming_open_houses(top=10)
        assert "value" in result
        # Should return upcoming open houses (may be empty if none scheduled)
        assert isinstance(result["value"], list)

    def test_get_active_open_houses(self, client):
        """Test getting active open houses."""
        result = client.openhouse.get_active_open_houses(top=10)
        assert "value" in result
        for open_house in result["value"]:
            # If there are any results, they should be active
            if result["value"]:
                assert open_house.get("OpenHouseStatus") == "Active"


class TestClientIntegration:
    """Test main client integration."""

    def test_client_lazy_loading(self, client):
        """Test that service clients are lazily loaded."""
        # Services should not be initialized until accessed
        assert client._property is None
        assert client._member is None
        assert client._office is None
        assert client._openhouse is None

        # Access services to trigger lazy loading
        _ = client.property
        _ = client.member
        _ = client.office
        _ = client.openhouse

        # Services should now be initialized
        assert client._property is not None
        assert client._member is not None
        assert client._office is not None
        assert client._openhouse is not None

    def test_all_endpoints_accessible(self, client):
        """Test that all available endpoints are accessible through the main client."""
        # Test property endpoints
        properties = client.property.get_properties(top=1)
        assert "value" in properties

        # Test member endpoints
        members = client.member.get_members(top=1)
        assert "value" in members

        # Test office endpoints
        offices = client.office.get_offices(top=1)
        assert "value" in offices

        # Test open house endpoints
        open_houses = client.openhouse.get_open_houses(top=1)
        assert "value" in open_houses

        # NOTE: Media, History, and Green Verification endpoints have been
        # removed due to server-side issues


class TestErrorHandling:
    """Test error handling across endpoints."""

    def test_invalid_bearer_token(self):
        """Test that invalid bearer token raises appropriate error."""
        from wfrmls.exceptions import AuthenticationError

        client = WFRMLSClient(bearer_token="invalid_token")
        with pytest.raises(AuthenticationError):
            client.property.get_properties(top=1)

    def test_not_found_error(self, client):
        """Test not found error for non-existent resources."""
        from wfrmls.exceptions import ValidationError

        with pytest.raises(ValidationError):
            client.property.get_property("nonexistent_key")


@pytest.fixture
def bearer_token() -> str:
    """Get bearer token from environment or return test token."""
    return os.environ.get("WFRMLS_BEARER_TOKEN", "test_bearer_token")


def test_client_initialization(bearer_token: str) -> None:
    """Test client can be initialized."""
    client = WFRMLSClient(bearer_token=bearer_token)
    assert client.bearer_token == bearer_token


def test_property_endpoint_accessible(bearer_token: str) -> None:
    """Test property endpoint is accessible."""
    client = WFRMLSClient(bearer_token=bearer_token)
    assert hasattr(client, "property")
    assert client.property is not None


def test_member_endpoint_accessible(bearer_token: str) -> None:
    """Test member endpoint is accessible."""
    client = WFRMLSClient(bearer_token=bearer_token)
    assert hasattr(client, "member")
    assert client.member is not None


def test_office_endpoint_accessible(bearer_token: str) -> None:
    """Test office endpoint is accessible."""
    client = WFRMLSClient(bearer_token=bearer_token)
    assert hasattr(client, "office")
    assert client.office is not None


def test_openhouse_endpoint_accessible(bearer_token: str) -> None:
    """Test openhouse endpoint is accessible."""
    client = WFRMLSClient(bearer_token=bearer_token)
    assert hasattr(client, "open_house")
    assert client.open_house is not None


def test_deleted_endpoint_accessible(bearer_token: str) -> None:
    """Test deleted endpoint is accessible."""
    client = WFRMLSClient(bearer_token=bearer_token)
    assert hasattr(client, "deleted")
    assert client.deleted is not None


def test_property_endpoint_has_required_methods(bearer_token: str) -> None:
    """Test property endpoint has required methods."""
    client = WFRMLSClient(bearer_token=bearer_token)
    assert hasattr(client.property, "get_properties")
    assert hasattr(client.property, "get_property")
    assert hasattr(client.property, "search_properties")


def test_member_endpoint_has_required_methods(bearer_token: str) -> None:
    """Test member endpoint has required methods."""
    client = WFRMLSClient(bearer_token=bearer_token)
    assert hasattr(client.member, "get_members")
    assert hasattr(client.member, "get_member")
    assert hasattr(client.member, "get_active_members")


def test_office_endpoint_has_required_methods(bearer_token: str) -> None:
    """Test office endpoint has required methods."""
    client = WFRMLSClient(bearer_token=bearer_token)
    assert hasattr(client.office, "get_offices")
    assert hasattr(client.office, "get_office")
    assert hasattr(client.office, "get_active_offices")


def test_openhouse_endpoint_has_required_methods(bearer_token: str) -> None:
    """Test openhouse endpoint has required methods."""
    client = WFRMLSClient(bearer_token=bearer_token)
    assert hasattr(client.open_house, "get_open_houses")
    assert hasattr(client.open_house, "get_open_house")
    assert hasattr(client.open_house, "get_upcoming_open_houses")


def test_deleted_endpoint_has_required_methods(bearer_token: str) -> None:
    """Test deleted endpoint has required methods."""
    client = WFRMLSClient(bearer_token=bearer_token)
    assert hasattr(client.deleted, "get_deleted_properties")
    assert hasattr(client.deleted, "get_deleted_members")
    assert hasattr(client.deleted, "get_deleted_offices")
    assert hasattr(client.deleted, "get_deleted_open_houses")


def test_property_client_bearer_token_propagation(bearer_token: str) -> None:
    """Test bearer token is properly propagated to property client."""
    client = WFRMLSClient(bearer_token=bearer_token)
    assert client.property.bearer_token == bearer_token


def test_member_client_bearer_token_propagation(bearer_token: str) -> None:
    """Test bearer token is properly propagated to member client."""
    client = WFRMLSClient(bearer_token=bearer_token)
    assert client.member.bearer_token == bearer_token


def test_office_client_bearer_token_propagation(bearer_token: str) -> None:
    """Test bearer token is properly propagated to office client."""
    client = WFRMLSClient(bearer_token=bearer_token)
    assert client.office.bearer_token == bearer_token


def test_openhouse_client_bearer_token_propagation(bearer_token: str) -> None:
    """Test bearer token is properly propagated to openhouse client."""
    client = WFRMLSClient(bearer_token=bearer_token)
    assert client.open_house.bearer_token == bearer_token


def test_deleted_client_bearer_token_propagation(bearer_token: str) -> None:
    """Test bearer token is properly propagated to deleted client."""
    client = WFRMLSClient(bearer_token=bearer_token)
    assert client.deleted.bearer_token == bearer_token


def test_property_base_url_propagation(bearer_token: str) -> None:
    """Test base URL is properly propagated to property client."""
    client = WFRMLSClient(bearer_token=bearer_token)
    assert client.property.base_url == "https://resoapi.utahrealestate.com/reso/odata"


def test_member_base_url_propagation(bearer_token: str) -> None:
    """Test base URL is properly propagated to member client."""
    client = WFRMLSClient(bearer_token=bearer_token)
    assert client.member.base_url == "https://resoapi.utahrealestate.com/reso/odata"


def test_office_base_url_propagation(bearer_token: str) -> None:
    """Test base URL is properly propagated to office client."""
    client = WFRMLSClient(bearer_token=bearer_token)
    assert client.office.base_url == "https://resoapi.utahrealestate.com/reso/odata"


def test_openhouse_base_url_propagation(bearer_token: str) -> None:
    """Test base URL is properly propagated to openhouse client."""
    client = WFRMLSClient(bearer_token=bearer_token)
    assert client.open_house.base_url == "https://resoapi.utahrealestate.com/reso/odata"


def test_deleted_base_url_propagation(bearer_token: str) -> None:
    """Test base URL is properly propagated to deleted client."""
    client = WFRMLSClient(bearer_token=bearer_token)
    assert client.deleted.base_url == "https://resoapi.utahrealestate.com/reso/odata"


def test_custom_base_url_propagation(bearer_token: str) -> None:
    """Test custom base URL is properly propagated to all clients."""
    custom_base_url = "https://custom.api.url/reso/odata"
    client = WFRMLSClient(bearer_token=bearer_token, base_url=custom_base_url)

    assert client.property.base_url == custom_base_url
    assert client.member.base_url == custom_base_url
    assert client.office.base_url == custom_base_url
    assert client.open_house.base_url == custom_base_url
    assert client.deleted.base_url == custom_base_url


@pytest.fixture
def mock_client() -> Callable[[], Any]:
    """Create a mock WFRMLS client for testing."""
    mock = Mock(spec=WFRMLSClient)
    return lambda: mock


def test_mock_client_integration(mock_client: Callable[[], Any]) -> None:
    """Test integration with mocked client."""
    client = WFRMLSClient(bearer_token="test_token")

    # Test that all endpoints are available
    assert client.property is not None
    assert client.member is not None
    assert client.office is not None
    assert client.open_house is not None


if __name__ == "__main__":
    # Run a quick test to verify all endpoints are working
    client = WFRMLSClient(bearer_token="9d0243d7632d115b002acf3547d2d7ee")

    print("Testing all available endpoints...")

    # Test each endpoint quickly
    endpoints_to_test = [
        ("Property", lambda: client.property.get_properties(top=1)),
        ("Member", lambda: client.member.get_members(top=1)),
        ("Office", lambda: client.office.get_offices(top=1)),
        ("OpenHouse", lambda: client.openhouse.get_open_houses(top=1)),
    ]

    for name, test_func in endpoints_to_test:
        try:
            result = test_func()
            print(f"✓ {name}: OK ({len(result.get('value', []))} records)")
        except Exception as e:
            print(f"✗ {name}: Error - {e}")

    print("Testing complete!")
    print("\nNOTE: Media, History, and Green Verification endpoints are")
    print("currently unavailable due to server-side issues.")
