import pytest

from toydb.ast import Program
from toydb.lexer import Lexer
from toydb.parser import Parser
from toydb.statement import Select
from toydb.where import Predicate, Where


class TestParser:
    @pytest.mark.parametrize(
        argnames=("statement", "expected"),
        argvalues=[
            ("select a from b", Select(columns=["a"], table_name="b")),
            ("select a, b from b", Select(columns=["a", "b"], table_name="b")),
            (
                "select a from b where a = 'a'",
                Select(columns=["a"], table_name="b", where=Where(column="a", predicate=Predicate.EQUALS, value="a")),
            ),
            (
                "select a from b where a = 1",
                Select(columns=["a"], table_name="b", where=Where(column="a", predicate=Predicate.EQUALS, value=1)),
            ),
        ],
    )
    def test_parse_select(self, statement, expected):
        lexer = Lexer(program=statement)
        parser = Parser(lexer=lexer)
        program = parser.parse()
        statements = [expected]
        assert program == Program(statements=statements)
