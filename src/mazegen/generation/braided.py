import random
from typing import List, Generator
from mazegen.models.maze import Maze
from mazegen.models.cell import Cell
from mazegen.models.direction import Direction
from mazegen.generation.generator_base import GeneratorBase


class BraidedGenerator(GeneratorBase):

    def __init__(
        self,
        width: int,
        height: int,
        seed: int | None = None,
        braid_ratio: float = 1.0,
        base_algorithm: str = "recursive_backtracker",
    ) -> None:
        super().__init__(width, height, seed)
        if not 0.0 <= braid_ratio <= 1.0:
            raise ValueError("braid_ratio 0.0 ile 1.0 arasında olmalıdır.")
        self.braid_ratio = braid_ratio
        self.base_algorithm = base_algorithm

    def generate_steps(self) -> Generator[None, None, None]:
        yield from self._generate_perfect_steps(self.maze)

        rng = random.Random(self.seed)
        dead_ends = self._find_dead_ends(self.maze)
        rng.shuffle(dead_ends)

        to_open = int(len(dead_ends) * self.braid_ratio)
        for cell in dead_ends[:to_open]:
            closed_walls = [d for d in Direction if cell.has_wall(d)]
            if len(closed_walls) < 3:
                continue

            rng.shuffle(closed_walls)
            for direction in closed_walls:
                n_col = cell.col + direction.dx
                n_row = cell.row + direction.dy
                if self.maze.in_bounds(n_col, n_row):
                    neighbor = self.maze.grid[n_row][n_col]
                    if not neighbor.is_42:
                        self.maze.remove_wall_between(cell, neighbor, direction)
                        yield None
                        break

    def _generate_perfect_steps(self, maze: Maze) -> Generator[None, None, None]:
        maze.apply_42_pattern()
        rng = random.Random(self.seed)

        if self.base_algorithm == "prim":
            yield from self._prim_steps(maze, rng)
        else:
            yield from self._backtracker_steps(maze, rng)

    def _backtracker_steps(
        self, maze: Maze, rng: random.Random
    ) -> Generator[None, None, None]:
        start = maze.grid[0][0]
        start.visited = True
        stack = [start]

        while stack:
            current = stack[-1]
            candidates = []

            for direction in Direction:
                n_col = current.col + direction.dx
                n_row = current.row + direction.dy
                if maze.in_bounds(n_col, n_row):
                    neighbor = maze.grid[n_row][n_col]
                    if not neighbor.visited:
                        candidates.append((direction, neighbor))

            if candidates:
                direction, neighbor = rng.choice(candidates)
                maze.remove_wall_between(current, neighbor, direction)
                neighbor.visited = True
                stack.append(neighbor)
                yield None
            else:
                stack.pop()

    def _prim_steps(
        self, maze: Maze, rng: random.Random
    ) -> Generator[None, None, None]:
        start = maze.grid[0][0]
        start.visited = True

        frontier: list[tuple[Direction, Cell, Cell]] = []
        self._add_frontier(maze, start, frontier)

        while frontier:
            idx = rng.randrange(len(frontier))
            direction, from_cell, to_cell = frontier[idx]
            frontier[idx] = frontier[-1]
            frontier.pop()

            if to_cell.visited:
                continue

            maze.remove_wall_between(from_cell, to_cell, direction)
            to_cell.visited = True
            self._add_frontier(maze, to_cell, frontier)
            yield None

    def _add_frontier(
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

    def _find_dead_ends(self, maze: Maze) -> List[Cell]:
        dead_ends: List[Cell] = []
        for row in maze.grid:
            for cell in row:
                wall_count = sum(1 for d in Direction if cell.has_wall(d))
                if wall_count == 3:
                    dead_ends.append(cell)
        return dead_ends
