"""
Utility for creating standardized scrollable comboboxes to replace problematic OptionMenus
"""
from tkinter import ttk
from typing import List, Optional
from enum import Enum

class ScrollableComboboxFactory:
    """Factory for creating standardized scrollable comboboxes from Enum classes"""

    DEFAULT_HEIGHT = 4
    DEFAULT_WIDTH = 20

    @classmethod
    def create_enum_combobox(
            cls,
            parent,
            textvariable,
            enum_class: type[Enum],
            max_visible_items: int = DEFAULT_HEIGHT,
            width: Optional[int] = None,
            **kwargs
    ) -> ttk.Combobox:
        """
        Create a combobox populated with enum values

        Args:
            parent: Parent widget
            textvariable: tkinter StringVar to bind to
            enum_class: Enum class to populate values from
            max_visible_items: Maximum items visible before scrolling (default: 4)
            width: Width of combobox in characters (optional)
            **kwargs: Additional arguments passed to ttk.Combobox

        Returns:
            Configured ttk.Combobox
        """
        values = [e.name for e in enum_class]

        combobox_kwargs = {
            'textvariable': textvariable,
            'values': values,
            'state': 'readonly',
            'height': max_visible_items,
            **kwargs
        }

        if width is not None:
            combobox_kwargs['width'] = width

        return ttk.Combobox(parent, **combobox_kwargs)

    @classmethod
    def create_list_combobox(
            cls,
            parent,
            textvariable,
            values: List[str],
            max_visible_items: int = DEFAULT_HEIGHT,
            width: Optional[int] = None,
            allow_custom_entry: bool = False,
            **kwargs
    ) -> ttk.Combobox:
        """
        Create a combobox populated with a list of values

        Args:
            parent: Parent widget
            textvariable: tkinter StringVar to bind to
            values: List of string values to populate
            max_visible_items: Maximum items visible before scrolling (default: 4)
            width: Width of combobox in characters (optional)
            allow_custom_entry: Whether to allow custom text entry (default: False)
            **kwargs: Additional arguments passed to ttk.Combobox

        Returns:
            Configured ttk.Combobox
        """
        combobox_kwargs = {
            'textvariable': textvariable,
            'values': values,
            'state': 'normal' if allow_custom_entry else 'readonly',
            'height': max_visible_items,
            **kwargs
        }

        if width is not None:
            combobox_kwargs['width'] = width

        return ttk.Combobox(parent, **combobox_kwargs)