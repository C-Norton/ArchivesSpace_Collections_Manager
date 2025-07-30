import model.node as Node
import model.operator_type as OperatorType


class OperatorNode(Node.Node):
    """An operator node is a node for a boolean operation within the tree. It will have one or two children, depending
    on if it's a not.

    todo: consider dropping NOT support, as it makes things more complicated, and individual statements can be NOTTED
    """

    def to_string(self):
        string = "$"
        string += self.operator.name
        for child in self.children:
            string += "{" + child.to_string() + "}"
        return string

    def __init__(self, operator_type: OperatorType.OperatorType, children):
        super().__init__()
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
        """
        we may want to intersperse extra operatortypes between children, not sure yet. Leaning towards the controller
        just having a parser function for this. A bit convoluted, but so are the functional requirements, so I'm not too
        bent out of shape
        """

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

    def traverse(self, depth, nodes):
        for child in self.children:
            nodes += child.traverse(depth + 1, nodes)
        return OperatorType, depth
