from __future__ import annotations

import logging
import os
import tkinter
from tkinter import ttk
from PIL import Image, ImageTk
from View import IfBlockFrame, QueryFrame, MenuFrame, RepoFrame


class MasterFrame(ttk.Frame):
    def __init__(self, main: Main.Main):
        self.root = tkinter.Tk()
        super().__init__()
        self.main = main
        self.root.geometry("950x200")
        project_root = os.path.dirname(os.path.abspath(__file__))[:-4]
        icon_path = os.path.join(
            project_root,
            "Public",
            "Icons",
            "ArchivesSpace_Collections_Manager-32x32.ico",
        )
        self.set_icon(icon_path)
        logging.debug("Frame Created")

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
    def set_icon(self, icon_path):
        if not os.path.exists(icon_path):
            logging.error(f"Icon file not found: {icon_path}")
            return

        try:
            # Try using iconbitmap first
            self.root.iconbitmap(icon_path)
            logging.debug("Icon set successfully using iconbitmap")
        except tkinter.TclError as e:
            logging.warning(f"Failed to set icon using iconbitmap: {e}")

            try:
                # If iconbitmap fails, try using PhotoImage
                icon = tkinter.PhotoImage(file=icon_path)
                self.root.iconphoto(False, icon)
                logging.debug("Icon set successfully using PhotoImage")
            except tkinter.TclError as e:
                logging.warning(f"Failed to set icon using PhotoImage: {e}")

                try:
                    # If both methods fail, try using PIL
                    icon = Image.open(icon_path)
                    photo = ImageTk.PhotoImage(icon)
                    self.root.iconphoto(False, photo)
                    logging.debug("Icon set successfully using PIL")
                except Exception as e:
                    logging.error(f"Failed to set icon using all methods: {e}")

        logging.debug(f"Icon path used: {icon_path}")