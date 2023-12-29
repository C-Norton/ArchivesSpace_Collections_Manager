import Model.Node
import Model.OperatorType
from Model.RecordType import RecordType


class OperatorNode(Model.Node.Node):
    def __init__(self, OperatorType: Model.OperatorType, children):
        self.Operator = OperatorType
        self.Children = children

    def validate(self) -> bool:
        for child in self.Children:
            if not isinstance(child, Model.Node):
                return False
            if not child.validate():
                return False
        if (
            self.Operator == Model.OperatorType.OperatorType.NOT
            and len(self.Children) == 1
        ):
            return True
        if (
            self.Operator != Model.OperatorType.OperatorType.NOT
            and len(self.Children) > 1
        ):
            return True
        return False

    def eval(self, repo, recordID: int):
        match self.Operator:
            case Model.OperatorType.NOT:
                return not self.Children[0].eval(repo, recordID)
            case Model.OperatorType.OR:
                for child in self.Children:
                    if child.eval(repo, recordID):
                        return True
                return False
            case Model.OperatorType.AND:
                for child in self.Children:
                    if not child.eval(repo, recordID):
                        return False
                return True

        # may want to intersperse extra operatortypes between children, not sure yet. I'm leaning towards the controller
        # just having a parser function for this. A bit convoluted, but so are the functional requirements so I'm not too
        # bent out of shape

    def traverse(self, depth, nodes):
        nodes = []
        for child in self.Children:
            nodes += child.traverse(depth + 1, nodes)
        return [(self.Operator, depth, self)] + nodes
