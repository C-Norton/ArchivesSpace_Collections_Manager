# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import logging
import tkinter
from tkinter import ttk

import Frames.MenuFrame
from Connection import Connection
from Frames.MenuButtons.ConfigureConnection import ConnectionDialog
from Frames.MenuButtons.Help import HelpDialog
from Frames.MenuButtons.SaveConnection import SaveConnection
from Frames.MenuButtons.TestConnection import TestConnection


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

        Frames.MenuFrame.drawMenuFrame(ttk.Frame(masterFrame, padding="3 3 12 12"))

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
    logging.basicConfig(level=logging.DEBUG)
    app = CollectionsManagerGui()
    app.mainloop()
