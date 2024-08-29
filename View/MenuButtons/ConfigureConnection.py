from __future__ import annotations
from tkinter import *
from tkinter import ttk
from View import MasterFrame

class ConnectionDialog:
    server = ""
    username = ""
    password = ""
    frame = {}

    def __init__(self, MasterFrame: MasterFrame):
        self.master_frame = MasterFrame
        self.server = StringVar()
        self.username = StringVar()
        self.password = StringVar()
        self.frame = Toplevel()
        self.frame.title("Configure Connection")
        main_frame = ttk.Frame(self.frame, padding="3 3 12 12")
        main_frame.grid(column=0, row=0, sticky="N, W, E, S")
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)

        ttk.Label(main_frame, text="ArchivesSpace API address", width=30).grid(
            column=1, row=1
        )
        ttk.Label(main_frame, text="API Username", width=30).grid(column=1, row=2)
        ttk.Label(main_frame, text="API Password", width=30).grid(column=1, row=3)

        ttk.Entry(main_frame, width=35, textvariable=self.server).grid(column=2, row=1)
        ttk.Entry(main_frame, width=35, textvariable=self.username).grid(column=2, row=2)
        ttk.Entry(main_frame, width=35, textvariable=self.password, show="*").grid(
            column=2, row=3
        )
        ttk.Button(
            main_frame, width=70, text="Save and Close", command=self.closeWindow
        ).grid(column=1, row=4, columnspan=2)

        for child in main_frame.winfo_children():
            child.grid_configure(padx=5, pady=5)
        self.frame.focus_set()
        self.frame.grab_set()

    def closeWindow(self):
        self.master_frame.main.connectionmanager.connection.server = self.server.get()
        self.master_frame.main.connectionmanager.connection.username = (
            self.username.get()
        )
        self.master_frame.main.connectionmanager.connection.password = (
            self.password.get()
        )

        ttk.Frame.destroy(self.frame)
