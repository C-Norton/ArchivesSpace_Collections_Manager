

def singleton(cls):
    """Decorator to implement singleton pattern."""
    instances = {}  # Dictionary to store instances

    def getinstance(*args, **kwargs):
        """Inner function to get or create the singleton instance."""
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)  # Create the instance if it doesn't exist
        return instances[cls]  # Return the existing or newly created instance

    return getinstance


@singleton
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
    _instance = None
    _initialized = False

    def __init__(self, main=None):
        # Only initialize once, even if called multiple times
        if not DataModel._initialized and main is not None:
            self.main = main
            self.repositories = None
            DataModel._initialized = True
            self.query = None
    def initialize_repositories(self):
        if self.repositories is None and hasattr(self, 'main') and self.main is not None:
            self.repositories = self.main.connection_manager.get_repositories()

    def get_repository_count(self) -> int:
        if self.repositories is None:
            return 0
        return len(self.repositories)

    def get_repositories(self):  # MAKE SURE THIS INCLUDES THE REPO IDs BUNDLED WITH
        if self.repositories is None:
            return []
        return [(repo["repo_code"], repo) for repo in self.repositories]
    def add_node(self, node)-> None:
        if self.query is None:
            self.query = node
        else:
            pass