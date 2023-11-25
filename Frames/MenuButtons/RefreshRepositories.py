from Connection import Connection
from Frames.MenuButtons import TestConnection
from RequestType import RequestType

def RefreshRepositories(connection):
    if Connection.test(connection):
        Repositories = Connection.Query(type=RequestType.GET,endpoint="repositories")
    else:
        TestConnection.TestConnection(connection)
        return False
