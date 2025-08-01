from typing import Protocol, Any, runtime_checkable, List, Dict
from .observer import Observer
from .ui_event import UiEvent


@runtime_checkable
class Subject(Protocol):
    """
    Protocol defining the interface for subjects in the Observer pattern.

    Any class that implements these methods is considered a Subject,
    regardless of inheritance hierarchy.
    """

    def attach(self, observer: Observer) -> None:
        """Add an observer to the notification list."""
        ...

    def detach(self, observer: Observer) -> None:
        """Remove an observer from the notification list."""
        ...

    def notify(self, event: UiEvent, data: Any = None) -> None:
        """Notify all observers of a change."""
        ...


class SubjectMixin:
    """Mixin class that provides Subject protocol implementation"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._observers: List[Observer] = []

    def attach(self, observer: Observer) -> None:
        """Attach an observer to the subject"""
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        """Detach an observer from the subject"""
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self, event: UiEvent, data: Dict[str, Any] = None) -> None:
        """Notify all observers about an event"""
        if data is None:
            data = {}
        for observer in self._observers:
            observer.update(event, data)
