import pytest

from toydb.query_parser import parse_command
from toydb.statement import CreateTable, Exit, Insert, Select
from toydb.where import Predicate, Where


class TestParseCommand:
    def test_exit_ok(self):
        assert parse_command("q") == Exit()

    def test_select_all_ok(self):
        assert parse_command("select * from tbl") == Select(columns=["all"], table_name="tbl")

    def test_select_columns_ok(self):
        assert parse_command("select a, b from tbl") == Select(columns=["a", "b"], table_name="tbl")

    def test_select_with_where(self):
        assert parse_command("select a, b from tbl where a = 1") == Select(
            columns=["a", "b"], where=Where(column="a", predicate=Predicate.EQUAL, value="1"), table_name="tbl"
        )

    def test_select_columns_invalid(self):
        assert parse_command("select a b") is None

    def test_insert_ok(self):
        assert parse_command("insert into b values (a)") == Insert(values=["a"], table_name="b")
        assert parse_command("insert into b values (a, b, c, d)") == Insert(values=["a", "b", "c", "d"], table_name="b")

    def test_create_table_ok__1(self):
        assert parse_command("create table a (b text)") == CreateTable(table_name="a", columns=[("b", str)])

    def test_create_table_ok__2(self):
        assert parse_command("create table tbl (a int, b text)") == CreateTable(
            table_name="tbl", columns=[("a", int), ("b", str)]
        )

    def test_insert_fail(self):
        assert parse_command("insert") is None
        assert parse_command("insert into b values c") is None

    @pytest.mark.parametrize(
        argnames="command", argvalues=["create", "create table", "create table tbl", "create table tbl a"]
    )
    def test_create_table_fail(self, command):
        assert parse_command(command) is None
