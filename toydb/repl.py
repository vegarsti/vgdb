import sys
from typing import Optional

from blessed import Terminal
from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style

from toydb.query_parser import parse_command
from toydb.statement import CreateTable, Exit, handle_command
from toydb.table import Table


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
        command = parse_command(c.lower().strip())
        if command is None:
            print(f"invalid command: {c}")
            continue
        if isinstance(command, Exit):
            break
        if isinstance(command, CreateTable):
            table = Table(name=command.table_name, columns=command.columns)
            print(f"created table {table.name} with schema {table.columns}")
        else:
            if table is None:
                print("please create a table")
            else:
                table = handle_command(table=table, command=command)


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
