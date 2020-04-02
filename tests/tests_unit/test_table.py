from toydb.table import Table


class TestTable:
    def test_init_ok(self):
        Table(name="a", columns=[("b", str)])
