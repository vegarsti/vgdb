from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass  # type: ignore
class Command(ABC):
    @abstractmethod
    def string(self) -> str:
        pass


@dataclass
class Insert(Command):
    key: str
    value: str

    @property
    def string(self) -> str:
        return "i"


@dataclass
class Select(Command):
    key: str

    @property
    def string(self) -> str:
        return "s"


@dataclass
class Delete(Command):
    key: str

    @property
    def string(self) -> str:
        return "d"


@dataclass
class Exit(Command):
    @property
    def string(self) -> str:
        return "_"
