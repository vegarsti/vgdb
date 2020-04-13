from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Sequence, Tuple, Type

from toydb.print_utils import print_selection
from toydb.table import Table
from toydb.where import Where


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
    where: Optional[Where] = None


@dataclass
class Exit(Command):
    pass


@dataclass
class CreateTable(Command):
    table_name: str
    columns: Sequence[Tuple[str, Type]]


def handle_command(table: Table, command: Command) -> Table:
    if isinstance(command, Insert):
        success = table.valid_insert(row=command.values)
        if success:
            table.insert(command.values)
            print("OK")
        else:
            print(f"attempted to insert invalid record, table has schema {table.columns}")
    elif isinstance(command, Select):
        table_indices = table.column_indices_from_names(command.columns)
        if table_indices is None:
            print(f"incorrect selection, table has schema {table.columns}")
            return table
        if command.where is not None:
            i = table.column_name_to_index(command.where.column)
            if i is None:
                print(f"incorrect column {command.where.column}, table has schema {table.columns}")
                return table
        table_ = list(table.select(table_indices, where=command.where))
        print_selection(table_)
    else:
        raise ValueError("command not handled")
    return table
