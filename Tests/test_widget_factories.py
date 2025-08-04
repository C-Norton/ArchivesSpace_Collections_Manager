"""
Fixed tests for ScrollableComboboxFactory with correct import paths
"""

import pytest
from enum import Enum
from tkinter import ttk
from view.util.widget_factories import ScrollableComboboxFactory


class TestScrollableComboboxFactory:
    """Test the ScrollableComboboxFactory with correct mocking"""

    def test_create_enum_combobox_basic(self, mocker):
        """Test basic enum combobox creation"""
        class TestEnum(Enum):
            OPTION1 = 1
            OPTION2 = 2
            OPTION3 = 3

        parent = mocker.Mock()
        textvariable = mocker.Mock()

        # Mock ttk.Combobox with the correct import path
        mock_combobox_class = mocker.patch('view.util.widget_factories.ttk.Combobox')
        mock_combobox = mocker.Mock()
        mock_combobox_class.return_value = mock_combobox

        result = ScrollableComboboxFactory.create_enum_combobox(
            parent, textvariable, TestEnum
        )

        # Verify combobox was created with correct parameters
        mock_combobox_class.assert_called_once_with(
            parent,
            textvariable=textvariable,
            values=['OPTION1', 'OPTION2', 'OPTION3'],
            state='readonly',
            height=4
        )
        assert result == mock_combobox

    def test_create_list_combobox_readonly(self, mocker):
        """Test list combobox creation in readonly mode"""
        parent = mocker.Mock()
        textvariable = mocker.Mock()
        values = ['Option A', 'Option B', 'Option C']

        mock_combobox_class = mocker.patch('view.util.widget_factories.ttk.Combobox')
        mock_combobox = mocker.Mock()
        mock_combobox_class.return_value = mock_combobox

        result = ScrollableComboboxFactory.create_list_combobox(
            parent, textvariable, values, max_visible_items=3
        )

        mock_combobox_class.assert_called_once_with(
            parent,
            textvariable=textvariable,
            values=values,
            state='readonly',
            height=3
        )
        assert result == mock_combobox

    def test_create_list_combobox_with_custom_entry(self, mocker):
        """Test list combobox creation allowing custom entry"""
        parent = mocker.Mock()
        textvariable = mocker.Mock()
        values = ['Option A', 'Option B']

        mock_combobox_class = mocker.patch('view.util.widget_factories.ttk.Combobox')
        mock_combobox = mocker.Mock()
        mock_combobox_class.return_value = mock_combobox

        result = ScrollableComboboxFactory.create_list_combobox(
            parent, textvariable, values, allow_custom_entry=True
        )

        mock_combobox_class.assert_called_once_with(
            parent,
            textvariable=textvariable,
            values=values,
            state='normal',
            height=4
        )
        assert result == mock_combobox

    def test_custom_width_parameter(self, mocker):
        """Test that custom width is properly applied"""
        class TestEnum(Enum):
            OPTION1 = 1

        parent = mocker.Mock()
        textvariable = mocker.Mock()

        mock_combobox_class = mocker.patch('view.util.widget_factories.ttk.Combobox')
        mock_combobox = mocker.Mock()
        mock_combobox_class.return_value = mock_combobox

        ScrollableComboboxFactory.create_enum_combobox(
            parent, textvariable, TestEnum, width=25
        )

        # Verify width was included in the call
        call_kwargs = mock_combobox_class.call_args[1]
        assert call_kwargs['width'] == 25

    def test_enum_combobox_with_all_parameters(self, mocker):
        """Test enum combobox creation with all optional parameters"""
        class TestEnum(Enum):
            A = 1
            B = 2

        parent = mocker.Mock()
        textvariable = mocker.Mock()

        mock_combobox_class = mocker.patch('view.util.widget_factories.ttk.Combobox')
        mock_combobox = mocker.Mock()
        mock_combobox_class.return_value = mock_combobox

        # Test with custom parameters
        result = ScrollableComboboxFactory.create_enum_combobox(
            parent,
            textvariable,
            TestEnum,
            max_visible_items=6,
            width=30,
            font=('Arial', 10)  # Additional tkinter parameter
        )

        # Verify all parameters were passed correctly
        mock_combobox_class.assert_called_once_with(
            parent,
            textvariable=textvariable,
            values=['A', 'B'],
            state='readonly',
            height=6,
            width=30,
            font=('Arial', 10)
        )
        assert result == mock_combobox

    def test_list_combobox_empty_values(self, mocker):
        """Test list combobox with empty values list"""
        parent = mocker.Mock()
        textvariable = mocker.Mock()
        values = []

        mock_combobox_class = mocker.patch('view.util.widget_factories.ttk.Combobox')
        mock_combobox = mocker.Mock()
        mock_combobox_class.return_value = mock_combobox

        result = ScrollableComboboxFactory.create_list_combobox(
            parent, textvariable, values
        )

        mock_combobox_class.assert_called_once_with(
            parent,
            textvariable=textvariable,
            values=[],
            state='readonly',
            height=4
        )
        assert result == mock_combobox

    def test_default_values_are_correct(self, mocker):
        """Test that default class values are set correctly"""
        assert ScrollableComboboxFactory.DEFAULT_HEIGHT == 4
        assert ScrollableComboboxFactory.DEFAULT_WIDTH == 20

    def test_enum_values_extraction(self, mocker):
        """Test that enum values are correctly extracted as names"""
        class TestEnum(Enum):
            FIRST_OPTION = "value1"
            SECOND_OPTION = "value2"
            THIRD_OPTION = "value3"

        parent = mocker.Mock()
        textvariable = mocker.Mock()

        mock_combobox_class = mocker.patch('view.util.widget_factories.ttk.Combobox')
        mock_combobox = mocker.Mock()
        mock_combobox_class.return_value = mock_combobox

        ScrollableComboboxFactory.create_enum_combobox(
            parent, textvariable, TestEnum
        )

        # Verify that enum names (not values) are used
        call_kwargs = mock_combobox_class.call_args[1]
        expected_values = ['FIRST_OPTION', 'SECOND_OPTION', 'THIRD_OPTION']
        assert call_kwargs['values'] == expected_values


