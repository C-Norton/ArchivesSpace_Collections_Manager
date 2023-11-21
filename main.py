# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import tkinter
import logging
from tkinter import *
from tkinter import ttk
from MenuButtons.ConfigureConnection import ConnectionDialog
from MenuButtons.TestConnection import TestConnection
from Connection import Connection
from MenuButtons.Help import HelpDialog
from MenuButtons.SaveConnection import SaveConnection


class CollectionsManagerGui():
    connection = {}

    def __init__(self):
        root = tkinter.Tk()
        root.geometry("750x200")
        masterFrame = ttk.Frame()
        logging.debug("Frame Created")

        self.connection = Connection("", "", "")

        # Set the properties of our main frame
        masterFrame.pack(fill="both", expand=True)
        root.title("ArchivesSpace Collections Manager")
        menu = ttk.Frame(masterFrame, padding="3 3 12 12")
        menu.pack(side="top", fill='x')
        logging.debug("Initial frame setup complete")

        # Create top menu
        Buttons = [
            ttk.Button(menu, text="Configure Connection", command=self.connectionDialog).grid(column=0, row=0,
                                                                                              sticky="EW"),
            ttk.Button(menu, text="Save Connection", command=self.saveConnection).grid(column=1, row=0, sticky="EW"),
            ttk.Button(menu, text="Manage Saved Connections").grid(column=2, row=0, sticky="EW"),
            ttk.Button(menu, text="Test Connection", command=self.testConnection).grid(column=3, row=0, sticky="EW"),
            ttk.Button(menu, text="Save Query").grid(column=4, row=0, sticky="EW"),
            ttk.Button(menu, text="Load Query").grid(column=5, row=0, sticky="EW"),
            ttk.Button(menu, text="Refresh Repositories").grid(column=6, row=0, sticky="EW"),
            ttk.Button(menu, text="Help", command=self.helpButton).grid(column=7, row=0, sticky="EW")]

        logging.debug("buttons created")

        # Set up dynamic button resizing
        Grid.rowconfigure(menu, index=0, weight=1)
        for i in range(len(Buttons)):
            Grid.columnconfigure(menu, index=i, weight=1)

        for child in menu.winfo_children():
            child.grid_configure(padx=2, pady=5)
        logging.debug("Main menu created successfully!")

        # Start setting up the lower portion of our window
        queryRegion = ttk.Frame(masterFrame, padding="3 3 12 12")
        queryRegion.pack(side="bottom", fill='x')
        ttk.Label(queryRegion, text="foo").grid(column=1, row=1)

        for child in queryRegion.winfo_children():
            child.grid_configure(padx=5, pady=5)
        logging.debug("UI initialized successfully!")

        masterFrame.mainloop()
        masterFrame.focus_force()
        logging.info("UI started successfully!")

    # These functions here serve as connectors to the appropriate class. This can likely be avoided
    def connectionDialog(self):
        ConnectionDialog(self)


    def testConnection(self):
        test = Connection(self.connection.server, self.connection.username, self.connection.password)
        TestConnection(self, test)

    def helpButton(self):
        HelpDialog(self)

    def saveConnection(self):
        SaveConnection(self.connection)


if __name__ == "__main__":
    # logging.basicConfig(level=logging.DEBUG, format=f'[{levelname}] {asctime} - {message}')
    app = CollectionsManagerGui()
    app.mainloop()
