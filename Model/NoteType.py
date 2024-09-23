from enum import Enum


class NoteType(Enum):
    """
    Notes in archivesspace have a type. This is the list of all 28 of them. Quite a few have unique handling
    instructions that affect the JSON structure. This is going to be a PAIN.

    Each notetype has its own JSON schema. We may need a note validator. This gets difficult because the docs are also
    incomplete as of 9/23/24

    https://archivesspace.github.io/archivesspace/doc/abstract_note_schema.html
    https://archivesspace.github.io/archivesspace/doc/note_singlepart_schema.html
    https://archivesspace.github.io/archivesspace/doc/note_multipart_schema.html

    """

    Abstract = (
        0  # https://archivesspace.github.io/archivesspace/doc/note_abstract_schema.html
    )
    Accruals = 1  # No dedicated doc page
    Appraisal = 2  # No dedicated doc page
    Arrangement = 3  # No dedicated doc page
    Bibliography = 4  # https://archivesspace.github.io/archivesspace/doc/note_bibliography_schema.html
    Biographical_Historical = (
        5  # https://archivesspace.github.io/archivesspace/doc/note_bioghist_schema.html
    )
    Conditions_Governing_Access = 6  # No dedicated doc page
    Conditions_Governing_Use = 7  # No dedicated doc page
    Custodial_History = 8  # No dedicated doc page
    Dimensions = 9  # No dedicated doc page
    Existence_and_Location_of_Copies = 10  # No dedicated doc page
    Existence_and_Location_of_Originals = 11  # No dedicated doc page
    File_Plan = 12
    General = 13
    Immediate_Source_of_Acquisition = 14
    Index = 15
    Legal_Status = 16
    Materials_Specific_Details = 17
    Other_Finding_Aids = 18
    Physical_Characteristics_and_Technical_Requirements = 19
    Physical_Description = 20
    Physical_Facet = 21
    Physical_Location = 22
    Preferred_Citation = 23
    Processing_Information = 24
    Related_Materials = 25
    Scope_and_Contents = 26
    Separated_Materials = 27
