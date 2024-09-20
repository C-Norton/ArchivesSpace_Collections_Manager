from requests import Response

from Model.Node import Node
from Model.Note import Note
from Model.NoteType import NoteType
from Model.QueryNode import QueryNode


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
    def __init__(self):
        self.loaded_query = None

    def place_query(self, query) -> Response:
        return None

    def render_query(self, query: Node) -> str:
        return query.to_string()

    def set_loaded_query(self, query : QueryNode):
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
    def construct_from_string(self, query:str):
        pass