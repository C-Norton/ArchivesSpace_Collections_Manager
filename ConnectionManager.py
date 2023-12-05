import json

from Connection import *


class ConnectionManager:
    def __init__(self,connection:Connection):
        self.connection:Connection = connection
    def getRepository(self, repoNumber:int) -> json:
        repo = self.connection.Query(RequestType.GET,f"/repositories/{repoNumber}")
        return repo.json

    def getResourceRecord(self, repoNumber:int,resourceNumber:int) -> json:
        resource = self.connection.Query(RequestType.GET,f"/repositories/{repoNumber}/resources/{resourceNumber}")
        return resource.json
    def getRepositoryList(self)-> dict:
        repos = self.connection.Query(RequestType.GET,"/repositories")
        return dict([(repo.repo_code,repo.json) for repo in repos])
    def getResourceList(self,repoNumber:int)->dict:
        pass
    def getResourceRecords(self,repoNumber:int,resourcesToGet:list)->dict:
        resources = dict()
        for resource in resourcesToGet:
            resources.update({resource,self.getResourceRecord(repoNumber,resource)})
        return resources
