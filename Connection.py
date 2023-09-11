from tkinter import *
class Connection:
    server = ""
    username = ""
    password = ""
    def __init__(self,s,u,p):
        self.server=s
        self.username=u
        self.password=p
    def __str__(self):
        return self.server+self.username+self.password

