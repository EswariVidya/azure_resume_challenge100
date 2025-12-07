
"""test_app.py - unit tests for app.py using built-in unittest and simple mock objects.
These tests do NOT require any Azure SDKs and exercise success & error paths.
"""

import unittest
from function_app import handle_request

# Simple mock cosmos client classes
class MockCosmosGood:
    def __init__(self, start=0):
        self._count = start
    def get_visits(self):
        return self._count
    def increment_visits(self):
        self._count += 1
        return self._count

class MockCosmosError:
    def get_visits(self):
        raise RuntimeError("cosmos unavailable")
    def increment_visits(self):
        raise RuntimeError("cosmos write failed")

class MockCosmosSlow:
    def __init__(self, start=5):
        self._count = start
    def get_visits(self):
        # simulate heavy but deterministic behavior
        return self._count
    def increment_visits(self):
        self._count += 10  # unusual behaviour to test contract assumptions
        return self._count

class TestAppHandler(unittest.TestCase):

    def test_get_returns_current_visits(self):
        cosmos = MockCosmosGood(start=7)
        status, body = handle_request('GET', None, cosmos)
        self.assertEqual(status, 200)
        self.assertIsInstance(body, dict)
        self.assertEqual(body.get('visits'), 7)

    def test_post_increments_and_returns_new_visits(self):
        cosmos = MockCosmosGood(start=0)
        status, body = handle_request('POST', {'action': 'visit'}, cosmos)
        self.assertEqual(status, 201)
        self.assertEqual(body.get('visits'), 1)
        # confirm second increment works too
        status2, body2 = handle_request('POST', {'action': 'visit'}, cosmos)
        self.assertEqual(status2, 201)
        self.assertEqual(body2.get('visits'), 2)

    def test_post_invalid_body_returns_400(self):
        cosmos = MockCosmosGood(start=1)
        status, body = handle_request('POST', None, cosmos)
        self.assertEqual(status, 400)
        self.assertIn('error', body)

        status2, body2 = handle_request('POST', {'action': 'wrong'}, cosmos)
        self.assertEqual(status2, 400)
        self.assertIn('error', body2)

    def test_method_not_allowed_returns_405(self):
        cosmos = MockCosmosGood(start=3)
        status, body = handle_request('DELETE', None, cosmos)
        self.assertEqual(status, 405)
        self.assertIn('error', body)

    def test_cosmos_exceptions_return_500(self):
        cosmos = MockCosmosError()
        status, body = handle_request('GET', None, cosmos)
        self.assertEqual(status, 500)
        self.assertIn('error', body)
        status2, body2 = handle_request('POST', {'action': 'visit'}, cosmos)
        self.assertEqual(status2, 500)
        self.assertIn('error', body2)

    def test_nonstandard_increment_behavior(self):
        cosmos = MockCosmosSlow(start=5)
        status, body = handle_request('POST', {'action': 'visit'}, cosmos)
        self.assertEqual(status, 201)
        # check the unusual increment logic reflected
        self.assertEqual(body.get('visits'), 15)

if __name__ == '__main__':
    unittest.main(verbosity=2)
