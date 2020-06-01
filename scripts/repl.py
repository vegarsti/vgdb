import readline  # noqa
import sys
from typing import List, Optional, Union

from blessed import Terminal

from vgdb.evaluator import Evaluator
from vgdb.get_tables import get_tables
from vgdb.lexer import Lexer
from vgdb.parser import Parser
from vgdb.statement import CreateTable, Insert, Select


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


def loop() -> None:
    prompt = "vgdb> "
    red = "\033[31m"
    default = "\033[0m"
    prompt_with_color = f"{red}{prompt}{default}"
    while True:
        tables = get_tables()
        evaluator = Evaluator(tables=tables)
        try:
            user_input = input(prompt_with_color)
        except (KeyboardInterrupt, EOFError):
            sys.exit(1)
        if user_input == "exit":
            break
        lexer = Lexer(program=user_input)
        parser = Parser(lexer=lexer)
        command: Optional[Union[CreateTable, Insert, Select]] = None
        try:
            command = parser.parse()
        except ValueError as e:
            print(e)
            continue
        if command is None:
            print("no command given")
            continue
        try:
            result = evaluator.handle_command(command)
            if isinstance(result, str):
                print(result)
            else:
                print_selection(result)
        except ValueError as e:
            print(e)


def main() -> None:
    fullscreen = len(sys.argv) > 1 and sys.argv[1] == "f"
    if fullscreen:
        term = Terminal()
        with term.fullscreen(), term.location(0, 0):
            loop()
    else:
        loop()


if __name__ == "__main__":
    main()
