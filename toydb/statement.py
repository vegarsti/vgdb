from dataclasses import dataclass, field
from enum import Enum
from typing import List, Tuple, Type, Union

from toydb.where import Where


@dataclass
class Statement:
    pass


@dataclass
class Insert(Statement):
    values: List[Union[int, str]]
    table_name: str


class Conjunction(Enum):
    AND = "and"
    OR = "or"


@dataclass
class WhereStatement:
    conditions: List[Where] = field(default_factory=lambda: [])
    conjunctions: List[Conjunction] = field(default_factory=lambda: [])


@dataclass
class Select(Statement):
    columns: List[str]
    table_name: str
    where: WhereStatement
    limit: int = -1


@dataclass
class CreateTable(Statement):
    table_name: str
    columns: List[Tuple[str, Type]]
