from tkinter import *
from tkinter import ttk


class ConnectionDialog(ttk.Frame):
    server = ""
    username = ""
    password = ""
    frame = {}
    parent = {}
    def __init__(self, parent):
        self.parent = parent
        self.server = StringVar()
        self.username = StringVar()
        self.password = StringVar()
        super().__init__()
        connectionWindow = Toplevel(parent)
        self.frame = connectionWindow
        connectionWindow.title("Configure Connection")
        mainframe = ttk.Frame(connectionWindow, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky="N, W, E, S")
        connectionWindow.columnconfigure(0, weight=1)
        connectionWindow.rowconfigure(0, weight=1)

        ttk.Label(mainframe,text="ArchivesSpace API address",width= 30).grid(column=1, row=1)
        ttk.Label(mainframe,text="API Username",width= 30).grid(column=1, row=2)
        ttk.Label(mainframe,text="API Password",width= 30).grid(column=1, row=3)

        ttk.Entry(mainframe, width=35, textvariable=self.server).grid(column=2, row=1)
        ttk.Entry(mainframe, width=35, textvariable=self.username).grid(column=2, row=2)
        ttk.Entry(mainframe, width=35, textvariable=self.password).grid(column=2, row=3)
        ttk.Button(mainframe, width=70,text="Save and Close",command=self.closeWindow).grid(column=1,row=4,columnspan=2)

        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)
        connectionWindow.focus_set()
        connectionWindow.grab_set()

    def closeWindow(self):
        self.parent.Connection = (self.server.get(), self.username.get(), self.password.get())
        self.destroy()
        ttk.Frame.destroy(self.frame)