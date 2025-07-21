"""
Mediator pattern implementation for the ArchivesSpace Collections Manager.

The mediator pattern allows components to communicate without direct dependencies,
reducing coupling and improving maintainability.
"""

from .ApplicationMediator import ApplicationMediator
from .EventDispatcher import EventDispatcher

__all__ = ["ApplicationMediator", "EventDispatcher"]
