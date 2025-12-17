import unittest
from unittest.mock import MagicMock, patch
import azure.functions as func
import json
from azure.cosmos.errors import CosmosResourceNotFoundError

# Import the function from your file (assuming the file is named function_app.py)
from function_app import visitor_counter

class TestVisitorCounter(unittest.TestCase):

    def setUp(self):
        # Create a mock for the Cosmos Container
        self.mock_container = MagicMock()
        
        # Patch the global cosmos_container variable in function_app
        # This bypasses the get_cosmos_container() logic that looks for env vars
        self.patcher = patch('function_app.cosmos_container', self.mock_container)
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()

    def test_visitor_counter_new_item(self):
        """Test scenario where the item does not exist (First Visit)"""
        # Mock read_item to raise a 404 error
        self.mock_container.read_item.side_effect = CosmosResourceNotFoundError()

        # Construct a mock HTTP request
        req = func.HttpRequest(
            method='GET',
            body=None,
            url='/api/visits'
        )

        # Call the function
        resp = visitor_counter(req)
        resp_body = json.loads(resp.get_body())

        # Assertions
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp_body['visits'], 1)
        self.mock_container.upsert_item.assert_called_with(body={'id': '1', 'count': 1})

    def test_visitor_counter_existing_item(self):
        """Test scenario where the item exists (Increment Visit)"""
        # Mock read_item to return an existing record
        self.mock_container.read_item.return_value = {'id': '1', 'count': 5}

        req = func.HttpRequest(
            method='GET',
            body=None,
            url='/api/visits'
        )

        resp = visitor_counter(req)
        resp_body = json.loads(resp.get_body())

        # Assertions
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp_body['visits'], 6)
        self.mock_container.upsert_item.assert_called_with(body={'id': '1', 'count': 6})

    def test_visitor_counter_options_request(self):
        """Test CORS preflight OPTIONS request"""
        req = func.HttpRequest(
            method='OPTIONS',
            body=None,
            url='/api/visits'
        )

        resp = visitor_counter(req)

        self.assertEqual(resp.status_code, 204)
        self.assertEqual(resp.headers.get('Access-Control-Allow-Origin'), '*')

    def test_visitor_counter_error_handling(self):
        """Test scenario where Cosmos DB throws an unexpected error"""
        self.mock_container.read_item.side_effect = Exception("Connection Failed")

        req = func.HttpRequest(
            method='GET',
            body=None,
            url='/api/visits'
        )

        resp = visitor_counter(req)
        
        self.assertEqual(resp.status_code, 500)
        self.assertIn("unexpected error", resp.get_body().decode())

if __name__ == '__main__':
    unittest.main()
