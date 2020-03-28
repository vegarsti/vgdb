from dataclasses import dataclass


@dataclass
class Record:
    value: int

    def __str__(self) -> str:
        return str(self.value)
