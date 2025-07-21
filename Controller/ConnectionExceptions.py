class ConnectionException(Exception):
    pass


class ConfigurationError(ConnectionException):
    """Missing or invalid configuration"""

    pass


class NetworkError(ConnectionException):
    """Network error"""

    pass


class ServerError(ConnectionException):
    """Server error"""

    pass


class AuthenticationError(ConnectionException):
    """Authentication error"""

    pass
