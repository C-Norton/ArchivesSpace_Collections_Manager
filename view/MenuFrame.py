import logging
import tkinter
from tkinter import ttk, Grid

import view.MasterFrame as MasterFrame
from controller.connection_manager import ConnectionManager
from view.menu_buttons.ConfigureConnection import ConnectionDialog
from view.menu_buttons.Help import HelpDialog
from view.menu_buttons.ManageConnections import ManageConnections
from view.menu_buttons.SaveConnection import save_connection
from view.menu_buttons.TestConnection import TestConnection

class UpdatedMenuFrame(ttk.Frame):
    """
    Example showing how MenuFrame would be updated to use the new button system.
    """

    def __init__(self, parent, connection_manager:ConnectionManager):
        super().__init__(master=parent, padding="3 3 12 12")
        self.master_frame = parent
        self.pack(side="top", fill="x")

        # Create button instances
        self.configure_conn_btn = ConfigureConnectionButton(self.master_frame)
        self.save_conn_btn = SaveConnectionButton(self.master_frame)
        self.manage_conn_btn = ManageConnectionsButton(self.master_frame)
        self.test_conn_btn = TestConnectionButton(self.master_frame)
        self.help_btn = HelpButton(self.master_frame)

        # TODO: When mediator pattern is implemented, set mediator for all buttons:
        # mediator = SomeMediator()
        # for button in [self.configure_conn_btn, self.save_conn_btn, ...]:
        #     button.set_mediator(mediator)

        # Create UI buttons that trigger the actions
        buttons = [
            ttk.Button(self, text="Configure Connection",
                       command=self.configure_conn_btn.show_dialog),
            ttk.Button(self, text="Save Connection",
                       command=self.save_conn_btn.execute_and_show_result),
            ttk.Button(self, text="Manage Saved Connections",
                       command=self.manage_conn_btn.execute_and_show_result),
            ttk.Button(self, text="Test Connection",
                       command=self.test_conn_btn.execute_and_show_result),
            ttk.Button(self, text="Save Query"),  # TODO: Implement
            ttk.Button(self, text="Load Query"),  # TODO: Implement
            ttk.Button(self, text="Refresh Repositories",
                       command=self.master_frame.repo_frame.refresh),
            ttk.Button(self, text="Help",
                       command=self.help_btn.execute_and_show_result),
        ]

        # Grid layout
        for i, button in enumerate(buttons):
            button.grid(column=i, row=0, sticky="EW", padx=2, pady=5)
            self.columnconfigure(i, weight=1)
class MenuFrame(ttk.Frame):
    """This is the set of buttons at the top row of the UI. I'd love for some stylization here, overall the code works
    well, most of the buttons work at this time, but the query related ones do not"""

    def __init__(self, parent: MasterFrame,connection_manager:ConnectionManager):
        super().__init__(master=parent, padding="3 3 12 12")
        self.master_frame = parent
        self.connection_manager = connection_manager
        self.pack(side="top", fill="x")
        logging.debug("Initial frame setup complete")

        # Create top shelf
        Buttons = [
            ttk.Button(
                self, text="Configure Connection", command=self.connectionDialog
            ).grid(column=0, row=0, sticky="EW"),
            ttk.Button(self, text="Save Connection", command=self.saveConnection).grid(
                column=1, row=0, sticky="EW"
            ),
            ttk.Button(
                self, text="Manage Saved Connections", command=self.manageConnections
            ).grid(column=2, row=0, sticky="EW"),
            ttk.Button(self, text="Test Connection", command=self.testConnection).grid(
                column=3, row=0, sticky="EW"
            ),
            ttk.Button(self, text="Save Query").grid(column=4, row=0, sticky="EW"),
            ttk.Button(self, text="Load Query").grid(column=5, row=0, sticky="EW"),
            ttk.Button(
                self,
                text="Refresh Repositories",
                command=self.master_frame.repo_frame.refresh,
            ).grid(column=6, row=0, sticky="EW"),
            ttk.Button(self, text="Help", command=self.helpButton).grid(
                column=7, row=0, sticky="EW"
            ),
        ]

        logging.debug("buttons created")

        # Set up dynamic button resizing
        Grid.rowconfigure(self, index=0, weight=1)
        self.pack(side="top", fill="x")
        for i in range(len(Buttons)):
            Grid.columnconfigure(self, index=i, weight=1)

        for child in self.winfo_children():
            child.grid_configure(padx=2, pady=5)
        logging.debug("Main self created successfully!")

    def connectionDialog(self):
        ConnectionDialog(self.master_frame,self.connection_manager)

    def testConnection(self):
        TestConnection(self.connection_manager.connection)

    def helpButton(self):
        HelpDialog(self.master_frame)

    def saveConnection(self):
        save_connection(self.connection_manager.connection)

    def manageConnections(self):
        connection_management_pane = ManageConnections(self.master_frame,self.connection_manager)
        connection_management_pane.on_click()
    # These functions here serve as connectors to the appropriate class. This can likely be avoided
