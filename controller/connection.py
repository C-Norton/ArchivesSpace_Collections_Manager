import logging
import asnake.client.web_client

from dataclasses import dataclass

import requests.exceptions
from asnake.client import ASnakeClient
from time import sleep
from controller.connection_exceptions import (
    ConfigurationError,
    NetworkError,
    ServerError,
    AuthenticationError,
)
from controller.HttpRequestType import HttpRequestType


@dataclass
class Connection:
    """
    A Connection is a small class used to pass around connection information to an archivesspace server, as well as the
    API object it creates. It provides its own methods for validation. It is the only class that should be interacting
    with the API directly.
    TODO: add or fix connection.test
    TODO: Add a mechanism for representing server timeout, and force revalidation if a connection has not been used
    Within 300 seconds.

    TODO: Complete Query for different types

    TODO: Add a ratelimit to avoid overloading the archivesspace server and getting API errors. Make it dynamic (opt)

    TODO: Add logging to this file
    """

    def __init__(self, s: str, u: str, p: str):
        self.server: str = s
        self.username: str = u
        self.password: str = p
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
        except requests.exceptions.MissingSchema as e:
            logging.error(e)
            return False
        return True

    def __str__(self):
        return self.server + self.username + self.password

    def test_connection(self) -> None:
        """
        Test connection validity. Raises appropriate exception on failure.

        Raises:
            ConfigurationError: Missing server/username/password
            AuthenticationError: Invalid credentials
            NetworkError: Connection failed after retries
            ServerError: Server returned an error
        """
        # Validate configuration first
        if not all([self.server.strip(), self.username.strip(), self.password.strip()]):
            raise ConfigurationError("Connection configuration is incomplete")

        # Retry logic with exponential backoff
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                self.client = self.create_session()
                # Test that we actually got a working client
                self._verify_connection()
                return  # Success!

            except asnake.client.web_client.ASnakeAuthError as e:
                # Don't retry auth errors - they won't get better
                raise AuthenticationError("Invalid username or password") from e

            except (
                requests.exceptions.ConnectionError,
                requests.exceptions.Timeout,
            ) as e:
                if attempt == max_attempts - 1:  # Last attempt
                    raise NetworkError(
                        f"Connection failed after {max_attempts} attempts"
                    ) from e
                # Wait before retry (exponential backoff)
                sleep(2**attempt)

            except Exception as e:
                # Unexpected errors shouldn't be retried
                raise ServerError(f"Unexpected error: {e}") from e

    def _verify_connection(self) -> None:
        """Verify the client connection actually works"""
        if not self.client:
            raise NetworkError("Failed to create client session")

        # Actually test the connection with a simple API call
        try:
            self.client.get("version")
        except Exception as e:
            raise NetworkError("Connection test failed") from e

    def query(self, http_request_type: HttpRequestType, endpoint: str):
        """
        Actually makes a query of the archives_space server
        :param http_request_type: does what it says on the tin
        :param endpoint: it's not this classes job to tell you what to query, go talk to QueryManager
        :return: the result of the API Query

        todo: complete this for different HTTP request types, and automatically manage a 429 error (too many requests)
        """
        if not self.validated:
            self.validated = self.create_session()
        match http_request_type:
            case HttpRequestType.GET:
                return self.client.get(endpoint)

            case _:
                pass
