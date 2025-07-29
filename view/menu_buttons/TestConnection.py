from tkinter import ttk, Toplevel

import asnake.client.web_client

from controller.connection_exceptions import AuthenticationError, NetworkError, ServerError
from view.util.FrameUtils import FrameUtils


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
        try:
            self.connection.test_connection()
        except AuthenticationError as e:
            text = "Connection failed due to a bad username or password."
        except asnake.client.web_client.ASnakeAuthError as e:
            text = "Connection failed due to a bad username or password."
        except NetworkError as e:
            text = "Connection failed due to a network error. Are you sure you have the correct API address?"
        except ServerError as e:
            text = "Connection failed due to an unknown error."
        else:
            text = "Connection successful! Your connection is ready to use."
        ttk.Label(self.frame, text=text, wraplength=220).grid(column=1, row=1)

        for child in self.frame.winfo_children():
            child.grid_configure(padx=5, pady=5)
        self.frame.focus_set()
        self.frame.grab_set()

    def close_window(self):
        ttk.Frame.destroy(self.frame)
