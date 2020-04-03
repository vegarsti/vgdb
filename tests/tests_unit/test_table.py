from toydb.table import Table


class TestTable:
    def test_insert_ok(self):
        t = Table(name="a", columns=[("b", str)])
        assert t.insert(["hei"]) is True
        assert t._records == [["hei"]]

    def test_insert_incorrect_value(self):
        t = Table(name="a", columns=[("b", str)])
        assert t.insert([1]) is False

    def test_get_all(self):
        t = Table(name="a", columns=[("b", int)])
        t.insert(["1"])
        t.insert(["2"])
        assert list(i for i in t.get_all()) == [[1], [2]]
