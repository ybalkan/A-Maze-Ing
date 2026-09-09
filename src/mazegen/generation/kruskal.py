# ADIM 13 (Bonus) - Kruskal algoritması
import random
from mazegen.models.maze import Maze
from mazegen.models.direction import Direction
from mazegen.generation.generator_base import GeneratorBase


class KruskalGenerator(GeneratorBase):

    def generate(self) -> Maze:
        maze = Maze(self.width, self.height)
        rng = random.Random(self.seed)

        parent: dict[tuple[int, int], tuple[int, int]] = {}
        rank: dict[tuple[int, int], int] = {}

        for row in range(self.height):
            for col in range(self.width):
                key = (col, row)
                parent[key] = key
                rank[key] = 0

        def find(k: tuple[int, int]) -> tuple[int, int]:
            while parent[k] != k:
                parent[k] = parent[parent[k]]
                k = parent[k]
            return k

        def union(a: tuple[int, int], b: tuple[int, int]) -> bool:
            ra, rb = find(a), find(b)
            if ra == rb:
                return False
            if rank[ra] < rank[rb]:
                ra, rb = rb, ra
            parent[rb] = ra
            if rank[ra] == rank[rb]:
                rank[ra] += 1
            return True


        walls: list[tuple[int, int, Direction]] = []
        for row in range(self.height):
            for col in range(self.width):
                if col + 1 < self.width:
                    walls.append((col, row, Direction.EAST))
                if row + 1 < self.height:
                    walls.append((col, row, Direction.SOUTH))

        rng.shuffle(walls)

        for col, row, direction in walls:
            n_col = col + direction.dx
            n_row = row + direction.dy
            if union((col, row), (n_col, n_row)):
                cell = maze.grid[row][col]
                neighbor = maze.grid[n_row][n_col]
                maze.remove_wall_between(cell, neighbor, direction)

        return maze