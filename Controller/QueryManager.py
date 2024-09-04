from requests import Response

from Model.Node import Node
from Model.Note import Note
from Model.NoteType import NoteType


class QueryManager:
    def __init__(self):
        pass

    def place_query(self, query) -> Response:
        return None

    def render_query(self, query: Model.Node) -> str:
        return query.to_string()

    def set_loaded_query(self, query):
        pass

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
        return None
