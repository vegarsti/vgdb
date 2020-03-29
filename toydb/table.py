import json
from typing import Dict, Optional


class Table:
    def __init__(self, records: Optional[Dict[str, str]] = None) -> None:
        if records is None:
            self._records: Dict[str, str] = {}
        else:
            self._records = records

    def get(self, key: str) -> Optional[str]:
        return self._records.get(key)

    def set(self, key: str, value: str) -> "Table":
        new_records = {key: value, **self._records}
        return Table(records=new_records)

    def delete(self, key: str) -> "Table":
        new_records = {**self._records}
        del new_records[key]
        return Table(records=new_records)

    def __str__(self) -> str:
        return json.dumps(self._records)
