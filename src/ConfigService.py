import logging
from threading import Lock
from datetime import datetime, timedelta

from src.models.Caller import Caller
from src.models.Service import Service


class ConfigService:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

    def __init__(self, grace_time):
        self.grace_time = timedelta(seconds=grace_time)
        self.lock = Lock()
        self.services = {}
        self.callers = {}
        logging.info(f"ConfigService initialized with grace time: {self.grace_time.total_seconds()} seconds")

    def register_service(self, host, port):
        with self.lock:
            if (host, port) not in self.services:
                service = Service(host, port)
                service.last_checked = datetime.now() - self.grace_time
                self.services[(host, port)] = service
                logging.info(f"Service registered: {host}:{port}")
            else:
                logging.warning(f"Service already registered: {host}:{port}")

    def unregister_service(self, host, port):
        with self.lock:
            if (host, port) in self.services:
                service = self.services[(host, port)]
                for subs in service.subscribers:
                    subs.remove_subscription((host, port))
                del self.services[(host, port)]
                logging.info(f"Service unregistered: {host}:{port}")
            else:
                logging.warning(f"Attempted to unregister non-existing service: {host}:{port}")

    def set_outage_time(self, host, port, start: datetime, end: datetime):
        with self.lock:
            if (host, port) in self.services:
                service = self.services[(host, port)]
                service.outage_start = start
                service.outage_end = end
                logging.info(f"Outage time set for service {host}:{port} from {start.strftime(ConfigService.DATE_FORMAT)} to {end.strftime(ConfigService.DATE_FORMAT)}")
            else:
                logging.warning(f"Attempted to set outage time for non-existing service: {host}:{port}")

    def register_caller(self, name, callerId):
        with self.lock:
            if callerId not in self.callers:
                caller = Caller(name, callerId)
                self.callers[callerId] = caller
                logging.info(f"Caller registered: {name} with ID {callerId}")
            else:
                logging.warning(f"Caller already registered with ID {callerId}")

    def unregister_caller(self, callerId):
        with self.lock:
            if callerId in self.callers:
                caller = self.callers[callerId]
                for host, port in caller.subscribed.keys():
                    service = self.services[(host, port)]
                    service.remove_subscriber(callerId)
                del self.callers[callerId]
                logging.info(f"Caller unregistered with ID {callerId}")
            else:
                logging.warning(f"Attempted to unregister non-existing caller with ID {callerId}")

    def subscribe_service(self, host, port, callerId, polling_frequency):
        polling_frequency = timedelta(seconds=polling_frequency)
        with self.lock:
            if (host, port) in self.services and callerId in self.callers:
                caller = self.callers[callerId]
                service = self.services[(host, port)]

                caller.add_subscription(host, port, max(polling_frequency, self.grace_time))
                service.add_subscriber(callerId)
                logging.info(f"Caller {callerId} subscribed to service {host}:{port}")
                return True
            else:
                logging.warning(f"Subscription attempt failed for caller {callerId} to service {host}:{port}")
                return False

    def unsubscribe_service(self, host, port, callerId):
        with self.lock:
            if (host, port) in self.services and callerId in self.callers:
                caller = self.callers[callerId]
                service = self.services[(host, port)]

                caller.remove_subscription(host, port)
                service.remove_subscriber(callerId)
                logging.info(f"Caller {callerId} unsubscribed from service {host}:{port}")
            else:
                logging.warning(f"Unsubscription attempt failed for caller {callerId} to service {host}:{port}")
