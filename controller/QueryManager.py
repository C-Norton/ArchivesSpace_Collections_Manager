from requests import Response

from model.Node import Node
from model.Note import Note
from model.NoteType import NoteType
from model.QueryNode import QueryNode


def singleton(cls):
    """Decorator to implement singleton pattern."""
    instances = {}  # Dictionary to store instances

    def getinstance():
        """Inner function to get or create the singleton instance."""
        if cls not in instances:
            instances[cls] = cls()  # Create the instance if it doesn't exist
        return instances[cls]  # Return the existing or newly created instance

    return getinstance


@singleton  # Apply the sin
class QueryManager:
    """
    The job of QueryManager to turn QueryNodes into queries, and pass them to the ConnectionManager, manager their
    responses, and return all this to the user.

    todo: There's a lot of stubcode here. We also need querystrings up and running for parsing, a lot of the code for
    which will likely be done here.
    """

    def __init__(self):
        self.loaded_query = None

    def place_query(self, query) -> Response:
        """todo"""
        raise NotImplementedError

    def render_query(self, query: Node) -> str:
        return query.to_string()

    def set_loaded_query(self, query: QueryNode):
        self.loaded_query = query

    def add_query_line(
        self,
        note_type: NoteType,
        note_content: str,
        publish: bool,
        label: str,
        persistent_id: str,
    ):
        if Note.is_multipart(note_type):
            raise NotImplementedError
        if note_type is NoteType.Index:
            raise NotImplementedError

    def get_loaded_query(self) -> QueryNode:
        return self.loaded_query

    def construct_from_string(self, query: str):
        pass
