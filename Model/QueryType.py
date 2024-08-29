from enum import Enum


class QueryType(Enum):
    Equals = 1
    Not_Equals = 2
    Empty = 3
    Not_Empty = 4
    Starts_With = 5
    Not_Starts_With = 6
    Ends_With = 7
    Not_Ends_With = 8
    Contains = 9
    Not_Contains = 10
