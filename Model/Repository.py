import Main


class Repository:
    def __init__(self, Number: int):
        self.repoNumber = Number
        self.repoName = Main.connectionmanager.get_repository(self.repoNumber)["name"]
