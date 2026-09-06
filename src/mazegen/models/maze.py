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
            [Cell(col, row) for col in range(self.width)]
            for row in range(self.height)
        ]
    def get_cell(self, col: int, row: int) -> Cell:
        if not self.in_bounds(col, row):
            raise ValueError(f"Invalid coordinate: ({col},{row})")
        else:
            return self.grid[col][row]

    def in_bounds(self, col: int, row: int):
        return 0 < row < self.height and 0 <= col < self.width

    def get_adjacent_cell(self, cell: Cell) -> List[Tuple[Direction, Cell]]:
        neighbors = []

        for direction in Direction:
            if not cell.has_wall(direction):
                n_col = cell.col + direction.dx
                n_row = cell.row + direction.dy
                if self.in_bounds(n_col, n_row):
                    neighbors.append((direction, self.grid[n_col][n_row]))
        return neighbors

    def get_accessable_neighbors(self, cell: Cell) -> List[Tuple[Direction, Cell]]:
        accessable = []

        for direction in Direction:
            if not cell.has_wall(direction):
                n_col = cell.col + direction.dx
                n_row = cell.row + direction.dy
                if self.in_bounds(n_col, n_row):
                    accessable.append((direction, self.grid[n_col][n_row]))
        return accessable

    def remove_wall_between(self, cell: Cell, neighbor: Cell, direction: Direction) -> None:
        cell.remove_wall(direction)
        neighbor.remove_wall(direction.opposite)

    def reset_visited_flags(self) -> None:
        for row in self.grid:
            for cell in row:
                cell.visited = False
