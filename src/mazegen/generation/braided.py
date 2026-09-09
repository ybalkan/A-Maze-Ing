import random
from mazegen.models.maze import Maze
from mazegen.models.direction import Direction
from mazegen.generation.generator_base import GeneratorBase


class BraidedGenerator(GeneratorBase):

    def __init__(
        self,
        width: int,
        height: int,
        seed: int | None = None,
        braid_ratio: float = 1.0,
    ) -> None:
        super().__init__(width, height, seed)
        if not 0.0 <= braid_ratio <= 1.0:
            raise ValueError("braid_ratio should be between 0.0 and 1.0")
        self.braid_ratio = braid_ratio

    def generate(self) -> Maze:
        maze = self._generate_perfect(Maze(self.width, self.height))

        rng = random.Random(self.seed)
        dead_ends = self._find_dead_ends(maze)
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
                if maze.in_bounds(n_col, n_row):
                    neighbor = maze.grid[n_row][n_col]
                    maze.remove_wall_between(cell, neighbor, direction)
                    break

        return maze


    def _generate_perfect(self, maze: Maze) -> Maze:
        rng = random.Random(self.seed)

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
            else:
                stack.pop()

        maze.reset_visited_flags()
        return maze

    def _find_dead_ends(self, maze: Maze) -> list:
        dead_ends = []
        for row in maze.grid:
            for cell in row:
                wall_count = sum(1 for d in Direction if cell.has_wall(d))
                if wall_count == 3:
                    dead_ends.append(cell)
        return dead_ends