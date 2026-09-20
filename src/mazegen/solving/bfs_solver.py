from collections import deque
from typing import Deque, Dict, Optional, Tuple
from mazegen.models.solution import Solution
from mazegen.models.cell import Cell
from mazegen.models.direction import Direction
from mazegen.solving.solver_base import SolverBase


class BFSSolver(SolverBase):

    def solve(self) -> Solution | None:
        maze = self.maze
        start_col, start_row = self.entry
        end_col, end_row = self.exit_

        start = maze.grid[start_row][start_col]
        end = maze.grid[end_row][end_col]

        came_from: Dict[Cell, Optional[Tuple[Cell, Direction]]] = {start: None}

        queue: Deque[Cell] = deque([start])

        while queue:
            current = queue.popleft()

            if current is end:
                return self._reconstruct_path(came_from, end_col, end_row)

            for direction, neighbor in maze.get_accessible_neighbors(current):
                if neighbor not in came_from:
                    came_from[neighbor] = (current, direction)
                    queue.append(neighbor)

        return None

    def _reconstruct_path(
        self,
        came_from: dict['Cell', tuple['Cell', Direction] | None],
        end_col: int,
        end_row: int
    ) -> Solution:
        path_cells: list[tuple[int, int]] = []
        directions: list[Direction] = []

        node = self.maze.grid[end_row][end_col]

        while came_from[node] is not None:
            val = came_from[node]
            if val is None:
                break
            prev, direction = val
            path_cells.append((node.col, node.row))
            directions.append(direction)
            node = prev

        start_col, start_row = self.entry
        path_cells.append((start_col, start_row))

        path_cells.reverse()
        directions.reverse()

        return Solution(path_cells, directions)
