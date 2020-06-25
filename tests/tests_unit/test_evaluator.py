from typing import List, Optional, Union

from vgdb.evaluator import Evaluator
from vgdb.lexer import Lexer
from vgdb.parser import Parser
from vgdb.statement import CreateTable, Insert, Select
from vgdb.table import Table


class TestEvaluator:
    def test_a(self):
        user_input = "select * from family"
        lexer = Lexer(program=user_input)
        parser = Parser(lexer=lexer)
        commands: List[Optional[Union[CreateTable, Insert, Select]]] = []
        commands = list(parser.parse())
        table = Table.from_file("family")
        tables = {"family": table}
        evaluator = Evaluator(tables=tables)
        result = evaluator.handle_command(commands[0])
        assert len(result) > 10
        assert result[0] == ["vegard", 26]

    def test_in_memory(self):
        user_input = "select * from family"
        lexer = Lexer(program=user_input)
        parser = Parser(lexer=lexer)
        commands: List[Optional[Union[CreateTable, Insert, Select]]] = []
        commands = list(parser.parse())
        table = Table.from_file("family", storage_type="in-memory")
        tables = {"family": table}
        evaluator = Evaluator(tables=tables)
        result = evaluator.handle_command(commands[0])
        assert len(result) > 10
        assert result[0] == ["vegard", 26]
