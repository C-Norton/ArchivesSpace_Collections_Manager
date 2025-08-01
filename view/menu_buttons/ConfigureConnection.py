from __future__ import annotations
from tkinter import *
from tkinter import ttk

from controller.connection_manager import ConnectionManager
from view import MasterFrame
from view.util.FrameUtils import FrameUtils


class ConnectionDialog:
    """
    Connectiondialog draws a dialog box, and displays it to the user. This box has 3 text fields, and a submit button.
    These fields set the server, username, and password used by the API.
    todo: Add more testing, logging, and error handling, Consider adding a cancel button
    """

    server = ""
    username = ""
    password = ""
    frame = {}

    def __init__(
        self, master_frame: MasterFrame, connection_manager: ConnectionManager
    ):
        self.master_frame = master_frame
        self.connection_manager = connection_manager
        self.server = StringVar()
        self.username = StringVar()
        self.password = StringVar()
        self.frame = Toplevel()
        FrameUtils.set_icon(self.frame)
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
        ttk.Entry(main_frame, width=35, textvariable=self.username).grid(
            column=2, row=2
        )
        ttk.Entry(main_frame, width=35, textvariable=self.password, show="*").grid(
            column=2, row=3
        )
        ttk.Button(
            main_frame, width=70, text="Save and Close", command=self.close_window
        ).grid(column=1, row=4, columnspan=2)

        for child in main_frame.winfo_children():
            child.grid_configure(padx=5, pady=5)
        self.frame.focus_set()
        self.frame.grab_set()

    def close_window(self):
        self.connection_manager.set_connection(
            self.server.get(), self.username.get(), self.password.get()
        )
        self.frame.destroy()
