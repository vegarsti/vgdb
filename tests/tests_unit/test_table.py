import pytest

from toydb.table import Table


@pytest.fixture
def table():
    t = Table(name="a", columns=[("b", str), ("a", int)])
    t.create()
    yield t
    t._file.unlink()


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
