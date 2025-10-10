"""Tests for member client."""

from datetime import date
from unittest.mock import MagicMock, patch

import pytest
import responses

from wfrmls.exceptions import NotFoundError
from wfrmls.member import MemberClient, MemberStatus, MemberType


class TestMemberClient:
    """Test cases for MemberClient."""

    def setup_method(self) -> None:
        """Set up test client."""
        self.client = MemberClient(bearer_token="test_bearer_token")

    @responses.activate
    def test_get_members_success(self) -> None:
        """Test successful get members request."""
        mock_response = {
            "@odata.context": "https://resoapi.utahrealestate.com/reso/odata/$metadata#Member",
            "value": [
                {
                    "MemberKey": "12345",
                    "MemberFirstName": "John",
                    "MemberLastName": "Doe",
                    "MemberStatus": "Active",
                },
                {
                    "MemberKey": "67890",
                    "MemberFirstName": "Jane",
                    "MemberLastName": "Smith",
                    "MemberStatus": "Active",
                },
            ],
        }

        responses.add(
            responses.GET,
            "https://resoapi.utahrealestate.com/reso/odata/Member",
            json=mock_response,
            status=200,
        )

        result = self.client.get_members()
        assert result == mock_response
        assert len(responses.calls) == 1

    @responses.activate
    def test_get_members_with_odata_params(self) -> None:
        """Test get members with OData parameters."""
        mock_response = {"@odata.context": "test", "value": []}

        responses.add(
            responses.GET,
            "https://resoapi.utahrealestate.com/reso/odata/Member",
            json=mock_response,
            status=200,
        )

        result = self.client.get_members(
            top=10,
            skip=20,
            filter_query="MemberStatus eq 'Active'",
            select=["MemberKey", "MemberFirstName", "MemberLastName"],
            orderby="MemberLastName desc",
        )

        assert result == mock_response

        # Verify query parameters (URL encoded)
        request = responses.calls[0].request
        assert request.url is not None
        assert "%24top=10" in request.url
        assert "%24skip=20" in request.url
        assert "%24filter=MemberStatus+eq+%27Active%27" in request.url
        assert "MemberKey" in request.url
        assert "MemberFirstName" in request.url
        assert "MemberLastName" in request.url
        assert "%24orderby=MemberLastName+desc" in request.url

    @responses.activate
    def test_get_member_not_found(self) -> None:
        """Test get member not found error."""
        responses.add(
            responses.GET,
            "https://resoapi.utahrealestate.com/reso/odata/Member('nonexistent')",
            json={"error": {"message": "Member not found"}},
            status=404,
        )

        with pytest.raises(NotFoundError, match="Resource not found"):
            self.client.get_member("nonexistent")

    @responses.activate
    def test_get_active_members(self) -> None:
        """Test get active members convenience method."""
        mock_response = {"@odata.context": "test", "value": []}

        responses.add(
            responses.GET,
            "https://resoapi.utahrealestate.com/reso/odata/Member",
            json=mock_response,
            status=200,
        )

        result = self.client.get_active_members(top=50)

        assert result == mock_response
        request = responses.calls[0].request
        assert request.url is not None
        assert (
            "%24filter=MemberStatus+eq+%27Active%27" in request.url
            or "MemberStatus+eq+%27Active%27" in request.url
        )
        assert "%24top=50" in request.url

    @responses.activate
    def test_get_members_by_office(self) -> None:
        """Test get members by office."""
        mock_response = {"@odata.context": "test", "value": []}

        responses.add(
            responses.GET,
            "https://resoapi.utahrealestate.com/reso/odata/Member",
            json=mock_response,
            status=200,
        )

        result = self.client.get_members_by_office(office_key="12345", top=25)

        assert result == mock_response
        request = responses.calls[0].request
        assert request.url is not None
        assert "OfficeKey+eq+%27" in request.url or "OfficeKey eq '" in request.url
        assert "12345" in request.url
        assert "%24top=25" in request.url

    @responses.activate
    def test_search_members_by_name(self) -> None:
        """Test search members by name."""
        mock_response = {"@odata.context": "test", "value": []}

        responses.add(
            responses.GET,
            "https://resoapi.utahrealestate.com/reso/odata/Member",
            json=mock_response,
            status=200,
        )

        result = self.client.search_members_by_name(
            first_name="John", last_name="Smith"
        )

        assert result == mock_response
        request = responses.calls[0].request
        assert request.url is not None
        assert "contains" in request.url
        assert "MemberFirstName" in request.url
        assert "MemberLastName" in request.url
        assert "John" in request.url
        assert "Smith" in request.url

    @responses.activate
    def test_search_members_by_last_name_only(self) -> None:
        """Test search members by last name only."""
        mock_response = {"@odata.context": "test", "value": []}

        responses.add(
            responses.GET,
            "https://resoapi.utahrealestate.com/reso/odata/Member",
            json=mock_response,
            status=200,
        )

        result = self.client.search_members_by_name(last_name="Smith")

        assert result == mock_response
        request = responses.calls[0].request
        assert request.url is not None
        assert "contains" in request.url
        assert "MemberLastName" in request.url
        assert "Smith" in request.url

    @responses.activate
    def test_get_members_with_office(self) -> None:
        """Test get members with office info expanded."""
        mock_response = {"@odata.context": "test", "value": []}

        responses.add(
            responses.GET,
            "https://resoapi.utahrealestate.com/reso/odata/Member",
            json=mock_response,
            status=200,
        )

        result = self.client.get_members_with_office(top=25)

        assert result == mock_response
        request = responses.calls[0].request
        assert request.url is not None
        assert "%24expand=Office" in request.url or "$expand=Office" in request.url
        assert "%24top=25" in request.url

    @responses.activate
    def test_get_modified_members(self) -> None:
        """Test get modified members."""
        mock_response = {"@odata.context": "test", "value": []}

        responses.add(
            responses.GET,
            "https://resoapi.utahrealestate.com/reso/odata/Member",
            json=mock_response,
            status=200,
        )

        test_date = date(2023, 1, 1)
        result = self.client.get_modified_members(since=test_date)

        assert result == mock_response
        request = responses.calls[0].request
        assert request.url is not None
        assert "ModificationTimestamp+gt+2023-01-01Z" in request.url

    def test_enum_values(self) -> None:
        """Test enum values are correct."""
        assert MemberStatus.ACTIVE.value == "Active"
        assert MemberStatus.INACTIVE.value == "Inactive"
        assert MemberStatus.SUSPENDED.value == "Suspended"

        assert MemberType.AGENT.value == "Agent"
        assert MemberType.BROKER.value == "Broker"
        assert MemberType.ASSISTANT.value == "Assistant"

    @responses.activate
    def test_top_limit_enforcement(self) -> None:
        """Test that top parameter is limited to 200."""
        mock_response = {"@odata.context": "test", "value": []}

        responses.add(
            responses.GET,
            "https://resoapi.utahrealestate.com/reso/odata/Member",
            json=mock_response,
            status=200,
        )

        # Request more than 200 records
        result = self.client.get_members(top=500)

        assert result == mock_response
        request = responses.calls[0].request
        assert request.url is not None
        # Should be capped at 200
        assert "%24top=200" in request.url or "$top=200" in request.url

    @responses.activate
    def test_select_list_parameter(self) -> None:
        """Test select parameter with list input."""
        mock_response = {"@odata.context": "test", "value": []}

        responses.add(
            responses.GET,
            "https://resoapi.utahrealestate.com/reso/odata/Member",
            json=mock_response,
            status=200,
        )

        result = self.client.get_members(
            select=["MemberKey", "MemberFirstName", "MemberLastName"]
        )

        assert result == mock_response
        request = responses.calls[0].request
        assert request.url is not None
        assert "MemberKey" in request.url
        assert "MemberFirstName" in request.url
        assert "MemberLastName" in request.url

    @responses.activate
    def test_expand_list_parameter(self) -> None:
        """Test expand parameter with list input."""
        mock_response = {"@odata.context": "test", "value": []}

        responses.add(
            responses.GET,
            "https://resoapi.utahrealestate.com/reso/odata/Member",
            json=mock_response,
            status=200,
        )

        result = self.client.get_members(expand=["Office", "Property"])

        assert result == mock_response
        request = responses.calls[0].request
        assert request.url is not None
        assert "%24expand=Office%2CProperty" in request.url

    @responses.activate
    def test_combined_filters_in_office_search(self) -> None:
        """Test combining office filter with additional filters."""
        mock_response = {"@odata.context": "test", "value": []}

        responses.add(
            responses.GET,
            "https://resoapi.utahrealestate.com/reso/odata/Member",
            json=mock_response,
            status=200,
        )

        result = self.client.get_members_by_office(
            office_key="12345", filter_query="MemberStatus eq 'Active'"
        )

        assert result == mock_response
        request = responses.calls[0].request
        assert request.url is not None
        # Should contain both filters combined with 'and'
        assert "OfficeKey" in request.url
        assert "12345" in request.url
        assert "MemberStatus" in request.url
        assert "Active" in request.url


