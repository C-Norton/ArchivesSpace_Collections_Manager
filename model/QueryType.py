from enum import Enum

class QueryType(Enum):
    EQUALS = 1
    NOTEQUALS = 2
    EMPTY = 3
    NOTEMPTY = 4
    STARTSWITH = 5
    ENDSWITH = 6
    CONTAINS = 7
    NOTCONTAINS = 8