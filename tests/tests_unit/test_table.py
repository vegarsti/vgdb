import pytest

from toydb.table import Table


@pytest.fixture
def table():
    yield Table(name="a", spec=["b", "c"])


class TestTable:
    def test_init_ok(self):
        Table(name="a", spec=["b", "c"])

    def test_set_does_not_mutate(self, table):
        table.set("a", "b")

    def test_get_ok(self):
        assert Table().set("a", "b").get("a") == "b"
        assert Table().get("b") is None
