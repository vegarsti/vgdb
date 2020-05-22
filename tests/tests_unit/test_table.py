from operator import and_, or_

import pytest

from toydb.statement import WhereStatement
from toydb.table import Table, reduce_booleans_using_conjunctions
from toydb.where import Predicate, Where


@pytest.fixture
def table():
    t = Table(name="a", columns=[("b", str), ("a", int)])
    t.persist()
    yield t
    t._file.delete()


class TestTable:
    def test_insert_ok(self, table):
        table.insert(["hei", 1])
        assert list(table.all_rows()) == [["hei", 1]]

    def test_insert_incorrect_value(self, table):
        with pytest.raises(ValueError):
            table.insert(["a", "a"])

    def test_all_rows(self, table):
        table.insert(["a", "1"])
        table.insert(["b", "2"])
        rows = list(i for i in table.all_rows())
        assert rows == [["a", 1], ["b", 2]]

    def test_rows_with_where(self, table):
        table.insert(["a", 1])
        table.insert(["b", 2])
        result = table.where(
            rows=table.all_rows(),
            where=WhereStatement(conditions=[Where(column="a", predicate=Predicate.EQUALS, value=1)], conjunctions=[]),
        )
        assert list(result) == [["a", 1]]
        result = table.where(
            rows=table.all_rows(),
            where=WhereStatement(conditions=[Where(column="a", predicate=Predicate.EQUALS, value=3)], conjunctions=[]),
        )
        assert list(result) == []

    def test_limit(self, table):
        table.insert(["a", 1])
        table.insert(["b", 2])
        result = table.limit(rows=table.all_rows(), limit=1)
        assert list(result) == [["a", 1]]

    def test_reduce(self):
        assert reduce_booleans_using_conjunctions(conditions=[True, False], conjunctions=[and_]) is False
        assert reduce_booleans_using_conjunctions(conditions=[True, False], conjunctions=[or_]) is True
        assert reduce_booleans_using_conjunctions(conditions=[False, False, True], conjunctions=[and_, or_]) is True
