
from tkinter import ttk
from typing import TYPE_CHECKING, Dict, Any

from observer.ui_event import UiEvent
from view.ui_event_manager import UiEventManager

if TYPE_CHECKING:
    from view.MasterFrame import MasterFrame


class ConnectionFrame(ttk.Frame):

    def __init__(self, parent: ttk.Frame, event_manager: UiEventManager = None):
        super().__init__(master=parent, padding="3 3 12 12")
        self.master_frame = parent
        if event_manager is None:
            event_manager = UiEventManager()
        self.event_manager = event_manager
        self.event_manager.attach(self)
        self.connection_label = ttk.Label(self, text="No server connection")
        self.connection_label.pack(side="right")

    def handle_event(self, event, data: Dict[str, Any]):
        if event == UiEvent.CONNECTION_CHANGED:
            if data["server"] is None:
                self.connection_label.configure(text="gNo server connection")
                return
            self.connection_label.configure(text=f"Connected to {data["server"]}")


