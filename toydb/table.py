from typing import Dict, Iterator, List, Optional, Sequence, Tuple, Type, Union

from toydb.row import Row
from toydb.where import Predicate, Where


class Table:
    def __init__(self, name: str, columns: Sequence[Tuple[str, Type]]) -> None:
        self.name = name
        self._spec = tuple(columns)
        self._columns: Dict[str, Type] = {name: type_ for name, type_ in columns}
        self._rows: List[Row] = []

    @property
    def columns(self) -> str:
        d: Dict[Type, str] = {str: "str", int: "int"}
        return "{" + ", ".join(f"{name}: {d[type_]}" for name, type_ in self._columns.items()) + "}"

    def all_rows(self) -> Iterator[Row]:
        for record in self._rows:
            yield record

    def column_name_to_index(self, c: str) -> Optional[int]:
        try:
            i = list(self._columns.keys()).index(c)
            return i
        except ValueError:
            return None

    def column_indices_from_names(self, columns: List[str]) -> Optional[List[int]]:
        column_indices_to_select = []
        if columns == ["all"]:
            for i, _ in enumerate(self._columns.keys()):
                column_indices_to_select.append(i)
        else:
            for c in columns:
                j = self.column_name_to_index(c)
                if j is None:
                    return None
                column_indices_to_select.append(j)
        return column_indices_to_select

    def select(self, columns: List[int], where: Optional[Where]) -> Iterator[List[Union[str, int]]]:
        for row in self.all_rows():
            if where is not None:
                i = self.column_name_to_index(where.column)
                assert i is not None
                where_value_typed = list(self._columns.values())[i](where.value)
                row_matches = {Predicate.EQUAL: lambda a, b: a == b}[where.predicate](row[i], where_value_typed)
            else:
                row_matches = True
            if row_matches:
                to_return = [row[i] for i in columns]
                yield to_return

    def _strings_to_row(self, row: Sequence[str]) -> Row:
        data = [type_(value) for value, type_ in zip(row, self._columns.values())]
        return Row(data=data)

    def insert(self, row: Sequence[str]) -> bool:
        if len(row) == len(self._columns.items()):
            try:
                row_ = self._strings_to_row(row)
            except ValueError:
                return False
            self._rows.append(row_)
            return True
        else:
            return False
