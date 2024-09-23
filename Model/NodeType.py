from enum import Enum


class NodeType(Enum):
    """Used to easily identify which implementation of a node is being used, when necessary"""

    OperatorNode = 0
    QueryNode = 1
