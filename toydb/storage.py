from pathlib import Path
from typing import IO, Dict, Iterator, List, Sequence, Tuple, Type, Union

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


def write_tiny_int(f: IO[bytes], i: int) -> None:
    f.write(i.to_bytes(NUMBER_OF_COLUMNS_INT_LENGTH, ENDIANNESS))


def read_tiny_int(f: IO[bytes]) -> int:
    return int.from_bytes(f.read(NUMBER_OF_COLUMNS_INT_LENGTH), ENDIANNESS)


def read_int(f: IO[bytes]) -> int:
    return int.from_bytes(f.read(INT_BYTE_SIZE), ENDIANNESS)


class Storage:
    """Storage layer for a table"""

    def __init__(self, filename: str, columns: Sequence[Tuple[str, Type]]) -> None:
        self._file = Path(f"{filename}.db")
        self._filename = filename
        self._spec = tuple(type_ for name, type_ in columns)
        self._columns: Dict[str, Type] = {name: type_ for name, type_ in columns}
        self._header_bytes = 0

    def persist(self) -> None:
        self._error_if_exists()
        header_bytes = 0
        with self._file.open("wb") as f:
            write_tiny_int(f, len(self._spec))
            header_bytes += NUMBER_OF_COLUMNS_INT_LENGTH
            for column_name, column_type in self._columns.items():
                wrote = write_null_terminated_string(f, column_name)
                header_bytes += wrote
                wrote = write_null_terminated_string(f, d[column_type])
                header_bytes += wrote
        self._header_bytes = header_bytes

    def _error_if_exists(self) -> None:
        try:
            with self._file.open("bx"):
                pass
        except FileExistsError:
            raise ValueError

    def delete(self) -> None:
        self._file.unlink()

    @classmethod
    def from_file(cls, table_name: str) -> "Storage":
        columns: List[Tuple[str, Type]] = []
        with open(f"{table_name}.db", "br+") as f:
            header_bytes = 0
            number_of_columns = read_tiny_int(f)
            header_bytes += NUMBER_OF_COLUMNS_INT_LENGTH
            for _ in range(number_of_columns):
                column_name = read_null_terminated_string(f)
                header_bytes += len(column_name.encode("ascii")) + 1
                column_type = read_null_terminated_string(f)
                header_bytes += len(column_type.encode("ascii")) + 1
                columns.append((column_name, d_inv[column_type]))
        s = Storage(filename=table_name, columns=columns)
        s._header_bytes = header_bytes
        return s

    def insert(self, row: Sequence[Union[int, str]]) -> None:
        with self._file.open("ba+") as f:
            for cell, typ in zip(row, self._columns.values()):
                if typ == str:
                    write_null_terminated_string(f, str(cell))
                elif typ == int:
                    write_int(f, int(cell))
                else:
                    raise ValueError("unsupported type")

    def read_rows(self) -> Iterator[List[Union[int, str]]]:
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
