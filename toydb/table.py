import json
from typing import Iterator, List, Optional, Sequence, Tuple


class Table:
    def __init__(self, name: str, spec: Sequence[str]) -> None:
        self._name = name
        self._spec = set(spec)
        self._columns = len(self._spec)
        self._records: List[Tuple[int, List[str]]] = []
        self._min_available_index = 0

    def get(self, i: int) -> Optional[List[str]]:
        for idx, (j, record) in enumerate(self._records):
            if i == j:
                return record
        return None

    def get_all(self) -> Iterator[List[str]]:
        for _, record in self._records:
            yield record

    def insert(self, record: Sequence[str]) -> bool:
        if len(record) == self._columns:
            self._records.append((self._min_available_index, list(record)))
            self._min_available_index += 1
            return True
        else:
            return False

    def delete(self, i: int) -> bool:
        for idx, (j, _) in enumerate(self._records):
            if i == j:
                self._records.pop(idx)
                return True
        return False

    def __str__(self) -> str:
        return json.dumps(self._records)
