import unittest
from datetime import timedelta

from src.ConfigService import ConfigService


class TestConfigService(unittest.TestCase):

    def setUp(self):
        self.config_service = ConfigService(timedelta(seconds=10))

    def test_register_service(self):
        self.config_service.register_service('127.0.0.1', 8080)
        self.assertIn(('127.0.0.1', 8080), self.config_service.services)

    def test_register_caller(self):
        self.config_service.register_caller('John Doe', 'caller1')
        self.assertIn('caller1', self.config_service.callers)

    def test_subscribe_service(self):
        self.config_service.register_service('127.0.0.1', 8080)
        self.config_service.register_caller('John Doe', 'caller1')
        self.assertTrue(self.config_service.subscribe_service('127.0.0.1', 8080, 'caller1', timedelta(seconds=30)))


if __name__ == '__main__':
    unittest.main()
