import Main


class Repository:
    """
    ToDo: Consider using namedtuple classes for this
    """

    def __init__(self, number: int):
        self.repo_number = number
        self.repo_name = Main.connection_manager.get_repository(self.repo_number)[
            "name"
        ]
