from dataclasses import dataclass
from typing import List, Sequence, Tuple, Type


@dataclass
class Command:
    pass


@dataclass
class Insert(Command):
    values: List[str]


@dataclass
class Select(Command):
    pass


@dataclass
class Exit(Command):
    pass


@dataclass
class CreateTable(Command):
    table_name: str
    columns: Sequence[Tuple[str, Type]]
