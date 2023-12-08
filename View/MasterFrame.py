import tkinter
import logging
from tkinter import ttk
from Controller.ConnectionManager import *
from Model.DataModel import *
from View import MenuFrame
from View import RepoFrame


class MasterFrame(ttk.Frame):
    def __init__(self, main):
        self.root = tkinter.Tk()
        super().__init__()
        self.main = main
        self.root.geometry("950x200")
        logging.debug("Frame Created")

        # Set the properties of our main frame

        self.root.title("ArchivesSpace Collections Manager")
        self.RepoFrame = RepoFrame.RepoFrame(self)
        self.menuframe = MenuFrame.MenuFrame(self)

        self.pack(fill="both", expand=True)

        logging.debug("UI initialized successfully!")


        self.mainloop()
        self.focus_force()
        logging.info("UI started successfully!")