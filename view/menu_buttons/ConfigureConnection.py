from __future__ import annotations
from tkinter import *
from tkinter import ttk
from typing import TYPE_CHECKING, Optional

from controller.connection_manager import ConnectionManager
from observer.ui_event import UiEvent
from view.menu_buttons.MenuButton import MenuButtonWidget, BaseMenuButtonImpl
from view.ui_event_manager import UiEventManager
from view.util.FrameUtils import FrameUtils

if TYPE_CHECKING:
    from view.MasterFrame import MasterFrame


class ConnectionDialog:
    """
    Connectiondialog draws a dialog box, and displays it to the user. This box has 3 text fields, and a submit button.
    These fields set the server, username, and password used by the API.
    todo: Add more testing, logging, and error handling, Consider adding a cancel button
    """

    server = ""
    username = ""
    password = ""
    frame = {}

    def __init__(
        self, master_frame: 'MasterFrame', connection_manager: ConnectionManager,event_manager :Optional[UiEventManager] = None
    ):
        if event_manager is None:
            event_manager = UiEventManager()
        self.event_manager = event_manager
        self.master_frame = master_frame
        self.connection_manager = connection_manager
        self.server = StringVar()
        self.username = StringVar()
        self.password = StringVar()
        self.frame = Toplevel()
        FrameUtils.set_icon(self.frame)
        self.frame.title("Configure Connection")
        main_frame = ttk.Frame(self.frame, padding="3 3 12 12")
        main_frame.grid(column=0, row=0, sticky="N, W, E, S")
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)

        ttk.Label(main_frame, text="ArchivesSpace API address", width=30).grid(
            column=1, row=1
        )
        ttk.Label(main_frame, text="API Username", width=30).grid(column=1, row=2)
        ttk.Label(main_frame, text="API Password", width=30).grid(column=1, row=3)

        ttk.Entry(main_frame, width=35, textvariable=self.server).grid(column=2, row=1)
        ttk.Entry(main_frame, width=35, textvariable=self.username).grid(
            column=2, row=2
        )
        ttk.Entry(main_frame, width=35, textvariable=self.password, show="*").grid(
            column=2, row=3
        )
        # Use the close_window method as the button's command
        ttk.Button(
            main_frame, width=70, text="Save and Close", command=self.close_window
        ).grid(column=1, row=4, columnspan=2)

        for child in main_frame.winfo_children():
            child.grid_configure(padx=5, pady=5)
        self.frame.focus_set()
        self.frame.grab_set()

    def close_window(self):
        self.connection_manager.set_connection(
            self.server.get(), self.username.get(), self.password.get()
        )
        self.event_manager.publish_event(
            UiEvent.CONNECTION_CHANGED, {"server": self.server.get()}
        )
        self.frame.destroy()
def create_configure_connection_button(parent, connection_manager, **kwargs) -> MenuButtonWidget:
    """Factory function to create Configure Connection button"""
    impl = ConfigureConnectionButtonImpl(parent, connection_manager)
    return MenuButtonWidget(parent, impl, **kwargs)
class ConfigureConnectionButtonImpl(BaseMenuButtonImpl):
    """Implementation for Configure Connection button"""

    def __init__(self, parent, connection_manager):
        super().__init__(parent, "Configure Connection")
        self.connection_manager = connection_manager
        self._dialog = None

    def on_click(self) -> None:
        """Show connection configuration dialog"""
        if self._dialog and hasattr(self._dialog, 'frame') and self._dialog.frame.winfo_exists():
            self._dialog.frame.lift()
            self._dialog.frame.focus_force()
        else:
            self._dialog = ConnectionDialog(self.parent, self.connection_manager)

