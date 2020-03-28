from abc import ABC


class Command(ABC):
    pass


class Insert(Command):
    s = "i"

    def __init__(self, v: int) -> None:
        self.value = v


class Select(Command):
    s = "s"

    def __init__(self, v: int) -> None:
        self.value = v


class Delete(Command):
    s = "d"

    def __init__(self, v: int) -> None:
        self.value = v


class Exit(Command):
    def __init__(self) -> None:
        pass