@pytest.fixture
def member_client():
    """Create a member client for testing."""
    return MemberClient(bearer_token="test_token")


@pytest.fixture
def mock_response():
    """Create a mock response for testing."""
    return {
        "@odata.context": "https://api.example.com/odata/$metadata#Member",
        "value": [
            {
                "MemberKey": "12345",
                "MemberKeyNumeric": 12345,
                "MemberMlsId": "4020986",
                "MemberFirstName": "Lena",
                "MemberLastName": "Watson",
                "MemberFullName": "Lena A Watson",
                "MemberEmail": "lena@example.com",
                "MemberPreferredPhone": "801-414-3095",
                "MemberStatus": "Active",
                "OfficeName": "Real Broker, LLC",
                "OfficeKey": "54321",
            }
        ],
    }


@pytest.fixture
def mock_empty_response():
    """Create an empty mock response for testing."""
    return {
        "@odata.context": "https://api.example.com/odata/$metadata#Member",
        "value": [],
    }


def test_get_members(member_client):
    """Test getting members with various parameters."""
    with patch.object(member_client, "get") as mock_get:
        mock_get.return_value = {"value": []}

        # Test with no parameters
        member_client.get_members()
        mock_get.assert_called_with("Member", params={})

        # Test with top parameter
        member_client.get_members(top=10)
        mock_get.assert_called_with("Member", params={"$top": 10})

        # Test with filter parameter
        member_client.get_members(filter_query="MemberStatus eq 'Active'")
        mock_get.assert_called_with(
            "Member", params={"$filter": "MemberStatus eq 'Active'"}
        )

        # Test with select parameter as list
        member_client.get_members(select=["MemberKey", "MemberFullName"])
        mock_get.assert_called_with(
            "Member", params={"$select": "MemberKey,MemberFullName"}
        )

        # Test with select parameter as string
        member_client.get_members(select="MemberKey,MemberFullName")
        mock_get.assert_called_with(
            "Member", params={"$select": "MemberKey,MemberFullName"}
        )

        # Test with expand parameter as list
        member_client.get_members(expand=["Office", "Property"])
        mock_get.assert_called_with("Member", params={"$expand": "Office,Property"})

        # Test with expand parameter as string
        member_client.get_members(expand="Office,Property")
        mock_get.assert_called_with("Member", params={"$expand": "Office,Property"})

        # Test with count parameter
        member_client.get_members(count=True)
        mock_get.assert_called_with("Member", params={"$count": "true"})

        # Test with multiple parameters
        member_client.get_members(
            top=10,
            skip=5,
            filter_query="MemberStatus eq 'Active'",
            select=["MemberKey", "MemberFullName"],
            orderby="MemberLastName asc",
            expand="Office",
            count=True,
        )
        mock_get.assert_called_with(
            "Member",
            params={
                "$top": 10,
                "$skip": 5,
                "$filter": "MemberStatus eq 'Active'",
                "$select": "MemberKey,MemberFullName",
                "$orderby": "MemberLastName asc",
                "$expand": "Office",
                "$count": "true",
            },
        )


