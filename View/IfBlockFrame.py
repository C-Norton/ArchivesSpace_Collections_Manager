from __future__ import annotations

import tkinter
from tkinter import ttk, Grid

import Model.ResourceField
import Model.QueryType

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
        field = tkinter.StringVar()
        ttk.OptionMenu(self,field,"id_0",*[e.name for e in Model.ResourceField.ResourceField]).grid(row=0,column=1)
        querytype = tkinter.StringVar()
        ttk.OptionMenu(self,querytype,"EQUALS",*[e.name for e in Model.QueryType.QueryType]).grid(row=0,column=2)
        input = tkinter.StringVar()
        ttk.Entry(self,textvariable=input, width=35).grid(row=0,column=3)