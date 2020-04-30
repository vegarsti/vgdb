from pathlib import Path
from typing import IO, Dict, Iterator, List, Optional, Sequence, Tuple, Type, Union

from toydb.where import Predicate, Where

NUMBER_OF_COLUMNS_INT_LENGTH = 1
INT_BYTE_SIZE = 4
ENDIANNESS = "little"

d: Dict[Type, str] = {str: "text", int: "int"}
d_inv: Dict[str, Type] = {"text": str, "int": int}


def read_null_terminated_string(f: IO[bytes]) -> str:
    s = ""
    while True:
        new_byte = f.read(1)
        if new_byte == b"\x00":
            break
        s += new_byte.decode("ascii")
    return s


def write_null_terminated_string(f: IO[bytes], s: str) -> int:
    s_ascii = s.encode("ascii")
    f.write(s_ascii)
    f.write(b"\x00")
    bytes_written = len(s_ascii) + 1
    return bytes_written


def write_int(f: IO[bytes], i: int) -> None:
    f.write(i.to_bytes(INT_BYTE_SIZE, ENDIANNESS))


def read_int_tiny(f: IO[bytes]) -> int:
    return int.from_bytes(f.read(NUMBER_OF_COLUMNS_INT_LENGTH), ENDIANNESS)


def read_int(f: IO[bytes]) -> int:
    return int.from_bytes(f.read(INT_BYTE_SIZE), ENDIANNESS)


class Table:
    """
    Table file schema:
    - Number of columns as NUMBER_OF_COLUMNS_INT_LENGTH sized int
    - Sequence of column names and types. These strings are terminated by a null byte
    - Sequence of rows
    """

    def __init__(self, name: str, columns: List[Tuple[str, Type]]) -> None:
        self.name = name
        self._file: Path = Path(f"{name}.db")
        self._spec = tuple(columns)
        self._columns: Dict[str, Type] = {name: type_ for name, type_ in columns}
        self._header_bytes = 0

    def create(self) -> None:
        try:
            header_bytes = 0
            with self._file.open("bx") as f:
                f.write(len(self._columns).to_bytes(NUMBER_OF_COLUMNS_INT_LENGTH, ENDIANNESS))
                header_bytes += NUMBER_OF_COLUMNS_INT_LENGTH
                for column_name, column_type in self._columns.items():
                    wrote = write_null_terminated_string(f, column_name)
                    header_bytes += wrote
                    wrote = write_null_terminated_string(f, d[column_type])
                    header_bytes += wrote
                self._header_bytes = header_bytes
        except FileExistsError:
            raise ValueError

    @property
    def columns(self) -> str:
        return "(" + ", ".join(f"{name} {d[type_]}" for name, type_ in self._columns.items()) + ")"

    def all_rows(self) -> Iterator[List[Union[int, str]]]:
        with self._file.open("rb") as f:
            f.read(self._header_bytes)
            while f.peek(1) != b"":  # type: ignore
                row: List[Union[int, str]] = []
                for typ in self._columns.values():
                    if typ == str:
                        s = read_null_terminated_string(f)
                        row.append(s)
                    elif typ == int:
                        i = read_int(f)
                        row.append(i)
                    else:
                        raise ValueError("unsupported type")
                yield row

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

    def insert(self, row: Sequence[Union[int, str]]) -> None:
        with open(f"{self.name}.db", "ba+") as f:
            for cell, typ in zip(row, self._columns.values()):
                if typ == str:
                    write_null_terminated_string(f, str(cell))
                elif typ == int:
                    write_int(f, int(cell))
                else:
                    raise ValueError("unsupported type")

    @classmethod
    def from_file(cls, table_name: str) -> "Table":
        columns: List[Tuple[str, Type]] = []
        with open(f"{table_name}.db", "br+") as f:
            header_bytes = 0
            number_of_columns = read_int_tiny(f)
            header_bytes += NUMBER_OF_COLUMNS_INT_LENGTH
            for _ in range(number_of_columns):
                column_name = read_null_terminated_string(f)
                header_bytes += len(column_name.encode("ascii")) + 1
                column_type = read_null_terminated_string(f)
                header_bytes += len(column_type.encode("ascii")) + 1
                columns.append((column_name, d_inv[column_type]))
        t = Table(name=table_name, columns=columns)
        t._header_bytes = header_bytes
        return t
