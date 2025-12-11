# test_app.py (UPDATED)
import pytest
import json
from unittest.mock import patch, MagicMock
import azure.functions as func

# Import the function you want to test
from function_app import visitor_counter, get_cosmos_container

# Use a fixture to provide a consistent mock container object for all tests
@pytest.fixture
def mock_container_client():
    """Provides a mock object that simulates the Cosmos DB container."""
    return MagicMock()

# Patch the get_cosmos_container function to return our mock
@patch('function_app.get_cosmos_container')
def test_visitor_counter_initial_visit(mock_get_container, mock_container_client):
    """
    Test the scenario where the item does not exist (first visit).
    """
    # Arrange
    # Configure the mock to be returned when get_cosmos_container() is called
    mock_get_container.return_value = mock_container_client

    # Simulate that read_item raises an exception (item not found)
    mock_container_client.read_item.side_effect = Exception("Item not found")

    # Define the expected item created by the function
    expected_item = {"id": "1", "count": 1}
    mock_container_client.upsert_item.return_value = expected_item

    # Create a mock HTTP request object
    req = func.HttpRequest(method='GET', url='/api/visits', headers={}, body=None)

    # Act
    resp: func.HttpResponse = visitor_counter(req)

    # Assert
    assert resp.status_code == 200
    assert json.loads(resp.get_body()) == {"visits": 1}
    mock_container_client.read_item.assert_called_once()
    mock_container_client.upsert_item.assert_called_once_with(expected_item)


@patch('function_app.get_cosmos_container')
def test_visitor_counter_subsequent_visit(mock_get_container, mock_container_client):
    """
    Test the scenario where the item exists and the count needs to be incremented.
    """
    # Arrange
    mock_get_container.return_value = mock_container_client

    # Simulate an existing item being read
    existing_item = {"id": "1", "count": 5}
    mock_container_client.read_item.return_value = existing_item

    # Create a mock HTTP request
    req = func.HttpRequest(method='GET', url='/api/visits', headers={}, body=None)

    # Act
    resp: func.HttpResponse = visitor_counter(req)

    # Assert the response structure and content
    assert resp.status_code == 200
    assert json.loads(resp.get_body()) == {"visits": 6}

    # Verify that upsert was called with the *incremented* item data
    updated_item = {"id": "1", "count": 6}
    mock_container_client.upsert_item.assert_called_once_with(updated_item)
