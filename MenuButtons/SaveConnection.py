import keyring
from tkinter import ttk, Toplevel

class SaveConnection():
    frame = {}
    parent = {}
    connection = {}
    def __init__(self, parent, connection):
        self.parent = parent
        self.connection = connection
        self.frame = Toplevel()
        self.frame.title("Credential Storage")

        ttk.Button(self.frame, width=70, text="Close", command=self.closeWindow).grid(column=1, row=2)

        if not connection.test()[0]:
            text = "Unable to store connection: This connection is not valid"
        else:
            try:
                keyring.get_keyring().set_password("BulkEdit UI",connection.username+connection.server
                                                   ,connection.password)
                text = "Successfully stored credentials"
            except BaseException as e:
                text = "Unable to store connection: System Keychain configuration is not valid."
        ttk.Label(self.frame, text=text, wraplength=220).grid(column=1, row=1)

        for child in self.frame.winfo_children():
            child.grid_configure(padx=5, pady=5)
        self.frame.focus_set()
        self.frame.grab_set()
    def closeWindow(self):
        self.destroy()
        ttk.Frame.destroy(self.frame)