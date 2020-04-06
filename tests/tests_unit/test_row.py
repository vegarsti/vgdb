from dataclasses import dataclass
from typing import List, Union

from toydb.row import Row


@dataclass
class PseudoRow:
    data: List[Union[str, int]]


class TestRow:
    def test_repr(self):
        r = Row(data=[1, "a"])
        assert str(r) == "1 a"

    def test_eq_true(self):
        r1 = Row(data=[1, "a"])
        r2 = Row(data=[1, "a"])
        assert r1 == r2

    def test_eq_false(self):
        r1 = Row(data=[1, "a"])
        r2 = Row(data=[1, "a", "b"])
        assert r1 != r2

    def test_eq_structural_equality_fails(self):
        r1 = Row(data=[1, "a"])
        r2 = PseudoRow(data=[1, "a"])
        assert r1 != r2
