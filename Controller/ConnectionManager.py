from __future__ import annotations
import json
import logging
from json import JSONDecodeError

from requests import Response

from Controller.Connection import *
from Controller.Interfaces import IQueryService


class ConnectionManager(IQueryService):
    """
    Connection manager is a friendly frontend to the connection class that adds in both tracking of an active connection
    as well as common tasks. It should also parse the data out. Most of this code is fairly theorhetical at the moment,
    and requires testing.

    todo: weigh pros and cons of converting this class to a singleton.
    todo: Add lots of logging
    """

    def execute_query(self, query) -> Response:
        return Response()

    def validate_query(self, query) -> bool:
        return True

    def __init__(self, server: str = "", username: str = "", password: str = ""):
        self.connection = Connection("", "", "")

    def get_repository(self, repo_number: int) -> json:
        """
        Does what it says on the tin.
        :param repo_number: which repository are we getting information for?
        :return: json representing the repository
        https://archivesspace.github.io/archivesspace/doc/repository_schema.html
        """
        repo = self.connection.query(
            HttpRequestType.GET, f"/repositories/{repo_number}"
        )

        try:
            json.loads(repo.json)
            return repo.json
        except JSONDecodeError as e:
            logging.error(f"Error decoding JSON: {e}")
            return "{}"

    def get_resource_record(self, repo_number: int, resource_number: int) -> json:
        """
        Does what it says on the tin.
        :param repo_number:what repository is this resource in?
        :param resource_number: what resource id are we getting?
        :return: json representing the resource
        https://archivesspace.github.io/archivesspace/doc/resource_schema.html
        """
        resource = self.connection.query(
            HttpRequestType.GET,
            f"/repositories/{repo_number}/resources/{resource_number}",
        )
        return resource.json

    def get_repositories(self) -> dict:
        """
        Get a list of all repository names and URIs. This code is used by the refresh repositories button.
        repository IDs start counting at 1, but 1 is always the "Archivesspace" repository, which is a system repo for
        archivesspace, so we start returning at 2, hence the 2 start.
        :return: a dict of jsons representing the repos.

        todo: Add better error handling
        """
        repos = dict()
        i: int = 2
        result = self.connection.query(HttpRequestType.GET, "/repositories/2").json()
        while "error" not in result:
            repo = {result["uri"]: result}
            repos.update(repo)
            i += 1
            result = self.connection.query(
                HttpRequestType.GET, f"/repositories/{i}"
            ).json()
        return repos

    def get_resource_list(self, repo_number: int) -> dict:
        """
        get a list of all resource IDs in a repository. NOT FULL DETAILS.
        :param repo_number:
        :return:
        """
        pass

    def get_resource_records(self, repo_number: int, resources_to_get: list) -> dict:
        """
        Make the queries necessary to turn a list of resources in a repo into a dict of resource JSONs
        :param repo_number:
        :param resources_to_get:
        :return:
        """
        resources = dict()
        for resource in resources_to_get:
            resources.update(
                {resource: self.get_resource_record(repo_number, resource)}  # Fixed: colon instead of comma
            )
        return resources

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