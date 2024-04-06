import logging
import socket

from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta
from threading import Thread, Event
from time import sleep

from src.ConfigService import ConfigService

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class MonitorService(ConfigService):
    DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

    def __init__(self, grace_time=10, shutdown_event=None):
        super().__init__(grace_time)
        self.logs = defaultdict(list)
        self.shutdown_event = shutdown_event or Event()
        self.check_thread = Thread(target=self.check_services, daemon=True)
        self.check_thread.start()
        logging.info("MonitorService initialized and monitoring thread started.")

    def check_services(self):
        while True:
            if len(self.services) != 0:

                with ThreadPoolExecutor(max_workers=len(self.services)) as executor:

                    future_to_service = {}
                    for (host, port) in self.services.keys():
                        service = self.services[(host, port)]
                        time_now = datetime.now()
                        if self.should_check_status(service, time_now):
                            future_to_service[executor.submit(self.__check_service_status, host, port, time_now)] = (host, port)

                    for future in as_completed(future_to_service):
                        host, port = future_to_service[future]
                        try:
                            status = future.result()
                            with self.lock:
                                service = self.services[(host, port)]
                                service.is_up = status
                                self.__notify_subscribers(service)

                        except Exception as exc:
                            logging.error(f'{host}:{port} generated an exception: {exc}')

            sleep(1)

    def __check_service_status(self, host, port, time_now):
        status = False
        while not status and datetime.now() - time_now < self.grace_time:
            try:
                with socket.create_connection((host, port), timeout=2):
                    status = True
            except socket.error:
                status = False
            except Exception as e:
                status = False
                logging.error(f"__check_service_status() - ERROR: {e}")
                break
        return status

    def __notify_subscribers(self, service):
        log_message = f"Service {service.host}:{service.port} is {'up' if service.is_up else 'down'}"
        logging.debug(log_message)

        for callerId in service.subscribers:
            time_now = datetime.now()
            caller = self.callers[callerId]

            polling_frequency = caller.subscribed[(service.host, service.port)]['polling_frequency']
            last_checked = caller.subscribed[(service.host, service.port)]['last_checked']

            if last_checked + polling_frequency <= time_now:
                caller.subscribed[(service.host, service.port)]['last_checked'] = time_now
                caller.subscribed[(service.host, service.port)]['status'] = service.is_up
                logging.info(f"Notifying {caller.name} about service status change: {log_message}")
                self.logs[caller.callerId].append(log_message)

    @staticmethod
    def should_check_status(service, time_now):
        return service.last_checked + timedelta(seconds=1) <= time_now and \
               not (service.outage_start and service.outage_end and (service.outage_start <= time_now <= service.outage_end))
