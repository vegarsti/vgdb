from dataclasses import dataclass, field
from typing import List, Tuple, Type, Union

from toydb.where import Where


@dataclass
class Statement:
    pass


@dataclass
class Insert(Statement):
    values: List[Union[int, str]]
    table_name: str


@dataclass
class Select(Statement):
    columns: List[str]
    table_name: str
    where: List[Where] = field(default_factory=lambda: [])
    limit: int = -1


@dataclass
class CreateTable(Statement):
    table_name: str
    columns: List[Tuple[str, Type]]
