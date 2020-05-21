import operator
from typing import Callable, Dict, Iterator, List, Optional, Sequence, Tuple, Type, Union

from toydb.statement import Conjunction, WhereStatement
from toydb.storage import Storage
from toydb.where import Predicate

d: Dict[Type, str] = {str: "text", int: "int"}
d_inv: Dict[str, Type] = {"text": str, "int": int}


def reduce_booleans_using_conjunctions(
    conditions: List[bool], conjunctions: List[Callable[[bool, bool], bool]]
) -> bool:
    assert len(conditions) == len(conjunctions) + 1
    if len(conditions) == 1:
        return conditions[0]
    condition_1 = conditions.pop(0)
    condition_2 = conditions.pop(0)
    conjunction = conjunctions.pop(0)
    new_value = conjunction(condition_1, condition_2)
    new_conditions = [new_value] + conditions
    return reduce_booleans_using_conjunctions(conditions=new_conditions, conjunctions=conjunctions)


class Table:
    """
    Table file schema:
    - Number of columns as NUMBER_OF_COLUMNS_INT_LENGTH sized int
    - Sequence of column names and types. These strings are terminated by a null byte
    - Sequence of rows
    """

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
            raise ValueError

    @property
    def columns(self) -> str:
        return "(" + ", ".join(f"{name} {d[type_]}" for name, type_ in self._columns.items()) + ")"

    def all_rows(self) -> Iterator[List[Union[int, str]]]:
        return self._file.read_rows()

    def column_name_to_index(self, c: str) -> Optional[int]:
        try:
            i = list(self._columns.keys()).index(c)
            return i
        except ValueError:
            return None

    def column_indices_from_names(self, columns: List[str]) -> Optional[List[int]]:
        column_indices_to_select = []
        if columns == ["all"]:
            for i, _ in enumerate(self._columns.keys()):
                column_indices_to_select.append(i)
        else:
            for c in columns:
                j = self.column_name_to_index(c)
                if j is None:
                    return None
                column_indices_to_select.append(j)
        return column_indices_to_select

    def select(
        self, columns: List[int], where: Optional[WhereStatement] = None, limit: int = -1
    ) -> Iterator[List[Union[str, int]]]:
        predicate_map = {
            Predicate.EQUALS: lambda a, b: a == b,
            Predicate.NOT_EQUALS: lambda a, b: a != b,
            Predicate.LT: lambda a, b: a < b,
            Predicate.GT: lambda a, b: a > b,
            Predicate.LTEQ: lambda a, b: a <= b,
            Predicate.GTEQ: lambda a, b: a >= b,
        }
        conjunction_map = {
            Conjunction.AND: operator.and_,
            Conjunction.OR: operator.or_,
        }
        count = 0
        for row in self.all_rows():
            if count == limit:
                return
            should_yield = True
            if where is not None:
                row_matches = [] * len(where.conditions)
                for w in where.conditions:
                    i = self.column_name_to_index(w.column)
                    assert i is not None
                    where_value_typed = list(self._columns.values())[i](w.value)
                    row_matches.append(predicate_map[w.predicate](row[i], where_value_typed))
                conjunctions = [conjunction_map[c] for c in where.conjunctions]
                should_yield = reduce_booleans_using_conjunctions(conditions=row_matches, conjunctions=conjunctions)
            if should_yield:
                to_return = [row[i] for i in columns]
                count += 1
                yield to_return

    def _strings_to_row(self, row: Sequence[str]) -> List[Union[int, str]]:
        data = [type_(value) for value, type_ in zip(row, self._columns.values())]
        return data

    def insert(self, row: Sequence[Union[int, str]]) -> None:
        self._file.insert(row)

    @classmethod
    def from_file(cls, name: str) -> "Table":
        s = Storage.from_file(name)
        columns = s._columns_as_they_came
        return Table(name, columns)
