import pytest

from toydb.table import Table
from toydb.where import Predicate, Where


@pytest.fixture
def table():
    t = Table(name="a", columns=[("b", str), ("a", int)])
    t.persist()
    yield t
    t._file.delete()


class TestTable:
    def test_insert_ok(self, table):
        table.insert(["hei", 1])
        assert list(table.all_rows()) == [["hei", 1]]

    def test_insert_incorrect_value(self, table):
        with pytest.raises(ValueError):
            table.insert(["a", "a"])

    def test_strings_to_record_ok(self, table):
        assert table._strings_to_row(["hei", "1"]) == ["hei", 1]

    def test_all_rows(self, table):
        table.insert(["a", "1"])
        table.insert(["b", "2"])
        rows = list(i for i in table.all_rows())
        assert rows == [["a", 1], ["b", 2]]

    def test_select_limit(self, table):
        table.insert(["a", 1])
        table.insert(["b", 2])
        assert list(table.select(columns=[0, 1])) == [["a", 1], ["b", 2]]
        assert list(table.select(columns=[0, 1], limit=1)) == [["a", 1]]

    def test_select_where(self, table):
        table.insert(["a", 1])
        table.insert(["b", 2])
        assert list(table.select(columns=[0, 1], where=Where(column="a", predicate=Predicate.EQUAL, value=1))) == [
            ["a", 1]
        ]
        assert list(table.select(columns=[0, 1], where=Where(column="a", predicate=Predicate.EQUAL, value=3))) == []
