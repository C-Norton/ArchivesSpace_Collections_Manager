import abc


class Node:
    @abc.abstractmethod
    def validate(self) -> bool:
        pass

    @abc.abstractmethod
    def eval(self, repo, recordID: int) -> bool:
        pass

    @abc.abstractmethod
    def traverse(self, depth, nodes):
        pass
