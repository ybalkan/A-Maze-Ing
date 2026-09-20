import random
from typing import Optional, Tuple, Generator
from mazegen.models.maze import Maze
from mazegen.models.direction import Direction
from mazegen.models.cell import Cell
from mazegen.generation.generator_base import GeneratorBase


class RecursiveBacktracker(GeneratorBase):

    def generate_steps(self) -> Generator[None, None, None]:
        self.maze.apply_42_pattern()

        rng = random.Random(self.seed)

        start = self.maze.grid[0][0]
        start.visited = True
        stack = [start]

        while stack:
            current = stack[-1]

            unvisited = self._unvisited_neighbors(self.maze, current, rng)

            if unvisited:
                direction, neighbor = unvisited

                self.maze.remove_wall_between(current, neighbor, direction)

                neighbor.visited = True
                stack.append(neighbor)
                yield None
            else:
                stack.pop()

    def _unvisited_neighbors(
        self,
        maze: Maze,
        cell: Cell,
        rng: random.Random,
    ) -> Optional[Tuple[Direction, Cell]]:
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
