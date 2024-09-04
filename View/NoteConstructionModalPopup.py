from tkinter import ttk, Toplevel, StringVar, BooleanVar
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
        self.publish = BooleanVar()
        self.publish.set(False)
        self.label = StringVar()
        self.persistent_id = StringVar()
        self.draw_note_definition_menu()
        self.frame.focus_set()
        self.frame.grab_set()

    def draw_note_definition_menu(self):
        ttk.Label(self.frame, text="Define Note").grid(row=0, column=0)
        ttk.OptionMenu(
            self.frame, self.note_type, *[e.name for e in Model.NoteType.NoteType]
        ).grid(row=1, column=0, columnspan=2)
        ttk.Label(self.frame, text="Note Content (required)").grid(
            row=2, column=0, columnspan=2
        )
        Text(self.frame).grid(row=3, column=0, columnspan=2)
        ttk.Checkbutton(self.frame, text="Publish?", variable=self.publish).grid(
            row=4, column=0, columnspan=2
        )
        self.publish.set(self.publish.get())
        ttk.Label(self.frame, text="Label").grid(row=5, column=0)
        ttk.Entry(self.frame, textvariable=self.label).grid(row=5, column=1)
        ttk.Label(self.frame, text="Persistent ID").grid(row=6, column=0)
        ttk.Entry(self.frame, textvariable=self.persistent_id).grid(row=6, column=1)

    def layout_manager(self):
        pass

    def validate(self) -> bool:
        raise NotImplementedError
