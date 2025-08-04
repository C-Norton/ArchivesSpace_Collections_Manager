import json
import logging
from json import JSONDecodeError
from typing import Optional

from controller.HttpRequestType import HttpRequestType
from observer.subject import SubjectMixin
from observer.ui_event import UiEvent
from view.ui_event_manager import UiEventManager
from .connection import Connection
from .connection_exceptions import NetworkError, ServerError


class ConnectionManager(SubjectMixin):
    def __init__(self, main):
        super().__init__()  # Initialize the mixin
        self.main = main
        self.connection: Optional[Connection] = None
        self.event_manager: UiEventManager = UiEventManager()

    def set_connection(self, server: str, username: str, password: str):
        """Set connection and notify observers"""
        from controller.connection import Connection
        from controller.connection_exceptions import (
            ConfigurationError,
            NetworkError,
            ServerError,
            AuthenticationError,
        )

        self.connection: Connection = Connection(server, username, password)

        # Test connection and determine validity
        is_valid: bool = False
        error_message: Optional[str] = None

        try:
            self.connection.test_connection()
            is_valid = True
        except ConfigurationError as e:
            error_message = f"Configuration error: {e}"
        except AuthenticationError as e:
            error_message = f"Authentication failed: {e}"
        except NetworkError as e:
            error_message = f"Network error: {e}"
        except ServerError as e:
            error_message = f"Server error: {e}"
        except Exception as e:
            error_message = f"Unexpected error: {e}"

        # Notify all interested components about the connection change
        self.event_manager.publish_event(
            UiEvent.CONNECTION_CHANGED,
            {
                "connection": self.connection,
                "server": server,
                "username": username,
                "is_valid": is_valid,
                "error_message": error_message,
            },
        )

    """def get_repository_list(self) -> dict:
        Get repositories and notify observers
        if not self.connection:
            self.event_manager.publish_event(
                UiEvent.REPOSITORY_LOADED,
                {"repositories": {}, "error": "No connection available"},
            )
            return {}

        try:
            # Ensure connection is valid before querying
            if not self.connection.validated:
                self.connection.test_connection()

            repos = self.connection.query(HttpRequestType.GET, "repositories").json()

            # Notify observers about successfully loaded repositories
            self.event_manager.publish_event(
                UiEvent.REPOSITORY_LOADED, {"repositories": repos, "error": None}
            )
            return repos

        except Exception as e:
            # Notify observers about repository loading failure
            self.event_manager.publish_event(
                UiEvent.REPOSITORY_LOADED,
                {"repositories": {}, "error": f"Failed to load repositories: {e}"},
            )
            return {}"""

    def get_repository(self, repo_number: int) -> json:
        repo = self.connection.query(
            HttpRequestType.GET, f"/repositories/{repo_number}"
        )

        try:
            json_string = repo.json()
            json.loads(json_string) #validation
            return json_string
        except JSONDecodeError as e:
            logging.error(f"Error decoding JSON: {e}")
            raise

    def get_resource_list(self, repo_number) -> list[int]:
        """AI Generated. Double check especially lines 118, 119
        todo: Add error handling
        """
        resources = []
        result = self.connection.query(
            HttpRequestType.GET, f"/repositories/{repo_number}/resources"
        ).json()
        while "error" not in result:
            resources.append(result["uri"])
            result = self.connection.query(
                HttpRequestType.GET,
                f"/repositories/{repo_number}/resources?page={len(resources)}",
            ).json()
        return resources

    def get_resource_records(self, repo_number: int, resources_to_get: list) -> dict:
        """
        Make the queries necessary to turn a list of resources in a repo into a dict of resource JSONs.

        Args:
            repo_number: The repository number to query
            resources_to_get: List of resource identifiers to retrieve

        Returns:
            dict: Mapping of resource identifier to resource data

        Raises:
            ValueError: If repo_number is invalid or resources_to_get is empty
            ConnectionError: If connection issues occur during retrieval
            JSONDecodeError: If server returns invalid JSON
            ServerError: If server returns unexpected errors
            NetworkError: If network connectivity issues occur
        """
        # Input validation
        if not isinstance(repo_number, int) or repo_number <= 0:
            raise ValueError(f"Invalid repository number: {repo_number}")

        if not resources_to_get:
            logging.warning(f"No resources requested for repository {repo_number}")
            return {}

        if not isinstance(resources_to_get, list):
            raise ValueError("resources_to_get must be a list")

        logging.info(
            f"Fetching {len(resources_to_get)} resources from repository {repo_number}"
        )

        resources = {}
        failed_resources = []

        for resource_id in resources_to_get:
            try:
                logging.debug(
                    f"Fetching resource {resource_id} from repository {repo_number}"
                )
                resource_data = self.get_resource_record(repo_number, resource_id)

                resources[resource_id] = resource_data
                logging.debug(f"Successfully fetched resource {resource_id}")

            except (JSONDecodeError, ConnectionError, NetworkError, ServerError) as e:
                # These are critical errors - propagate immediately with same type
                error_msg = f"Critical error fetching resource {resource_id} from repository {repo_number}: {e}"
                logging.warning(error_msg)
                raise  # Re-raise the original exception with same type
            except ValueError as e:
                error_msg = f"Invalid resource ID {resource_id} in repository {repo_number}: {e}"
                logging.warning(error_msg)
                raise
            except Exception as e:
                # Unexpected errors - log and continue, but track the failure
                error_msg = f"Unexpected error fetching resource {resource_id}: {e}"
                logging.error(error_msg)
                failed_resources.append((resource_id, f"Unexpected error: {str(e)}"))

        # Log summary of results
        success_count = len(resources)
        failure_count = len(failed_resources)
        total_count = len(resources_to_get)

        if failure_count > 0:
            logging.warning(
                f"Resource retrieval completed with {failure_count} failures: "
                f"{success_count}/{total_count} resources retrieved successfully"
            )

        else:
            logging.info(
                f"Successfully retrieved all {success_count} resources from repository {repo_number}"
            )

        return resources
    def get_resource_record(self, repo_number: int, resource_number: int) -> dict:
        """
        Fetches a specific resource record from a repository using its resource number.

        :param repo_number: The ID of the repository.
        :param resource_number: The specific resource number to retrieve.
        :return: A dictionary containing the resource record data or an error message.
        """
        try:
            # Query the specific resource record
            response = self.connection.query(
                HttpRequestType.GET,
                f"/repositories/{repo_number}/resources/{resource_number}",
            )

            # Parse the response JSON
            resource_data = response.json()
            return resource_data

        except JSONDecodeError as e:
            logging.error(
                f"Error decoding JSON for resource #{resource_number} in repository #{repo_number}: {e}"
            )
            return {"error": "Failed to decode server response."}

        except Exception as e:
            logging.error(
                f"Unexpected error while fetching resource #{resource_number}: {e}"
            )
            return {"error": str(e)}

    def put_resource_record(
        self, repo_number: int, resource_number: int, resource_record: dict
    ) -> bool:
        """
        Edit a resource record in a repository. You don't need the original resource, just a dict representing the
        final form of the data, and the numbers used to locate it. Resource_record should probably be broken out into
        its own class at some point
        :param repo_number:
        :param resource_number:
        :param resource_record:
        :return:

        TODO: Test, log, add userlogging
        """
        try:
            # Construct the URL for the specific resource
            url = f"/repositories/{repo_number}/resources/{resource_number}"

            # Make the PUT request to update the resource - Fixed: use self.connection.client
            response = self.connection.client.put(url, json=resource_record)

            # Check if the update was successful based on the response status code
            if (
                response.status_code == 200
            ):  # Assuming 200 indicates a successful update
                logging.info(
                    f"Updated {url} with new value {resource_record} successfully!"
                )
                return True
            else:
                logging.warning(
                    f"Failed to update resource. Status code: {response.status_code}"
                )
                return False

        except Exception as e:
            logging.warning(f"An error occurred while updating the resource: {e}")
            return False
    def get_repositories(self) ->dict:
        return json.loads(self.connection.query(HttpRequestType.GET, "repositories").json())

