from typing import Sequence, Union


class Record:
    def __init__(self, data: Sequence[Union[int, str]]) -> None:
        self.data = tuple(data)

    def __repr__(self) -> str:
        return " ".join(str(v) for v in self.data)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Record):
            return self.data == other.data
        else:
            return False
