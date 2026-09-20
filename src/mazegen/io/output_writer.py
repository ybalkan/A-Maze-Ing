from __future__ import annotations

from typing import Optional, Tuple

from ..models.maze import Maze
from ..models.solution import Solution


def write_output(
    maze: Maze,
    entry: Tuple[int, int],
    exit_: Tuple[int, int],
    output_path: str,
    solution: Optional[Solution] = None,
) -> None:
    with open(output_path, "w", encoding="utf-8") as f:
        for row in range(maze.height):
            line = ""
            for col in range(maze.width):
                cell = maze.grid[row][col]
                line += format(cell.walls, "x")
            f.write(line + "\n")

        f.write("\n")

        f.write(f"{entry[0]},{entry[1]}\n")
        f.write(f"{exit_[0]},{exit_[1]}\n")

        if solution is not None:
            f.write(solution.to_string() + "\n")
