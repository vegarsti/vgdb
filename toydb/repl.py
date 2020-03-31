import sys
from enum import Enum
from typing import Optional

from blessed import Terminal
from prompt_toolkit import PromptSession
from prompt_toolkit.output import ColorDepth
from prompt_toolkit.styles import Style

from toydb.command import Command, Create, Delete, Exit, Insert, Select, SelectAll
from toydb.table import Table


class Commands(Enum):
    INSERT = "insert"
    SELECT = "select"
    DELETE = "delete"
    EXIT = "q"
    CREATE = "create"


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
        columns = args[3:]
        return Create(table_name=table_name, columns=columns)
    elif c == Commands.INSERT.value:
        values = args[1:]
        return Insert(values=values)
    elif c == Commands.SELECT.value:
        if len(args) != 2:
            return None
        if args[1] == "*":
            return SelectAll()
        try:
            k = int(args[1])
        except ValueError:
            return None
        return Select(key=k)
    elif c == Commands.DELETE.value:
        try:
            k = int(args[1])
        except ValueError:
            return None
        return Delete(key=k)
    return None


def main() -> None:
    term = Terminal()
    style = Style.from_dict({"prompt": "#cb4239"})
    message = [("class:prompt", "toydb> ")]
    session = PromptSession(style=style, color_depth=ColorDepth.TRUE_COLOR)
    table: Optional[Table] = None
    with term.fullscreen(), term.location(0, 0):
        while True:
            try:
                i = session.prompt(message)
            except (KeyboardInterrupt, EOFError):
                sys.exit(1)
            command = parse_command(i.lower())
            if command is None:
                print(f"invalid command: {i}")
                continue
            if isinstance(command, Exit):
                break
            elif isinstance(command, Create):
                table = Table(name=command.table_name, spec=command.columns)
                print(f"created table {table._name} with columns {table._spec}")
            else:
                if table is None:
                    print("no table selected")
                else:
                    if isinstance(command, Insert):
                        success = table.insert(command.values)
                        if success:
                            print("OK")
                        else:
                            print(f"incorrect number of values, table has columns {table._spec}")
                    elif isinstance(command, Select):
                        print(table.get(command.key))
                    elif isinstance(command, SelectAll):
                        for record in table.get_all():
                            print(record)
                    elif isinstance(command, Delete):
                        success = table.delete(command.key)
                        if success:
                            print("OK")
                        else:
                            print("not found")
    print(f"Current database: {table}")


if __name__ == "__main__":
    main()
