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
        data_model: Model.DataModel.DataModel,
        query_type: QueryType,
        compare_field: Field,
        data_to_compare_to: str = None,
    ):
        self.query_type = query_type
        self.data_to_compare_to = data_to_compare_to
        self.compare_field = compare_field
        self.data_model = data_model

    def eval(self, repo, record_id: int) -> bool:
        """
        Record
        RecordType
        Repo
        QueryType
        Data (optional)

        Then, get the record from the record ID and record type
        then run through

        """

        record_data = None

        match self.compare_field:
            case RecordType.Resource:
                record_data = (
                    self.data_model.main.connection_manager.get_resource_record(
                        repo, record_id
                    )[self.compare_field.name]
                )
            case RecordType.ArchivalObject:
                pass
            case RecordType.DigitalObject:
                pass
            case RecordType.Subject:
                pass
            case RecordType.Agent:
                pass

        match self.query_type:
            case QueryType.Equals:
                if not self.data_to_compare_to:
                    raise Exception("InvalidQueryType for datatocompare value")
                return self.data_to_compare_to == self.archivalData
            case QueryType.Not_Equals:
                if not self.data_to_compare_to:
                    raise Exception("InvalidQueryType for datatocompare value")
                return not self.data_to_compare_to == self.archivalData
            case QueryType.Empty:
                if self.data_to_compare_to:
                    raise Exception("InvalidQueryType for datatocompare value")
                return self.archivalData == "" or (not self.archivalData)
            case QueryType.Not_Empty:
                if self.data_to_compare_to:
                    raise Exception("InvalidQueryType for datatocompare value")
                return not (self.archivalData == "" or (not self.archivalData))
            case QueryType.Starts_With:
                if not self.data_to_compare_to:
                    raise Exception("InvalidQueryType for datatocompare value")

            case QueryType.Not_Starts_With:
                if not self.data_to_compare_to:
                    raise Exception("InvalidQueryType for datatocompare value")

            case QueryType.Ends_With:
                if not self.data_to_compare_to:
                    raise Exception("InvalidQueryType for datatocompare value")

            case QueryType.Not_Ends_With:
                if not self.data_to_compare_to:
                    raise Exception("InvalidQueryType for datatocompare value")

            case QueryType.Contains:
                if not self.data_to_compare_to:
                    raise Exception("InvalidQueryType for datatocompare value")

            case QueryType.Not_Contains:
                if not self.data_to_compare_to:
                    raise Exception("InvalidQueryType for datatocompare value")

            case _:
                raise Exception("InvalidQueryType")

        return True
