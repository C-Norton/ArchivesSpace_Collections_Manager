from tkinter import ttk, Toplevel
from View import MasterFrame


class NoteConstructionModalPopup:
    def __init__(self, MasterFrame: MasterFrame):
        self.master_frame = MasterFrame
        self.frame = Toplevel()
        self.frame.title("Construct Note")
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)

        self.draw_note_definition_menu()
        self.frame.focus_set()
        self.frame.grab_set()

    def draw_note_definition_menu(self):
        ttk.Label(text="Define Note").grid(row=0, column=0)
