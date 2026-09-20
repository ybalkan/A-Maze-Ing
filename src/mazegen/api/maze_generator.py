from __future__ import annotations

from typing import Dict, Optional, Tuple, Type

from ..models.maze import Maze
from ..models.solution import Solution
from ..generation.generator_base import GeneratorBase
from ..generation.recursive_backtracker import RecursiveBacktracker
from ..generation.prim import PrimGenerator
from ..generation.braided import BraidedGenerator
from ..solving.bfs_solver import BFSSolver
from ..io.output_writer import write_output

_GENERATORS: Dict[str, Type[GeneratorBase]] = {
    "recursive_backtracker": RecursiveBacktracker,
    "backtracker":           RecursiveBacktracker,
    "prim":                  PrimGenerator,
    "braided":               BraidedGenerator,
}

_SOLVERS = {
    "bfs": BFSSolver,
}


class MazeGenerator:

    def __init__(
        self,
        width: int,
        height: int,
        seed: Optional[int] = None,
        perfect: bool = False,
        algorithm: str = "recursive_backtracker",
        entry: Tuple[int, int] = (0, 0),
        exit_: Optional[Tuple[int, int]] = None,
        solver: str = "bfs",
    ) -> None:
        self.width = width
        self.height = height
        self.seed = seed

        self.perfect = perfect

        self.algorithm = algorithm

        self.entry: Tuple[int, int] = entry

        self.exit_: Tuple[int, int] = exit_ if exit_ is not None else (width - 1, height - 1)
        self.solver_name = solver

        self._maze: Optional[Maze] = None
        self._solution: Optional[Solution] = None
        self.generator: Optional[GeneratorBase] = None

    def prepare_generator(self) -> GeneratorBase:

        if self.perfect and self.algorithm == "braided":
            self.algorithm = "recursive_backtracker"
            print("Warning: When PERFECT=true, the 'braided' algorithm "
                  "cannot be used. Using 'recursive_backtracker' instead.")

        algo_cls = _GENERATORS.get(self.algorithm)
        if algo_cls is None:
            raise ValueError(
                f"Unknown algorithm: '{self.algorithm}'. "
                f"Choices: {list(_GENERATORS)}"
            )

        if not self.perfect:

            base = self.algorithm if self.algorithm != "braided" else "recursive_backtracker"
            self.generator = BraidedGenerator(
                self.width, self.height, seed=self.seed, base_algorithm=base
            )
        else:

            self.generator = algo_cls(self.width, self.height, seed=self.seed)

        return self.generator

    def generate(self) -> "MazeGenerator":

        gen = self.prepare_generator()
        self._maze = gen.generate()

        self._solution = None
        return self

    def solve(self, solver: Optional[str] = None) -> Optional[Solution]:
        if self._maze is None:
            raise RuntimeError("Error: generate() must be called first.")

        solver_name = solver or self.solver_name
        solver_cls = _SOLVERS.get(solver_name)
        if solver_cls is None:
            raise ValueError(
                f"Unknown solver: '{solver_name}'. "
                f"Choices: {list(_SOLVERS)}"
            )

        s = solver_cls(self._maze, self.entry, self.exit_)
        self._solution = s.solve()
        return self._solution

    def get_maze(self) -> Maze:
        if self._maze is None:
            raise RuntimeError("Error: generate() must be called first.")
        return self._maze

    def get_solution(self) -> Optional[Solution]:
        return self._solution

    def export(self, output_path: str) -> None:
        if self._maze is None:
            raise RuntimeError("Error: generate() must be called first.")
        write_output(
            maze=self._maze,
            entry=self.entry,
            exit_=self.exit_,
            output_path=output_path,
            solution=self._solution,
        )
