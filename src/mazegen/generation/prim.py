import random
from typing import Generator
from mazegen.models.maze import Maze
from mazegen.models.cell import Cell
from mazegen.models.direction import Direction
from mazegen.generation.generator_base import GeneratorBase


class PrimGenerator(GeneratorBase):

    def generate_steps(self) -> Generator[None, None, None]:
        self.maze.apply_42_pattern()
        rng = random.Random(self.seed)

        start = self.maze.grid[0][0]
        start.visited = True

        frontier: list[tuple[Direction, Cell, Cell]] = []
        self._add_frontier_walls(self.maze, start, frontier)

        while frontier:
            idx = rng.randrange(len(frontier))
            direction, from_cell, to_cell = frontier[idx]
            frontier[idx] = frontier[-1]
            frontier.pop()

            if to_cell.visited:
                continue

            self.maze.remove_wall_between(from_cell, to_cell, direction)
            to_cell.visited = True
            self._add_frontier_walls(self.maze, to_cell, frontier)
            yield None

    def _add_frontier_walls(
        self,
        maze: Maze,
        cell: Cell,
        frontier: list[tuple[Direction, Cell, Cell]],
    ) -> None:
        for direction in Direction:
            n_col = cell.col + direction.dx
            n_row = cell.row + direction.dy
            if maze.in_bounds(n_col, n_row):
                neighbor = maze.grid[n_row][n_col]
                if not neighbor.visited:
                    frontier.append((direction, cell, neighbor))