class TestScrollableComboboxFactoryIntegration:
    """Integration tests that test the factory with real tkinter components"""

    def test_real_enum_combobox_creation(self):
        """Test creating a real combobox with enum (requires tkinter)"""
        import tkinter as tk
        from enum import Enum

        class TestEnum(Enum):
            OPTION1 = 1
            OPTION2 = 2

        # Create a root window for testing
        root = tk.Tk()
        root.withdraw()  # Hide the window

        try:
            textvariable = tk.StringVar()

            # This should create a real combobox without error
            combobox = ScrollableComboboxFactory.create_enum_combobox(
                root, textvariable, TestEnum
            )

            # Verify it's a real Combobox
            assert isinstance(combobox, ttk.Combobox)
            assert combobox['state'] == 'readonly'
            assert combobox['height'] == 4
            assert list(combobox['values']) == ['OPTION1', 'OPTION2']

        finally:
            root.destroy()

    def test_real_list_combobox_creation(self):
        """Test creating a real combobox with list values"""
        import tkinter as tk

        root = tk.Tk()
        root.withdraw()

        try:
            textvariable = tk.StringVar()
            values = ['Alpha', 'Beta', 'Gamma']

            combobox = ScrollableComboboxFactory.create_list_combobox(
                root, textvariable, values, max_visible_items=2
            )

            assert isinstance(combobox, ttk.Combobox)
            assert combobox['state'] == 'readonly'
            assert combobox['height'] == 2
            assert list(combobox['values']) == values

        finally:
            root.destroy()

    def test_combobox_with_custom_entry_enabled(self):
        """Test combobox allowing custom text entry"""
        import tkinter as tk

        root = tk.Tk()
        root.withdraw()

        try:
            textvariable = tk.StringVar()
            values = ['Predefined1', 'Predefined2']

            combobox = ScrollableComboboxFactory.create_list_combobox(
                root, textvariable, values, allow_custom_entry=True
            )

            assert isinstance(combobox, ttk.Combobox)
            assert combobox['state'] == 'normal'  # Should allow text entry
            assert list(combobox['values']) == values

        finally:
            root.destroy()


class TestScrollableComboboxFactoryErrorHandling:
    """Test error handling and edge cases"""

    def test_invalid_enum_class(self, mocker):
        """Test behavior with invalid enum class"""
        parent = mocker.Mock()
        textvariable = mocker.Mock()

        # Mock ttk.Combobox
        mock_combobox_class = mocker.patch('view.util.widget_factories.ttk.Combobox')
        mock_combobox = mocker.Mock()
        mock_combobox_class.return_value = mock_combobox

        # This should raise an AttributeError when trying to iterate over non-enum
        with pytest.raises(TypeError):
            ScrollableComboboxFactory.create_enum_combobox(
                parent, textvariable, str  # str is not an Enum
            )

    def test_negative_max_visible_items(self, mocker):
        """Test with negative max_visible_items parameter"""
        parent = mocker.Mock()
        textvariable = mocker.Mock()
        values = ['A', 'B']

        mock_combobox_class = mocker.patch('view.util.widget_factories.ttk.Combobox')
        mock_combobox = mocker.Mock()
        mock_combobox_class.return_value = mock_combobox

        # Should accept negative values (tkinter might handle this gracefully)
        result = ScrollableComboboxFactory.create_list_combobox(
            parent,         textvariable, values, max_visible_items=-1
        )

        call_kwargs = mock_combobox_class.call_args[1]
        assert call_kwargs['height'] == -1
        assert result == mock_combobox

    def test_none_values_in_list(self, mocker):
        """Test with None values in the list"""
        parent = mocker.Mock()
        textvariable = mocker.Mock()
        values = ['Option1', None, 'Option3']

        mock_combobox_class = mocker.patch('view.util.widget_factories.ttk.Combobox')
        mock_combobox = mocker.Mock()
        mock_combobox_class.return_value = mock_combobox

        # Should pass None values through to combobox
        result = ScrollableComboboxFactory.create_list_combobox(
            parent, textvariable, values
        )

        call_kwargs = mock_combobox_class.call_args[1]
        assert call_kwargs['values'] == ['Option1', None, 'Option3']
        assert result == mock_combobox