def test_get_member(member_client):
    """Test getting a member by key."""
    with patch.object(member_client, "get") as mock_get:
        mock_get.return_value = {"MemberKey": "12345"}

        result = member_client.get_member("12345")

        mock_get.assert_called_with("Member('12345')")
        assert result == {"MemberKey": "12345"}


def test_get_member_by_mls_id(member_client, mock_response):
    """Test getting a member by MLS ID."""
    with patch.object(member_client, "get_members") as mock_get_members:
        mock_get_members.return_value = mock_response

        result = member_client.get_member_by_mls_id("4020986")

        mock_get_members.assert_called_with(
            filter_query="MemberMlsId eq '4020986'", expand="Office", top=1
        )
        assert result["MemberMlsId"] == "4020986"
        assert result["MemberFullName"] == "Lena A Watson"
        assert result["OfficeName"] == "Real Broker, LLC"


def test_get_member_by_mls_id_not_found(member_client, mock_empty_response):
    """Test getting a member by MLS ID when not found."""
    with patch.object(member_client, "get_members") as mock_get_members:
        mock_get_members.return_value = mock_empty_response

        with pytest.raises(NotFoundError) as excinfo:
            member_client.get_member_by_mls_id("nonexistent")

        assert "No member found with MLS ID: nonexistent" in str(excinfo.value)


