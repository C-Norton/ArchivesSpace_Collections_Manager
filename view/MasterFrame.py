from __future__ import annotations

import logging
import tkinter
from tkinter import ttk
from typing import Optional

from controller.connection_manager import ConnectionManager
from view import IfBlockFrame, QueryFrame, MenuFrame, RepoFrame
from view.action_submit_frame import ActionSubmitFrame
from view.connection_frame import ConnectionFrame
from view.ui_event_manager import UiEventManager
from view.util.FrameUtils import FrameUtils


class MasterFrame(ttk.Frame):
    """
    Masterframe draws the main application window. Grid layout
    """

    def __init__(self, connection_manager: ConnectionManager, event_manager: Optional[UiEventManager] = None):
        if event_manager is None:
            event_manager = UiEventManager()
        self.event_manager = event_manager

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
        self.menu_frame = MenuFrame.MenuFrame(self, self.connection_manager)
        self.query_frame = QueryFrame.QueryFrame(self)
        self.if_block_frame = IfBlockFrame.IfBlockFrame(self)
        self.action_submit_frame = ActionSubmitFrame(self)
        self.connection_frame = ConnectionFrame(self, self.event_manager)



        # Position all frames in the master frame
        self.menu_frame.pack(side="top", fill="x")
        self.connection_frame.pack(side="top", fill="x")
        self.if_block_frame.pack(side="top", fill="x")
        self.action_submit_frame.pack(side="bottom", fill="x")
        self.query_frame.pack(side="bottom", fill="x")
        self.repo_frame.pack(side="bottom", fill="x")
        
        # Pack the master frame itself
        self.pack(fill="both", expand=True)

        logging.debug("UI initialized successfully!")

        self.focus_force()
        self.mainloop()
        logging.info("UI started successfully!")
