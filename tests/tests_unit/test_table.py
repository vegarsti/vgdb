from operator import and_, or_

import pytest

from vgdb.statement import WhereStatement
from vgdb.table import Table, create_like_key, reduce_booleans_using_conjunctions
from vgdb.where import Predicate, Where


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

    def test_rows_with_where_like(self, table):
        table.insert(["aaaa", 1])
        table.insert(["aaba", 2])
        table.insert(["abaaa", 3])
        result = table.where(
            rows=table.all_rows(),
            where=WhereStatement(
                conditions=[Where(column="b", predicate=Predicate.LIKE, value="aa%")], conjunctions=[]
            ),
        )
        assert list(result) == [["aaaa", 1], ["aaba", 2]]
        result = table.where(
            rows=table.all_rows(),
            where=WhereStatement(
                conditions=[Where(column="b", predicate=Predicate.LIKE, value="a___")], conjunctions=[]
            ),
        )
        assert list(result) == [["aaaa", 1], ["aaba", 2]]
        result = table.where(
            rows=table.all_rows(),
            where=WhereStatement(
                conditions=[Where(column="b", predicate=Predicate.LIKE, value="a_%a")], conjunctions=[]
            ),
        )
        assert list(result) == [["aaaa", 1], ["aaba", 2], ["abaaa", 3]]

    def test_limit(self, table):
        table.insert(["a", 1])
        table.insert(["b", 2])
        result = table.limit(rows=table.all_rows(), limit=1, offset=0)
        assert list(result) == [["a", 1]]

    def test_reduce(self):
        assert reduce_booleans_using_conjunctions(conditions=[True, False], conjunctions=[and_]) is False
        assert reduce_booleans_using_conjunctions(conditions=[True, False], conjunctions=[or_]) is True
        assert reduce_booleans_using_conjunctions(conditions=[False, False, True], conjunctions=[and_, or_]) is True

    def test_make_like(self):
        key1 = create_like_key(like="a_")
        assert key1("a") is False
        assert key1("aa") is True
        assert key1("bab") is False
        key2 = create_like_key(like="a%b")
        assert key2("abab") is True
        assert key2("aba") is False
        assert key2("ab") is True
        key3 = create_like_key(like="a_%b")
        assert key3("aab") is True
        assert key3("aaaaaaab") is True
        assert key3("ab") is False
