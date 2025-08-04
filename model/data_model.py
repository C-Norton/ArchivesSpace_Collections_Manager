from __future__ import annotations


class DataModel:
    """
    DataModel is OLD, Theoretical code, and reflects effectively a first draft of attempting to solve some of the
    model-side problems of this project. Below are some notes I took

    -------

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

    def __init__(self, main: Main.Main):
        self.main: main = main
        self.repositories = None

    def initialize_repositories(self):
        self.repositories = self.main.connection_manager.get_repositories()

    def get_repository_count(self) -> int:
        return len(self.repositories)

    def get_repositories(self):  # MAKE SURE THIS INCLUDES THE REPO IDs BUNDLED WITH
        return [(repo["repo_code"], repo) for repo in self.repositories]
