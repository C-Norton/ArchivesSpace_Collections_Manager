"""
Utility for creating standardized scrollable comboboxes to replace problematic OptionMenus
"""

from tkinter import ttk
from typing import List, Optional
from enum import Enum

from view.menu_buttons.MenuButton import MenuButtonWidget, FunctionMenuButtonImpl


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
        **kwargs,
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
            "textvariable": textvariable,
            "values": values,
            "state": "readonly",
            "height": max_visible_items,
            **kwargs,
        }

        if width is not None:
            combobox_kwargs["width"] = width

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
        **kwargs,
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
            "textvariable": textvariable,
            "values": values,
            "state": "normal" if allow_custom_entry else "readonly",
            "height": max_visible_items,
            **kwargs,
        }

        if width is not None:
            combobox_kwargs["width"] = width

        return ttk.Combobox(parent, **combobox_kwargs)

class MenuButtonFactory:
    """Factory for creating MenuButton widgets with various configurations"""

    @staticmethod
    def create_function_button(
            parent,
            text: str,
            on_click_func,
            initial_clickable: bool = True,
            **button_kwargs
    ) -> MenuButtonWidget:
        """
        Create a MenuButton that executes a provided function on click

        Args:
            parent: tkinter parent widget
            text: Button text
            on_click_func: Function to call when button is clicked
            initial_clickable: Initial clickable state (default: True)
            **button_kwargs: Additional arguments for ttk.Button

        Returns:
            MenuButtonWidget configured with the provided function
        """
        impl = FunctionMenuButtonImpl(parent, text, on_click_func, initial_clickable)
        return MenuButtonWidget(parent, impl, **button_kwargs)

    @staticmethod
    def create_lambda_button(
            parent,
            text: str,
            lambda_func,
            initial_clickable: bool = True,
            **button_kwargs
    ) -> MenuButtonWidget:
        """
        Convenience method for creating buttons with lambda functions

        Args:
            parent: tkinter parent widget
            text: Button text
            lambda_func: Lambda function to execute on click
            initial_clickable: Initial clickable state (default: True)
            **button_kwargs: Additional arguments for ttk.Button

        Returns:
            MenuButtonWidget configured with the lambda function
        """
        return MenuButtonFactory.create_function_button(
            parent, text, lambda_func, initial_clickable, **button_kwargs
        )

    @staticmethod
    def create_method_button(
            parent,
            text: str,
            obj,
            method_name: str,
            initial_clickable: bool = True,
            **button_kwargs
    ) -> MenuButtonWidget:
        """
        Create a MenuButton that calls a method on a provided object

        Args:
            parent: tkinter parent widget
            text: Button text
            obj: Object containing the method to call
            method_name: Name of the method to call
            initial_clickable: Initial clickable state (default: True)
            **button_kwargs: Additional arguments for ttk.Button

        Returns:
            MenuButtonWidget configured to call the specified method
        """
        method_func = getattr(obj, method_name)
        return MenuButtonFactory.create_function_button(
            parent, text, method_func, initial_clickable, **button_kwargs
        )

    @staticmethod
    def create_callback_button(
            parent,
            text: str,
            callback,
            *args,
            initial_clickable: bool = True,
            **button_kwargs
    ) -> MenuButtonWidget:
        """
        Create a MenuButton that calls a callback function with provided arguments

        Args:
            parent: tkinter parent widget
            text: Button text
            callback: Function to call
            *args: Arguments to pass to the callback
            initial_clickable: Initial clickable state (default: True)
            **button_kwargs: Additional arguments for ttk.Button (must come after *args)

        Returns:
            MenuButtonWidget configured to call callback with args
        """
        def callback_wrapper():
            callback(*args)

        return MenuButtonFactory.create_function_button(
            parent, text, callback_wrapper, initial_clickable, **button_kwargs
        )

