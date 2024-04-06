import threading
import signal
from src.MonitorService import MonitorService
from src.DummyServices.DummyServicesCreationAndDeletion import PORTS, DummyServiceMain

shutdown_event = threading.Event()


def start_dummy_services():
    # Start DummyServices and pass the shutdown event
    services = DummyServiceMain(shutdown_event)
    return services


def setup_monitor_service():
    # Initialize MonitorService
    return MonitorService(5, shutdown_event)


def setup_config_service(monitor_service):
    # Register services
    for port in PORTS:
        monitor_service.register_service("localhost", port)

    # Register callers
    monitor_service.register_caller("Caller 1", "caller1")
    monitor_service.register_caller("Caller 2", "caller2")

    # Subscribe callers to services with specified polling frequencies
    monitor_service.subscribe_service("localhost", PORTS[0], "caller1", polling_frequency=3)
    monitor_service.subscribe_service("localhost", PORTS[1], "caller1", polling_frequency=10)
    monitor_service.subscribe_service("localhost", PORTS[1], "caller2", polling_frequency=10)
    monitor_service.subscribe_service("localhost", PORTS[2], "caller2", polling_frequency=10)


def shutdown_handler(signum, frame):
    # Set the shutdown event when a signal is received (e.g., SIGINT for KeyboardInterrupt)
    shutdown_event.set()


def main():
    signal.signal(signal.SIGINT, shutdown_handler)
    dummy_service_thread = threading.Thread(target=start_dummy_services)
    dummy_service_thread.start()

    monitor_service = setup_monitor_service()

    setup_config_service(monitor_service)

    # Wait for the threads to complete upon shutdown signal
    dummy_service_thread.join()
    monitor_service.join()  # Make sure to have a join method in MonitorService


if __name__ == "__main__":
    main()
