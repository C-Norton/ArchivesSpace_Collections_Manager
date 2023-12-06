import logging
from tkinter import ttk, Grid

from Controller.Connection import Connection
import View.MasterFrame as MasterFrame
from View.MenuButtons.ConfigureConnection import ConnectionDialog
from View.MenuButtons.Help import HelpDialog
from View.MenuButtons.SaveConnection import SaveConnection
from View.MenuButtons.TestConnection import TestConnection
from View.RepoFrame import RepoFrame

class MenuFrame(ttk.Frame):
    def __init__(self, masterframe: MasterFrame):
        super().__init__()
        self.masterframe = masterframe
        menu = ttk.Frame(self.masterframe,padding="3 3 12 12")
        menu.pack(side="top", fill='x')
        logging.debug("Initial frame setup complete")

        # Create top menu
        Buttons = [
            ttk.Button(menu, text="Configure Connection", command=connectionDialog).grid(
                column=0, row=0,
                sticky="EW"),
            ttk.Button(menu, text="Save Connection", command=saveConnection).grid(column=1,
                                                                                  row=0,
                                                                                  sticky="EW"),
            ttk.Button(menu, text="Manage Saved Connections").grid(column=2, row=0, sticky="EW"),
            ttk.Button(menu, text="Test Connection", command=testConnection).grid(column=3,
                                                                                  row=0,
                                                                                  sticky="EW"),
            ttk.Button(menu, text="Save Query").grid(column=4, row=0, sticky="EW"),
            ttk.Button(menu, text="Load Query").grid(column=5, row=0, sticky="EW"),
            ttk.Button(menu, text="Refresh Repositories", command=self.masterframe.RepoFrame.refresh()).grid(column=6, row=0, sticky="EW"),
            ttk.Button(menu, text="Help", command=helpButton).grid(column=7, row=0, sticky="EW")]

        logging.debug("buttons created")

        # Set up dynamic button resizing
        Grid.rowconfigure(menu, index=0, weight=1)
        for i in range(len(Buttons)):
            Grid.columnconfigure(menu, index=i, weight=1)

        for child in menu.winfo_children():
            child.grid_configure(padx=2, pady=5)
        logging.debug("Main menu created successfully!")

def connectionDialog():
    ConnectionDialog()


def testConnection():
    test = Connection(Connection.server, Connection.username, Connection.password)
    TestConnection(test)


def helpButton():
    HelpDialog()


def saveConnection():
    SaveConnection()

    # These functions here serve as connectors to the appropriate class. This can likely be avoided
