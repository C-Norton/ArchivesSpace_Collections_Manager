from __future__ import annotations

import tkinter
from tkinter import ttk

import Model.QueryType
import Model.ResourceField
from Model import OperatorNode


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
        field = tkinter.StringVar()
        ttk.OptionMenu(
            self, field, "id_0", *[e.name for e in Model.ResourceField.ResourceField]
        ).grid(row=0, column=1)
        querytype = tkinter.StringVar()
        ttk.OptionMenu(
            self, querytype, "EQUALS", *[e.name for e in Model.QueryType.QueryType]
        ).grid(row=0, column=2)
        input = tkinter.StringVar()
        ttk.Entry(self, textvariable=input, width=35).grid(row=0, column=3)

    """
    drawline needs a few items to be drawn
    1, an indentation level of a given number of spaces
    2, EITHER the data (spanning multiple columns, with edit dropdowns) OR the boolean operator (also spanning multiple columns)
    3, A data entry field (spanning multiple columns) ONLY WHERE RELEVANT
    BEGIN RIGHT JUSTIFICATION (still using left to right ordering)
    4, A button to invert the operation this node represents
    5, A button to delete this node (Question, how does this get handled for deleting an operator node? Does this button appear?)
    6, A button to create a new node at one level of depth above
    7, A button to create a new node at this same level of depth
    8, A button to create a new node below this node at the same level.
    
    6-8 determine the rules for when each of these buttons should be drawn so that there's exactly one button to create
    a node at any given height
    
    After a loop of drawline calls, the display should be good to go, save for a button to create a new node at the bottom
    
    """

    def draw_line(self, row: int, data: tuple, maxdepth: int):
        offset = data[1]
        if isinstance(data[2], OperatorNode.OperatorNode):
            pass
        else:
            field = tkinter.StringVar()
            ttk.OptionMenu(
                self, field, data[0][0].name, *[e.name for e in Model.ResourceField.ResourceField]
            ).grid(row=row, column=offset)
            querytype = tkinter.StringVar()
            ttk.OptionMenu(
                self, querytype, data[0][1], *[e.name for e in Model.QueryType.QueryType]
            ).grid(row=row, column=offset+1)




