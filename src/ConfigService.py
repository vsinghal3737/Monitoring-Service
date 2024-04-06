from threading import Lock
from datetime import datetime, timedelta

from models.Caller import Caller
from models.Service import Service


class ConfigService:

    def __init__(self, grace_time):
        self.grace_time = timedelta(seconds=grace_time)
        self.lock = Lock()
        self.services = {}
        self.callers = {}

    def register_service(self, host, port):
        with self.lock:
            if (host, port) not in self.services:
                service = Service(host, port)
                service.last_checked = datetime.now() - self.grace_time
                self.services[(host, port)] = service

    def unregister_service(self, host, port):
        with self.lock:
            if (host, port) in self.services:
                service = self.services[(host, port)]
                for subs in service.subscribers:
                    subs.remove_subscription((host, port))

                del self.services[(host, port)]

    def set_outage_time(self, host, port, start: datetime, end: datetime):
        with self.lock:
            if (host, port) in self.services:
                service = self.services[(host, port)]
                service.outage_start = start
                service.outage_end = end

    def register_caller(self, name, callerId):
        with self.lock:
            if callerId not in self.callers:
                caller = Caller(name, callerId)
                self.callers[callerId] = caller

    def unregister_caller(self, callerId):
        with self.lock:
            if callerId in self.callers:
                caller = self.callers[callerId]
                for host, port in caller.subscribed.keys():
                    service = self.services[(host, port)]
                    service.remove_subscriber(callerId)
                del self.callers[callerId]

    def subscribe_service(self, host, port, callerId, polling_frequency):
        polling_frequency = timedelta(seconds=polling_frequency)
        with self.lock:
            if (host, port) in self.services and callerId in self.callers:
                caller = self.callers[callerId]
                service = self.services[(host, port)]

                caller.add_subscription(host, port, max(polling_frequency, self.grace_time))
                service.add_subscriber(callerId)
                return True

    def unsubscribe_service(self, host, port, callerId):
        with self.lock:
            if (host, port) in self.services and callerId in self.callers:
                caller = self.callers[callerId]
                service = self.services[(host, port)]

                caller.remove_subscription(host, port)
                service.remove_subscriber(callerId)
