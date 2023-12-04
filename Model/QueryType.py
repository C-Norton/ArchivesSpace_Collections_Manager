from enum import Enum

class QueryType(Enum):
    EQUALS = 1
    NOTEQUALS = 2
    EMPTY = 3
    NOTEMPTY = 4
    STARTSWITH = 5
    NOTSTARTSWITH = 6
    ENDSWITH = 7
    NOTENDSWITH = 8
    CONTAINS = 9
    NOTCONTAINS = 10