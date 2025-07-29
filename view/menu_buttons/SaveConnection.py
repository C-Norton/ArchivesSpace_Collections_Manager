from tkinter import ttk, Toplevel

import keyring
import keyring.errors

from controller.connection import Connection
from controller.connection_exceptions import AuthenticationError, NetworkError, ServerError
from view.util.FrameUtils import FrameUtils


def save_connection(connection: Connection):
    """
    This function checks the connection, and saves it to the system keyring if, and only if it is valid. If it's not
    valid, it pops up an error message explaining why it will not save it.
    :param connection: see Connection.py
    :return: None
    """
    frame = Toplevel()
    frame.title("Credential Storage")

    FrameUtils.set_icon(frame)
    ttk.Button(
        frame, width=70, text="Close", command=lambda: ttk.Frame.destroy(frame)
    ).grid(column=1, row=2)
    text = "Your connection has been saved."
    try:
        connection.test_connection()
    except AuthenticationError as e:
        text = f"Unable to store connection: Bad username or password.\n{e}"
    except NetworkError as e:
        text = f"Unable to store connection: Network error.\n{e}"
    except ServerError as e:
        text = f"Unable to store connection: Server error.\n{e}"
    else:
        try:
            keyring.get_keyring().set_password(
                "ArchivesSpace Collections Manager",
                connection.username + connection.server,
                connection.password,
            )
            text = "Successfully stored credentials"
        except keyring.errors.KeyringError as e:
            text = f"Unable to store connection: System Keychain configuration is not valid.\n{e}"
    ttk.Label(frame, text=text, wraplength=220).grid(column=1, row=1)

    for child in frame.winfo_children():
        child.grid_configure(padx=5, pady=5)
    frame.focus_set()
    frame.grab_set()
