from abc import ABC, abstractmethod
from requests import Response


class IConnection(ABC):
    @abstractmethod
    def test_connection(self) -> None:
        pass


class IQueryService(ABC):
    @abstractmethod
    def validate_query(self, query) -> bool:
        pass

    @abstractmethod
    def execute_query(self, query) -> Response:
        pass

    @abstractmethod
    def get_repositories(self) -> dict:
        pass
