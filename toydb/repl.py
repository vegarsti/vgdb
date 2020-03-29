import sys
from contextlib import contextmanager
from typing import Iterator, Optional

from toydb.command import Command, Delete, Exit, Insert, Select
from toydb.table import Table


@contextmanager
def repl() -> Iterator[None]:
    try:
        yield
    except KeyboardInterrupt:
        sys.exit()


def parse_command(command: str) -> Optional[Command]:
    if command == "q" or command == "exit" or command == "quit":
        return Exit()
    args = command.split()
    if len(args) == 3:
        c, k, v = args
        if c == Insert.s:
            return Insert(key=k, value=v)
    elif len(args) == 2:
        c, k = args
        if c == Select.s:
            return Select(key=k)
        elif c == Delete.s:
            return Delete(key=k)
    return None


def main() -> None:
    with repl():
        db = Table()
        while True:
            i = input("> ")
            command = parse_command(i.lower())
            if command is None:
                print(f"invalid command: {i}")
                continue
            if isinstance(command, Exit):
                break
            elif isinstance(command, Insert):
                db = db.set(command.key, command.value)
                print("OK")
            elif isinstance(command, Select):
                print(db.get(command.key))
            elif isinstance(command, Delete):
                db = db.delete(command.key)
                print("OK")
        print()
        print(f"Database: {db}")


if __name__ == "__main__":
    main()
