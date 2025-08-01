import json


class Resource:
    """
    The goal of the resource class is to unpack the JSON data we get from archivessnake into a more usable format, allow
    it to be updated, then validate and repack it before submitting it back to archivessnake
    todo: Convert keys to enums
    """

    def __init__(self):
        self.data = dict()
        self.data["id_0"] = ""
        self.data["id_1"] = ""
        self.data["id_2"] = ""
        self.data["id_3"] = ""
        self.data["external_ark_url"] = ""
        self.data["import_current_ark"] = ""
        self.data["import_previous_arks"] = []
        self.data["level"] = ""
        self.data["other_level"] = ""
        self.data["slug"] = ""
        self.data["is_slug_auto"] = False
        self.data["resource_type"] = ""
        self.data["tree"] = None
        self.data["restrictions"] = False
        self.data["repository_processing_note"] = ""
        self.data["ead_id"] = ""
        self.data["ead_location"] = ""
        self.data["finding_aid_title"] = ""
        self.data["finding_aid_subtitle"] = ""
        self.data["finding_aid_filing_title"] = ""
        self.data["finding_aid_date"] = ""
        self.data["finding_aid_author"] = ""
        self.data["finding_aid_description_rules"] = ""
        self.data["finding_aid_language"] = ""
        self.data["finding_aid_script"] = ""
        self.data["finding_aid_language_note"] = ""
        self.data["finding_aid_sponsor"] = ""
        self.data["finding_aid_edition_statement"] = ""
        self.data["finding_aid_series_statement"] = ""
        self.data["finding_aid_status"] = ""
        self.data["finding_aid_note"] = ""
        self.data["lang_materials"] = []
        self.data["extents"] = []
        self.data["revision_statements"] = []
        self.data["dates"] = []
        self.data["instances"] = []
        self.data["deaccessions"] = []
        self.data["collection_management"] = json
        self.data["user_defined"] = json
        self.data["related_accessions"] = []
        self.data["classifications"] = []
        self.data["notes"] = []
        self.data["ark_name"] = json
        self.data["metadata_rights_declarations"] = []

    @classmethod
    def from_dict(cls, data):
        data = data

    @classmethod
    def from_json(cls, data):
        pass
