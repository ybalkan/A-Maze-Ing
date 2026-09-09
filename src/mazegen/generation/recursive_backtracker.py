# ADIM 11 (Temel) - Ana labirent üretme algoritması (DFS tabanlı)
import random
from mazegen.models.maze import Maze
from mazegen.models.direction import Direction
from mazegen.generation.generator_base import GeneratorBase


class RecursiveBacktracker(GeneratorBase):

    def generate(self) -> Maze:
        maze = Maze(self.width, self.height)
        rng = random.Random(self.seed)

        # Başlangıç hücresi: (col=0, row=0)
        start = maze.grid[0][0]
        start.visited = True
        stack = [start]

        while stack:
            current = stack[-1]
            unvisited = self._unvisited_neighbors(maze, current, rng)

            if unvisited:
                direction, neighbor = unvisited
                maze.remove_wall_between(current, neighbor, direction)
                neighbor.visited = True
                stack.append(neighbor)
            else:
                stack.pop()

        maze.reset_visited_flags()
        return maze

    def _unvisited_neighbors(
        self,
        maze: Maze,
        cell: 'Cell',  # type: ignore[name-defined]
        rng: random.Random,
    ) -> tuple | None:
        candidates = []

        for direction in Direction:
            n_col = cell.col + direction.dx
            n_row = cell.row + direction.dy
            if maze.in_bounds(n_col, n_row):
                neighbor = maze.grid[n_row][n_col]
                if not neighbor.visited:
                    candidates.append((direction, neighbor))

        if not candidates:
            return None

        return rng.choice(candidates)
