import re
from itertools import islice
from operator import and_, eq, ge, gt, le, lt, ne, or_
from typing import Callable, Dict, Iterable, Iterator, List, Optional, Sequence, Tuple, Type, Union

from toydb.statement import Conjunction, OrderBy, WhereStatement
from toydb.storage import Storage
from toydb.type import type_to_string
from toydb.where import Predicate, Where


def create_sort_key(
    indices: Sequence[int], signs: Sequence[int]
) -> Callable[[Sequence[Union[str, int]]], Tuple[Union[str, int], ...]]:
    def sort_key(row: Sequence[Union[str, int]]) -> Tuple[Union[str, int], ...]:
        return tuple(-sign * row[i] for i, sign in zip(indices, signs))

    return sort_key


def create_like_key(like: str) -> Callable[[str], bool]:
    pattern = "^"
    for i in like:
        if i == "%":
            pattern += "(.*)"
        elif i == "_":
            pattern += "(.){1}"
        else:
            pattern += i
    pattern += "$"
    regex_rule = re.compile(pattern)

    def f(cell: str) -> bool:
        return regex_rule.search(cell) is not None

    return f


predicate_map = {
    Predicate.EQUALS: eq,
    Predicate.NOT_EQUALS: ne,
    Predicate.LT: lt,
    Predicate.GT: gt,
    Predicate.LTEQ: le,
    Predicate.GTEQ: ge,
}
conjunction_map = {
    Conjunction.AND: and_,
    Conjunction.OR: or_,
}


def reduce_booleans_using_conjunctions(
    conditions: List[bool], conjunctions: List[Callable[[bool, bool], bool]]
) -> bool:
    if len(conditions) == 1:
        return conditions[0]
    condition_1 = conditions.pop(0)
    condition_2 = conditions.pop(0)
    conjunction = conjunctions.pop(0)
    new_value = conjunction(condition_1, condition_2)
    new_conditions = [new_value] + conditions
    return reduce_booleans_using_conjunctions(conditions=new_conditions, conjunctions=conjunctions)


class Table:
    def __init__(self, name: str, columns: Sequence[Tuple[str, Type]]) -> None:
        self.name = name
        self._file = Storage(filename=name, columns=columns)
        self._spec = tuple(columns)
        self._columns: Dict[str, Type] = {name: type_ for name, type_ in columns}
        self._types = list(self._columns.values())

    def persist(self) -> None:
        try:
            self._file.persist()
        except FileExistsError:
            raise ValueError(f"table {self.name} already exists")

    @property
    def columns(self) -> str:
        return "(" + ", ".join(f"{name} {type_to_string[type_]}" for name, type_ in self._columns.items()) + ")"

    def all_rows(self) -> Iterator[List[Union[int, str]]]:
        return self._file.read_rows()

    def column_name_to_index(self, c: str) -> int:
        try:
            return list(self._columns.keys()).index(c)
        except ValueError:
            raise ValueError(f"incorrect column {c}, table has schema {self.columns}")

    def column_indices_from_names(self, columns: List[str]) -> Optional[List[int]]:
        if columns == ["all"]:
            return [i for i, _ in enumerate(self._columns.keys())]
        column_indices_to_select = []
        for c in columns:
            j = self.column_name_to_index(c)
            if j is None:
                return None
            column_indices_to_select.append(j)
        return column_indices_to_select

    def _where(self, row: List[Union[str, int]], where: Where) -> bool:
        column_index = self.column_name_to_index(where.column)
        type_of_column = self._types[column_index]
        where_value_typed = type_of_column(where.value)
        cell = row[column_index]
        if where.predicate == Predicate.LIKE:
            if not isinstance(cell, str):
                raise ValueError("LIKE must be used with string columns")
            condition = create_like_key(where_value_typed)(cell)
        else:
            condition = predicate_map[where.predicate](cell, where_value_typed)
        return condition

    def where(self, rows: Iterable[List[Union[str, int]]], where: WhereStatement) -> Iterator[List[Union[str, int]]]:
        for row in rows:
            conditions = [self._where(row=row, where=w) for w in where.conditions]
            conjunctions = [conjunction_map[c] for c in where.conjunctions]
            should_yield = reduce_booleans_using_conjunctions(conditions=conditions, conjunctions=conjunctions)
            if should_yield:
                yield row

    def order_by(self, rows: Iterable[List[Union[str, int]]], order_by: OrderBy) -> Iterator[List[Union[str, int]]]:
        order_by_indices = self.column_indices_from_names(order_by.columns)
        if order_by_indices is None:
            raise ValueError(
                f"incorrect columns {', '.join(order_by.columns)} in ORDER BY: table has schema {self.columns}"
            )
        signs = [2 * int(b) - 1 for b in order_by.descending]
        sort_key = create_sort_key(order_by_indices, signs)
        return iter(sorted(rows, key=sort_key))

    def limit(self, rows: Iterable[List[Union[str, int]]], limit: int) -> Iterator[List[Union[str, int]]]:
        return islice(rows, limit)

    def insert(self, row: Sequence[Union[int, str]]) -> None:
        self._file.insert(row)

    @classmethod
    def from_file(cls, name: str) -> "Table":
        s = Storage.from_file(name)
        columns = s._columns_as_they_came
        return Table(name, columns)
