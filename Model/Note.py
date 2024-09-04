"""
A note is a dictionary of Key-Value pairs with some required fields.


Look up builder or Factory, as they will likely be useful here, and its a great time to use a design pattern!
"""

from datetime import datetime

from Model.LocalAccessRestrictionType import LocalAccessRestrictionType
from Model.ModelValidityError import ModelValidityError
from Model.NoteSubType import NoteSubType
from Model.NoteType import NoteType
from Model.SubNote import SubNote


class Note:

    def __init__(self, type: NoteType):
        self.note = dict()
        self.note["publish"] = (bool, False)
        self.note["type"] = type
        self.note["persistent_id"] = (str, None)
        self.note["label"] = (str, None)
        self.note["is_multipart"] = Note.is_multipart(type)
        match type:
            case NoteType.Abstract:
                self.note["sub_type"] = (NoteSubType, NoteSubType.Abstract)
            case NoteType.Bibliography:
                self.note["items"] = (list, None)
            case NoteType.Conditions_Governing_Access:
                self.note["restriction_begin"] = (datetime.date, None)
                self.note["restriction_end"] = (datetime.date, None)
                self.note["local_access_restriction_type"] = (
                    LocalAccessRestrictionType,
                    None,
                )

            case NoteType.Conditions_Governing_Use:
                self.note["restriction_begin"] = (datetime.date, None)
                self.note["restriction_end"] = (datetime.date, None)
            case NoteType.Materials_Specific_Details:
                self.note["sub_type"] = (
                    NoteSubType,
                    NoteSubType.Materials_Specific_Details,
                )
            case NoteType.Physical_Description:
                self.note["sub_type"] = (NoteSubType, NoteSubType.Physical_Description)
            case NoteType.Physical_Facet:
                self.note["sub_type"] = (NoteSubType, NoteSubType.Physical_Facet)
            case NoteType.Physical_Location:
                self.note["sub_type"] = (NoteSubType, NoteSubType.Physical_Location)
            case _:
                pass

        if self.note["is_multipart"]:
            self.note["sub_notes"] = (list, None)
        elif not self.note["is_multipart"]:
            self.note["content"] = (str, None)

    def validate(self):
        raise NotImplementedError

    def to_json(self):
        if not self.validate():
            raise ModelValidityError(f"Note {self} failed validity check")

    def add_subnote(self, subnote: SubNote):
        if self.note["Is_Multipart"]:
            if self.note["SubNotes"][1] is None:
                self.note["SubNotes"][1] = []
            self.note["SubNotes"][1].append(subnote)
        else:
            raise ModelValidityError("Attempting to add SubNote to single part note")

    @staticmethod
    def has_subtype(type: NoteType) -> bool:
        match type:
            case NoteType.Abstract:
                return True
            case NoteType.Materials_Specific_Details:
                return True
            case NoteType.Physical_Description:
                return True
            case NoteType.Physical_Facet:
                return True
            case NoteType.Physical_Location:
                return True
            case _:
                return False

    @staticmethod
    def is_multipart(type: NoteType) -> bool:
        match type:
            case NoteType.Abstract:
                return False
            case NoteType.Accruals:
                return True
            case NoteType.Appraisal:
                return True
            case NoteType.Arrangement:
                return True
            case NoteType.Bibliography:
                return False
            case NoteType.Biographical_Historical:
                return True
            case NoteType.Conditions_Governing_Access:
                return True
            case NoteType.Conditions_Governing_Use:
                return True
            case NoteType.Custodial_History:
                return True
            case NoteType.Dimensions:
                return False
            case NoteType.Existence_and_Location_of_Copies:
                return True
            case NoteType.Existence_and_Location_of_Originals:
                return True
            case NoteType.File_Plan:
                return True
            case NoteType.General:
                return True
            case NoteType.Immediate_Source_of_Acquisition:
                return True
            case NoteType.Index:
                return False
            case NoteType.Legal_Status:
                return True
            case NoteType.Materials_Specific_Details:
                return False
            case NoteType.Other_Finding_Aids:
                return True
            case NoteType.Physical_Characteristics_and_Technical_Requirements:
                return True
            case NoteType.Physical_Description:
                return False
            case NoteType.Physical_Facet:
                return False
            case NoteType.Physical_Location:
                return False
            case NoteType.Preferred_Citation:
                return True
            case NoteType.Processing_Information:
                return True
            case NoteType.Related_Materials:
                return True
            case NoteType.Scope_and_Contents:
                return True
            case NoteType.Separated_Materials:
                return True
