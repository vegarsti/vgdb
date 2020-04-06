import json
from typing import Dict, Iterator, List, Sequence, Tuple, Type

from toydb.record import Record


class Table:
    def __init__(self, name: str, columns: Sequence[Tuple[str, Type]]) -> None:
        self.name = name
        self._spec = tuple(columns)
        self._columns: Dict[str, Type] = {name: type_ for name, type_ in columns}
        self._records: List[Record] = []

    @property
    def columns(self) -> str:
        d: Dict[Type, str] = {str: "str", int: "int"}
        return "{" + ", ".join(f"{name}: {d[type_]}" for name, type_ in self._columns.items()) + "}"

    def select(self) -> Iterator[Record]:
        for record in self._records:
            yield record

    def _strings_to_record(self, record: Sequence[str]) -> Record:
        data = [type_(value) for value, type_ in zip(record, self._columns.values())]
        return Record(data=data)

    def insert(self, record: Sequence[str]) -> bool:
        if len(record) == len(self._columns.items()):
            try:
                record_ = self._strings_to_record(record)
            except ValueError:
                return False
            self._records.append(record_)
            return True
        else:
            return False

    def __str__(self) -> str:
        return json.dumps(self._records)
