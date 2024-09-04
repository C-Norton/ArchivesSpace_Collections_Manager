from enum import Enum


class LocalAccessRestrictionType(Enum):
    Donor = 1
    Repository = 2
    Fragile = 3
    In_Process = 4
    Others = 5
