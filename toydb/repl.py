import sys
from contextlib import contextmanager
from typing import Iterator, Optional


@contextmanager
def repl() -> Iterator[None]:
    try:
        yield
    except KeyboardInterrupt:
        sys.exit()


def parse_command(command: str) -> Optional[str]:
    return command


with repl():
    while True:
        i = input("> ")
        should_exit = i == "q" or i == "exit" or i == "quit"
        if should_exit:
            sys.exit()
        command = parse_command(i)
        if command is None:
            print("invalid command")
        else:
            print(command)
