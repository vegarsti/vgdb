import sys
from typing import Dict, Union

from toydb.repl_utils import print_selection
from toydb.statement import CreateTable, Insert, Select
from toydb.table import Table


class Evaluator:
    def __init__(self, tables: Dict[str, Table]):
        self.tables = tables

    def handle_command(self, command: Union[CreateTable, Insert, Select]) -> None:
        if isinstance(command, CreateTable):
            self.handle_create(command)
        elif isinstance(command, Select):
            self.handle_select(command=command)
        elif isinstance(command, Insert):
            self.handle_insert(command=command)
        else:
            print("Command not handled. This shouldn't happen")
            sys.exit(1)

    def handle_create(self, command: CreateTable) -> None:
        table = self.tables.get(command.table_name)
        if table is not None:
            raise ValueError(f"table {table.name} already exists with schema {table.columns}")
        else:
            table = Table(name=command.table_name, columns=command.columns)
            table.persist()
            print(f"created table {table.name} with schema {table.columns}")

    def handle_insert(self, command: Insert) -> None:
        table = self.tables.get(command.table_name)
        if table is None:
            raise ValueError(f"table {command.table_name} does not exist")
        try:
            table.insert(command.values)
            print("OK")
        except ValueError:
            print(f"attempted to insert invalid record, table has schema {table.columns}")

    def handle_select(self, command: Select) -> None:
        table = self.tables.get(command.table_name)
        if table is None:
            raise ValueError(f"table {command.table_name} does not exist")
        table_indices = table.column_indices_from_names(command.columns)
        if table_indices is None:
            raise ValueError(
                f"incorrect selection of columns {', '.join(command.columns)}: table has schema {table.columns}"
            )
        if len(command.where) > 0:
            for w in command.where:
                i = table.column_name_to_index(w.column)
                if i is None:
                    raise ValueError(f"incorrect column {w.column}, table has schema {table.columns}")
        table_ = list(table.select(columns=table_indices, where=command.where, limit=command.limit))
        if table_ is not None:
            print_selection(table_)
