import keyring
from tkinter import ttk, Toplevel

class SaveConnection(ttk.Frame):
    frame = {}
    parent = {}
    connection = {}
    def __init__(self, parent):
        keys = keyring.get_keyring()
        keys.get_credential("BulkEdit UI")
