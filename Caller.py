class Caller:
    def __init__(self, name, callerId):
        self._name = name
        self._callerId = callerId
        self._subscribed = {}  # key: (host, port), value: polling_frequency

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
    def add_subscription(self, host: str, port: int, polling_frequency):
        self._subscribed[(host, port)] = polling_frequency

    # Method to remove subscription
    def remove_subscription(self, host: str, port: int):
        if (host, port) in self._subscribed:
            del self._subscribed[(host, port)]
