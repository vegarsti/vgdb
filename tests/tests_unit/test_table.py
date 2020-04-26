import pytest

from toydb.table import Table


class TestTable:
    def test_insert_ok(self):
        t = Table(name="a", columns=[("b", str)])
        t.create()
        t.insert([("hei", str)])
        assert list(t.all_rows()) == [["hei"]]
        t._file.unlink()

    def test_insert_incorrect_value(self):
        t = Table(name="a", columns=[("b", int)])
        t.create()
        with pytest.raises(ValueError):
            t.insert([("a", str)])
        t._file.unlink()

    def test_strings_to_record_fails(self):
        t = Table(name="a", columns=[("b", str), ("a", int)])
        t.create()
        with pytest.raises(ValueError):
            t._strings_to_row(["1", "hei"])
        t._file.unlink()

    def test_strings_to_record_ok(self):
        t = Table(name="a", columns=[("b", str), ("a", int)])
        assert t._strings_to_row(["hei", "1"]) == ["hei", 1]

    def test_all_rows(self):
        t = Table(name="a", columns=[("a", str), ("b", int)])
        t.create()
        t.insert([("a", str), (1, int)])
        t.insert([("b", str), (2, int)])
        rows = list(i for i in t.all_rows())
        assert rows == [["a", 1], ["b", 2]]
        t._file.unlink()
