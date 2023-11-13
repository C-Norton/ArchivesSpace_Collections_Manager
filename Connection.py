import json
from asnake.client import ASnakeClient

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

    def test(self):
        if self.server == "" or self.username == "" or self.password == "":
            return False, "Missing Server Configuration"
        client = self.createsession()
        print("hello world")
    def createsession(self):
        client = ASnakeClient(baseurl=self.server, username=self.username, password=self.password)
        client.authorize()
        return client