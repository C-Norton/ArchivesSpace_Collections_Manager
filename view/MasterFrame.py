from __future__ import annotations

import logging
import tkinter
from tkinter import ttk


from controller.connection_manager import ConnectionManager
from view import IfBlockFrame, QueryFrame, MenuFrame, RepoFrame
from view.util.FrameUtils import FrameUtils


class MasterFrame(ttk.Frame):
    """
    Masterframe draws the main application window. Grid layout
    """

    def __init__(self,connection_manager: ConnectionManager):
        logging.debug("Initializing MasterFrame")
        self.root = tkinter.Tk()
        logging.debug(f"Created root: {self.root}")
        super().__init__(self.root)
        self.root.geometry("950x200")
        logging.debug("About to call set_icon")
        FrameUtils.set_icon(self.root)
        logging.debug("Finished calling set_icon")
        self.connection_manager = connection_manager
        # Set the properties of our main frame

        self.root.title("ArchivesSpace Collections Manager")
        self.repo_frame = RepoFrame.RepoFrame(self)
        self.menu_frame = MenuFrame.MenuFrame(self,self.connection_manager)
        self.query_frame = QueryFrame.QueryFrame(self)
        self.if_block_frame = IfBlockFrame.IfBlockFrame(self)
        self.pack(fill="both", expand=True)

        logging.debug("UI initialized successfully!")

        self.mainloop()
        self.focus_force()
        logging.info("UI started successfully!")

        logging.debug(f"Icon path used: {icon_path}")
