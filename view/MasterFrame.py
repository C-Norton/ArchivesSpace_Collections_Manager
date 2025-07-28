from __future__ import annotations

import logging
import tkinter
from tkinter import ttk

from View import IfBlockFrame, QueryFrame, MenuFrame, RepoFrame
from View.Util.FrameUtils import FrameUtils


class MasterFrame(ttk.Frame):
    """
    Masterframe draws the main application window. Grid layout
    """

    def __init__(self, main: Main.Main):
        logging.debug("Initializing MasterFrame")
        self.root = tkinter.Tk()
        logging.debug(f"Created root: {self.root}")
        super().__init__(self.root)
        self.main = main
        self.root.geometry("950x200")
        logging.debug("About to call set_icon")
        FrameUtils.set_icon(self.root)
        logging.debug("Finished calling set_icon")

        # Set the properties of our main frame

        self.root.title("ArchivesSpace Collections Manager")
        self.repo_frame = RepoFrame.RepoFrame(self)
        self.menu_frame = MenuFrame.MenuFrame(self)
        self.query_frame = QueryFrame.QueryFrame(self)
        self.if_block_frame = IfBlockFrame.IfBlockFrame(self)
        self.pack(fill="both", expand=True)

        logging.debug("UI initialized successfully!")

        self.mainloop()
        self.focus_force()
        logging.info("UI started successfully!")

        logging.debug(f"Icon path used: {icon_path}")
