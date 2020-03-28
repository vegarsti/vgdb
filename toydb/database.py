from typing import List


class Database:
    def __init__(self) -> None:
        self.records: List[int] = []

    def insert(self, i: int) -> None:
        self.records.append(i)

    def delete(self, i: int) -> None:
        j = self.records.index(i)
        self.records.pop(j)

    def exists(self, i: int) -> bool:
        return i in self.records

    def __str__(self) -> str:
        return "[" + ", ".join(record.__str__() for record in self.records) + "]"
