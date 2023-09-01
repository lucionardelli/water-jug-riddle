import enum


class Jug(enum.Enum):
    """
    Enum representing the jugs in the riddle (Jug 1 and Jug 2).
    """

    JUG_1 = enum.auto()
    JUG_2 = enum.auto()


class JugAction(enum.Enum):
    """
    Enum representing the actions that can be taken with the jugs.
    """

    FILL = enum.auto()
    EMPTY = enum.auto()
    TRANSFER = enum.auto()
