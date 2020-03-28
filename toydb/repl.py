import sys
from contextlib import contextmanager
from typing import Iterator, Optional

from toydb.database import Database
from toydb.record import Record


@contextmanager
def repl() -> Iterator[None]:
    try:
        yield
    except KeyboardInterrupt:
        sys.exit()


def parse_command(command: str) -> Optional[int]:
    if not command.startswith("i"):
        return None
    args = command.split()
    if len(args) != 2:
        return None
    value = args[1]
    try:
        value_ = int(value)
    except ValueError:
        return None
    return value_


with repl():
    db = Database()
    while True:
        i = input("> ")
        should_exit = i == "q" or i == "exit" or i == "quit"
        if should_exit:
            break
        value = parse_command(i.lower())
        if value is None:
            print(f"invalid command: {i}")
            continue
        else:
            print(value)
        r = Record(value=value)
        db = Database(db.records + [r])
    print(f"Inserted records: {db}")
