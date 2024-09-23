from enum import Enum


class ActionType(Enum):
    """Action types are the types of things we can actually do to a matched record"""

    Log = 0  # just list the record in the userlog
    Delete_Record = 1
    Duplicate_Record = 2  # how do we resolve name collision?
    Delete_Note = 3  # of specific type, OR matching note. This is undecided, and may be split into different operations
    Create_Note = 4
    Replace_Note = 5
