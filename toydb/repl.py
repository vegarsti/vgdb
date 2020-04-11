import sys
from typing import Optional

from blessed import Terminal
from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style

from toydb.command import Exit, handle_command, parse_command
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
