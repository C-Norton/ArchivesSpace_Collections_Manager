from tkinter import Text
from tkinter import ttk, Toplevel, StringVar, BooleanVar

import Model.NoteType
from Controller.NoteManager import NoteManager
from Model.Note import Note
from Model.NoteSubType import NoteSubType
from Model.NoteType import NoteType
from View import MasterFrame


class NoteConstructionModalPopup:
    def __init__(self, MasterFrame: MasterFrame):
        self.master_frame = MasterFrame
        self.frame = Toplevel()
        self.frame.geometry("450x600")
        self.frame.title("Construct Note")
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)

        self.note_type = StringVar()
        self.note_type.set("Abstract")
        self.note_value = StringVar()
        self.publish = BooleanVar()
        self.publish.set(False)
        self.label = StringVar()
        self.persistent_id = StringVar()
        self.has_subtype = None
        self.sub_type = StringVar()
        self.draw_note_definition_menu()
        self.frame.focus_set()
        self.frame.grab_set()

    def draw_note_definition_menu(self):
        ttk.Label(self.frame, text="Define Note").grid(row=0, column=0)
        ttk.Label(self.frame, text="Note Type").grid(row=1, column=0)
        ttk.OptionMenu(self.frame, self.note_type, self.note_type.get(),
            *[e.name for e in Model.NoteType.NoteType]).grid(row=1, column=1)
        ttk.Label(self.frame, text="Note Content (required)").grid(row=2, column=0, columnspan=2)
        Text(self.frame).grid(row=3, column=0, columnspan=2)
        ttk.Checkbutton(self.frame, text="Publish?", variable=self.publish).grid(row=4, column=0, columnspan=2)
        self.publish.set(self.publish.get())
        ttk.Label(self.frame, text="Label").grid(row=5, column=0)
        ttk.Entry(self.frame, textvariable=self.label).grid(row=5, column=1)
        ttk.Label(self.frame, text="Persistent ID").grid(row=6, column=0)
        ttk.Entry(self.frame, textvariable=self.persistent_id).grid(row=6, column=1)
        self.has_subtype = Note.has_subtype(Model.NoteType.NoteType[self.note_type.get()])
        if self.has_subtype:
            ttk.Label(self.frame, text="SubType").grid(row=7, column=0)
            self.sub_type.set(self.note_type.get())
            ttk.OptionMenu(self.frame, self.sub_type, self.sub_type.get(), *[e.name for e in NoteSubType]).grid(row=7,
                                                                                                                column=1)

        else:
            self.sub_type.set("")
        ttk.Button(self.frame, text="Submit Note", command=self.submit).grid(row=8, column=0)
        ttk.Button(self.frame, text="Cancel",command=self.frame.destroy).grid(row=8, column=1)

        def on_note_type_change(*args):
            self.redraw_layout()

        self.note_type.trace("w", on_note_type_change)

    def layout_manager(self):
        pass  # this won't be needed until multipart notes and the oddballs are addressed

    def redraw_layout(self):
        # Clear the existing widgets in the frame
        for widget in self.frame.winfo_children():
            widget.destroy()

        # Redraw the entire layout
        self.draw_note_definition_menu()

    def validate(self) -> bool:
        if Model.NoteType.NoteType[self.note_type.get()] is NoteType.Abstract:
            if self.note_value.get() != "":
                return True

        return False

    def submit(self):
        note_manager = NoteManager()
        note_manager.set_note(Model.NoteType.NoteType[self.note_type.get()], self.note_value.get(), self.publish.get(), self.label.get(),
                             self.persistent_id.get(), self.has_subtype, Model.NoteSubType.NoteSubType[self.sub_type.get()])
