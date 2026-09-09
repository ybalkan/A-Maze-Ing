import heapq
from mazegen.models.maze import Maze
from mazegen.models.solution import Solution
from mazegen.models.direction import Direction
from mazegen.solving.solver_base import SolverBase


class DijkstraSolver(SolverBase):
    def solve(self) -> Solution | None:
        maze = self.maze
        start_col, start_row = self.entry
        end_col, end_row = self.exit_

        start = maze.grid[start_row][start_col]
        end   = maze.grid[end_row][end_col]

        # dist: hücre → en düşük maliyet
        dist: dict = {start: 0}
        # came_from: hücre → (önceki_hücre, gelinen_yön)
        came_from: dict = {start: None}

        # heap elemanı: (maliyet, seri_no, hücre)  – eşit maliyette karşılaştırma hatası önlenir
        counter = 0
        heap = [(0, counter, start)]

        while heap:
            cost, _, current = heapq.heappop(heap)

            if current is end:
                return self._reconstruct(came_from, start, end)

            # Eski, daha pahalı bir kayıt mı?
            if cost > dist.get(current, float('inf')):
                continue

            for direction, neighbor in maze.get_accessible_neighbors(current):
                new_cost = cost + 1
                if new_cost < dist.get(neighbor, float('inf')):
                    dist[neighbor] = new_cost
                    came_from[neighbor] = (current, direction)
                    counter += 1
                    heapq.heappush(heap, (new_cost, counter, neighbor))

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
