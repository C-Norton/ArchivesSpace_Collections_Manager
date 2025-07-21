import logging
import weakref
from typing import Dict, List, Callable, Any
from threading import Lock


class EventDispatcher:
    """
    Central event dispatcher for managing event subscriptions and notifications.

    PSEUDOCODE:
    CLASS EventDispatcher:
        PROPERTIES:
            event_handlers: dict[string, list[function]]
            weak_references: dict[string, list[weakref]]
            lock: threading.Lock

        CONSTRUCTOR():
            SET event_handlers = empty dict
            SET weak_references = empty dict
            SET lock = new Lock()

        METHOD subscribe(event_type: string, handler: function, use_weak_ref: boolean = true) -> void:
            LOCK operation:
                IF event_type not in event_handlers:
                    CREATE empty list for event_type
                IF use_weak_ref:
                    ADD weak reference to handler
                ELSE:
                    ADD direct reference to handler

        METHOD unsubscribe(event_type: string, handler: function) -> void:
            LOCK operation:
                REMOVE handler from event_handlers[event_type]

        METHOD dispatch(event_type: string, event_data: any) -> void:
            LOCK operation:
                CLEAN up dead weak references
                FOR each handler in event_handlers[event_type]:
                    TRY:
                        CALL handler(event_data)
                    CATCH exception:
                        LOG error and continue
    """

    def __init__(self):
        """Initialize the event dispatcher"""
        self.event_handlers: Dict[str, List[Callable]] = {}
        self.weak_references: Dict[str, List[weakref.ref]] = {}
        self.lock = Lock()
        logging.debug("EventDispatcher initialized")

    def subscribe(
        self, event_type: str, handler: Callable[[Any], None], use_weak_ref: bool = True
    ) -> None:
        """
        Subscribe to an event type with a handler function.

        Args:
            event_type: Type of event to subscribe to
            handler: Function to call when event occurs
            use_weak_ref: Whether to use weak references (prevents memory leaks)
        """
        with self.lock:
            if event_type not in self.event_handlers:
                self.event_handlers[event_type] = []
                self.weak_references[event_type] = []

            if use_weak_ref:
                # Use weak reference to prevent memory leaks
                weak_handler = weakref.ref(handler)
                self.weak_references[event_type].append(weak_handler)
            else:
                # Use strong reference (for global functions, etc.)
                self.event_handlers[event_type].append(handler)

            logging.debug(f"Subscribed to event: {event_type}")

    def unsubscribe(self, event_type: str, handler: Callable[[Any], None]) -> None:
        """
        Unsubscribe from an event type.

        Args:
            event_type: Type of event to unsubscribe from
            handler: Handler function to remove
        """
        with self.lock:
            if event_type not in self.event_handlers:
                return

            # Remove from strong references
            if handler in self.event_handlers[event_type]:
                self.event_handlers[event_type].remove(handler)

            # Remove from weak references
            self.weak_references[event_type] = [
                ref
                for ref in self.weak_references[event_type]
                if ref() is not None and ref() != handler
            ]

            logging.debug(f"Unsubscribed from event: {event_type}")

    def dispatch(self, event_type: str, event_data: Any) -> None:
        """
        Dispatch an event to all subscribed handlers.

        Args:
            event_type: Type of event to dispatch
            event_data: Data to pass to handlers
        """
        with self.lock:
            if event_type not in self.event_handlers:
                logging.debug(f"No handlers for event type: {event_type}")
                return

            # Clean up dead weak references and collect live handlers
            live_handlers = []
            live_weak_refs = []

            for ref in self.weak_references[event_type]:
                handler = ref()
                if handler is not None:
                    live_handlers.append(handler)
                    live_weak_refs.append(ref)

            # Update weak references list
            self.weak_references[event_type] = live_weak_refs

            # Add strong references
            live_handlers.extend(self.event_handlers[event_type])

            logging.debug(
                f"Dispatching event {event_type} to {len(live_handlers)} handlers"
            )

        # Dispatch outside of lock to prevent deadlocks
        for handler in live_handlers:
            try:
                handler(event_data)
            except Exception as e:
                logging.error(f"Error in event handler for {event_type}: {e}")

    def get_handler_count(self, event_type: str) -> int:
        """
        Get the number of handlers subscribed to an event type.

        Args:
            event_type: Event type to check

        Returns:
            Number of active handlers
        """
        with self.lock:
            if event_type not in self.event_handlers:
                return 0

            # Count live weak references
            live_weak_count = sum(
                1 for ref in self.weak_references[event_type] if ref() is not None
            )

            # Count strong references
            strong_count = len(self.event_handlers[event_type])

            return live_weak_count + strong_count

    def clear_all_handlers(self) -> None:
        """Clear all event handlers"""
        with self.lock:
            self.event_handlers.clear()
            self.weak_references.clear()
            logging.debug("Cleared all event handlers")
