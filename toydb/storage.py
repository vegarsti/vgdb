import struct
from pathlib import Path
from typing import IO, Dict, Iterator, List, Sequence, Tuple, Type, Union

NUMBER_OF_COLUMNS_INT_LENGTH = 1
INT_BYTE_SIZE = 4
ENDIANNESS = "little"

d: Dict[Type, str] = {str: "text", int: "int"}
d_inv: Dict[str, Type] = {"text": str, "int": int}

NULL_BYTE = b"\x00"


def read_null_terminated_string(f: IO[bytes]) -> str:
    s = ""
    while True:
        new_byte = f.read(1)
        if new_byte == NULL_BYTE:
            break
        s += new_byte.decode("ascii")
    return s


def string_to_null_terminated_byte_string(s: str) -> bytes:
    return s.encode("ascii") + NULL_BYTE


def write_string(f: IO[bytes], s: str) -> None:
    f.write(string_to_null_terminated_byte_string(s))


def int_to_bytes(i: int) -> bytes:
    return i.to_bytes(INT_BYTE_SIZE, ENDIANNESS)


def write_int(f: IO[bytes], i: int) -> None:
    f.write(int_to_bytes(i))


def write_tiny_int(f: IO[bytes], i: int) -> None:
    f.write(i.to_bytes(NUMBER_OF_COLUMNS_INT_LENGTH, ENDIANNESS))


def read_tiny_int(f: IO[bytes]) -> int:
    return int.from_bytes(f.read(NUMBER_OF_COLUMNS_INT_LENGTH), ENDIANNESS)


def read_int(f: IO[bytes]) -> int:
    return int.from_bytes(f.read(INT_BYTE_SIZE), ENDIANNESS)


class Storage:
    """Storage layer for a table

    Table file schema:
    - Number of columns as NUMBER_OF_COLUMNS_INT_LENGTH sized int
    - Sequence of column names and types. These strings are terminated by a null byte
    - Sequence of rows
    """

    def __init__(self, filename: str, columns: Sequence[Tuple[str, Type]]) -> None:
        self._file = Path(f"{filename}.db")
        self._filename = filename
        self._spec = tuple(type_ for name, type_ in columns)
        self._columns_as_they_came = columns
        self._columns: Dict[str, Type] = {name: type_ for name, type_ in columns}
        self._header_bytes = self.infer_header_bytes()

    def infer_header_bytes(self) -> int:
        s = NUMBER_OF_COLUMNS_INT_LENGTH
        for column_name, column_type in self._columns.items():
            s += len(column_name.encode("ascii")) + 1
            s += len(d[column_type].encode("ascii")) + 1
        return s

    def persist(self) -> None:
        self._error_if_exists()
        with self._file.open("wb") as f:
            write_tiny_int(f, len(self._spec))
            for column_name, column_type in self._columns.items():
                write_string(f, column_name)
                write_string(f, d[column_type])

    def _error_if_exists(self) -> None:
        try:
            with self._file.open("bx"):
                pass
        except FileExistsError:
            raise ValueError("File exists")

    def delete(self) -> None:
        self._file.unlink()

    @classmethod
    def from_file(cls, table_name: str) -> "Storage":
        columns: List[Tuple[str, Type]] = []
        with open(f"{table_name}.db", "br+") as f:
            number_of_columns = read_tiny_int(f)
            for _ in range(number_of_columns):
                column_name = read_null_terminated_string(f)
                column_type = read_null_terminated_string(f)
                columns.append((column_name, d_inv[column_type]))
        s = Storage(filename=table_name, columns=columns)
        return s

    def insert(self, row: Sequence[Union[int, str]]) -> None:
        fields = ["<"]
        values: List[bytes] = []
        for cell, typ in zip(row, self._columns.values()):
            if typ == str:
                v = string_to_null_terminated_byte_string(str(cell))
                fields.append(str(len(v)) + "s")
                values.append(v)
            elif typ == int:
                fields.append("I")
                values.append(int_to_bytes(int(cell)))
            else:
                raise ValueError(f"{cell} is of unsupported type {typ}")
        s = struct.Struct(" ".join(fields))
        # to_write: bytes = ""
        try:
            to_write = s.pack(*values)
        except struct.error as e:
            raise ValueError(e)
        with self._file.open("ba+") as f:
            f.write(to_write)

    def read_rows(self) -> Iterator[List[Union[int, str]]]:
        with self._file.open("rb") as f:
            f.read(self._header_bytes)
            while len(f.peek(1)) > 0:  # type: ignore
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
