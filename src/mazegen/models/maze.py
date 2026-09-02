from dataclasses import dataclass, field
from typing import List, Tuple
from .cell import Cell
from .direction import Direction


@dataclass
class Maze:
    width: int
    height: int

    grid: List[List[Cell]] = field(init=False)

    def __post_init__(self) -> None:
        self.grid = [
            [Cell(row, col) for col in range(self.width)]
            for row in range(self.height)
        ]