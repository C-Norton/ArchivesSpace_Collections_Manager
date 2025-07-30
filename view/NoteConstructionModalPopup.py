import logging
from tkinter import Text
from tkinter import ttk, Toplevel, StringVar, BooleanVar

import model.note_type
from controller.NoteManager import NoteManager
from model.note import Note
from model.note_sub_type import NoteSubType
from model.note_type import NoteType
from view import MasterFrame
from view.util.FrameUtils import FrameUtils

"""
TODO:Make it so that when a note is already defined, that note data is loaded
this is in progress, but may have some bugs

todo: It's crashing when you set it to notetype bibliography, let's figure out why.
"""


class NoteConstructionModalPopup:
    def __init__(self, MasterFrame: MasterFrame):
        self.master_frame = MasterFrame
        self.frame = Toplevel()
        FrameUtils.set_icon(self.frame)
        self.frame.geometry("450x600")
        self.frame.title("Construct Note")
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)
        self.note_manager = NoteManager()

        self.note_type = StringVar()
        self.note_type.set("Abstract")
        self.note_content = Text(self.frame)
        self.publish = BooleanVar()
        self.publish.set(False)
        self.label = StringVar()
        self.persistent_id = StringVar()
        self.has_subtype = None
        self.sub_type = StringVar()
        self.draw_note_definition_menu()
        if self.note_manager.get_note() is not None:
            self.note_type.set(self.note_manager.get_note()["type"][1].name)
            self.publish.set(self.note_manager.get_note()["publish"][1])
            self.label.set(self.note_manager.get_note()["label"][1])
            self.persistent_id.set(self.note_manager.get_note()["persistent_id"][1])
            self.sub_type.set(self.note_manager.get_note()["sub_type"][1])
            self.has_subtype = Note.has_subtype(NoteType[self.note_type.get()])
        self.frame.focus_set()
        self.frame.grab_set()

    def draw_note_definition_menu(self):
        ttk.Label(self.frame, text="Define Note").grid(row=0, column=0)
        ttk.Label(self.frame, text="Note Type").grid(row=1, column=0)
        ttk.OptionMenu(
            self.frame,
            self.note_type,
            self.note_type.get(),
            *[e.name for e in model.NoteType.NoteType],
        ).grid(row=1, column=1)

        ttk.Label(self.frame, text="Note Content (required)").grid(
            row=2, column=0, columnspan=2
        )
        self.note_content = Text(self.frame)
        self.note_content.grid(row=3, column=0, columnspan=2)
        ttk.Checkbutton(self.frame, text="Publish?", variable=self.publish).grid(
            row=4, column=0, columnspan=2
        )
        self.publish.set(self.publish.get())
        ttk.Label(self.frame, text="Label").grid(row=5, column=0)
        ttk.Entry(self.frame, textvariable=self.label).grid(row=5, column=1)
        ttk.Label(self.frame, text="Persistent ID").grid(row=6, column=0)
        ttk.Entry(self.frame, textvariable=self.persistent_id).grid(row=6, column=1)
        self.has_subtype = Note.has_subtype(
            model.NoteType.NoteType[self.note_type.get()]
        )
        if self.has_subtype:
            ttk.Label(self.frame, text="SubType").grid(row=7, column=0)
            self.sub_type.set(self.note_type.get())
            ttk.OptionMenu(
                self.frame,
                self.sub_type,
                self.sub_type.get(),
                *[e.name for e in NoteSubType],
            ).grid(row=7, column=1)

        else:
            self.sub_type.set("")
        ttk.Button(self.frame, text="Submit Note", command=self.submit).grid(
            row=8, column=0
        )
        ttk.Button(self.frame, text="Cancel", command=self.frame.destroy).grid(
            row=8, column=1
        )

        def on_note_type_change(*args):
            self.redraw_layout()

        self.note_type.trace("w", on_note_type_change)

    def layout_manager(self):
        pass  # this won't be needed until multipart notes and the oddballs are addressed

    def redraw_layout(self):
        insert = self.note_content.get("1.0", "end-1c")

        for widget in self.frame.winfo_children():
            logging.debug(
                "NoteConstructionModalPopup: Destroying widget: "
                + widget.widgetName
                + widget.__str__()
            )
            widget.destroy()
        self.draw_note_definition_menu()
        # Re-populate fields if necessary

        logging.debug("Repopulating fields")
        if insert != "":
            try:
                self.note_content.insert(
                    "1.0", self.note_manager.get_note()["content"][1]
                )
            except Exception as e:
                logging.warning(e.__str__())

    def validate(self) -> bool:
        if model.NoteType.NoteType[self.note_type.get()] is NoteType.Abstract:
            if self.note_content.get("1.0", "end-1c").strip() != "":
                return True

        return False

    def submit(self):
        if self.validate():
            note_manager = NoteManager()
            note_manager.set_note(
                model.NoteType.NoteType[self.note_type.get()],
                self.note_content.get("1.0", "end-1c").strip(),
                self.publish.get(),
                self.label.get(),
                self.persistent_id.get(),
                self.has_subtype,
                model.NoteSubType.NoteSubType[self.sub_type.get()],
            )
            self.frame.destroy()
        else:
            FrameUtils.modal_message_popup(
                self.frame, "Invalid note or Unsupported note type"
            )

    def close(self):
        self.frame.destroy()
