from Controller.Connection import Connection
from View.MenuButtons import TestConnection
from Controller.HttpRequestType import HttpRequestType


def refresh_repositories(connection):
    if Connection.test(connection):
        repositories = Connection.query(
            http_request_type=HttpRequestType.GET, endpoint="repositories"
        )
    else:
        TestConnection.TestConnection(connection)
        return False
