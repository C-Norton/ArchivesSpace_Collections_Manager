from tkinter import ttk, Toplevel

import keyring

from Controller.Connection import Connection


def SaveConnection(connection: Connection):
    frame = Toplevel()
    frame.title("Credential Storage")
    ttk.Button(
        frame, width=70, text="Close", command=lambda: ttk.Frame.destroy(frame)
    ).grid(column=1, row=2)

    if not Connection.test(connection)[0]:
        text = "Unable to store connection: This connection is not valid"
    else:
        try:
            keyring.get_keyring().set_password(
                "BulkEdit UI",
                Connection.username + Connection.server,
                Connection.password,
            )
            text = "Successfully stored credentials"
        except BaseException as e:
            text = "Unable to store connection: System Keychain configuration is not valid."
    ttk.Label(frame, text=text, wraplength=220).grid(column=1, row=1)

    for child in frame.winfo_children():
        child.grid_configure(padx=5, pady=5)
    frame.focus_set()
    frame.grab_set()
