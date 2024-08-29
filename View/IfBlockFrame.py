from __future__ import annotations

import tkinter
from tkinter import ttk

import Model.ActionType
import Model.QueryType
import Model.ResourceField
from View import MasterFrame


# this will need to be a grid type
class IfBlockFrame(ttk.Frame):

    def __init__(self, parent: MasterFrame):
        super().__init__(master=parent, padding="3 3 12 12")
        self.master_frame = parent
        self.pack(side="bottom", fill="x")
        self.width = 1
        self.height = 1

        self.field = tkinter.StringVar()
        self.field.set("id_0")
        self.query_type = tkinter.StringVar()
        self.query_type.set("Equals")
        self.input = tkinter.StringVar()
        self.action = tkinter.StringVar()
        self.action.set("Log")
        self.note_layout = False
        self.draw_if_block()

    def draw_if_block(self):
        ttk.Label(self, text="If").grid(row=0, column=0)

        ttk.OptionMenu(self, self.field, self.field.get(),
            *[e.name for e in Model.ResourceField.ResourceField]).grid(row=0,
                                                                       column=1)

        ttk.OptionMenu(self, self.query_type, self.query_type.get(),
            *[e.name for e in Model.QueryType.QueryType]).grid(row=0, column=2)

        ttk.Entry(self, textvariable=self.input, width=35).grid(row=0,
                                                                column=3)
        ttk.Button(self, text="Add", command=self.query_add).grid(row=0,
                                                                  column=4)
        ttk.Label(self, text="Action").grid(row=1, column=0)

        ttk.OptionMenu(self, self.action, self.action.get(),
                       *[e.name for e in Model.ActionType.ActionType]).grid(
            row=1, column=1)
        ttk.Button(self, text="Submit", command=self.submit_query).grid(row=1,
                                                                        column= 4,
                                                                        columnspan=3 if not self.note_layout else 1)
        if self.note_layout:
            ttk.Button(self, text="Define Note", command=self.define_note).grid(row=1, column=2,columnspan=2)

        def on_action_change(*args):
            if self.action.get() == "Create_Note" or self.action.get() == "Replace_Note":
                self.note_layout = True
                self.redraw_layout()
            else:
                self.note_layout = False
                self.redraw_layout()
        self.action.trace("w", on_action_change)

    def submit_query(self):
        pass

    def query_add(self):
        pass

    def redraw_layout(self):
        # Clear the existing widgets in the frame
        for widget in self.winfo_children():
            widget.destroy()

        # Redraw the entire layout
        self.draw_if_block()

    def define_note(self):
        pass
