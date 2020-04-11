from typing import Dict, Iterator, List, Optional, Sequence, Tuple, Type, Union

from toydb.row import Row


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

    def column_indices_from_names(self, columns: List[str]) -> Optional[List[int]]:
        column_indices_to_select = []
        if columns == ["all"]:
            for i, _ in enumerate(self._columns.keys()):
                column_indices_to_select.append(i)
        else:
            for c in columns:
                try:
                    i = list(self._columns.keys()).index(c)
                except ValueError:
                    return None
                column_indices_to_select.append(i)
        return column_indices_to_select

    def select(self, columns: List[int]) -> Iterator[List[Union[str, int]]]:
        for row in self._rows:
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
