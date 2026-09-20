from abc import ABC, abstractmethod
from typing import Generator
from mazegen.models.maze import Maze


class GeneratorBase(ABC):

    def __init__(self, width: int, height: int, seed: int | None = None) -> None:
        self.width = width
        self.height = height
        self.seed = seed
        self.maze = Maze(self.width, self.height)

    @abstractmethod
    def generate_steps(self) -> Generator[None, None, None]:
        ...

    def generate(self) -> Maze:
        for _ in self.generate_steps():
            pass
        self.maze.reset_visited_flags()
        return self.maze
