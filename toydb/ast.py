from dataclasses import dataclass
from typing import List

from toydb.statement import Statement


@dataclass
class Program:
    statements: List[Statement]
