import logging
import asnake.client.web_client

import requests.exceptions
from asnake.client import ASnakeClient
import time
from controller.connection_exceptions import (
    ConfigurationError,
    NetworkError,
    ServerError,
    AuthenticationError,
)
from controller.HttpRequestType import HttpRequestType



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


    def create_session(self) -> ASnakeClient:
        """
        Create and return an authenticated ASnake client session.

        Returns:
            ASnakeClient: Authenticated client ready for API calls

        Raises:
            ConfigurationError: Invalid server URL or missing configuration
            AuthenticationError: Invalid credentials
            NetworkError: Network connectivity issues
            ServerError: Server-side errors or unexpected issues
        """
        logging.debug(f"Creating session for {self.username}@{self.server}")

        try:
            # Create the client
            client = ASnakeClient(
                baseurl=self.server, username=self.username, password=self.password
            )

            # Attempt authorization
            logging.debug("Attempting authorization...")
            client.authorize()
            logging.debug("Authorization successful")

            # Store the client and mark as validated
            self.client = client
            self.validated = True

            return client

        except requests.exceptions.MissingSchema as e:
            logging.error(f"Invalid server URL format: {e}")
            raise ConfigurationError(f"Invalid server URL: {self.server}") from e

        except requests.exceptions.InvalidURL as e:
            logging.error(f"Malformed server URL: {e}")
            raise ConfigurationError(f"Malformed server URL: {self.server}") from e

        except asnake.client.web_client.ASnakeAuthError as e:
            logging.error(f"Authentication failed: {e}")
            raise AuthenticationError("Invalid username or password") from e

        except (
            requests.exceptions.ConnectionError,
            requests.exceptions.ConnectTimeout,
            requests.exceptions.ReadTimeout,
            requests.exceptions.Timeout,
        ) as e:
            logging.error(f"Network error: {e}")
            raise NetworkError(f"Connection to server failed after 3 attempts: {e}") from e

        except requests.exceptions.HTTPError as e:
            logging.error(f"HTTP error: {e}")
            if hasattr(e.response, "status_code"):
                if 400 <= e.response.status_code < 500:
                    raise AuthenticationError(f"Client error: {e}") from e
                else:
                    raise ServerError(f"Server error: {e}") from e
            else:
                raise ServerError(f"HTTP error: {e}") from e

        except Exception as e:
            logging.error(f"Unexpected error during session creation: {e}")
            raise ServerError(f"Unexpected error: {e}") from e

    def __str__(self):
        return self.server + self.username + self.password

    def test_connection(self) -> None:
        """
        Test connection validity with automatic retry for network errors.
        Raises appropriate exception on failure.
        """
        self._validate_connection_config()

        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                self.client = self.create_session()
                self._verify_connection()
                return  # Success!

            except (ConfigurationError, AuthenticationError):
                # These errors won't improve with retries
                raise

            except Exception as e:
                self._handle_connection_error(e, attempt, max_attempts)

    def _validate_connection_config(self) -> None:
        """Validate that required connection configuration is present."""
        if not all([self.server.strip(), self.username.strip(), self.password.strip()]):
            raise ConfigurationError("Connection configuration is incomplete")

    def _handle_connection_error(
        self, error: Exception, attempt: int, max_attempts: int
    ) -> None:
        """
        Handle connection errors with appropriate retry logic.

        Args:
            error: The exception that occurred
            attempt: Current attempt number (0-based)
            max_attempts: Total number of attempts allowed
        """
        logging.debug(f"_handle_connection_error called with: {type(error)}, attempt={attempt}")
        is_final_attempt = attempt == max_attempts - 1
        logging.debug(f"is_final_attempt: {is_final_attempt}")

        # Network errors that should be retried
        retryable_network_errors = (
            requests.exceptions.ConnectionError,
            requests.exceptions.Timeout,
            requests.exceptions.ConnectTimeout,
            requests.exceptions.ReadTimeout,
            requests.exceptions.HTTPError,
            OSError,
            ConnectionRefusedError,
            ConnectionResetError,
            NetworkError,
        )

        # Configuration errors that should not be retried
        config_errors = (
            requests.exceptions.TooManyRedirects,
            requests.exceptions.URLRequired,
            requests.exceptions.InvalidURL,
            requests.exceptions.MissingSchema,
            requests.exceptions.RequestException,  # Base class for other config issues
        )

        # Handle configuration errors (no retry)
        if isinstance(error, config_errors):
            raise ConfigurationError(
                f"Invalid server configuration: {error}"
            ) from error

        # Handle retryable network errors
        if isinstance(error, retryable_network_errors):
            logging.debug(f"Error is retryable network error")
            if is_final_attempt:
                logging.debug(f"Final attempt, re-raising")
                if isinstance(error, NetworkError):
                    raise  # Re-raise original NetworkError
                else:
                    raise NetworkError(
                        f"Connection failed after {max_attempts} attempts"
                    ) from error
            else:
                # Wait before retry with exponential backoff
                logging.debug(f"Not final attempt, sleeping {2**attempt} seconds")
                time.sleep(2**attempt)
                return

        # Handle unexpected errors
        raise ServerError(f"Unexpected error: {error}") from error

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
            raise AuthenticationError("Connection not validated")
        match http_request_type:
            case HttpRequestType.GET:
                return self.client.get(endpoint)

            case _:
                pass
