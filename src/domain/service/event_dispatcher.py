class EventDispatcher:
    def __init__(self):
        self._listeners = []

    def add_listener(self, listener):
        """Register a new listener."""
        self._listeners.append(listener)

    def remove_listener(self, listener):
        """Unregister an existing listener."""
        if listener in self._listeners:
            self._listeners.remove(listener)

    def trigger_event(self, event_data=None):
        """Fire the event, passing event_data to every listener."""
        for listener in self._listeners:
            listener(event_data)

