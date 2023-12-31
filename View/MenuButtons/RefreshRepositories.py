from Controller.Connection import Connection
from View.MenuButtons import TestConnection
from Controller.RequestType import RequestType


def RefreshRepositories(connection):
    if Connection.test(connection):
        Repositories = Connection.Query(type=RequestType.GET, endpoint="repositories")
    else:
        TestConnection.TestConnection(connection)
        return False
