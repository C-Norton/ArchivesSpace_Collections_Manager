from enum import Enum


class NoteSubType(Enum):
    """
    Some note types can specify a subtype. This is the list of them. Conveniently, the list of subtypes and the list
    of notetypes that HAVE subtypes are the same

    Per Lev, we don't actually use this functionality in our workflows, but it exists for a reason, and other
    institutions may use it. Therefore, while it would be nice to support this functionality, having separate notetypes
    is not strictly necessary for our development until we are ready for public release. That aside, supporting them was
    easy provided it was built into the architecture of the system, so they should be pretty easy to keep working where
    possible. I guess what I'm saying is don't be afraid to break this if it's important to get a feature working, at
    least for now. Once we get towards final release, we will want to support this, and see if we can get feedback from
    the wider archivesspace community on how it truely gets used. Might be a place to ask Lyrasis about.
    """

    Abstract = 1
    Materials_Specific_Details = 2
    Physical_Description = 3
    Physical_Facet = 4
    Physical_Location = 5
