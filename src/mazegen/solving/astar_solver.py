import heapq
from mazegen.models.maze import Maze
from mazegen.models.solution import Solution
from mazegen.models.direction import Direction
from mazegen.solving.solver_base import SolverBase


class AStarSolver(SolverBase):
    def solve(self) -> Solution | None:
        maze = self.maze
        start_col, start_row = self.entry
        end_col, end_row = self.exit_

        start = maze.grid[start_row][start_col]
        end   = maze.grid[end_row][end_col]

        def h(cell) -> int:
            """Manhattan mesafesi heuristiği."""
            return abs(cell.col - end_col) + abs(cell.row - end_row)

        # g_score: başlangıçtan hücreye gerçek maliyet
        g_score: dict = {start: 0}
        came_from: dict = {start: None}

        counter = 0
        # heap: (f, seri_no, hücre)
        heap = [(h(start), counter, start)]

        while heap:
            f, _, current = heapq.heappop(heap)

            if current is end:
                return self._reconstruct(came_from, start, end)

            g = g_score.get(current, float('inf'))

            # Eski, daha pahalı bir kayıt mı?
            if f > g + h(current):
                continue

            for direction, neighbor in maze.get_accessible_neighbors(current):
                g_new = g + 1
                if g_new < g_score.get(neighbor, float('inf')):
                    g_score[neighbor] = g_new
                    came_from[neighbor] = (current, direction)
                    f_new = g_new + h(neighbor)
                    counter += 1
                    heapq.heappush(heap, (f_new, counter, neighbor))

        return None

    def _reconstruct(self, came_from: dict, start, end) -> Solution:
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
