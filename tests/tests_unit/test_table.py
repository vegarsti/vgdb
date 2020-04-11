import pytest

from toydb.row import Row
from toydb.table import Table


class TestTable:
    def test_insert_ok(self):
        t = Table(name="a", columns=[("b", str)])
        assert t.insert(["hei"]) is True
        assert t._rows == [Row(data=["hei"])]

    def test_insert_incorrect_value(self):
        t = Table(name="a", columns=[("b", int)])
        insertion_ok = t.insert(["a"])
        assert insertion_ok is False

    def test_strings_to_record_fails(self):
        t = Table(name="a", columns=[("b", str), ("a", int)])
        with pytest.raises(ValueError):
            t._strings_to_row(["1", "hei"])

    def test_strings_to_record_ok(self):
        t = Table(name="a", columns=[("b", str), ("a", int)])
        assert t._strings_to_row(["hei", 1]) == Row(data=["hei", 1])

    def test_all_rows(self):
        t = Table(name="a", columns=[("a", str), ("b", int)])
        t.insert(["a", "1"])
        t.insert(["b", "2"])
        records = list(i for i in t.all_rows())
        assert all(isinstance(record, Row) for record in records)
        assert records == [Row(data=["a", 1]), Row(data=["b", 2])]
