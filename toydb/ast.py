from dataclasses import dataclass
from typing import List, Union

from toydb.statement import CreateTable, Insert, Select


@dataclass
class Program:
    statements: List[Union[Select, Insert, CreateTable]]
