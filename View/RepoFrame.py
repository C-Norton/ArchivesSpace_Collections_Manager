import tkinter
from tkinter import ttk

import View.MasterFrame as MasterFrame
class RepoFrame(ttk.Frame):
    def __init__(self,masterframe:MasterFrame):
        super().__init__(master=masterframe.masterFrame, padding="3 3 12 12")
        self.masterframe = masterframe


    def refresh(self):
        if self.masterframe.main.initialized:
            repos = self.masterframe.main.datamodel.getRepositories()
            checkbuttons = dict()
            i = 0
            for repo in repos:
                checkvar = tkinter.IntVar()
                checkbuttons.update({repo[0], (checkvar,
                                               ttk.Checkbutton(self, text=repo[1]["name"], variable=checkvar,
                                                               onvalue=1, offvalue=0).grid(column=i % 3, row=i // 3))})
                i += 1
            for child in self.winfo_children():
                child.grid_configure(padx=2, pady=5)