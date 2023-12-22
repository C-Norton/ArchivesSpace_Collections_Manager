from __future__ import annotations

import tkinter
from tkinter import ttk, Toplevel

import keyring

from Controller.Connection import Connection


class ManageConnections(ttk.Frame):
    frame = {}
    parent = {}
    credentials = list()

    """
    This logic is cursed
    Read the username. It contains both a username, and a server
    
    Reading from the END (in case the username has :// in it), look for the first (or last if you will) instance of 
    '://'
    
    return the credential split up based off that
    
    """

    def readCredential(self, credential):
        buffer = []
        seencolon = False
        beginning = -1
        for index in range(len(credential.username)):
            index = len(credential.username) - index - 1
            value = credential.username[index]
            buffer += [value]
            if buffer[-3:] == ["/", "/", ":"]:
                seencolon = True
            if seencolon and value == "h":
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
        self.masterframe = masterFrame
        self.master.title("Manage Connections")
        self.checkbuttons = dict()
        keys = keyring.get_keyring()
        keys = keys.get_credential("BulkEdit UI", "")
        if isinstance(keys, (tuple, list)):
            self.credentials = [self.readCredential(key) for key in keys]
        else:
            self.credentials = [self.readCredential(keys)]
        self.createCredentialFrame()
        # now time for the window

    def createCredentialFrame(self):
        if len(self.credentials) == 1:
            ttk.Label(
                self,
                text=f"{self.credentials[0].server} - {self.credentials[0].username}",
            ).pack(side="top", fill="both", expand=False)
            ttk.Button(self, text="Load Credential", command=self.loadCredential).pack(
                side="top", fill="both", expand=False
            )
            ttk.Button(
                self, text="Delete Credential", command=self.deleteCredential
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
            ttk.Button(self, text="Load Credential", command=self.loadCredential).pack(
                side="top", fill="both", expand=False
            )
            ttk.Button(
                self, text="Delete Credential", command=self.deleteCredential
            ).pack(side="top", fill="both", expand=False)

    def loadCredential(self):
        if len(self.credentials) == 1:
            self.masterframe.main.connectionmanager.connection = self.credentials[0]
        self.master.destroy()

    def deleteCredential(self):
        if len(self.credentials) == 1:
            keyring.delete_password(
                "BulkEdit UI", self.credentials[0].username + self.credentials[0].server
            )
        self.master.destroy()
