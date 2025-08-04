from enum import Enum


class UiEvent(Enum):
    """
    Enumeration for UI events.

    This class represents various user interface (UI) events that can occur in the
    application. It is used to standardize and handle specific UI-related actions or
    changes, allowing consistent interaction and processing of these events throughout
    the system.
    """
    REPOSITORY_SELECTION_CHANGED = "repository_selection_changed"
    CONNECTION_CHANGED = "connection_changed"
    REPOSITORIES_LOADED = "repositories_loaded"
    QUERY_UPDATED = "query_updated"
    NOTE_CREATED = "note_created"
    ACTION_SELECTED = "action_selected"
