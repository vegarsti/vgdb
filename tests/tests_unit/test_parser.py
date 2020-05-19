import pytest

from toydb.lexer import Lexer
from toydb.parser import Parser
from toydb.statement import CreateTable, Insert, Select
from toydb.where import Predicate, Where


class TestParser:
    @pytest.mark.parametrize(
        argnames=("statement", "expected"),
        argvalues=[
            ("select a from b", Select(columns=["a"], table_name="b", where=[])),
            ("select a, b from b", Select(columns=["a", "b"], table_name="b", where=[])),
            ("select * from b", Select(columns=["all"], table_name="b", where=[])),
            (
                "select a from b where a = 'a'",
                Select(columns=["a"], table_name="b", where=[Where(column="a", predicate=Predicate.EQUALS, value="a")]),
            ),
            (
                "select a from b where a = 1",
                Select(columns=["a"], table_name="b", where=[Where(column="a", predicate=Predicate.EQUALS, value=1)]),
            ),
            (
                "select a from b where a < 1",
                Select(columns=["a"], table_name="b", where=[Where(column="a", predicate=Predicate.LT, value=1)]),
            ),
            (
                "select a from b where a > 1",
                Select(columns=["a"], table_name="b", where=[Where(column="a", predicate=Predicate.GT, value=1)]),
            ),
            (
                "select a from b where a != 1",
                Select(
                    columns=["a"], table_name="b", where=[Where(column="a", predicate=Predicate.NOT_EQUALS, value=1)]
                ),
            ),
            (
                "select a from b where a <= 1",
                Select(columns=["a"], table_name="b", where=[Where(column="a", predicate=Predicate.LTEQ, value=1)]),
            ),
            (
                "select a from b where a >= 1",
                Select(columns=["a"], table_name="b", where=[Where(column="a", predicate=Predicate.GTEQ, value=1)]),
            ),
            (
                "select a from b where a < 1 and a > 0",
                Select(
                    columns=["a"],
                    table_name="b",
                    where=[
                        Where(column="a", predicate=Predicate.LT, value=1),
                        Where(column="a", predicate=Predicate.GT, value=0),
                    ],
                ),
            ),
        ],
    )
    def test_parse_select(self, statement, expected):
        lexer = Lexer(program=statement)
        parser = Parser(lexer=lexer)
        statement = parser.parse()
        assert statement == expected

    @pytest.mark.parametrize(
        argnames=("statement", "expected"),
        argvalues=[
            ("insert into b values ('a', 'b', 1)", Insert(values=["a", "b", 1], table_name="b")),
            ("insert into b values ('a')", Insert(values=["a"], table_name="b")),
        ],
    )
    def test_parse_insert(self, statement, expected):
        lexer = Lexer(program=statement)
        parser = Parser(lexer=lexer)
        statement = parser.parse()
        assert statement == expected

    @pytest.mark.parametrize(
        argnames=("statement", "expected"),
        argvalues=[
            ("create table a (a text)", CreateTable(table_name="a", columns=[("a", str)])),
            ("create table a (a text, b int)", CreateTable(table_name="a", columns=[("a", str), ("b", int)])),
        ],
    )
    def test_parse_create_table(self, statement, expected):
        lexer = Lexer(program=statement)
        parser = Parser(lexer=lexer)
        statement = parser.parse()
        assert statement == expected
