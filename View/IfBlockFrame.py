from __future__ import annotations

import tkinter
from tkinter import ttk, Grid

from click import command

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
        self.draw_if_block()

    def draw_if_block(self):
        ttk.Label(self, text="If").grid(row=0, column=0)
        self.field = tkinter.StringVar()
        ttk.OptionMenu(
            self, self.field, "id_0", *[e.name for e in Model.ResourceField.ResourceField]
        ).grid(row=0, column=1)
        self.querytype = tkinter.StringVar()
        ttk.OptionMenu(
            self, self.querytype, "EQUALS", *[e.name for e in Model.QueryType.QueryType]
        ).grid(row=0, column=2)
        self.input = tkinter.StringVar()
        ttk.Entry(self, textvariable=self.input, width=35).grid(row=0, column=3)
        ttk.Button(self,text="Add", command = self.query_add).grid(row=0, column=4)
        ttk.Button(self,text="Submit",command=self.submit_query).grid(row=1, column=0, columnspan=5)

    def submit_query(self):
        pass
    def query_add(self):
        pass