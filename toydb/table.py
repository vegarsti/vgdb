from typing import Dict, Iterator, List, Sequence, Tuple, Type

from toydb.row import Row


class Table:
    def __init__(self, name: str, columns: Sequence[Tuple[str, Type]]) -> None:
        self.name = name
        self._spec = tuple(columns)
        self._columns: Dict[str, Type] = {name: type_ for name, type_ in columns}
        self._records: List[Row] = []

    @property
    def columns(self) -> str:
        d: Dict[Type, str] = {str: "str", int: "int"}
        return "{" + ", ".join(f"{name}: {d[type_]}" for name, type_ in self._columns.items()) + "}"

    def select(self) -> Iterator[Row]:
        for record in self._records:
            yield record

    def _strings_to_record(self, record: Sequence[str]) -> Row:
        data = [type_(value) for value, type_ in zip(record, self._columns.values())]
        return Row(data=data)

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

    def __repr__(self) -> str:
        return "\n".join(str(record) for record in self.select())
