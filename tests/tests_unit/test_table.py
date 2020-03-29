from toydb.table import Table


class TestTable:
    def test_set_does_not_mutate(self):
        table = Table()
        table_records = table._records
        table.set("a", "b")
        assert table._records == table_records

    def test_get_ok(self):
        assert Table().set("a", "b").get("a") == "b"
        assert Table().get("b") is None
