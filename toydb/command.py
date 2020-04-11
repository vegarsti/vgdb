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
