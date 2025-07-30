import field


class SubjectField(Field):
    """I'm not entirely clear on what this class is anymore. It inherits from field, so is clearly related to that.
    Research the two based off this file's clear mirroring of an archivesspace data model concept.
    """

    URI = 0
    TITLE = 1
    EXTERNAL_IDS = 2
    IS_LINKED_TO_PUBLISHED_RECORD = 3
    PUBLISH = 4
    SLUG = 5
    IS_SLUG_AUTO = 6
    USED_WITHIN_REPOSITORIES = 7
    SOURCE = 8
    SCOPE_NOTE = 9
    TERMS = 10
    VOCABULARY = 11
    AUTHORITY_ID = 12
    EXTERNAL_DOCUMENTS = 13
    METADATA_RIGHTS_DECLARATIONS = 14
