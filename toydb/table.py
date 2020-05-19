from typing import Dict, Iterator, List, Optional, Sequence, Tuple, Type, Union

from toydb.storage import Storage
from toydb.where import Predicate, Where

d: Dict[Type, str] = {str: "text", int: "int"}
d_inv: Dict[str, Type] = {"text": str, "int": int}


class Table:
    """
    Table file schema:
    - Number of columns as NUMBER_OF_COLUMNS_INT_LENGTH sized int
    - Sequence of column names and types. These strings are terminated by a null byte
    - Sequence of rows
    """

    def __init__(self, name: str, columns: Sequence[Tuple[str, Type]]) -> None:
        self.name = name
        self._file = Storage(filename=name, columns=columns)
        self._spec = tuple(columns)
        self._columns: Dict[str, Type] = {name: type_ for name, type_ in columns}
        self._types = list(self._columns.values())

    def persist(self) -> None:
        try:
            self._file.persist()
        except FileExistsError:
            raise ValueError

    @property
    def columns(self) -> str:
        return "(" + ", ".join(f"{name} {d[type_]}" for name, type_ in self._columns.items()) + ")"

    def all_rows(self) -> Iterator[List[Union[int, str]]]:
        return self._file.read_rows()

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

    def select(
        self, columns: List[int], where: Optional[Where] = None, limit: int = -1
    ) -> Iterator[List[Union[str, int]]]:
        predicate_map = {
            Predicate.EQUALS: lambda a, b: a == b,
            Predicate.NOT_EQUALS: lambda a, b: a != b,
            Predicate.LT: lambda a, b: a < b,
            Predicate.GT: lambda a, b: a > b,
            Predicate.LTEQ: lambda a, b: a <= b,
            Predicate.GTEQ: lambda a, b: a >= b,
        }
        count = 0
        for row in self.all_rows():
            if count == limit:
                return
            if where is None:
                to_return = [row[i] for i in columns]
                count += 1
                yield to_return
            else:
                i = self.column_name_to_index(where.column)
                assert i is not None
                where_value_typed = list(self._columns.values())[i](where.value)
                row_matches = predicate_map[where.predicate](row[i], where_value_typed)
                if row_matches:
                    to_return = [row[i] for i in columns]
                    count += 1
                    yield to_return

    def _strings_to_row(self, row: Sequence[str]) -> List[Union[int, str]]:
        data = [type_(value) for value, type_ in zip(row, self._columns.values())]
        return data

    def insert(self, row: Sequence[Union[int, str]]) -> None:
        self._file.insert(row)

    @classmethod
    def from_file(cls, name: str) -> "Table":
        s = Storage.from_file(name)
        columns = s._columns_as_they_came
        return Table(name, columns)
