from enum import Enum


class LocalAccessRestrictionType(Enum):
    """This enum is used to model out the archivesspace resource repository data type"""

    Donor = 1
    Repository = 2
    Fragile = 3
    In_Process = 4
    Others = 5
