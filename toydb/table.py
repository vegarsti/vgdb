import json
from typing import Dict, Iterator, List, Sequence, Tuple, Type, Union


class Table:
    def __init__(self, name: str, columns: Sequence[Tuple[str, Type]]) -> None:
        self.name = name
        self._spec = tuple(columns)
        self._columns: Dict[str, Type] = {name: type_ for name, type_ in columns}
        self._records: List[List[Union[int, str]]] = []

    @property
    def columns(self) -> str:
        d: Dict[Type, str] = {str: "str", int: "int"}
        return "{" + ", ".join(f"{name}: {d[type_]}" for name, type_ in self._columns.items()) + "}"

    def select(self) -> Iterator[List[Union[int, str]]]:
        for record in self._records:
            yield record

    def _strings_to_record(self, record: Sequence[str]) -> List[Union[int, str]]:
        return [type_(value) for value, type_ in zip(record, self._columns.values())]

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
