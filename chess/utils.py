from dataclasses import dataclass
from enum import Enum
from typing import List, Union

EMPTY_SQUARE = "**"
Board = List[List[Union[str, object]]]  # Board is composed of pieces/empty squares (strings)


@dataclass
class Square:
    row: int
    col: int


class Color(Enum):
    WHITE = "w"
    BLACK = "b"
