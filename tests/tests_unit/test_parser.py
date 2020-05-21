import pytest

from toydb.lexer import Lexer
from toydb.parser import Parser
from toydb.statement import Conjunction, CreateTable, Insert, OrderBy, Select, WhereStatement
from toydb.where import Predicate, Where


class TestParser:
    @pytest.mark.parametrize(
        argnames=("statement", "expected"),
        argvalues=[
            ("select a from b", Select(columns=["a"], table_name="b", where=None)),
            ("select a, b from b", Select(columns=["a", "b"], table_name="b", where=None)),
            ("select * from b", Select(columns=["all"], table_name="b", where=None)),
            ("select * from b limit 1", Select(columns=["all"], table_name="b", where=None, limit=1)),
            (
                "select * from b limit 1 order by b",
                Select(
                    columns=["all"],
                    table_name="b",
                    where=None,
                    limit=1,
                    order_by=OrderBy(columns=["b"], descending=[False]),
                ),
            ),
            (
                "select * from b limit 1 order by b desc",
                Select(
                    columns=["all"],
                    table_name="b",
                    where=None,
                    limit=1,
                    order_by=OrderBy(columns=["b"], descending=[True]),
                ),
            ),
            (
                "select * from b limit 1 order by b, a",
                Select(
                    columns=["all"],
                    table_name="b",
                    where=None,
                    limit=1,
                    order_by=OrderBy(columns=["b", "a"], descending=[False, False]),
                ),
            ),
            (
                "select * from b limit 1 order by b, a desc",
                Select(
                    columns=["all"],
                    table_name="b",
                    where=None,
                    limit=1,
                    order_by=OrderBy(columns=["b", "a"], descending=[False, True]),
                ),
            ),
            (
                "select a from b where a = 'a'",
                Select(
                    columns=["a"],
                    table_name="b",
                    where=WhereStatement(
                        conditions=[Where(column="a", predicate=Predicate.EQUALS, value="a")], conjunctions=[],
                    ),
                ),
            ),
            (
                "select a from b where a = 1",
                Select(
                    columns=["a"],
                    table_name="b",
                    where=WhereStatement(
                        conditions=[Where(column="a", predicate=Predicate.EQUALS, value=1)], conjunctions=[],
                    ),
                ),
            ),
            (
                "select a from b where a < 1",
                Select(
                    columns=["a"],
                    table_name="b",
                    where=WhereStatement(
                        conditions=[Where(column="a", predicate=Predicate.LT, value=1)], conjunctions=[],
                    ),
                ),
            ),
            (
                "select a from b where a > 1",
                Select(
                    columns=["a"],
                    table_name="b",
                    where=WhereStatement(
                        conditions=[Where(column="a", predicate=Predicate.GT, value=1)], conjunctions=[],
                    ),
                ),
            ),
            (
                "select a from b where a != 1",
                Select(
                    columns=["a"],
                    table_name="b",
                    where=WhereStatement(
                        conditions=[Where(column="a", predicate=Predicate.NOT_EQUALS, value=1)], conjunctions=[],
                    ),
                ),
            ),
            (
                "select a from b where a <= 1",
                Select(
                    columns=["a"],
                    table_name="b",
                    where=WhereStatement(
                        conditions=[Where(column="a", predicate=Predicate.LTEQ, value=1)], conjunctions=[],
                    ),
                ),
            ),
            (
                "select a from b where a >= 1",
                Select(
                    columns=["a"],
                    table_name="b",
                    where=WhereStatement(
                        conditions=[Where(column="a", predicate=Predicate.GTEQ, value=1)], conjunctions=[],
                    ),
                ),
            ),
            (
                "select a from b where a < 1 and a > 0",
                Select(
                    columns=["a"],
                    table_name="b",
                    where=WhereStatement(
                        conditions=[
                            Where(column="a", predicate=Predicate.LT, value=1),
                            Where(column="a", predicate=Predicate.GT, value=0),
                        ],
                        conjunctions=[Conjunction.AND],
                    ),
                ),
            ),
            (
                "select a from b where a < 1 and a > 0 or a = 1",
                Select(
                    columns=["a"],
                    table_name="b",
                    where=WhereStatement(
                        conditions=[
                            Where(column="a", predicate=Predicate.LT, value=1),
                            Where(column="a", predicate=Predicate.GT, value=0),
                            Where(column="a", predicate=Predicate.EQUALS, value=1),
                        ],
                        conjunctions=[Conjunction.AND, Conjunction.OR],
                    ),
                ),
            ),
            (
                "select a from b where a < 1 or a > 0",
                Select(
                    columns=["a"],
                    table_name="b",
                    where=WhereStatement(
                        conditions=[
                            Where(column="a", predicate=Predicate.LT, value=1),
                            Where(column="a", predicate=Predicate.GT, value=0),
                        ],
                        conjunctions=[Conjunction.OR],
                    ),
                ),
            ),
            (
                "select a from b where a < 1 or a > 0 limit 2",
                Select(
                    columns=["a"],
                    table_name="b",
                    where=WhereStatement(
                        conditions=[
                            Where(column="a", predicate=Predicate.LT, value=1),
                            Where(column="a", predicate=Predicate.GT, value=0),
                        ],
                        conjunctions=[Conjunction.OR],
                    ),
                    limit=2,
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
