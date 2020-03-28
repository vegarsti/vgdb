import sys
from contextlib import contextmanager
from typing import Iterator, Optional

from toydb.command import Command, Delete, Exit, Insert, Select
from toydb.database import Database


@contextmanager
def repl() -> Iterator[None]:
    try:
        yield
    except KeyboardInterrupt:
        sys.exit()


def parse_command(command: str) -> Optional[Command]:
    if command == "q" or command == "exit" or command == "quit":
        return Exit()
    if not any((command.startswith(Insert.s), command.startswith(Select.s), command.startswith(Delete.s))):
        return None
    args = command.split()
    if len(args) != 2:
        return None
    c, v = args
    try:
        value = int(v)
    except ValueError:
        return None
    if c == Insert.s:
        return Insert(value)
    elif c == Select.s:
        return Select(value)
    elif c == Delete.s:
        return Delete(value)
    else:
        raise ValueError("weird")


def main() -> None:
    with repl():
        db = Database()
        while True:
            i = input("> ")
            i_ = i.lower()
            command = parse_command(i_)
            if command is None:
                print(f"invalid command: {i}")
                continue
            if isinstance(command, Exit):
                break
            elif isinstance(command, Insert):
                db.insert(command.value)
                print(f"{i} OK")
            elif isinstance(command, Select):
                print(f"{i} {db.exists(command.value)}")
            elif isinstance(command, Delete):
                db.delete(command.value)
                print(f"{i} OK")
        print()
        print(f"Inserted records: {db}")


if __name__ == "__main__":
    main()
