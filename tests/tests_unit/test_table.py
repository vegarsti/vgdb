from pathlib import Path

import pytest

from toydb.table import Table


class TestTable:
    def test_insert_ok(self):
        t = Table(name="a", columns=[("b", str)])
        t.insert(["hei"])
        p = Path(f"{t.name}.db")
        assert list(t.all_rows()) == [["hei"]]
        p = Path(f"{t.name}.db")
        print(p)
        p.unlink()

    def test_insert_incorrect_value(self):
        t = Table(name="a", columns=[("b", int)])
        with pytest.raises(ValueError):
            t.insert(["a"])

    def test_strings_to_record_fails(self):
        t = Table(name="a", columns=[("b", str), ("a", int)])
        with pytest.raises(ValueError):
            t._strings_to_row(["1", "hei"])

    def test_strings_to_record_ok(self):
        t = Table(name="a", columns=[("b", str), ("a", int)])
        assert t._strings_to_row(["hei", "1"]) == ["hei", 1]

    def test_all_rows(self):
        t = Table(name="a", columns=[("a", str), ("b", int)])
        t.insert(["a", "1"])
        t.insert(["b", "2"])
        rows = list(i for i in t.all_rows())
        assert rows == [["a", 1], ["b", 2]]
