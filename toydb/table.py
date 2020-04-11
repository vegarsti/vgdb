from typing import Dict, Iterator, List, Optional, Sequence, Tuple, Type

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

    def select_all(self) -> Iterator[Optional[Row]]:
        for record in self._records:
            yield record

    def select(self, columns: List[str]) -> Iterator[Optional[str]]:
        if columns == ["all"]:
            for r in self.select_all():
                yield str(r)
        else:
            column_indices_to_select = []
            for c in columns:
                try:
                    i = list(self._columns.keys()).index(c)
                except ValueError:
                    yield None
                    raise StopIteration
                column_indices_to_select.append(i)
            for record in self._records:
                to_return = []
                for i in column_indices_to_select:
                    to_return.append(str(record[i]))
                yield " ".join(to_return)

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
        return "\n".join(str(record) for record in self.select(["all"]))
