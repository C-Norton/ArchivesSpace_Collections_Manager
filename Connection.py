import json
import sys
from asnake import *
from dataclasses import dataclass
import asnake.client.web_client
from asnake.client import ASnakeClient
from requests.exceptions import MissingSchema, ConnectionError
from RequestType import RequestType

@dataclass
class Connection:
    server = ""
    username = ""
    password = ""
    def __init__(self, s,u,p):
        Connection.server = s
        Connection.username = u
        Connection.password = p
    def createsession(self):
        client = ASnakeClient(baseurl=Connection.server, username=Connection.username, password=Connection.password)
        client.authorize()
        return client
    def __str__(self):
        return Connection.server + Connection.username + Connection.password

    def test(self):
        if Connection.server == "" or Connection.username == "" or Connection.password == "":
            return False, "Missing Server Configuration"
        try:
            client = self.createsession()
        except asnake.client.web_client.ASnakeAuthError as e:
            return False, "Bad Username or Password"
        except MissingSchema:
            return False, "Bad URL Structure. Ensure your URL has https:// at the beginning"
        except ConnectionError:
            return (False, "Could not connect to server. Ensure your URL is correct, and that your IP is whitelisted "
                           "for the API")
        except BaseException as e:
            return False, e, e.__traceback__
        return True, "Your connection is working"


    def Query(self,type,endpoint):
        client = self.createsession()
        match type:
            case RequestType.GET:
                #return client.get(endpoint)
                pass
            case _:
                pass
