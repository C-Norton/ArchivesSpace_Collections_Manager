from enum import Enum

class RequestType(Enum):
    GET=0
    HEAD=1
    POST=2
    PUT=3
    DELETE=4
    CONNECTION=5
    OPTIONS=6
    TRACE=7
    PATCH=8
