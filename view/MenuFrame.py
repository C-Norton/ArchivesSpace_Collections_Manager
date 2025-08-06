import logging
from tkinter import ttk, Grid
from typing import Any, Dict

import view.MasterFrame as MasterFrame
from controller.connection_manager import ConnectionManager
from observer import ui_event
from observer.observer import Observer
from observer.subject import SubjectMixin
from observer.ui_event import UiEvent
from view.menu_buttons.ConfigureConnection import create_configure_connection_button
from view.menu_buttons.Help import create_help_button
from view.menu_buttons.ManageConnections import create_manage_connections_button
from view.menu_buttons.SaveConnection import create_save_connection_button
from view.menu_buttons.TestConnection import create_test_connection_button
from view.menu_buttons.RefreshRepositories import create_refresh_repositories_button
from view.menu_buttons.SaveQuery import create_save_query_button, create_load_query_button
from view.ui_event_manager import UiEventManager


class MenuFrame(ttk.Frame, SubjectMixin, Observer):
    """This is the set of buttons at the top row of the UI. I'd love for some stylization here, overall the code works
    well, most of the buttons work at this time, but the query related ones do not"""

    def handle_event(self, event: ui_event, data: Dict[str, Any]) -> None:
        """Handle UI events to update button states"""
        if event == UiEvent.CONNECTION_CHANGED:
            self.refresh_button_states()

    def __init__(
        self,
        parent: MasterFrame,
        connection_manager: ConnectionManager,
        event_manager: UiEventManager = None,
    ):
        super().__init__(master=parent, padding="3 3 12 12")
        self.master_frame = parent
        self.connection_manager = connection_manager
        self.pack(side="top", fill="x")
        logging.debug("Initial frame setup complete")

        # Create buttons using the new factory functions
        self.configure_connection_button = create_configure_connection_button(
            self, connection_manager, width=15
        )

        self.save_connection_button = create_save_connection_button(
            self, connection_manager, width=15
        )
        
        self.manage_saved_connections_button = create_manage_connections_button(
            self, connection_manager, width=15
        )
        
        self.test_connection_button = create_test_connection_button(
            self, connection_manager, width=15
        )
        
        self.save_query_button = create_save_query_button(
            self, None, width=15
        )
        
        self.load_query_button = create_load_query_button(
            self, None, width=15
        )
        
        self.refresh_repositories_button = create_refresh_repositories_button(
            self, self.master_frame.repo_frame, width=15
        )
        
        self.help_button = create_help_button(
            self, width=15
        )

        self.buttons = [
            self.configure_connection_button,
            self.save_connection_button,
            self.manage_saved_connections_button,
            self.test_connection_button,
            self.save_query_button,
            self.load_query_button,
            self.refresh_repositories_button,
            self.help_button,
        ]
        for index, button in enumerate(self.buttons):
            button.grid(column=index, row=0, sticky="EW")


        logging.debug("buttons created")

        # Set up dynamic button resizing
        Grid.rowconfigure(self, index=0, weight=1)
        self.pack(side="top", fill="x")
        for i in range(len(self.buttons)):
            Grid.columnconfigure(self, index=i, weight=1)

        for child in self.winfo_children():
            child.grid_configure(padx=2, pady=5)
        logging.debug("Main self created successfully!")

    def handle_event(self, event: ui_event, data: Dict[str, Any]) -> None:
        """Handle UI events to update button states"""
        if event == UiEvent.CONNECTION_CHANGED:
            self.refresh_button_states()
    
    def refresh_button_states(self):
        """Refresh all button states - call when connection state changes"""
        for button in self.buttons:
            if hasattr(button, 'refresh'):
                button.refresh()
