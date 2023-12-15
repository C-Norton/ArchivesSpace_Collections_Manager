from Model.RecordType import RecordType


class Node:
    def validate(self) -> bool:
        pass

    def eval(self, repo, recordType: RecordType, recordID: int) -> bool:
        pass
