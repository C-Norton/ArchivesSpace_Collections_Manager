from tkinter import ttk, Toplevel

from Connection import Connection


class TestConnection(ttk.Frame):
    connection = {}
    parent = {}
    frame = {}

    def __init__(self, parent, connection):
        self.parent = parent
        self.connection = connection
        super().__init__()
        self.frame = Toplevel(parent)
        self.frame.title("Test results")
        results = self.connection.test()
