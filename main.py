# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from tkinter import *
from tkinter import ttk
from MenuButtons.ConfigureConnection import ConnectionDialog
from Connection import Connection
from MenuButtons.Help import HelpDialog


class CollectionsManagerGui(Tk):

    connection = {}
    def __init__(self):
        buttonwidth = 22

        super().__init__()
        self = self
        self.title("ArchivesSpace Collections Manager")
        mainframe = ttk.Frame(self, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky="N, W, E, S")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)



        ttk.Button(mainframe, text="Configure Connection", width=buttonwidth, command=self.connectionDialog).grid(
            column=1, row=1)
        ttk.Button(mainframe, text="Save Connection", width=buttonwidth).grid(column=2, row=1)
        ttk.Button(mainframe, text="Load Connection", width=buttonwidth).grid(column=3, row=1)
        ttk.Button(mainframe, text="Test Connection", width=buttonwidth, command=self.testConnection).grid(column=4, row=1)
        ttk.Button(mainframe, text="Save Query", width=buttonwidth).grid(column=5, row=1)
        ttk.Button(mainframe, text="Load Query", width=buttonwidth).grid(column=6, row=1)
        ttk.Button(mainframe, text="Help", width=buttonwidth, command=self.helpButton).grid(column=7, row=1)
        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)
        self.mainloop()
        self.focus_force()


    def connectionDialog(self):
        ConnectionDialog(self)
    def testConnection(self):
        test = Connection(self.connection.get("server"),self.connection.get("username"),self.connection.get("password"))
        testconn = test.test()
    def helpButton(self):
        HelpDialog(self)
if __name__ == "__main__":
    app = CollectionsManagerGui()
    app.mainloop()
