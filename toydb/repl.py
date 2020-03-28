import sys
from contextlib import contextmanager
from typing import Iterator, Optional, Tuple

from toydb.command import Command
from toydb.database import Database


@contextmanager
def repl() -> Iterator[None]:
    try:
        yield
    except KeyboardInterrupt:
        sys.exit()


def parse_command(command: str) -> Optional[Tuple[Command, int]]:
    if command == "q" or command == "exit" or command == "quit":
        return Command.EXIT, 0
    if not command.startswith(Command.INSERT.value) and not command.startswith(Command.SELECT.value):
        return None
    args = command.split()
    if len(args) != 2:
        return None
    c, v = args
    try:
        value = int(v)
    except ValueError:
        return None
    return Command(c), value


with repl():
    db = Database()
    while True:
        i = input("> ")
        i_ = i.lower()
        result = parse_command(i_)
        if result is None:
            print(f"invalid command: {i}")
            continue
        command, value = result
        if command is Command.EXIT:
            break
        if command is Command.INSERT:
            db.insert(value)
            print(f"{i} OK")
        elif command is Command.SELECT:
            print(f"{i} {db.exists(value)}")
    print()
    print(f"Inserted records: {db}")
