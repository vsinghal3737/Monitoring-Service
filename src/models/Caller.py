from datetime import datetime, timedelta


class Caller:
    def __init__(self, name, callerId):
        self._name = name
        self._callerId = callerId
        self._subscribed = {}
        # key: (host, port),
            # value: {
                # polling_frequency: deltatime,
                # last_checked: datetime,
                # status: bool
        # }

    # Getter for name
    @property
    def name(self):
        return self._name

    # Setter for name
    @name.setter
    def name(self, value):
        self._name = value

    # Getter for callerId
    @property
    def callerId(self):
        return self._callerId

    # Setter for callerId
    @callerId.setter
    def callerId(self, value):
        self._callerId = value

    # Getter for subscribed
    @property
    def subscribed(self):
        return self._subscribed

    # Method to add or update subscription
    def add_subscription(self, host, port, polling_frequency):
        last_checked = datetime.now() - timedelta(minutes=10)
        self._subscribed[(host, port)] = {
            'polling_frequency': polling_frequency,
            'last_checked': last_checked,
            'last_status': False
        }

    # Method to remove subscription
    def remove_subscription(self, host, port):
        if (host, port) in self._subscribed:
            del self._subscribed[(host, port)]
