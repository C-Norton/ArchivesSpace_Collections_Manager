from requests import Response

from Model.Node import Node


class QueryManager:
    def __init__(self):
        pass

    def place_query(self, query) -> Response:
        return None

    def render_query(self, query: Model.Node) -> str:
        return query.to_string()

    def set_loaded_query(self, query):
        pass

    def get_loaded_query(self) -> QueryNode:
        return None
