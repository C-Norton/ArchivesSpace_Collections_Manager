from __future__ import annotations

import tkinter
from tkinter import ttk, Toplevel

import keyring

from controller.Connection import Connection
from View.Util.FrameUtils import FrameUtils


class ManageConnections(ttk.Frame):
    """
    This logic is cursed
    Read the username. It contains both a username, and a server
    (apparently this is actually a standard use of credential manager)
    Reading from the END (in case the username has :// in it), look for the first (or last if you will) instance of
    '://'

    return the credential split up based off that

    EDIT: Turns out this means of doing things is actually somewhat standard. Seriously?

    """

    frame = {}
    parent = {}
    credentials = list()

    def read_credential(self, credential):
        """
        My editor informs me that this can be made static. Consider doing so
        :param credential: Credential from the keychain
        :return: a plaintext username, server, password combo stored in a new Connection class
        TODO: Additional cross-platform testing. This is known not to work on Linux Debian with Gnome_Keyring package.
        No clue how it's handled on mac. Mac support in particular is important for the archivesspace community
        TODO: Handle no credentials better.
        """
        buffer = []
        seen_colon = False
        beginning = -1
        if credential.username is not None:
            for index in range(len(credential.username)):
                index = len(credential.username) - index - 1
                value = credential.username[index]
                buffer += [value]
                if buffer[-3:] == ["/", "/", ":"]:
                    seen_colon = True
                if seen_colon and value == "h":
                    beginning = index
                    break
            return Connection(
                credential.username[beginning:],
                credential.username[0:beginning],
                credential.password,
            )

    def __init__(self, masterFrame: MasterFrame):
        self.master = Toplevel()

        super().__init__(master=self.master)
        self.master.geometry("500x175")
        self.pack()
        self.master_frame = masterFrame
        self.master.title("Manage Connections")
        FrameUtils.set_icon(self.master)
        self.checkbuttons = dict()
        keys = keyring.get_keyring()
        keys = keys.get_credential("BulkEdit UI", "")
        if isinstance(keys, (tuple, list)):
            self.credentials = [self.read_credential(key) for key in keys]
        else:
            self.credentials = [self.read_credential(keys)]
        self.create_credential_frame()
        # now time for the window

    def create_credential_frame(self):
        if len(self.credentials) == 1:
            ttk.Label(
                self,
                text=f"{self.credentials[0].server} - {self.credentials[0].username}",
            ).pack(side="top", fill="both", expand=False)
            ttk.Button(self, text="Load Credential", command=self.load_credential).pack(
                side="top", fill="both", expand=False
            )
            ttk.Button(
                self, text="Delete Credential", command=self.delete_credential
            ).pack(side="top", fill="both", expand=False)
        elif len(self.credentials) == 0:
            # WE HAVE NO CREDENTIALS
            ttk.Label(self, text="You currently have no saved connections").pack(
                side="bottom", fill="both"
            )
        else:
            options = list()
            self.clicked = tkinter.StringVar()
            for credential in self.credentials:
                options += [f"{credential.server} - {credential.username}"]
            ttk.OptionMenu(self, self.clicked, *options).pack(
                side="top", fill="both", expand=False
            )
            ttk.Button(self, text="Load Credential", command=self.load_credential).pack(
                side="top", fill="both", expand=False
            )
            ttk.Button(
                self, text="Delete Credential", command=self.delete_credential
            ).pack(side="top", fill="both", expand=False)

    def load_credential(self):
        if len(self.credentials) == 1:
            self.master_frame.main.connection_manager.connection = self.credentials[0]
        self.master.destroy()

    def delete_credential(self):
        if len(self.credentials) == 1:
            keyring.delete_password(
                "BulkEdit UI", self.credentials[0].username + self.credentials[0].server
            )
        self.master.destroy()
