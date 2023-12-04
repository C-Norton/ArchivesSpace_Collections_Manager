"""The goal of the Query Node is to determine true or false based off data actively in the archivesspace system"""
import mypy
import typing
from QueryType import *
import Node


class QueryNode(Node.Node):

    def __init__(self, queryType: QueryType, archivalData: str, dataToCompareTo: str = None):
        self.queryType = queryType
        self.dataToCompareTo = dataToCompareTo
        self.archivalData = archivalData

    def eval(self) -> bool:

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
