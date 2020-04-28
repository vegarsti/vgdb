from pathlib import Path
from typing import IO, Dict, Iterator, List, Optional, Sequence, Tuple, Type, Union

from toydb.where import Predicate, Where

NUMBER_OF_COLUMNS_INT_LENGTH = 1
ENDIANNESS = "little"

d: Dict[Type, str] = {str: "str", int: "int"}
d_inv: Dict[str, Type] = {"str": str, "int": int}


def read_null_terminated_string(f: IO[bytes]) -> str:
    s = ""
    while True:
        new_byte = f.read(1)
        if new_byte == b"\x00":
            break
        s += new_byte.decode("ascii")
    return s


def write_null_terminated_string(f: IO[bytes], s: str) -> None:
    f.write(s.encode("ascii"))
    f.write(b"\x00")


class Table:
    """
    Table file schema:
    Line 0: Number of columns as 2-sized int
    Line 0: sequence of column names and types. Column name is string terminated by a null byte
    """

    def __init__(self, name: str, columns: List[Tuple[str, Type]]) -> None:
        self.name = name
        self._file: Path = Path(f"{name}.db")
        self._spec = tuple(columns)
        self._columns: Dict[str, Type] = {name: type_ for name, type_ in columns}

    def create(self) -> None:
        try:
            with self._file.open("bx") as f:
                f.write(len(self._columns).to_bytes(NUMBER_OF_COLUMNS_INT_LENGTH, ENDIANNESS))
                for column_name, column_type in self._columns.items():
                    write_null_terminated_string(f, column_name)
                    write_null_terminated_string(f, d[column_type])
                f.write(b"\n")
        except FileExistsError:
            raise ValueError

    @property
    def columns(self) -> str:
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

    def insert(self, row: Sequence[str]) -> None:
        row_ = self._strings_to_row(row)
        to_write = " ".join(str(cell) for cell in row_)
        with open(f"{self.name}.db", "a+") as f:
            f.write(to_write)
            f.write("\n")

    @classmethod
    def from_file(cls, table_name: str) -> "Table":
        columns: List[Tuple[str, Type]] = []
        with open(f"{table_name}.db", "br+") as f:
            num_columns_as_bytes = f.read(NUMBER_OF_COLUMNS_INT_LENGTH)
            number_of_columns = int.from_bytes(num_columns_as_bytes, ENDIANNESS)
            for _ in range(number_of_columns):
                column_name = read_null_terminated_string(f)
                column_type = read_null_terminated_string(f)
                columns.append((column_name, d_inv[column_type]))
        print(columns)
        return Table(name=table_name, columns=columns)
