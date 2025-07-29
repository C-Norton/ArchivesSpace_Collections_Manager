from typing import Dict, Any

from observer.subject import Subject
from observer.ui_event import UiEvent


class UiEventManager(Subject):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__init__()
        return cls._instance

    def publish_event(self, event: UiEvent, data: Dict[str, Any] = None):
        """Publish an event to all observers"""
        self.notify(event, data)