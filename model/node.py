

"""***DO NOT DELETE. USED AS AN INTERFACE***"""

import abc


class Node:
    """Node base class for the various types of node used in construction of a query"""

    @abc.abstractmethod
    def validate(self) -> bool:
        pass

    @abc.abstractmethod
    def eval(self, repo, recordID: int) -> bool:
        pass

    @abc.abstractmethod
    def traverse(self, depth, nodes):
        pass

    @abc.abstractmethod
    def to_string(self):
        pass
