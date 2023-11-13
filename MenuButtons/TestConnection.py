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

        ttk.Button(self.frame, width=70, text="Close", command=self.closeWindow).grid(column=1, row=2)
        text = str()
        results = self.connection.test()
        if results[0]:
            text = "Test successful! Your connection is ready to use."
        elif isinstance(results[1], str):
            text = "Test failed for the following reason: \n" + results[1]
        else:

            text = "Test failed for an unknown reason. Please open a GitHub issue at"\
                                "https://github.com/C-Norton/BulkEditUI \n"\
                                "This issue should include the exact URL in your connection, as well as the following "\
                                "information \n" + results[2]
        resultslabel = ttk.Label(self.frame, text=text, wraplength=220).grid(column=1, row=1)

        for child in self.frame.winfo_children():
            child.grid_configure(padx=5, pady=5)
        self.frame.focus_set()
        self.frame.grab_set()
    def closeWindow(self):
        self.destroy()
        ttk.Frame.destroy(self.frame)
