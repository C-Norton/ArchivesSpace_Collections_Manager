import tkinter
import logging
from tkinter import ttk
from Controller.ConnectionManager import *
from Model.DataModel import *
from View import MenuFrame
from View import RepoFrame


class MasterFrame(ttk.Frame):
    def __init__(self, main):

        super().__init__()
        self.main = main
        self.root = tkinter.Tk()
        self.root.geometry("950x200")
        self.masterFrame = ttk.Frame()
        logging.debug("Frame Created")

        # Set the properties of our main frame
        self.masterFrame.pack(fill="both", expand=True)
        self.root.title("ArchivesSpace Collections Manager")
        self.RepoFrame = RepoFrame.RepoFrame(self)
        self.menuframe = MenuFrame.MenuFrame(self)
        self.menuframe.pack(side="bottom",fill="x")
        self.RepoFrame.pack(side="bottom",fill="x")


        logging.debug("UI initialized successfully!")

        self.masterFrame.mainloop()
        self.masterFrame.focus_force()
        logging.info("UI started successfully!")