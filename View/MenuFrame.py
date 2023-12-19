import logging
from tkinter import ttk, Grid

from Controller.Connection import Connection
import View.MasterFrame as MasterFrame
from View.MenuButtons.ConfigureConnection import ConnectionDialog
from View.MenuButtons.Help import HelpDialog
from View.MenuButtons.ManageConnection import ManageConnections
from View.MenuButtons.SaveConnection import SaveConnection
from View.MenuButtons.TestConnection import TestConnection
from View.RepoFrame import RepoFrame


class MenuFrame(ttk.Frame):
    def __init__(self, parent: MasterFrame):
        super().__init__(master=parent, padding="3 3 12 12")
        self.masterframe = parent
        self.pack(side="top", fill="x")
        logging.debug("Initial frame setup complete")

        # Create top self
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
                command=self.masterframe.RepoFrame.refresh,
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
        ConnectionDialog(self.masterframe)

    def testConnection(self):
        TestConnection(self.masterframe.main.connectionmanager.connection)

    def helpButton(self):
        HelpDialog()

    def saveConnection(self):
        SaveConnection(self.masterframe.main.connectionmanager.connection)

    def manageConnections(self):
        ManageConnections(self.masterframe.main.connectionmanager)

    # These functions here serve as connectors to the appropriate class. This can likely be avoided
