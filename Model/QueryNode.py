from __future__ import annotations

import Model.DataModel
from QueryType import *
import Node
import Field

"""The goal of the Query Node is to determine true or false based off data actively in the archivesspace system"""


class QueryNode(Node.Node):

    def __init__(self, datamodel:Model.DataModel.DataModel, queryType: QueryType, compareField: Field, dataToCompareTo: str = None):
        self.queryType = queryType
        self.dataToCompareTo = dataToCompareTo
        self.archivalData = compareField

    def eval(self, repo, resource) -> bool:

        match self.queryType:
            case QueryType.EQUALS:
                return self.dataToCompareTo == self.archivalData
            case QueryType.NOTEQUALS:
                return not self.dataToCompareTo == self.archivalData
            case QueryType.EMPTY:
                return self.archivalData == "" or (not self.archivalData)
            case QueryType.NOTEMPTY:
                return not (self.archivalData == "" or (not self.archivalData))
            case QueryType.STARTSWITH:
                pass
            case QueryType.NOTSTARTSWITH:
                pass
            case QueryType.ENDSWITH:
                pass
            case QueryType.NOTENDSWITH:
                pass
            case QueryType.CONTAINS:
                pass
            case QueryType.NOTCONTAINS:
                pass
            case _:
                raise Exception("InvalidQueryType")

        return True
