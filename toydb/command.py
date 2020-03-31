from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Sequence


@dataclass  # type: ignore
class Command(ABC):
    @abstractmethod
    def string(self) -> str:
        pass


@dataclass
class Insert(Command):
    values: List[str]

    @property
    def string(self) -> str:
        return "i"


@dataclass
class Select(Command):
    key: int

    @property
    def string(self) -> str:
        return "s"


@dataclass
class SelectAll(Command):
    @property
    def string(self) -> str:
        return "s"


@dataclass
class Delete(Command):
    key: int

    @property
    def string(self) -> str:
        return "d"


@dataclass
class Exit(Command):
    @property
    def string(self) -> str:
        return "_"


@dataclass
class Create(Command):
    table_name: str
    columns: Sequence[str]

    @property
    def string(self) -> str:
        return "i"
