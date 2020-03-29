from abc import ABC


class Command(ABC):
    pass


class Insert(Command):
    s = "i"

    def __init__(self, key: str, value: str) -> None:
        self.key = key
        self.value = value


class Select(Command):
    s = "s"

    def __init__(self, key: str) -> None:
        self.key = key


class Delete(Command):
    s = "d"

    def __init__(self, key: str) -> None:
        self.key = key


class Exit(Command):
    def __init__(self) -> None:
        pass
