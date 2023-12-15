import Node
import OperatorType
from Model.RecordType import RecordType


class OperatorNode(Node.Node):
    def __init__(self, OperatorType: OperatorType.OperatorType, children):
        self.Operator = OperatorType
        self.Children = children

    def validate(self) -> bool:
        for child in self.Children:
            if not isinstance(child, Node):
                return False
            if not child.validate():
                return False
        if self.Operator == OperatorType.OperatorType.NOT and len(self.Children) == 1:
            return True
        if self.Operator != OperatorType.OperatorType.NOT and len(self.Children) > 1:
            return True
        return False

    def eval(self, repo, recordType: RecordType, recordID: int):
        match self.Operator:
            case OperatorType.OperatorType.NOT:
                return not self.Children[0].eval(repo, recordType, recordID)
            case OperatorType.OperatorType.OR:
                for child in self.Children:
                    if child.eval(repo, recordType, recordID):
                        return True
                return False
            case OperatorType.OperatorType.AND:
                for child in self.Children:
                    if not child.eval(repo, recordType, recordID):
                        return False
                return True
