import unittest
from datetime import timedelta

from src.models.Caller import Caller


class TestCaller(unittest.TestCase):

    def test_subscription(self):
        caller = Caller('John Doe', 'caller1')
        caller.add_subscription('127.0.0.1', 8080, timedelta(seconds=30))
        caller.add_subscription('127.0.0.2', 8082, timedelta(seconds=30))
        self.assertTrue(caller.subscribed[('127.0.0.2', 8082)])
        self.assertIn(('127.0.0.1', 8080), caller.subscribed)
        caller.remove_subscription('127.0.0.1', 8080)
        self.assertNotIn(('127.0.0.1', 8080), caller.subscribed)


if __name__ == '__main__':
    unittest.main()
