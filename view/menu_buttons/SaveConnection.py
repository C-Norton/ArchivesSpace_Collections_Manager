from tkinter import ttk, Toplevel

import keyring

from controller.Connection import Connection
from View.Util.FrameUtils import FrameUtils


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

    if not Connection.test(connection)[0]:
        text = "Unable to store connection: This connection is not valid"
    else:
        try:
            keyring.get_keyring().set_password(
                "BulkEdit UI",
                connection.username + connection.server,
                connection.password,
            )
            text = "Successfully stored credentials"
        except BaseException:
            text = "Unable to store connection: System Keychain configuration is not valid."
    ttk.Label(frame, text=text, wraplength=220).grid(column=1, row=1)

    for child in frame.winfo_children():
        child.grid_configure(padx=5, pady=5)
    frame.focus_set()
    frame.grab_set()
