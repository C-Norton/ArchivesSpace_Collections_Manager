# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import tkinter
from tkinter import *
from tkinter import ttk
from MenuButtons.ConfigureConnection import ConnectionDialog
from MenuButtons.TestConnection import TestConnection
from Connection import Connection
from MenuButtons.Help import HelpDialog
from MenuButtons.SaveConnection import SaveConnection


class CollectionsManagerGui(Tk):

    connection = {}
    def __init__(self):
        root = tkinter.Tk()
        masterFrame = ttk.Frame(root)
        buttonwidth = 22
        masterFrame.connection = Connection("","","")


        masterFrame.pack(fill="both", expand=True)

        root.title("ArchivesSpace Collections Manager")
        menu = ttk.Frame(masterFrame, padding="3 3 12 12")
        menu.pack(side="top",fill='x')

        ttk.Button(menu, text="Configure Connection", command=self.connectionDialog).pack(side="left", fill="both",expand=1)
        ttk.Button(menu, text="Save Connection", command=self.saveConnection).pack(side="left", fill="both",expand=1)
        ttk.Button(menu, text="Load Connection").pack(side="left", fill="both",expand=1)
        ttk.Button(menu, text="Test Connection", command=self.testConnection).pack(side="left", fill="both",expand=1)
        ttk.Button(menu, text="Save Query").pack(side="left", fill="both",expand=1)
        ttk.Button(menu, text="Load Query").pack(side="left", fill="both",expand=1)
        ttk.Button(menu, text="Help", command=self.helpButton).pack(side="left", fill="both",expand=1)

        queryRegion = ttk.Frame(masterFrame,padding="3 3 12 12")
        queryRegion.pack(side="bottom",fill='x')
        ttk.Label(queryRegion,text="foo").grid(column=1,row=1)
        
        for child in queryRegion.winfo_children():
            child.grid_configure(padx=5, pady=5)

        masterFrame.mainloop()
        masterFrame.focus_force()


    def connectionDialog(self):
        ConnectionDialog(self)
    def testConnection(self):
        test = Connection(self.connection.server,self.connection.username,self.connection.password)
        TestConnection(self,test)
    def helpButton(self):
        HelpDialog(self)
    def saveConnection(self):
        SaveConnection(self, self.connection)
if __name__ == "__main__":
    app = CollectionsManagerGui()
    app.mainloop()
