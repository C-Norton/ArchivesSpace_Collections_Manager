from __future__ import annotations
import tkinter
import logging
from tkinter import ttk
import platform


from View import MenuFrame
from View import IfBlockFrame
from View import RepoFrame


class MasterFrame(ttk.Frame):
    def __init__(self, main: Main.Main):
        self.root = tkinter.Tk()
        super().__init__()
        self.main = main
        self.root.geometry("950x200")
        if platform.system() == "Windows":
            self.root.iconbitmap("Public/Icons/ArchivesSpace_Collections_Manager-32x32.ico")
        elif platform.system()=="Linux":
            self.root.iconphoto(True,tkinter.PhotoImage("Public/Icons/ArchivesSpace_Collections_Manager-32x32.gif"))
        logging.debug("Frame Created")

        # Set the properties of our main frame

        self.root.title("ArchivesSpace Collections Manager")
        self.RepoFrame = RepoFrame.RepoFrame(self)
        self.menuframe = MenuFrame.MenuFrame(self)
        self.IfBlockFrame = IfBlockFrame.IfBlockFrame(self)
        self.pack(fill="both", expand=True)

        logging.debug("UI initialized successfully!")

        self.mainloop()
        self.focus_force()
        logging.info("UI started successfully!")
