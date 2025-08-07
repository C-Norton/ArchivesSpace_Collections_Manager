from __future__ import annotations

import tkinter
from tkinter import ttk
from typing import TYPE_CHECKING

import model.query_type
import model.resource_field
import model.operator_node
from controller.QueryManager import QueryManager

if TYPE_CHECKING:
    from view.MasterFrame import MasterFrame
from view.util.widget_factories import ScrollableComboboxFactory


# this will need to be a grid type
class IfBlockFrame(ttk.Frame):
    """
    Ifblockframe might be due for a rename. The goal is to draw the section of the UI that requests conditions from the
    user. we may need to split drawline into its own class to represent each line of a query statement.
    """

    def __init__(self, parent: MasterFrame):
        super().__init__(master=parent, padding="3 3 12 12")
        self.master_frame = parent
        self.width = 1
        self.height = 1

        self.field = tkinter.StringVar()
        self.field.set("id_0")
        self.query_type = tkinter.StringVar()
        self.query_type.set("Equals")
        self.input = tkinter.StringVar()
        self.draw_if_block()

    def draw_if_block(self):
        ttk.Label(self, text="If").grid(row=0, column=0)

        resource_field_combobox = ScrollableComboboxFactory.create_enum_combobox(
            self,
            self.field,
            model.resource_field.ResourceField,
            max_visible_items=4,
            width=30,
        )
        resource_field_combobox.grid(row=0, column=1)

        query_type_combobox = ScrollableComboboxFactory.create_enum_combobox(
            self,
            self.query_type,
            model.query_type.QueryType,
            max_visible_items=4,
            width=15,
        )
        query_type_combobox.grid(row=0, column=2)

        ttk.Entry(self, textvariable=self.input, width=35).grid(row=0, column=3)
        ttk.Button(self, text="Add", command=self.query_add).grid(row=0, column=4)

    def query_add(self):
        """
        The goal of query add is to
        - Notify the Query controller of the new QueryNode
        - Update the UI to  reflect the new query node
        """
        query_manager = QueryManager()
        QueryManager.construct_from_string()
        query_manager.set_loaded_query()

    def redraw_layout(self):
        # Clear the existing widgets in the frame
        for widget in self.winfo_children():
            widget.destroy()

        # Redraw the entire layout
        self.draw_if_block()

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

    def draw_line(self, row: int, data: tuple, maxdepth: int, fields: list = None):
        offset = data[1]
        if isinstance(data[2], model.OperatorNode):
            pass
        else:
            if fields is None:
                fields = []
            elements = []
            fields.append(tkinter.StringVar())
            elements.append(
                ttk.OptionMenu(
                    self,
                    fields[0],
                    data[0][0].name,
                    *[e.name for e in model.ResourceField.ResourceField],
                )
            )
            elements[0].grid(row=row, column=offset)
            fields.append(tkinter.StringVar())
            elements.append(
                ttk.OptionMenu(
                    self,
                    fields[1],
                    data[0][1],
                    *[e.name for e in model.QueryType.QueryType],
                )
            )
            elements[1].grid(row=row, column=offset + 1)
            if not (fields[1] == "EMPTY" or fields[1] == "NOTEMPTY"):
                fields.append(tkinter.StringVar())
                elements.append(ttk.Entry())


def redraw_line(self, elments: list, row: int, maxdepth: int):
    pass
