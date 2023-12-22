from __future__ import annotations

import tkinter
from tkinter import ttk, Grid

import Model.ResourceField


# this will need to be a grid type
class IfBlockFrame(ttk.Frame):
    def __init__(self, parent: MasterFrame):
        super().__init__(master=parent, padding="3 3 12 12")
        self.masterframe = parent
        self.pack(side="bottom", fill="x")
        self.width = 1
        self.height = 1
        self.drawIfBlock()

    def drawIfBlock(self):
        ttk.Label(self,text="If").grid(row=0, column = 0)
        foo = tkinter.StringVar()
        ttk.OptionMenu(self,foo,"id_0",*[e.name for e in Model.ResourceField.ResourceField]).grid(row=0,column=1)
