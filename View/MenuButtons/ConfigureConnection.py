from __future__ import annotations
from tkinter import *
from tkinter import ttk


class ConnectionDialog:
    server = ""
    username = ""
    password = ""
    frame = {}

    def __init__(self, MasterFrame: MasterFrame):
        self.masterframe = MasterFrame
        self.server = StringVar()
        self.username = StringVar()
        self.password = StringVar()
        self.frame = Toplevel()
        self.frame.title("Configure Connection")
        mainframe = ttk.Frame(self.frame, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky="N, W, E, S")
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)

        ttk.Label(mainframe, text="ArchivesSpace API address", width=30).grid(
            column=1, row=1
        )
        ttk.Label(mainframe, text="API Username", width=30).grid(column=1, row=2)
        ttk.Label(mainframe, text="API Password", width=30).grid(column=1, row=3)

        ttk.Entry(mainframe, width=35, textvariable=self.server).grid(column=2, row=1)
        ttk.Entry(mainframe, width=35, textvariable=self.username).grid(column=2, row=2)
        ttk.Entry(mainframe, width=35, textvariable=self.password, show="*").grid(
            column=2, row=3
        )
        ttk.Button(
            mainframe, width=70, text="Save and Close", command=self.close_window
        ).grid(column=1, row=4, columnspan=2)

        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)
        self.frame.focus_set()
        self.frame.grab_set()

    def close_window(self):
        self.masterframe.main.connectionmanager.connection.server = self.server.get()
        self.masterframe.main.connectionmanager.connection.username = (
            self.username.get()
        )
        self.masterframe.main.connectionmanager.connection.password = (
            self.password.get()
        )

        ttk.Frame.destroy(self.frame)
