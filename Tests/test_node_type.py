from model.node_type import NodeType
import pytest
from enum import Enum


class TestNodeType:
    """Test the NodeType enum"""

    def test_enum_has_expected_members(self):
        """Test that enum has exactly the expected members"""
        expected_members = {"OperatorNode", "QueryNode"}
        actual_members = {member.name for member in NodeType}
        assert actual_members == expected_members

    def test_enum_member_count(self):
        """Test that enum has expected number of members"""
        assert len(NodeType) == 2

    def test_enum_values_are_correct_type(self):
        """Test that enum values have correct underlying type"""
        for member in NodeType:
            assert isinstance(member.value, int)

    def test_enum_values_are_unique(self):
        """Test that all enum values are unique"""
        values = [member.value for member in NodeType]
        assert len(values) == len(set(values))

    def test_enum_member_access_by_name(self):
        """Test that we can access enum members by name"""
        assert NodeType["OperatorNode"] == NodeType.OperatorNode
        assert NodeType["QueryNode"] == NodeType.QueryNode

    def test_enum_member_access_by_value(self):
        """Test that we can access enum members by value"""
        assert NodeType(0) == NodeType.OperatorNode
        assert NodeType(1) == NodeType.QueryNode

    def test_enum_string_representation(self):
        """Test string representation of enum members"""
        assert str(NodeType.OperatorNode) == "NodeType.OperatorNode"
        assert str(NodeType.QueryNode) == "NodeType.QueryNode"

    def test_enum_name_property(self):
        """Test the name property of enum members"""
        assert NodeType.OperatorNode.name == "OperatorNode"
        assert NodeType.QueryNode.name == "QueryNode"

    def test_enum_value_property(self):
        """Test the value property of enum members"""
        assert NodeType.OperatorNode.value == 0
        assert NodeType.QueryNode.value == 1

    def test_enum_equality(self):
        """Test enum member equality"""
        assert NodeType.OperatorNode == NodeType.OperatorNode
        assert NodeType.QueryNode != NodeType.OperatorNode

    def test_enum_identity(self):
        """Test enum member identity"""
        assert NodeType.OperatorNode is NodeType.OperatorNode
        assert NodeType.QueryNode is NodeType.QueryNode

    def test_enum_hashable(self):
        """Test that enum members are hashable (can be used as dict keys)"""
        node_dict = {NodeType.OperatorNode: "operator", NodeType.QueryNode: "query"}
        assert node_dict[NodeType.OperatorNode] == "operator"
        assert node_dict[NodeType.QueryNode] == "query"

    def test_enum_iteration(self):
        """Test iteration over enum members"""
        members = list(NodeType)
        assert len(members) == 2
        assert NodeType.OperatorNode in members
        assert NodeType.QueryNode in members

    def test_invalid_enum_access_raises_error(self):
        """Test that accessing invalid enum members raises appropriate errors"""
        with pytest.raises(KeyError):
            NodeType["InvalidNode"]

        with pytest.raises(ValueError):
            NodeType(999)

    def test_enum_is_enum_instance(self):
        """Test that NodeType is an Enum"""
        assert issubclass(NodeType, Enum)
        assert isinstance(NodeType.OperatorNode, NodeType)
        assert isinstance(NodeType.QueryNode, NodeType)
