from enum import Enum


class ActionType(Enum):
    Log = 0
    Delete_Record = 1
    Duplicate_Record = 2
    Delete_Note = 3
    Create_Note = 4
    Replace_Note = 5
