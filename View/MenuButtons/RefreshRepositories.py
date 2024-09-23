from Controller.Connection import Connection
from View.MenuButtons import TestConnection
from Controller.RequestType import RequestType


def refresh_repositories(connection):
    if Connection.test(connection):
        Repositories = Connection.query(http_request_type=RequestType.GET, endpoint="repositories")
    else:
        TestConnection.TestConnection(connection)
        return False
