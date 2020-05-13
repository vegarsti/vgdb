from dataclasses import dataclass
from enum import Enum
from typing import Union


class Predicate(Enum):
    EQUALS = "="
    NOT_EQUALS = "!="
    LT = "<"
    GT = ">"
    LTEQ = "<="
    GTEQ = ">="


@dataclass
class Where:
    column: str
    predicate: Predicate
    value: Union[str, int]
