import pytest

from toydb.command import Exit, Insert
from toydb.repl import parse_command


class TestREPL:
    def test_parse_command__insert(self):
        command = "i a b"
        assert parse_command(command) == Insert(key="a", value="b")

    @pytest.mark.parametrize(argnames="command", argvalues=["q", "exit", "quit"])
    def test_parse_command__exit(self, command):
        assert parse_command(command) == Exit()
