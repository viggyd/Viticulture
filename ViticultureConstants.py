from enum import Enum
from enum import IntEnum

# Maximum grade of grape/wine
MAX_GRADE = 9

# Different wine types
class WineType(IntEnum):
    RED = 0
    WHITE = 1
    BLUSH = 2
    SPARKLING = 3

# Different cellar types
class CellarType(IntEnum):
    SMALL = 0
    MEDIUM = 1
    LARGE = 2

# Different cellar types
class FieldType(IntEnum):
    SMALL = 0
    MEDIUM = 1
    LARGE = 2


class GrapeType(IntEnum):
    RED = 0
    WHITE = 1


