import pytest

from toydb.record import Record
from toydb.table import Table


class TestTable:
    def test_insert_ok(self):
        t = Table(name="a", columns=[("b", str)])
        assert t.insert(["hei"]) is True
        assert t._records == [Record(data=["hei"])]

    def test_insert_incorrect_value(self):
        t = Table(name="a", columns=[("b", int)])
        insertion_ok = t.insert(["a"])
        assert insertion_ok is False

    def test_strings_to_record_fails(self):
        t = Table(name="a", columns=[("b", str), ("a", int)])
        with pytest.raises(ValueError):
            t._strings_to_record(["1", "hei"])

    def test_strings_to_record_ok(self):
        t = Table(name="a", columns=[("b", str), ("a", int)])
        assert t._strings_to_record(["hei", 1]) == Record(data=["hei", 1])

    def test_select(self):
        t = Table(name="a", columns=[("a", str), ("b", int)])
        t.insert(["a", "1"])
        t.insert(["b", "2"])
        records = list(i for i in t.select())
        assert all(isinstance(record, Record) for record in records)
        assert records == [Record(data=["a", 1]), Record(data=["b", 2])]

    def test_repr(self):
        table = Table(name="hei", columns=[("a", str), ("b", int)])
        table.insert(["a", "1"])
        table.insert(["hello", "9001"])
        assert str(table) == "a 1\nhello 9001"
