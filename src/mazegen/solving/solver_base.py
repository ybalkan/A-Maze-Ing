from abc import ABC, abstractmethod
from mazegen.models.maze import Maze
from mazegen.models.solution import Solution


class SolverBase(ABC):

    def __init__(
        self,
        maze: Maze,
        entry: tuple[int, int],
        exit_: tuple[int, int],
    ) -> None:
        self.maze = maze
        self.entry = entry
        self.exit_ = exit_

    @abstractmethod
    def solve(self) -> Solution | None:
        ...
