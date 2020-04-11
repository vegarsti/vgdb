from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Sequence, Tuple, Type

from toydb.print_utils import print_selection
from toydb.table import Table


class Commands(Enum):
    INSERT = "insert"
    SELECT = "select"
    DELETE = "delete"
    EXIT = "q"
    CREATE = "create"


@dataclass
class Command:
    pass


@dataclass
class Insert(Command):
    values: List[str]


@dataclass
class Select(Command):
    columns: List[str]


@dataclass
class Exit(Command):
    pass


@dataclass
class CreateTable(Command):
    table_name: str
    columns: Sequence[Tuple[str, Type]]


def parse_command(command: str) -> Optional[Command]:
    args = command.split()
    if len(args) == 0:
        return None
    c = args[0]
    if c == Commands.EXIT.value:
        return Exit()
    elif c == Commands.CREATE.value:
        if len(args) < 4:
            return None
        if args[1] != "table":
            return None
        table_name = args[2]
        columns_ = args[3:]
        if len(columns_) % 2 != 0:
            return None
        columns = parse_columns(columns_)
        if columns is None:
            return None
        return CreateTable(table_name=table_name, columns=columns)
    elif c == Commands.INSERT.value:
        if len(args) == 1:
            return None
        values = args[1:]
        return Insert(values=values)
    elif c == Commands.SELECT.value:
        if len(args) == 1:
            return None
        columns_str = " ".join(args[1:])
        columns_ = [c.strip().replace("*", "all") for c in columns_str.split(",")]
        if len(columns_) == len(args) - 1:
            return Select(columns=columns_)
    return None


def handle_command(table: Optional[Table], command: Command) -> Optional[Table]:
    if isinstance(command, CreateTable):
        table = Table(name=command.table_name, columns=command.columns)
        print(f"created table {table.name} with schema {table.columns}")
    else:
        if isinstance(command, Insert):
            if table is None:
                print("no table selected")
            else:
                success = table.insert(command.values)
                if success:
                    print("OK")
                else:
                    print(f"attempted to insert incorrect record, table has schema {table.columns}")
        elif isinstance(command, Select):
            if table is None:
                print("no table selected")
            else:
                table_indices = table.column_indices_from_names(command.columns)
                if table_indices is None:
                    print(f"incorrect selection, table has schema {table.columns}")
                else:
                    table_ = list(table.select(table_indices))
                    print_selection(table_)
        else:
            raise ValueError("command not handled")
    return table


def parse_columns(columns_: List[str]) -> Optional[Sequence[Tuple[str, Type]]]:
    number_of_columns = len(columns_) // 2
    columns = []
    for i in range(number_of_columns):
        column_name = columns_[i * 2]
        column_type_str = columns_[i * 2 + 1]
        column_type = {"str": str, "int": int}.get(column_type_str)
        if column_type is None:
            return None
        else:
            columns.append((column_name, column_type))
    return columns
