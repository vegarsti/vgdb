from dataclasses import dataclass
from typing import List, Union

from toydb.record import Record


@dataclass
class PseudoRecord:
    data: List[Union[str, int]]


class TestRecord:
    def test_repr(self):
        r = Record(data=[1, "a"])
        assert str(r) == "1 a"

    def test_eq_true(self):
        r1 = Record(data=[1, "a"])
        r2 = Record(data=[1, "a"])
        assert r1 == r2

    def test_eq_false(self):
        r1 = Record(data=[1, "a"])
        r2 = Record(data=[1, "a", "b"])
        assert r1 != r2

    def test_eq_structural_equality_fails(self):
        r1 = Record(data=[1, "a"])
        r2 = PseudoRecord(data=[1, "a"])
        assert r1 != r2
