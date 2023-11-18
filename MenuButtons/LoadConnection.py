import keyring
from tkinter import ttk, Toplevel

from Connection import Connection


class LoadConnection(ttk.Frame):
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
        seencolon=False
        beginning = -1
        for index,value in reversed(credential.username):
            buffer += [value]
            if buffer[-3:-1]=="//:":
                seencolon=True
            if seencolon and value=="h":
                beginning = len(credential.username)-index
                break
        return Connection(credential.username[beginning:],credential.username[0:beginning],credential.password)
    def __init__(self, parent):
        keys = keyring.get_keyring()
        keys = keys.get_credential("BulkEdit UI")
        if isinstance(keys,(tuple,list)):
            self.credentials = [self.readCredential(key) for key in keys]
        else:
            self.credentials = [self.readCredential(keys)]

