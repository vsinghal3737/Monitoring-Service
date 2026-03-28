import unittest
from datetime import timedelta, datetime
from unittest.mock import patch

from src.ConfigService import ConfigService


class TestConfigService(unittest.TestCase):

    @patch('src.ConfigService.logging')  # Adjust the import path as necessary
    def test_initialization_values(self, mock_logging):
        grace_time_seconds = 60
        service = ConfigService(grace_time_seconds)

        self.assertEqual(service.grace_time, timedelta(seconds=grace_time_seconds),
                         "Grace time should be set correctly.")
        self.assertIsNotNone(service.lock, "Lock should be initialized.")
        self.assertDictEqual(service.services, {}, "Services should be initialized to an empty dictionary.")
        self.assertDictEqual(service.callers, {}, "Callers should be initialized to an empty dictionary.")

    @patch('src.ConfigService.logging')  # Adjust the import path as necessary
    def test_logging_output_on_initialization(self, mock_logging):
        grace_time_seconds = 60
        ConfigService(grace_time=grace_time_seconds)

        mock_logging.info.assert_called_with(
            f"ConfigService initialized with grace time: {timedelta(seconds=grace_time_seconds).total_seconds()} seconds")

    @patch('src.ConfigService.logging')
    def test_register_service_success(self, mock_logging):
        host = "127.0.0.1"
        port = 8080
        self.config_service = ConfigService(60)  # Recreate config_service for isolation
        self.config_service.register_service(host, port)
        self.assertIn((host, port), self.config_service.services, "Service should be registered.")
        mock_logging.info.assert_called_with(f"Service registered: {host}:{port}")

    @patch('src.ConfigService.logging')
    def test_register_service_duplicate(self, mock_logging):
        host = "127.0.0.1"
        port = 8080
        self.config_service = ConfigService(60)
        self.config_service.register_service(host, port)  # First registration
        mock_logging.reset_mock()  # Reset mock to only capture the next call
        self.config_service.register_service(host, port)  # Duplicate registration
        mock_logging.warning.assert_called_with(f"Service already registered: {host}:{port}")

    @patch('src.ConfigService.logging')
    def test_unregister_service_success(self, mock_logging):
        host = "127.0.0.1"
        port = 8080
        self.config_service = ConfigService(60)
        self.config_service.register_service(host, port)
        self.config_service.unregister_service(host, port)
        self.assertNotIn((host, port), self.config_service.services, "Service should be unregistered.")
        mock_logging.info.assert_called_with(f"Service unregistered: {host}:{port}")

    @patch('src.ConfigService.logging')
    def test_unregister_service_non_existing(self, mock_logging):
        host = "127.0.0.1"
        port = 8080
        self.config_service = ConfigService(60)
        self.config_service.unregister_service(host, port)  # Attempting to unregister a non-existing service
        mock_logging.warning.assert_called_with(f"Attempted to unregister non-existing service: {host}:{port}")

    @patch('src.ConfigService.logging')
    def test_set_outage_time_success(self, mock_logging):
        host = "127.0.0.1"
        port = 8080
        self.config_service = ConfigService(60)  # Instantiate for isolation
        # Pre-register service for testing
        self.config_service.register_service(host, port)

        start_time = datetime.now()
        end_time = start_time + timedelta(hours=1)

        self.config_service.set_outage_time(host, port, start_time, end_time)

        service = self.config_service.services[(host, port)]
        self.assertEqual(service.outage_start, start_time, "Outage start time should be set correctly.")
        self.assertEqual(service.outage_end, end_time, "Outage end time should be set correctly.")

        expected_log_message = f"Outage time set for service {host}:{port} from {start_time.strftime(ConfigService.DATE_FORMAT)} to {end_time.strftime(ConfigService.DATE_FORMAT)}"
        mock_logging.info.assert_called_with(expected_log_message)

    @patch('src.ConfigService.logging')
    def test_set_outage_time_non_existing_service(self, mock_logging):
        host = "127.0.0.1"
        port = 8080
        self.config_service = ConfigService(60)  # Instantiate for isolation

        start_time = datetime.now()
        end_time = start_time + timedelta(hours=1)

        self.config_service.set_outage_time(host, port, start_time, end_time)

        mock_logging.warning.assert_called_with(f"Attempted to set outage time for non-existing service: {host}:{port}")

    @patch('src.ConfigService.logging')
    def test_register_caller_success(self, mock_logging):
        name = "John Doe"
        callerId = "123"
        self.config_service = ConfigService(60)

        self.config_service.register_caller(name, callerId)

        self.assertIn(callerId, self.config_service.callers, "Caller should be registered.")
        mock_logging.info.assert_called_with(f"Caller registered: {name} with ID {callerId}")

    @patch('src.ConfigService.logging')
    def test_register_caller_duplicate(self, mock_logging):
        name = "John Doe"
        callerId = "123"
        self.config_service = ConfigService(60)
        self.config_service.register_caller(name, callerId)  # First registration
        mock_logging.reset_mock()  # Reset mock to only capture the next call
        self.config_service.register_caller(name, callerId)  # Attempt duplicate registration

        mock_logging.warning.assert_called_with(f"Caller already registered with ID {callerId}")

    @patch('src.ConfigService.logging')
    def test_unregister_caller_success(self, mock_logging):
        name = "John Doe"
        callerId = "123"
        self.config_service = ConfigService(60)
        self.config_service.register_caller(name, callerId)
        self.config_service.unregister_caller(callerId)

        self.assertNotIn(callerId, self.config_service.callers, "Caller should be unregistered.")
        mock_logging.info.assert_called_with(f"Caller unregistered with ID {callerId}")

    @patch('src.ConfigService.logging')
    def test_unregister_caller_non_existing(self, mock_logging):
        callerId = "123"
        self.config_service = ConfigService(60)
        self.config_service.unregister_caller(callerId)  # Attempt to unregister non-existing caller

        mock_logging.warning.assert_called_with(f"Attempted to unregister non-existing caller with ID {callerId}")

    @patch('src.ConfigService.logging')
    def test_subscribe_service_success(self, mock_logging):
        self.config_service = ConfigService(60)  # Assuming grace_time is 60 seconds for initialization
        host, port, callerId, polling_frequency = "127.0.0.1", 8080, "caller123", 30
        # Setup - register service and caller
        self.config_service.register_service(host, port)
        self.config_service.register_caller("John Doe", callerId)

        result = self.config_service.subscribe_service(host, port, callerId, polling_frequency)

        self.assertTrue(result, "Subscription should be successful.")
        self.assertIn(callerId, self.config_service.services[(host, port)].subscribers,
                      "Caller should be added to service's subscribers.")
        mock_logging.info.assert_called_with(f"Caller {callerId} subscribed to service {host}:{port}")

    @patch('src.ConfigService.logging')
    def test_subscribe_service_failure(self, mock_logging):
        self.config_service = ConfigService(60)
        host, port, callerId, polling_frequency = "127.0.0.1", 8080, "caller123", 30
        # No service or caller registration here

        result = self.config_service.subscribe_service(host, port, callerId, polling_frequency)

        self.assertFalse(result, "Subscription should fail for non-existing service or caller.")
        mock_logging.warning.assert_called_with(
            f"Subscription attempt failed for caller {callerId} to service {host}:{port}")

    @patch('src.ConfigService.logging')
    def test_unsubscribe_service_success(self, mock_logging):
        self.config_service = ConfigService(60)
        host, port, callerId = "127.0.0.1", 8080, "caller123"
        # Setup - register service and caller, then subscribe
        self.config_service.register_service(host, port)
        self.config_service.register_caller("John Doe", callerId)
        self.config_service.subscribe_service(host, port, callerId, 30)

        self.config_service.unsubscribe_service(host, port, callerId)

        self.assertNotIn(callerId, self.config_service.services[(host, port)].subscribers,
                         "Caller should be removed from service's subscribers.")
        mock_logging.info.assert_called_with(f"Caller {callerId} unsubscribed from service {host}:{port}")

    @patch('src.ConfigService.logging')
    def test_unsubscribe_service_failure(self, mock_logging):
        self.config_service = ConfigService(60)
        host, port, callerId = "127.0.0.1", 8080, "caller123"
        # No service or caller registration and subscription

        self.config_service.unsubscribe_service(host, port, callerId)

        mock_logging.warning.assert_called_with(
            f"Unsubscription attempt failed for caller {callerId} to service {host}:{port}")


if __name__ == '__main__':
    unittest.main()
