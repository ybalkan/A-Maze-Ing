from abc import ABC, abstractmethod
from mazegen.models.maze import Maze


class GeneratorBase(ABC):
    def __init__(self, width: int, height: int, seed: int | None = None) -> None:
        self.width = width
        self.height = height
        self.seed = seed

    @abstractmethod
    def generate(self) -> Maze:
        ...