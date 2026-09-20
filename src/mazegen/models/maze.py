from dataclasses import dataclass, field
from typing import List, Tuple
from .cell import Cell
from .direction import Direction


@dataclass
class Maze:
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
            return self.grid[row][col]

    def in_bounds(self, col: int, row: int) -> bool:
        return 0 <= row < self.height and 0 <= col < self.width

    def get_adjacent_cell(self, cell: Cell) -> List[Tuple[Direction, Cell]]:
        neighbors = []

        for direction in Direction:
            n_col = cell.col + direction.dx
            n_row = cell.row + direction.dy
            if self.in_bounds(n_col, n_row):
                neighbors.append((direction, self.grid[n_row][n_col]))
        return neighbors

    def get_accessible_neighbors(self, cell: Cell) -> List[Tuple[Direction, Cell]]:
        accessible = []

        for direction in Direction:
            if not cell.has_wall(direction):
                n_col = cell.col + direction.dx
                n_row = cell.row + direction.dy
                if self.in_bounds(n_col, n_row):
                    accessible.append((direction, self.grid[n_row][n_col]))
        return accessible

    def remove_wall_between(self, cell: Cell, neighbor: Cell, direction: Direction) -> None:
        cell.remove_wall(direction)
        neighbor.remove_wall(direction.opposite)

    def reset_visited_flags(self) -> None:
        for row in self.grid:
            for cell in row:
                cell.visited = False

    def apply_42_pattern(self) -> None:
        pattern = [
            "X...X XXXX",
            "X...X ...X",
            "XXXXX XXXX",
            "....X X...",
            "....X XXXX",
        ]

        p_width = len(pattern[0])
        p_height = len(pattern)

        if self.width < p_width + 2 or self.height < p_height + 2:
            print("Uyarı: Labirent boyutu '42' desenini çizmek için çok küçük.")
            return

        start_col = (self.width - p_width) // 2
        start_row = (self.height - p_height) // 2

        for r, row_str in enumerate(pattern):
            for c, char in enumerate(row_str):
                if char == 'X':
                    cell = self.grid[start_row + r][start_col + c]
                    cell.visited = True
                    cell.is_42 = True
