"""
Updated MenuButton system using composition over inheritance for Protocol compliance
"""
from typing import Protocol, runtime_checkable, TYPE_CHECKING
from tkinter import ttk
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from view.MenuFrame import MenuFrame


@runtime_checkable
class MenuButton(Protocol):
    """Protocol for menu button implementations"""
    
    @property
    def clickable(self) -> bool:
        """Whether the button should be clickable"""
        ...
    
    def on_click(self) -> None:
        """Handle button click events"""
        ...


@runtime_checkable  
class PopupButton(MenuButton, Protocol):
    """Protocol for buttons that create popup dialogs"""
    
    def on_close(self) -> None:
        """Handle dialog close events"""
        ...


class BaseMenuButtonImpl(ABC):
    """Base implementation for menu button logic - not a Protocol!"""
    
    def __init__(self, parent, text: str):
        self.parent = parent
        self.text = text
        self._clickable = True
        
    @property
    def clickable(self) -> bool:
        """Whether the button should be clickable"""
        return self._clickable
    
    @clickable.setter
    def clickable(self, value: bool) -> None:
        """Set button clickability"""
        self._clickable = value
    
    @abstractmethod
    def on_click(self) -> None:
        """Handle button click - must be implemented by subclasses"""
        pass
    
    def set_enabled(self, enabled: bool) -> None:
        """Enable/disable the button (convenience method)"""
        self.clickable = enabled


class MenuButtonWidget:
    """
    Wrapper class that provides a tkinter button with MenuButton protocol compliance
    Uses composition instead of multiple inheritance
    """
    
    def __init__(self, parent, button_impl: MenuButton, **button_kwargs):
        """
        Create a MenuButton widget
        
        Args:
            parent: tkinter parent widget  
            button_impl: Object implementing MenuButton protocol
            **button_kwargs: Additional arguments for ttk.Button
        """
        self.impl = button_impl
        
        # Extract text from button_impl if it has it, or use default
        button_text = getattr(button_impl, 'text', 'Button')
        
        # Create the actual tkinter button
        self.button = ttk.Button(
            parent, 
            text=button_text,
            command=self._handle_click,
            **button_kwargs
        )
        
        # Update button state based on implementation
        self._update_button_state()
    
    def _handle_click(self) -> None:
        """Internal click handler that delegates to implementation"""
        if self.impl.clickable:
            self.impl.on_click()
    
    def _update_button_state(self) -> None:
        """Update button visual state based on implementation"""
        if self.impl.clickable:
            self.button.configure(state='normal')
        else:
            self.button.configure(state='disabled')
    
    def refresh(self) -> None:
        """Refresh button state - call when implementation state changes"""
        self._update_button_state()
    
    # Delegate common tkinter.Button methods
    def grid(self, **kwargs):
        return self.button.grid(**kwargs)
    
    def pack(self, **kwargs):  
        return self.button.pack(**kwargs)
    
    def place(self, **kwargs):
        return self.button.place(**kwargs)
        
    def configure(self, **kwargs):
        return self.button.configure(**kwargs)
    
    def cget(self, key):
        return self.button.cget(key)


# Generic MenuButton implementation for function-based buttons
class FunctionMenuButtonImpl(BaseMenuButtonImpl):
    """Generic implementation for buttons that execute a provided function"""
    
    def __init__(self, parent, text: str, on_click_func, initial_clickable: bool = True):
        super().__init__(parent, text)
        self._on_click_func = on_click_func
        self._clickable = initial_clickable
    
    def on_click(self) -> None:
        """Execute the provided function"""
        if self._on_click_func:
            self._on_click_func()


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


class MenuButtonObserver:
    """Observer that updates menu button states when connection changes"""

    def __init__(self, menu_frame: 'MenuFrame'):
        self.menu_frame = menu_frame

    def update(self, event, data):
        """Handle UI events and update button states"""
        if event.value == "connection_changed":
            self.menu_frame.refresh_button_states()
