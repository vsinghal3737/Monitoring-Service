from datetime import datetime, timedelta


class Service:
    DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

    def __init__(self, host, port):
        self._host = host
        self._port = port
        self._last_checked = datetime.now() - timedelta(minutes=10)
        self._is_up = False
        self._outage_start = None
        self._outage_end = None
        self._subscribers = set()  # calledId

    # Getter for host
    @property
    def host(self):
        return self._host

    # Setter for host
    @host.setter
    def host(self, value):
        self._host = value

    # Getter for port
    @property
    def port(self):
        return self._port

    # Setter for port
    @port.setter
    def port(self, value):
        self._port = value

    # Getter for is_up
    @property
    def is_up(self):
        return self._is_up

    # Setter for is_up
    @is_up.setter
    def is_up(self, value):
        self._is_up = value

    # Getter for last_checked
    @property
    def last_checked(self):
        return self._last_checked

    # Setter for last_checked
    @last_checked.setter
    def last_checked(self, value):
        self._last_checked = value

    # Getter for outage_start
    @property
    def outage_start(self):
        return self._outage_start

    # Setter for outage_start
    @outage_start.setter
    def outage_start(self, value):
        self._outage_start = value

    # Getter for outage_end
    @property
    def outage_end(self):
        return self._outage_end

    # Setter for outage_end
    @outage_end.setter
    def outage_end(self, value):
        self._outage_end = value

    # Getter for subscribers
    @property
    def subscribers(self):
        return self._subscribers

    # Method to get a single subscriber if exists
    def get_subscriber(self, subscriber):
        if subscriber in self._subscribers:
            return subscriber

    # Method to add a single subscriber
    def add_subscriber(self, subscriber):
        self._subscribers.add(subscriber)

    # Method to remove a single subscriber
    def remove_subscriber(self, subscriber):
        if subscriber in self._subscribers:
            self._subscribers.remove(subscriber)

    def __repr__(self):
        outage_info = f"Outage from {self._outage_start.strftime(Service.DATE_FORMAT)} to {self._outage_end.strftime(Service.DATE_FORMAT)}" if self._outage_start and self._outage_end else "No outage recorded"
        subscribers_repr = ', '.join([str(subscriber) for subscriber in self._subscribers]) or "No subscribers"
        return (
            f"Service(host={self._host!r}, port={self._port}, is_up={self._is_up}, "
            f"last_checked={self._last_checked.strftime(Service.DATE_FORMAT)}, {outage_info}, subscribers=[{subscribers_repr}])"
        )