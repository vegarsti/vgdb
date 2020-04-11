import pytest

from toydb.command import CreateTable, Exit, Insert, Select
from toydb.query_parser import parse_command


class TestParseCommand:
    def test_exit_ok(self):
        assert parse_command("q") == Exit()

    def test_select_all_ok(self):
        assert parse_command("select *") == Select(columns=["all"])

    def test_select_columns_ok(self):
        assert parse_command("select a, b") == Select(columns=["a", "b"])

    def test_select_columns_invalid(self):
        assert parse_command("select a b") is None

    def test_insert_ok(self):
        assert parse_command("insert a") == Insert(values=["a"])

    def test_create_table_ok__1(self):
        assert parse_command("create table a (b str)") == CreateTable(table_name="a", columns=[("b", str)])

    def test_create_table_ok__2(self):
        assert parse_command("create table tbl (a int, b str)") == CreateTable(
            table_name="tbl", columns=[("a", int), ("b", str)]
        )

    def test_insert_fail(self):
        assert parse_command("insert") is None

    @pytest.mark.parametrize(
        argnames="command", argvalues=["create", "create table", "create table tbl", "create table tbl a"]
    )
    def test_create_table_fail(self, command):
        assert parse_command(command) is None
