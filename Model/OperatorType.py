from enum import Enum


class OperatorType(Enum):
    """Used by operatorNodes to declare which operation they represent"""

    AND = 0
    OR = 1
    NOT = 2
