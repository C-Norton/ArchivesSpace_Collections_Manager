import tkinter
import logging
from tkinter import ttk
from Controller.ConnectionManager import *
from Model.DataModel import *
import View.MenuFrame
from View import RepoFrame


class MasterFrame:
    def __init__(self,main):
        self.main = main
        self.root = tkinter.Tk()
        self.root.geometry("950x200")
        self.masterFrame = ttk.Frame()
        logging.debug("Frame Created")

        # Set the properties of our main frame
        self.masterFrame.pack(fill="both", expand=True)
        self.root.title("ArchivesSpace Collections Manager")

        View.MenuFrame.drawMenuFrame(ttk.Frame(self.masterFrame, padding="3 3 12 12"))
        self.RepoFrame = RepoFrame.RepoFrame(self)
        self.RepoFrame.pack(side="bottom",fill="x")
        # Start setting up the lower portion of our window
        queryRegion = ttk.Frame(self.masterFrame, padding="3 3 12 12")
        queryRegion.pack(side="bottom", fill='x')
        ttk.Label(queryRegion, text="foo").grid(column=1, row=1)

        for child in queryRegion.winfo_children():
            child.grid_configure(padx=5, pady=5)
        logging.debug("UI initialized successfully!")

        self.masterFrame.mainloop()
        self.masterFrame.focus_force()
        logging.info("UI started successfully!")