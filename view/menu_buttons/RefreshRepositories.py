from controller.connection import Connection
from view.menu_buttons import TestConnection
from controller.HttpRequestType import HttpRequestType


def refresh_repositories(connection):
    """
    This method is used with an initally valid connection to get a set of repositories to return to the UI
    Notice this is just a method, and not a full class.
    :param connection: connection object (see Connection.py)
    :return:
    TODO: What if a user tries with no saved connection. Add logging and error handling
    """
    if connection.test_connection():
        repositories = Connection.query(
            http_request_type=HttpRequestType.GET, endpoint="repositories"
        )

    else:
        TestConnection.TestConnection(connection)
        return False
