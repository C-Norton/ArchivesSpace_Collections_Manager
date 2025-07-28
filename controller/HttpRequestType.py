from enum import Enum


class HttpRequestType(Enum):
    """
    Represents the different HTTP request types. Used by our API interaction code primarily.

    """

    GET = 0
    HEAD = 1
    POST = 2
    PUT = 3
    DELETE = 4
    CONNECTION = 5
    OPTIONS = 6
    TRACE = 7
    PATCH = 8
