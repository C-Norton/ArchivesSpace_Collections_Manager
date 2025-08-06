from tkinter import ttk, Toplevel

import asnake.client.web_client

from controller.connection_exceptions import (
    AuthenticationError,
    NetworkError,
    ServerError,
)
from view.util.FrameUtils import FrameUtils
from view.menu_buttons.MenuButton import MenuButtonWidget, BaseMenuButtonImpl


class TestConnection:
    """
    This class manages the dialog box for testing a connection. Per the comment in Help, I'd really like to genericize
    these popups and clean up the code. That said, test connection does some additional logic to actually, well, test
    the connection. So this is a challenge, but one that should be resolved through reducing coupling.
    """

    connection = {}
    parent = {}
    frame = {}

    def __init__(self, connection):
        self.connection = connection
        self.frame = Toplevel()
        self.frame.title("Test results")
        FrameUtils.set_icon(self.frame)
        ttk.Button(self.frame, width=70, text="Close", command=self.close_window).grid(
            column=1, row=2
        )
        text = str()
        try:
            self.connection.test_connection()
        except AuthenticationError:
            text = "Connection failed due to a bad username or password."
        except asnake.client.web_client.ASnakeAuthError:
            text = "Connection failed due to a bad username or password."
        except NetworkError:
            text = "Connection failed due to a network error. Are you sure you have the correct API address?"
        except ServerError:
            text = "Connection failed due to an unknown error."
        else:
            text = "Connection successful! Your connection is ready to use."
        ttk.Label(self.frame, text=text, wraplength=220).grid(column=1, row=1)

        for child in self.frame.winfo_children():
            child.grid_configure(padx=5, pady=5)
        self.frame.focus_set()
        self.frame.grab_set()

    def close_window(self):
        ttk.Frame.destroy(self.frame)

class TestConnectionButtonImpl(BaseMenuButtonImpl):
    """Implementation for Test Connection button"""
    
    def __init__(self, parent, connection_manager):
        super().__init__(parent, "Test Connection")  
        self.connection_manager = connection_manager
    
    @property
    def clickable(self) -> bool:
        """Only clickable when there's a connection to test"""
        return (self._clickable and 
                self.connection_manager.connection is not None)
    
    @clickable.setter
    def clickable(self, value: bool) -> None:
        """Set base clickability - actual clickability depends on connection state"""
        self._clickable = value
    
    def on_click(self) -> None:
        """Test the current connection"""
        if self.connection_manager.connection:
            TestConnection(self.connection_manager.connection)


def create_test_connection_button(parent, connection_manager, **kwargs) -> MenuButtonWidget:
    """Factory function to create Test Connection button"""
    impl = TestConnectionButtonImpl(parent, connection_manager)
    return MenuButtonWidget(parent, impl, **kwargs)