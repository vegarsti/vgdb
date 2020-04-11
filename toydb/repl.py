import sys
from enum import Enum
from typing import List, Optional, Sequence, Tuple, Type, Union

from blessed import Terminal
from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style

from toydb.command import Command, CreateTable, Exit, Insert, Select
from toydb.table import Table


class Commands(Enum):
    INSERT = "insert"
    SELECT = "select"
    DELETE = "delete"
    EXIT = "q"
    CREATE = "create"


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


def copy_nested_list(lst: List[List[str]]) -> List[List[str]]:
    """Return a copy of list l to one level of nesting"""
    return [list(i) for i in lst]


def column_widths(table: List[List[str]]) -> List[int]:
    """Get the maximum size for each column in table"""
    return [max(map(len, col)) for col in zip(*table)]


def align_table(table: List[List[str]]) -> List[List[str]]:
    """Return table justified according to align"""
    widths = column_widths(table)
    new_table = copy_nested_list(table)
    align = "<"
    for row in new_table:
        for cell_num, cell in enumerate(row):
            row[cell_num] = "{:{align}{width}}".format(cell, align=align, width=widths[cell_num])
    return new_table


def stringify_table(table: List[List[Union[int, str]]]) -> List[List[str]]:
    new_table = []
    for row in table:
        new_row = [str(i) for i in row]
        new_table.append(new_row)
    return new_table


def print_selection(table: List[List[Union[int, str]]]) -> None:
    for row in align_table(stringify_table(table)):
        print(" ".join(row))


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
                table_ = list(table.select(command.columns))
                print_selection(table_)
        else:
            raise ValueError("command not handled")
    return table


def loop() -> None:
    style = Style.from_dict({"prompt": "red"})
    message = [("class:prompt", "toydb> ")]
    session = PromptSession(style=style)
    table: Optional[Table] = None
    while True:
        try:
            c = session.prompt(message)
        except (KeyboardInterrupt, EOFError):
            sys.exit(1)
        command = parse_command(c.lower())
        if command is None:
            print(f"invalid command: {c}")
            continue
        if isinstance(command, Exit):
            break
        table = handle_command(table=table, command=command)
    print("Current database")
    print(table)


def main() -> None:
    fullscreen = False
    if fullscreen:
        term = Terminal()
        with term.fullscreen(), term.location(0, 0):
            loop()
    else:
        loop()


if __name__ == "__main__":
    main()
