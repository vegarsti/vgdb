from typing import Sequence, Union


class Row:
    def __init__(self, data: Sequence[Union[int, str]]) -> None:
        self.data = tuple(data)

    def __repr__(self) -> str:
        return " ".join(str(v) for v in self.data)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Row):
            return self.data == other.data
        else:
            return False

    def __getitem__(self, item: int) -> Union[int, str]:
        return self.data[item]
