from tkinter import ttk, Toplevel

"""
The way these dialogs are handled is pretty crap, it works here, but the amount of boilerplate doesn't scale.
"""


# TODO: address the amount of boilerplate code used in dialogs

class HelpDialog(ttk.Frame):
    frame = {}
    parent = {}

    def __init__(self, parent):
        self.parent = parent
        super().__init__()
        self.frame = Toplevel(parent)
        self.frame.title("Help")
        self.frame = ttk.Frame(self.frame, padding="3 3 12 12")
        self.frame.grid(column=0, row=0, sticky="N, W, E, S")
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)
        ttk.Label(self.frame,
            text="ArchiveSpace Bulk Edit UI can be found on GitHub for complete information on the program. To use, "
                 "first create a connection, then create a query. BACK UP YOUR DATA BEFORE RUNNING A QUERY, AND "
                 "ENSURE YOU WILL HAVE A STABLE SERVER CONNECTION. Failure to do so can cause issues with data "
                 "consistency in your instance.").grid(column=1, row=1)
        ttk.Label(self.frame,
            text="Credit to Channing Norton in collaboration with the University of Rochester. Code licensed under "
                 "the Mozzila Public License version 2.0").grid(column=1, row=2)
        ttk.Button(self.frame, width=70, text="Close", command=self.closeWindow).grid(column=1, row=4,
                                                                                     columnspan=2)
        for child in self.frame.winfo_children():
            child.grid_configure(padx=5, pady=5)
        self.frame.focus_set()
        self.frame.grab_set()
    def closeWindow(self):
        self.destroy()
        ttk.Frame.destroy(self.frame)