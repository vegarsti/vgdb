from pathlib import Path
from typing import Dict, Iterator, List, Optional, Sequence, Tuple, Type, Union

from toydb.parse_schema import parse_schema
from toydb.where import Predicate, Where


class Table:
    def __init__(self, name: str, columns: Sequence[Tuple[str, Type]]) -> None:
        self.name = name
        self._file: Path = Path(f"{name}.db")
        self._spec = tuple(columns)
        self._types = [r[1] for r in columns]
        self._columns: Dict[str, Type] = {name: type_ for name, type_ in columns}

    def create(self) -> None:
        try:
            with self._file.open("x") as f:
                f.write(self.columns)
                f.write("\n")
        except FileExistsError:
            raise ValueError

    @property
    def columns(self) -> str:
        d: Dict[Type, str] = {str: "str", int: "int"}
        return "(" + ", ".join(f"{name} {d[type_]}" for name, type_ in self._columns.items()) + ")"

    def all_rows(self) -> Iterator[List[Union[int, str]]]:
        with self._file.open("r") as f:
            f.readline()
            while True:
                line = f.readline().replace("\n", "")
                if line == "":
                    break
                record = self._strings_to_row(line.split())
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

    def _strings_to_row(self, row: Sequence[str]) -> List[Union[int, str]]:
        data = [type_(value) for value, type_ in zip(row, self._columns.values())]
        return data

    def insert(self, row: List[Tuple[Union[int, str], Type]]) -> None:
        types = [r[1] for r in row]
        if types != self._types:
            raise ValueError
        row_ = [r[0] for r in row]
        to_write = " ".join(str(cell) for cell in row_)
        with open(f"{self.name}.db", "a+") as f:
            f.write(to_write)
            f.write("\n")

    @classmethod
    def from_file(cls, table_name: str) -> "Table":
        with open(f"{table_name}.db", "r+") as f:
            schema_str = f.readline().strip().replace("\n", "")
        columns_ = [c.strip() for c in schema_str[1:-1].split(",")]
        columns = parse_schema(columns_)
        assert columns is not None
        return Table(name=table_name, columns=columns)
