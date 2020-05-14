from dataclasses import dataclass
from typing import List, Optional, Tuple, Type, Union

from toydb.get_tables import get_tables
from toydb.print_utils import print_selection
from toydb.where import Where


@dataclass
class Statement:
    pass


@dataclass
class Insert(Statement):
    values: List[Union[int, str]]
    table_name: str


@dataclass
class Select(Statement):
    columns: List[str]
    table_name: str
    where: Optional[Where] = None
    limit: int = -1


@dataclass
class CreateTable(Statement):
    table_name: str
    columns: List[Tuple[str, Type]]


def handle_command(command: Union[Select, Insert]) -> None:
    tables = get_tables()
    table = tables.get(command.table_name)
    if table is None:
        print(f"table {command.table_name} does not exist")
        return
    if isinstance(command, Insert):
        try:
            table.insert(command.values)
            print("OK")
        except ValueError:
            print(f"attempted to insert invalid record, table has schema {table.columns}")
    elif isinstance(command, Select):
        table_indices = table.column_indices_from_names(command.columns)
        if table_indices is None:
            print(f"incorrect selection, table has schema {table.columns}")
            return
        if command.where is not None:
            i = table.column_name_to_index(command.where.column)
            if i is None:
                print(f"incorrect column {command.where.column}, table has schema {table.columns}")
                return
        table_ = list(table.select(columns=table_indices, where=command.where, limit=command.limit))
        print_selection(table_)
    else:
        raise ValueError("command not handled")
