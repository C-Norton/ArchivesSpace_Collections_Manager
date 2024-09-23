import asnake.client.web_client

from dataclasses import dataclass

import asnake.client.web_client
import requests.exceptions
from asnake.client import ASnakeClient
from requests.exceptions import MissingSchema, ConnectionError

from Controller.RequestType import RequestType


@dataclass
class Connection:
    """
    A Connection is a small class used to pass around connection information to an archivesspace server, as well as the
    API object it creates. It provides its own methods for validation. It is the only class that should be interacting
    with the API directly.

    TODO: Add a mechanism for representing server timeout, and force revalidation if a connection has not been used
    Within 300 seconds.

    TODO: Complete Query for different types

    TODO: Add a ratelimit to avoid overloading the archivesspace server and getting API errors. Make it dynamic (opt)
    """
    def __init__(self, s, u, p):
        self.server = s
        self.username = u
        self.password = p
        self.client = None
        self.validated = False

    def create_session(self) -> bool:
        """
        Create session starts a server session using this connection. This is not necessary to call from outside this
        class, but it won't hurt anything
        :return: True if the connection was created successfully, False otherwise
        """
        self.client = ASnakeClient(
            baseurl=self.server, username=self.username, password=self.password
        )
        try:
            self.client.authorize()
        except requests.exceptions.MissingSchema:
            return False
        return True

    def __str__(self):
        return self.server + self.username + self.password

    def test(self):
        """
        Test Validates if a connection's info is ok.
        :return: true if the connection is valid, false otherwise
        """
        if self.server == "" or self.username == "" or self.password == "":
            return False, "Missing Server Configuration"
        try:
            self.client = self.create_session()
        except asnake.client.web_client.ASnakeAuthError as e:
            return False, "Bad Username or Password"
        except MissingSchema:
            return (
                False,
                "Bad URL Structure. Ensure your URL has https:// at the beginning",
            )
        except ConnectionError:
            return (
                False,
                "Could not connect to server. Ensure your URL is correct, and that your IP is whitelisted "
                "for the API",
            )
        except BaseException as e:
            return False, e, e.__traceback__
        return True, "Your connection is working"

    def query(self, http_request_type, endpoint: str):
        """
        Actually makes a query of the archives_space server
        :param http_request_type: does what it says on the tin
        :param endpoint: it's not this classes job to tell you what to query, go talk to query
        :return:
        """
        if not self.validated:
            self.validated = self.create_session()
        match http_request_type:
            case RequestType.GET:
                return self.client.get(endpoint)

            case _:
                pass
