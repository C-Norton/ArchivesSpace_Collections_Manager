"""
Needed classes

QueryType
    Equality
    Presence
    BeginsWith
    EndsWith
Query
Operation
    not
    or
    and
    submit
FieldType
    IntField
    DateField
    ETC
Field
RecordType
    DigitalObject
    Resource
    Item
    ETC
Record
Log (Use PANDAS)

So what does the dataflow actually look like
First build a query, A Query consists of QueryType, combined with operations
Query needs to be a tree
"""
import Controller.ConnectionManager
class DataModel:
    def __init__(self):
        self.repositories = None

    def initializeRepositories(self, ConnectionManager : Controller.ConnectionManager.ConnectionManager):
        self.repositories = ConnectionManager.getRepositoryList()

    def getRepositoryCount(self)->int:
        return len(self.repositories)

    def getRepositories(self): #MAKE SURE THIS INCLUDES THE REPO IDs BUNDLED WITH
        return [(repo["repo_code"],repo) for repo in self.repositories]
