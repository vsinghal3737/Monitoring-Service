import unittest
from datetime import datetime, timedelta

from src.models.Service import Service


class TestService(unittest.TestCase):

    def test_initialization(self):
        service = Service('127.0.0.1', 8080)
        self.assertEqual(service.host, '127.0.0.1')
        self.assertEqual(service.port, 8080)
        self.assertFalse(service.is_up)

    def test_subscribers_management(self):
        service = Service('127.0.0.1', 8080)
        service.add_subscriber('caller1')
        self.assertIn('caller1', service.subscribers)
        service.remove_subscriber('caller1')
        self.assertNotIn('caller1', service.subscribers)


# This allows the test to be run from the command line
if __name__ == '__main__':
    unittest.main()
