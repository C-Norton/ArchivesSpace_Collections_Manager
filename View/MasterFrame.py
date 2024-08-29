from __future__ import annotations

import logging
import os
import tkinter
from tkinter import ttk

from View import IfBlockFrame, QueryFrame, MenuFrame, RepoFrame


class MasterFrame(ttk.Frame):
    def __init__(self, main: Main.Main):
        self.root = tkinter.Tk()
        super().__init__()
        self.main = main
        self.root.geometry("950x200")
        project_root = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(project_root, "Public", "Icons",
                                 "ArchivesSpace_Collections_Manager-32x32.ico")
        try:
            self.root.iconbitmap(icon_path)

        except Exception as e:
            logging.debug(f"Error setting icon: {e}")
        logging.debug("Frame Created")

        # Set the properties of our main frame

        self.root.title("ArchivesSpace Collections Manager")
        self.RepoFrame = RepoFrame.RepoFrame(self)
        self.menuframe = MenuFrame.MenuFrame(self)
        self.queryframe = QueryFrame.QueryFrame(self)
        self.IfBlockFrame = IfBlockFrame.IfBlockFrame(self)
        self.pack(fill="both", expand=True)

        logging.debug("UI initialized successfully!")

        self.mainloop()
        self.focus_force()
        logging.info("UI started successfully!")
