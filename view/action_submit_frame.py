

import tkinter
from tkinter import ttk
from typing import TYPE_CHECKING

import model.action_type

if TYPE_CHECKING:
    from view.MasterFrame import MasterFrame
from view.note_construction_modal_popup import NoteConstructionModalPopup
from view.util.widget_factories import ScrollableComboboxFactory


class ActionSubmitFrame(ttk.Frame):
    """
    ActionSubmitFrame contains the Action label, ComboBox for action types, 
    Submit button, and conditional Define Note button.
    This frame allows these components to be independently positioned in the UI.
    """

    def __init__(self, parent: ttk.Frame):
        super().__init__(master=parent, padding="3 3 12 12")
        self.master_frame = parent

        # Initialize variables
        self.action = tkinter.StringVar()
        self.action.set("Log")
        self.note_layout = False

        # Draw the components
        self.draw_components()

    def draw_components(self):
        """Draw all components of the action submit frame"""
        ttk.Label(self, text="Action").grid(row=0, column=0)

        ScrollableComboboxFactory.create_enum_combobox(
            self, self.action, model.action_type.ActionType
        ).grid(row=0, column=1)

        if self.note_layout:
            ttk.Button(self, text="Define Note", command=self.define_note).grid(
                row=0, column=2
            )

        # Submit button always goes in the last column and sticks to the right
        ttk.Button(self, text="Submit", command=self.submit_query).grid(
            row=0, column=3, sticky="e"
        )

        # Configure column weights to push submit button to the right
        # Columns 0, 1, 2 have minimal width, column 3 expands to fill space
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=0)
        self.columnconfigure(2, weight=0)
        self.columnconfigure(3, weight=1)  # This column will expand

        # Set up action change callback
        def on_action_change(*args):
            if (
                    self.action.get() == "Create_Note"
                    or self.action.get() == "Replace_Note"
            ):
                self.note_layout = True
                self.redraw_layout()
            else:
                self.note_layout = False
                self.redraw_layout()

        self.action.trace("w", on_action_change)

    def submit_query(self):
        """Handle submit query action"""
        pass

    def define_note(self):
        """Open the note construction modal popup"""
        NoteConstructionModalPopup(self.master_frame)

    def redraw_layout(self):
        """Redraw the layout when components need to change"""
        # Clear the existing widgets in the frame
        for widget in self.winfo_children():
            widget.destroy()

        # Redraw the components
        self.draw_components()

    def get_action(self):
        """Get the current action value"""
        return self.action.get()