from tkinter import ttk, Toplevel

from View.Util.FrameUtils import FrameUtils


class TestConnection:
    """
    This class manages the dialog box for testing a connection. Per the comment in Help, I'd really like to genericize
    these popups and clean up the code. That said, test connection does some additional logic to actually, well, test
    the connection. So this is a challenge, but one that should be resolved through reducing coupling.
    """

    connection = {}
    parent = {}
    frame = {}

    def __init__(self, connection):
        self.connection = connection
        self.frame = Toplevel()
        self.frame.title("Test results")
        FrameUtils.set_icon(self.frame)
        ttk.Button(self.frame, width=70, text="Close", command=self.close_window).grid(
            column=1, row=2
        )
        text = str()
        results = self.connection.test()
        if results[0]:
            text = "Connection successful! Your connection is ready to use."
        elif isinstance(results[1], str):
            text = "Connection failed for the following reason: \n" + results[1]
        else:
            text = (
                "Connection failed for an unknown reason. Please open a GitHub issue at"
                "https://github.com/C-Norton/BulkEditUI \n"
                "This issue should include the exact URL in your connection, as well as the following "
                "information \n" + results[2]
            )
        ttk.Label(self.frame, text=text, wraplength=220).grid(column=1, row=1)

        for child in self.frame.winfo_children():
            child.grid_configure(padx=5, pady=5)
        self.frame.focus_set()
        self.frame.grab_set()

    def close_window(self):
        ttk.Frame.destroy(self.frame)
