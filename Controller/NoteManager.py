from Model.Note import Note
from Model.NoteSubType import NoteSubType
from Model.NoteType import NoteType


def singleton(cls):
    """Decorator to implement singleton pattern."""
    instances = {}  # Dictionary to store instances

    def getinstance():
        """Inner function to get or create the singleton instance."""
        if cls not in instances:
            instances[cls] = cls()  # Create the instance if it doesn't exist
        return instances[cls]  # Return the existing or newly created instance

    return getinstance


@singleton  # Apply the singleton decorator to the NoteManager class
class NoteManager:
    """A class to manage notes (implemented as a singleton)."""

    def __init__(self):
        self.active_note = None

    def set_note(
        self,
        note_type: NoteType,
        note_value: str,
        publish: bool,
        label: str,
        persistent_id: str,
        has_subtype: bool,
        sub_type: NoteSubType,
    ):
        """A note is functionally a key-enforced dictionary"""
        self.active_note = Note(note_type)
        self.active_note.note["type"] = (NoteType, note_type)
        self.active_note.note["publish"] = (bool, publish)
        self.active_note.note["label"] = (str, label)
        self.active_note.note["content"] = (str, note_value)
        self.active_note.note["sub_type"] = (NoteSubType, sub_type)
        self.active_note.note["persistent_id"] = (str, persistent_id)

    def get_note(self):
        """does what it says on the tin"""
        return self.active_note
