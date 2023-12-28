from __future__ import annotations

import Field
import Model.DataModel
import Node
from Model import RecordType
from QueryType import *
from RecordType import *

"""The goal of the Query Node is to determine true or false based off data actively in the archivesspace system"""


class QueryNode(Node.Node):
    def __init__(
        self,
        datamodel: Model.DataModel.DataModel,
        queryType: QueryType,
        compareField: Field,
        dataToCompareTo: str = None,
    ):
        self.queryType = queryType
        self.dataToCompareTo = dataToCompareTo
        self.compareField = compareField
        self.datamodel = datamodel

    def eval(self, repo, recordID: int) -> bool:
        """
        Record
        RecordType
        Repo
        QueryType
        Data (optional)

        Then, get the record from the record ID and record type
        then run through

        """

        recordData = None

        match self.compareField:
            case RecordType.Resource:
                recordData = self.datamodel.main.connectionmanager.get_resource_record(
                    repo, recordID
                )[self.compareField.name]
            case RecordType.ArchivalObject:
                pass
            case RecordType.DigitalObject:
                pass
            case RecordType.Subject:
                pass
            case RecordType.Agent:
                pass

        match self.queryType:
            case QueryType.EQUALS:
                if not self.dataToCompareTo:
                    raise Exception("InvalidQueryType for datatocompare value")
                return self.dataToCompareTo == self.archivalData
            case QueryType.NOTEQUALS:
                if not self.dataToCompareTo:
                    raise Exception("InvalidQueryType for datatocompare value")
                return not self.dataToCompareTo == self.archivalData
            case QueryType.EMPTY:
                if self.dataToCompareTo:
                    raise Exception("InvalidQueryType for datatocompare value")
                return self.archivalData == "" or (not self.archivalData)
            case QueryType.NOTEMPTY:
                if self.dataToCompareTo:
                    raise Exception("InvalidQueryType for datatocompare value")
                return not (self.archivalData == "" or (not self.archivalData))
            case QueryType.STARTSWITH:
                if not self.dataToCompareTo:
                    raise Exception("InvalidQueryType for datatocompare value")

            case QueryType.NOTSTARTSWITH:
                if not self.dataToCompareTo:
                    raise Exception("InvalidQueryType for datatocompare value")

            case QueryType.ENDSWITH:
                if not self.dataToCompareTo:
                    raise Exception("InvalidQueryType for datatocompare value")

            case QueryType.NOTENDSWITH:
                if not self.dataToCompareTo:
                    raise Exception("InvalidQueryType for datatocompare value")

            case QueryType.CONTAINS:
                if not self.dataToCompareTo:
                    raise Exception("InvalidQueryType for datatocompare value")

            case QueryType.NOTCONTAINS:
                if not self.dataToCompareTo:
                    raise Exception("InvalidQueryType for datatocompare value")

            case _:
                raise Exception("InvalidQueryType")

        return True

    def traverse(self, depth, nodes):
        return [
            ((self.compareField, self.queryType, self.dataToCompareTo), depth, self)
        ]
