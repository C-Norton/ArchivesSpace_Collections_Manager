import Node
import OperatorType
from Model.RecordType import RecordType


class OperatorNode(Node.Node):
    def to_string(self):
        raise NotImplementedError

    def __init__(self, operator_type: OperatorType.OperatorType, children):
        self.operator = operator_type
        self.children = children

    def validate(self) -> bool:
        for child in self.children:
            if not isinstance(child, Node):
                return False
            if not child.validate():
                return False
        if self.operator == OperatorType.OperatorType.NOT and len(self.children) == 1:
            return True
        if self.operator != OperatorType.OperatorType.NOT and len(self.children) > 1:
            return True
        return False

    def eval(self, repo, record_id: int):
        match self.operator:
            case OperatorType.OperatorType.NOT:
                return not self.children[0].eval(repo, record_id)
            case OperatorType.OperatorType.OR:
                for child in self.children:
                    if child.eval(repo, record_id):
                        return True
                return False
            case OperatorType.OperatorType.AND:
                for child in self.children:
                    if not child.eval(repo, record_id):
                        return False
                return True

        # may want to intersperse extra operatortypes between children, not sure yet. I'm leaning towards the controller
        # just having a parser function for this. A bit convoluted, but so are the functional requirements so I'm not too
        # bent out of shape

    def traverse(self, depth, nodes):
        for child in self.children:
            nodes += child.traverse(depth + 1, nodes)
        return OperatorType, depth
