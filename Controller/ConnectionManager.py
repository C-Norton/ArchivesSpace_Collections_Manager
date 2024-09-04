from __future__ import annotations
import json
import logging
from asnake import utils as asutils
from Controller.Connection import *


class ConnectionManager:
    def __init__(self, main: Main.Main):
        self.main = main
        self.connection: Connection = Connection("", "", "")

    def get_repository(self, repo_number: int) -> json:
        repo = self.connection.query(RequestType.GET, f"/repositories/{repo_number}")
        return repo.json

    def get_resource_record(self, repo_number: int, resource_number: int) -> json:
        resource = self.connection.query(
            RequestType.GET, f"/repositories/{repo_number}/resources/{resource_number}"
        )
        return resource.json

    def get_repository_list(self) -> dict:
        repos = dict()
        i: int = 2
        result = self.connection.query(RequestType.GET, f"/repositories/2").json()
        while "error" not in result:
            repo = {result["uri"]: result}
            repos.update(repo)
            i += 1
            result = self.connection.query(RequestType.GET, f"/repositories/{i}").json()
        return repos
        # return dict([(repo.json["repo_code"],repo.json) for repo in repos])

    def get_resource_list(self, repo_number: int) -> dict:
        pass

    def get_resource_records(self, repo_number: int, resources_to_get: list) -> dict:
        resources = dict()
        for resource in resources_to_get:
            resources.update(
                {resource, self.get_resource_record(repo_number, resource)}
            )
        return resources

    def put_resource_record(
        self, repo_number: int, resource_number: int, resource_record: dict
    ) -> bool:
        try:
            # Construct the URL for the specific resource
            url = f"/repositories/{repo_number}/resources/{resource_number}"

            # Make the PUT request to update the resource
            response = self.client.put(url, json=resource_record)

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
