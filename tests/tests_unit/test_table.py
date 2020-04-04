import pytest

from toydb.table import Table


class TestTable:
    def test_insert_ok(self):
        t = Table(name="a", columns=[("b", str)])
        assert t.insert(["hei"]) is True
        assert t._records == [["hei"]]

    def test_insert_incorrect_value(self):
        t = Table(name="a", columns=[("b", str)])
        assert t.insert([1]) is False

    def test_strings_to_record(self):
        t = Table(name="a", columns=[("b", str), ("a", int)])
        with pytest.raises(ValueError):
            t._strings_to_record(["1", "hei"])

    def test_get_all(self):
        t = Table(name="a", columns=[("b", int)])
        t.insert(["1"])
        t.insert(["2"])
        assert list(i for i in t.select()) == [[1], [2]]
