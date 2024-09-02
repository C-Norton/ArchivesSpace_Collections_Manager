from tkinter import ttk, Toplevel, StringVar
from tkinter import Text
import Model.NoteType
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
        self.note_value = StringVar()
        self.draw_note_definition_menu()
        self.frame.focus_set()
        self.frame.grab_set()

    def draw_note_definition_menu(self):
        ttk.Label(self.frame, text="Define Note").grid(row=0, column=0)
        ttk.OptionMenu(
            self.frame, self.note_type, *[e.name for e in Model.NoteType.NoteType]
        ).grid(row=1, column=0)
        Text(self.frame).grid(row=2, column=0)

    def layout_manager(self):
        pass
