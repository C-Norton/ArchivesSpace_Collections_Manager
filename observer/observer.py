from typing import Protocol, runtime_checkable, Dict, Any
from observer import ui_event


@runtime_checkable
class Observer(Protocol):
    def update(self, event: ui_event, data: Dict[str, Any]) -> None:
        """Handle the event with associated data"""
        ...
