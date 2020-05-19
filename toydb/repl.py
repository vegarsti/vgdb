import sys
from functools import partial
from typing import Callable, Optional, Union

from blessed import Terminal
from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style

from toydb.evaluator import Evaluator
from toydb.get_tables import get_tables
from toydb.lexer import Lexer
from toydb.parser import Parser
from toydb.statement import CreateTable, Insert, Select


def loop(prompt: Callable[[], str]) -> None:
    tables = get_tables()
    evaluator = Evaluator(tables=tables)
    while True:
        try:
            c = prompt()
        except (KeyboardInterrupt, EOFError):
            sys.exit(1)
        user_input = c.lower().strip()
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
            evaluator.handle_command(command)
        except ValueError as e:
            print(str(e))


def main() -> None:
    style = Style.from_dict({"prompt": "red"})
    message = [("class:prompt", "toydb> ")]
    session = PromptSession(style=style)
    toydb_prompt = partial(session.prompt, message)
    fullscreen = False
    if fullscreen:
        term = Terminal()
        with term.fullscreen(), term.location(0, 0):
            loop(toydb_prompt)
    else:
        loop(toydb_prompt)


if __name__ == "__main__":
    main()
