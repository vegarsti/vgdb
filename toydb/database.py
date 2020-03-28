from typing import List, Optional

from toydb.record import Record


class Database:
    def __init__(self, records: Optional[List[Record]] = None) -> None:
        if records is None:
            self.records: List[Record] = []
        else:
            self.records = records

    def __str__(self) -> str:
        return "[" + ", ".join(record.__str__() for record in self.records) + "]"
