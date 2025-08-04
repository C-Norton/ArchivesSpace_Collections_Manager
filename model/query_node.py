from __future__ import annotations

from typing import Optional, Any
from model.node import Node
from model.data_model import DataModel
from model.field import Field
from model.query_type import QueryType


class QueryNode(Node):
    """
    A query node that evaluates a single condition against ArchivesSpace records.

    This represents a leaf node in a query tree that compares a specific field
    of a record against a given value using various comparison operators.
    """

    def __init__(
        self,
        data_model: DataModel,
        query_type: QueryType,
        compare_field: Field,
        data_to_compare_to: Optional[str] = None,
    ):
        self.query_type = query_type
        self.data_to_compare_to = data_to_compare_to
        self.compare_field = compare_field
        self.data_model = data_model

    def validate(self) -> bool:
        """Validate that the query node configuration is valid."""
        # Check if data_to_compare_to is required for this query type
        requires_data = self.query_type not in [QueryType.Empty, QueryType.Not_Empty]

        if requires_data and not self.data_to_compare_to:
            return False

        if not requires_data and self.data_to_compare_to:
            return False

        return True

    def eval(self, repo: int, record_id: int) -> bool:
        """
        Evaluate this query condition against a specific record.

        Args:
            repo: Repository ID
            record_id: Record ID to evaluate

        Returns:
            bool: True if the record matches this condition

        Raises:
            NotImplementedError: For unsupported record types
            ValueError: For invalid query configurations
        """
        # Get the record data based on the record type
        record_data = self._get_record_data(repo, record_id)

        # Extract the field value we want to compare
        field_value = self._extract_field_value(record_data)

        # Perform the comparison
        return self._compare_values(field_value)

    def _get_record_data(self, repo: int, record_id: int) -> Any:
        """Get record data from ArchivesSpace based on record type."""
        # Note: The original logic seems confused - it's matching against compare_field
        # which should be a Field enum, not RecordType. This needs clarification.
        # For now, assuming we're always dealing with Resources
        return self.data_model.main.connection_manager.get_resource_record(
            repo, record_id
        )

    def _extract_field_value(self, record_data: dict) -> Any:
        """Extract the specific field value from the record data."""
        # This would need to be implemented based on how fields map to JSON keys
        # For now, using the field name directly
        return record_data.get(self.compare_field.name, "")

    def _compare_values(self, field_value: Any) -> bool:
        """Compare the field value according to the query type."""
        # Convert to string for comparison if needed
        field_str = str(field_value) if field_value is not None else ""

        match self.query_type:
            case QueryType.Equals:
                if not self.data_to_compare_to:
                    raise ValueError("Equals query requires comparison data")
                return field_str == self.data_to_compare_to

            case QueryType.Not_Equals:
                if not self.data_to_compare_to:
                    raise ValueError("Not_Equals query requires comparison data")
                return field_str != self.data_to_compare_to

            case QueryType.Empty:
                if self.data_to_compare_to:
                    raise ValueError("Empty query should not have comparison data")
                return field_str == "" or field_value is None

            case QueryType.Not_Empty:
                if self.data_to_compare_to:
                    raise ValueError("Not_Empty query should not have comparison data")
                return field_str != "" and field_value is not None

            case QueryType.Starts_With:
                if not self.data_to_compare_to:
                    raise ValueError("Starts_With query requires comparison data")
                return field_str.startswith(self.data_to_compare_to)

            case QueryType.Not_Starts_With:
                if not self.data_to_compare_to:
                    raise ValueError("Not_Starts_With query requires comparison data")
                return not field_str.startswith(self.data_to_compare_to)

            case QueryType.Ends_With:
                if not self.data_to_compare_to:
                    raise ValueError("Ends_With query requires comparison data")
                return field_str.endswith(self.data_to_compare_to)

            case QueryType.Not_Ends_With:
                if not self.data_to_compare_to:
                    raise ValueError("Not_Ends_With query requires comparison data")
                return not field_str.endswith(self.data_to_compare_to)

            case QueryType.Contains:
                if not self.data_to_compare_to:
                    raise ValueError("Contains query requires comparison data")
                return self.data_to_compare_to in field_str

            case QueryType.Not_Contains:
                if not self.data_to_compare_to:
                    raise ValueError("Not_Contains query requires comparison data")
                return self.data_to_compare_to not in field_str

            case _:
                raise ValueError(f"Unsupported query type: {self.query_type}")

    def traverse(self, depth: int, nodes: list) -> tuple:
        """
        Traverse this node for tree operations.

        Args:
            depth: Current depth in the tree
            nodes: List to collect node information

        Returns:
            tuple: (node_type, depth) information
        """
        # Add this node's information to the collection
        nodes.append((self, depth))
        return (type(self), depth)

    def to_string(self) -> str:
        """
        Convert this query node to a string representation.

        Returns:
            str: String representation of this query
        """
        field_name = (
            self.compare_field.name
            if hasattr(self.compare_field, "name")
            else str(self.compare_field)
        )
        query_name = (
            self.query_type.name
            if hasattr(self.query_type, "name")
            else str(self.query_type)
        )

        if self.data_to_compare_to:
            return f'%{field_name} &{query_name} "{self.data_to_compare_to}"'
        else:
            return f"%{field_name} &{query_name}"
