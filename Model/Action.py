from dataclasses import dataclass

from Model.ActionType import ActionType
from Model.Note import Note


@dataclass
class Action:
    def __init__(self,action_type : ActionType):
        self.action_type = action_type
        self.note = None
        self.note_type = None

    def add_note(self, note : Note):
        self.note = note
    def add_note_type(self, note : Note):
        self.note = note