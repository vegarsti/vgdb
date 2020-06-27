import re
from functools import partial
from itertools import islice
from operator import and_, eq, ge, gt, itemgetter, le, lt, ne, or_
from typing import Callable, Dict, Iterable, Iterator, List, Literal, Optional, Sequence, Tuple, Type, Union

from vgdb.statement import Conjunction, OrderBy, WhereStatement
from vgdb.storage import InMemoryStorage, PersistentStorage, StorageInterface
from vgdb.type import type_to_string
from vgdb.where import Predicate, Where


def create_sort_key(
    indices: Sequence[int], descending: Sequence[bool]
) -> Callable[[Sequence[Union[str, int]]], Tuple[Union[str, int], ...]]:
    signs = [2 * int(b) - 1 for b in descending]

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


predicate_map: Dict[Predicate, Callable[[Union[int, str], Union[int, str]], bool]] = {
    Predicate.EQUALS: eq,
    Predicate.NOT_EQUALS: ne,
    Predicate.LT: gt,
    Predicate.GT: lt,
    Predicate.LTEQ: ge,
    Predicate.GTEQ: le,
}
conjunction_map: Dict[Conjunction, Callable[[bool, bool], bool]] = {
    Conjunction.AND: and_,
    Conjunction.OR: or_,
}


def reduce_booleans_using_conjunctions(
    predicate_results: List[bool], conjunctions: Sequence[Callable[[bool, bool], bool]]
) -> bool:
    if len(predicate_results) == 1:
        return predicate_results[0]
    combined_value = conjunctions[0](predicate_results[0], predicate_results[1])
    return reduce_booleans_using_conjunctions(
        predicate_results=[combined_value] + predicate_results[2:], conjunctions=conjunctions[1:]
    )


class Table:
    def __init__(
        self,
        name: str,
        columns: Sequence[Tuple[str, Type]],
        storage_type: Literal["in-memory", "persistent"] = "persistent",
    ) -> None:
        self.name = name
        self._file: StorageInterface
        if storage_type == "in-memory":
            self._file = InMemoryStorage(name=name, columns=columns)
        elif storage_type == "persistent":
            self._file = PersistentStorage(filename=name, columns=columns)
        self._columns: Dict[str, Type] = {name: typ for name, typ in columns}
        self._types = tuple(self._columns.values())

    def persist(self) -> None:
        try:
            self._file.persist()
        except FileExistsError:
            raise ValueError(f"table {self.name} already exists")

    @property
    def columns(self) -> str:
        return "(" + ", ".join(f"{name} {type_to_string[typ]}" for name, typ in self._columns.items()) + ")"

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

    def create_predicate(self, where: Where) -> Callable[[Union[int, str]], bool]:
        column_index = self.column_name_to_index(where.column)
        type_of_column = self._types[column_index]
        predicate: Callable[[Union[int, str]], bool]
        if where.predicate == Predicate.LIKE:
            if type_of_column != str:
                raise ValueError("LIKE must be used with string columns")
            where_value_typed = str(where.value)
            predicate = create_like_key(where_value_typed)  # type: ignore
        else:
            where_value_typed = type_of_column(where.value)
            predicate_operator = predicate_map[where.predicate]
            predicate = partial(predicate_operator, where_value_typed)
        return predicate

    def where(self, rows: Iterable[List[Union[str, int]]], where: WhereStatement) -> Iterator[List[Union[str, int]]]:
        conjunctions = [conjunction_map[c] for c in where.conjunctions]
        predicates = [self.create_predicate(w) for w in where.conditions]
        column_indices = [self.column_name_to_index(w.column) for w in where.conditions]
        getters = [itemgetter(c) for c in column_indices]
        for row in rows:
            predicate_results = [predicate(getter(row)) for getter, predicate in zip(getters, predicates)]
            should_yield = reduce_booleans_using_conjunctions(
                predicate_results=predicate_results, conjunctions=conjunctions
            )
            if should_yield:
                yield row

    def order_by(self, rows: Iterable[List[Union[str, int]]], order_by: OrderBy) -> Iterator[List[Union[str, int]]]:
        order_by_indices = self.column_indices_from_names(order_by.columns)
        if order_by_indices is None:
            raise ValueError(
                f"incorrect columns {', '.join(order_by.columns)} in ORDER BY: table has schema {self.columns}"
            )
        sort_key = create_sort_key(order_by_indices, order_by.descending)
        return iter(sorted(rows, key=sort_key))

    def limit(
        self, rows: Iterable[List[Union[str, int]]], limit: int, offset: Optional[int]
    ) -> Iterator[List[Union[str, int]]]:
        if offset is None:
            return islice(rows, limit)
        else:
            return islice(rows, offset, limit + offset)

    def insert(self, row: Sequence[Union[int, str]]) -> None:
        self._file.insert(row)

    @classmethod
    def from_file(cls, name: str, storage_type: Literal["in-memory", "persistent"] = "persistent") -> "Table":
        s = PersistentStorage.from_file(name)
        rows = list(s.read_rows())
        columns = s._columns_as_they_came
        t = Table(name, columns, storage_type=storage_type)
        if storage_type == "in-memory":
            t.persist()
            for row in rows:
                t.insert(row)
        return t
