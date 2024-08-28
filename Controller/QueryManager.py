from requests import Response

from Model.QueryNode import QueryNode


class QueryManager:
    def __init__(self):
        pass
    def place_query(self,query)->Response:
        return None

    def render_query(self, query) -> str:
        return "foo"

    def set_loaded_query(self, query):
        pass

    def get_loaded_query(self)-> QueryNode:
        return None