"""
A note is a dictionary of Key-Value pairs with some required fields.


Look up builder or Factory, as they will likely be useful here, and its a great time to use a design pattern!
"""

from datetime import datetime

from Model.LocalAccessRestrictionType import LocalAccessRestrictionType
from Model.NoteType import NoteType


class Note:
    def __init__(self, type: NoteType):
        self.note = dict()
        self.note["publish"] = (bool, False)
        self.note["type"] = type
        self.note["Persistent_ID"] = (str, None)
        self.note["Label"] = (str, None)
        self.note["Is_Multipart"] = False
        match type:
            case NoteType.Abstract:
                pass
            case NoteType.Accruals:
                self.note["Is_Multipart"] = True
            case NoteType.Appraisal:
                self.note["Is_Multipart"] = True
            case NoteType.Arrangement:
                self.note["Is_Multipart"] = True
            case NoteType.Bibliography:
                pass
            case NoteType.Biographical_Historical:
                self.note["Is_Multipart"] = True
            case NoteType.Conditions_Governing_Access:
                self.note["Is_Multipart"] = True
                self.note["Restriction_Begin"] = (datetime.date, None)
                self.note["Restriction_End"] = (datetime.date, None)
                self.note["Local_Access_Restriction_Type"] = (
                    LocalAccessRestrictionType,
                    None,
                )
            case NoteType.Conditions_Governing_Use:
                self.note["Is_Multipart"] = True
                self.note["Restriction_Begin"] = (datetime.date, None)
                self.note["Restriction_End"] = (datetime.date, None)

            case NoteType.Custodial_History:
                self.note["Is_Multipart"] = True

            case NoteType.Dimensions:
                pass
            case NoteType.Existence_and_Location_of_Copies:
                self.note["Is_Multipart"] = True
            case NoteType.Existence_and_Location_of_Originals:
                self.note["Is_Multipart"] = True

            case NoteType.File_Plan:
                self.note["Is_Multipart"] = True

            case NoteType.General:
                self.note["Is_Multipart"] = True

            case NoteType.Immediate_Source_of_Acquisition:
                self.note["Is_Multipart"] = True
            case NoteType.Index:
                # NOTE: NO SUBTYPE?
                pass
            case NoteType.Legal_Status:
                self.note["Is_Multipart"] = True

            case NoteType.Materials_Specific_Details:
                pass
            case NoteType.Other_Finding_Aids:
                self.note["Is_Multipart"] = True

            case NoteType.Physical_Characteristics_and_Technical_Requirements:
                self.note["Is_Multipart"] = True

            case NoteType.Physical_Description:
                pass
            case NoteType.Physical_Facet:
                pass
            case NoteType.Physical_Location:
                pass
            case NoteType.Preferred_Citation:
                self.note["Is_Multipart"] = True

            case NoteType.Processing_Information:
                self.note["Is_Multipart"] = True

            case NoteType.Related_Materials:
                self.note["Is_Multipart"] = True

            case NoteType.Scope_and_Contents:
                self.note["Is_Multipart"] = True

            case NoteType.Separated_Materials:
                self.note["Is_Multipart"] = True

        if self.note["Is_Multipart"]:
            pass
        elif not self.note["Is_Multipart"]:
            self.note["Content"] = (str, None)

    def validate(self):
        raise NotImplementedError

    def to_json(self):
        raise NotImplementedError
