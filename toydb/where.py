from dataclasses import dataclass
from enum import Enum
from typing import Union


class Predicate(Enum):
    EQUAL = "="


@dataclass
class Where:
    column: str
    predicate: Predicate
    value: Union[str, int]
