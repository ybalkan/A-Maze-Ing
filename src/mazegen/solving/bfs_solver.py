from collections import deque
from mazegen.models.maze import Maze
from mazegen.models.solution import Solution
from mazegen.models.direction import Direction
from mazegen.solving.solver_base import SolverBase


class BFSSolver(SolverBase):
    def solve(self) -> Solution | None:
        maze = self.maze
        start_col, start_row = self.entry
        end_col, end_row = self.exit_

        start = maze.grid[start_row][start_col]
        end   = maze.grid[end_row][end_col]

        # came_from: hücre → (önceki_hücre, gelinen_yön)
        came_from: dict = {start: None}
        queue: deque = deque([start])

        while queue:
            current = queue.popleft()

            if current is end:
                return self._reconstruct(came_from, start, end)

            for direction, neighbor in maze.get_accessible_neighbors(current):
                if neighbor not in came_from:
                    came_from[neighbor] = (current, direction)
                    queue.append(neighbor)

        return None  # çözüm bulunamadı

    def _reconstruct(self, came_from: dict, start, end) -> Solution:
        """came_from tablosundan yolu ve yönleri geri izler."""
        path_cells: list[tuple[int, int]] = []
        directions: list[Direction] = []
        node = end

        while came_from[node] is not None:
            prev, direction = came_from[node]
            path_cells.append((node.col, node.row))
            directions.append(direction)
            node = prev

        path_cells.append((start.col, start.row))

        path_cells.reverse()
        directions.reverse()

        return Solution(path_cells, directions)
