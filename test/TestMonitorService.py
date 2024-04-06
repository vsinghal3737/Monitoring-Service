import unittest
from datetime import datetime

from src.MonitorService import MonitorService


class TestMonitorService(unittest.TestCase):

    def test_check_service_status_success(self):
        monitor_service = MonitorService(5)
        self.assertTrue(monitor_service._MonitorService__check_service_status('google.com', 80, datetime.now()))

    def test_check_service_status_failure(self):
        monitor_service = MonitorService(5)
        self.assertFalse(monitor_service._MonitorService__check_service_status('127.0.0.1', 8080, datetime.now()))


if __name__ == '__main__':
    unittest.main()
