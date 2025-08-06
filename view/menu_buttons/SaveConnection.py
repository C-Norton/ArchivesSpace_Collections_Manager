from tkinter import ttk, Toplevel

from controller.connection import Connection
from controller.connection_exceptions import (
    AuthenticationError,
    NetworkError,
    ServerError,
    ConfigurationError,
)
from view.util.FrameUtils import FrameUtils
from model.credential_index_manager import credential_manager
from view.menu_buttons.MenuButton import MenuButtonWidget, BaseMenuButtonImpl, PopupButton


def save_connection(connection: Connection):
    """
    This function checks the connection, and saves it to the system keyring if, and only if it is valid.
    Now uses the credential index manager for proper discovery.

    :param connection: see Connection.py
    :return: None
    """
    frame = Toplevel()
    frame.title("Credential Storage")

    FrameUtils.set_icon(frame)
    ttk.Button(
        frame, width=70, text="Close", command=lambda: ttk.Frame.destroy(frame)
    ).grid(column=1, row=2)
    text = "Your connection has been saved."

    try:
        # Test the connection first
        connection.test_connection()
    except ConfigurationError as e:
        text = f"Unable to store connection: Configuration error.\n{e}"
    except AuthenticationError as e:
        text = f"Unable to store connection: Bad username or password.\n{e}"
    except NetworkError as e:
        text = f"Unable to store connection: Network error.\n{e}"
    except ServerError as e:
        text = f"Unable to store connection: Server error.\n{e}"
    except Exception as e:
        text = f"Unable to store connection: Unexpected error.\n{e}"
    else:
        # Connection is valid, store it using the index manager
        try:
            success = credential_manager.store_credential(
                connection.server, connection.username, connection.password
            )

            if success:
                text = f"Successfully stored credentials for:\n{connection.username} @ {connection.server}"
            else:
                text = "Failed to store credentials. Check the application logs for details."

        except Exception as e:
            text = f"Unable to store connection: Storage error.\n{e}"

    ttk.Label(frame, text=text, wraplength=220).grid(column=1, row=1)

    for child in frame.winfo_children():
        child.grid_configure(padx=5, pady=5)
    frame.focus_set()
    frame.grab_set()

class SaveConnectionButtonImpl(BaseMenuButtonImpl, PopupButton):
    """Implementation for Save Connection button - also implements PopupButton"""
    
    def __init__(self, parent, connection_manager):
        super().__init__(parent, "Save Connection")
        self.connection_manager = connection_manager
    
    @property
    def clickable(self) -> bool:
        """Only clickable when there's a connection to save"""
        return (self._clickable and 
                self.connection_manager.connection is not None and
                self.connection_manager.connection.validated)
    
    @clickable.setter
    def clickable(self, value: bool) -> None:
        """Set base clickability - actual clickability depends on connection state"""
        self._clickable = value
    
    def on_click(self) -> None:
        """Save the current connection"""
        if self.connection_manager.connection:
            save_connection(self.connection_manager.connection)
    
    def on_close(self) -> None:
        """Handle any cleanup when popup closes"""
        pass  # No specific cleanup needed for this button


def create_save_connection_button(parent, connection_manager, **kwargs) -> MenuButtonWidget:
    """Factory function to create Save Connection button"""
    impl = SaveConnectionButtonImpl(parent, connection_manager)  
    return MenuButtonWidget(parent, impl, **kwargs)