from toydb.ast import Program
from toydb.lexer import Lexer
from toydb.parser import Parser
from toydb.statement import Select
from toydb.where import Predicate, Where


class TestParser:
    def test_parse_select(self):
        lexer = Lexer(program="select a from b")
        parser = Parser(lexer=lexer)
        program = parser.parse()
        statements = [Select(columns=["a"], table_name="b")]
        assert program == Program(statements=statements)

    def test_parse_select_with_were(self):
        lexer = Lexer(program="select a from b where a = 'a'")
        parser = Parser(lexer=lexer)
        program = parser.parse()
        statements = [
            Select(columns=["a"], table_name="b", where=Where(column="a", predicate=Predicate.EQUALS, value="a"))
        ]
        assert program == Program(statements=statements)
