import json
from typing import Dict, Optional


class Table:
    def __init__(self, records: Optional[Dict[str, str]] = None) -> None:
        if records is None:
            self.records: Dict[str, str] = {}
        else:
            self.records = records

    def get(self, key: str) -> Optional[str]:
        return self.records.get(key)

    def set(self, key: str, value: str) -> "Table":
        new_records = {key: value}
        new_records.update(self.records)
        return Table(records=new_records)

    def delete(self, key: str) -> "Table":
        new_records = {}
        new_records.update(self.records)
        del new_records[key]
        return Table(records=new_records)

    def __str__(self) -> str:
        return json.dumps(self.records)