def test_get_active_members(member_client):
    """Test getting active members."""
    with patch.object(member_client, "get_members") as mock_get_members:
        mock_get_members.return_value = {"value": []}

        member_client.get_active_members()

        mock_get_members.assert_called_with(filter_query="MemberStatus eq 'Active'")

        # Test with additional parameters
        member_client.get_active_members(top=10, orderby="MemberLastName")

        mock_get_members.assert_called_with(
            filter_query="MemberStatus eq 'Active'", top=10, orderby="MemberLastName"
        )


def test_get_members_by_office(member_client):
    """Test getting members by office."""
    with patch.object(member_client, "get_members") as mock_get_members:
        mock_get_members.return_value = {"value": []}

        # Test with no additional filter
        member_client.get_members_by_office("54321")

        mock_get_members.assert_called_with(filter_query="OfficeKey eq '54321'")

        # Test with additional filter
        member_client.get_members_by_office(
            "54321", filter_query="MemberStatus eq 'Active'"
        )

        mock_get_members.assert_called_with(
            filter_query="OfficeKey eq '54321' and MemberStatus eq 'Active'"
        )


def test_search_members_by_name(member_client):
    """Test searching members by name."""
    with patch.object(member_client, "get_members") as mock_get_members:
        mock_get_members.return_value = {"value": []}

        # Test with first name only
        member_client.search_members_by_name(first_name="John")

        mock_get_members.assert_called_with(
            filter_query="contains(MemberFirstName, 'John')"
        )

        # Test with last name only
        member_client.search_members_by_name(last_name="Smith")

        mock_get_members.assert_called_with(
            filter_query="contains(MemberLastName, 'Smith')"
        )

        # Test with both names
        member_client.search_members_by_name(first_name="John", last_name="Smith")

        mock_get_members.assert_called_with(
            filter_query="contains(MemberFirstName, 'John') and contains(MemberLastName, 'Smith')"
        )

        # Test with no names
        member_client.search_members_by_name()

        mock_get_members.assert_called_with()


def test_get_members_with_office(member_client):
    """Test getting members with office information."""
    with patch.object(member_client, "get_members") as mock_get_members:
        mock_get_members.return_value = {"value": []}

        member_client.get_members_with_office()

        mock_get_members.assert_called_with(expand="Office")

        # Test with additional parameters
        member_client.get_members_with_office(
            top=10, filter_query="MemberStatus eq 'Active'"
        )

        mock_get_members.assert_called_with(
            expand="Office", top=10, filter_query="MemberStatus eq 'Active'"
        )


def test_get_modified_members(member_client):
    """Test getting modified members."""
    with patch.object(member_client, "get_members") as mock_get_members:
        mock_get_members.return_value = {"value": []}

        # Test with string date
        member_client.get_modified_members("2023-01-01T00:00:00Z")

        mock_get_members.assert_called_with(
            filter_query="ModificationTimestamp gt 2023-01-01T00:00:00Z"
        )

        # Test with date object
        test_date = date(2023, 1, 1)

        member_client.get_modified_members(test_date)

        mock_get_members.assert_called_with(
            filter_query="ModificationTimestamp gt 2023-01-01Z"
        )


def test_member_status_enum():
    """Test the MemberStatus enum."""
    assert MemberStatus.ACTIVE.value == "Active"
    assert MemberStatus.INACTIVE.value == "Inactive"
    assert MemberStatus.SUSPENDED.value == "Suspended"


def test_member_type_enum():
    """Test the MemberType enum."""
    assert MemberType.AGENT.value == "Agent"
    assert MemberType.BROKER.value == "Broker"
    assert MemberType.ASSISTANT.value == "Assistant"
