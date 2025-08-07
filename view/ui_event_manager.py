from typing import Dict, Any

from observer.subject import SubjectMixin
from observer.ui_event import UiEvent


class UiEventManager(SubjectMixin):
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            super().__init__()
            self._initialized = True

    def publish_event(self, event: UiEvent, data: Dict[str, Any] = None):
        """Publish an event to all observers"""
        self.notify(event, data)