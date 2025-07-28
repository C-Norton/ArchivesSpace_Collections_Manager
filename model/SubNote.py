from dataclasses import dataclass


@dataclass
class SubNote:
    """
    Subnote for multipart note
    """

    Content: str
    Publish: bool
