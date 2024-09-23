class ModelValidityError(Exception):
    """
    This custom exception is used when something is tried that is syntactically valid, but violates the constraints of
    the archivesspace data model. Fail early.
    """

    def __init__(self, message):
        self.message = message
