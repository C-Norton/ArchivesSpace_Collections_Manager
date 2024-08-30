from __future__ import annotations
import json
import logging
from asnake import utils as asutils
from Controller.Connection import *


class ConnectionManager:
    def __init__(self, main: Main.Main):
        self.main = main
        self.connection: Connection = Connection("", "", "")

    def get_repository(self, repoNumber: int) -> json:
        repo = self.connection.query(RequestType.GET, f"/repositories/{repoNumber}")
        return repo.json

    def get_resource_record(self, repoNumber: int, resourceNumber: int) -> json:
        resource = self.connection.query(
            RequestType.GET, f"/repositories/{repoNumber}/resources/{resourceNumber}"
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

    def get_resource_list(self, repoNumber: int) -> dict:
        pass

    def get_resource_records(self, repoNumber: int, resourcesToGet: list) -> dict:
        resources = dict()
        for resource in resourcesToGet:
            resources.update({resource, self.get_resource_record(repoNumber, resource)})
        return resources
