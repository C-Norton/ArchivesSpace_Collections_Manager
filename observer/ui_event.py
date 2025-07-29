from enum import Enum

class UiEvent(Enum):
    CONNECTION_CHANGED = "connection_changed"
    REPOSITORY_LOADED = "repository_loaded"
    QUERY_UPDATED = "query_updated"
    NOTE_CREATED = "note_created"
    ACTION_SELECTED = "action_selected"