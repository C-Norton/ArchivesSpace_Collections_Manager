import asnake.client.web_client

from dataclasses import dataclass

import asnake.client.web_client
from asnake.client import ASnakeClient
from requests.exceptions import MissingSchema, ConnectionError

from Controller.RequestType import RequestType


@dataclass
class Connection:

    def __init__(self, s, u, p):
        self.server = s
        self.username = u
        self.password = p
        self.client = None

    def createsession(self) -> bool:
        self.client = ASnakeClient(baseurl=self.server, username=self.username, password=self.password)
        self.client.authorize()

    def __str__(self):
        return self.server + self.username + self.password

    def test(self):
        if self.server == "" or self.username == "" or self.password == "":
            return False, "Missing Server Configuration"
        try:
            self.client = self.createsession()
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

    def Query(self, type, endpoint: str):
        client = self.createsession()
        match type:
            case RequestType.GET:
                # return client.get(endpoint)
                pass
            case _:
                pass
