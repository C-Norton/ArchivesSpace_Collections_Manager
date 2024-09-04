class ModelValidityError(Exception):
    def __init__(self, message):
        self.message = message
