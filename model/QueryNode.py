"""The goal of the Query Node is to determine true or false based off data actively in the archivesspace system"""
import mypy
import typing
class QueryNode:

    queryType = {}
    dataToCompareTo = ""
    archivalData = ""

    def eval(self) -> bool:
        return True
