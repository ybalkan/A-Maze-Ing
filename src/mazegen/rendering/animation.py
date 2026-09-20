from __future__ import annotations

import time
from typing import Iterator, Optional, Set, Tuple

from ..models.maze import Maze
from ..models.solution import Solution
from ..generation.generator_base import GeneratorBase
from .ascii_renderer import render, _clear, STYLE_LINE, STYLES_42
from .color_palette import ColorPalette


def animate_generation(
    generator: GeneratorBase,
    delay: float = 0.02,
    palette: Optional[ColorPalette] = None,
    entry: Optional[Tuple[int, int]] = None,
    exit_: Optional[Tuple[int, int]] = None,
) -> Maze:
    p = palette or ColorPalette()
    maze = generator.maze

    actual_entry = entry if entry is not None else (0, 0)
    actual_exit = exit_ if exit_ is not None else (maze.width - 1, maze.height - 1)

    total_cells = maze.width * maze.height
    step_count = 0

    for _ in generator.generate_steps():
        step_count += 1
        _clear()
        print(render(maze, actual_entry, actual_exit, p, STYLE_LINE, STYLES_42[0]))
        pct = int(100 * step_count / max(1, total_cells - 1))
        print(f"⏳ Generating... {pct}%")
        time.sleep(delay)

    maze.reset_visited_flags()
    _clear()
    print(render(maze, actual_entry, actual_exit, p, STYLE_LINE, STYLES_42[0]))
    print("✅ Maze ready!")
    return maze


class SolutionAnimator:

    def __init__(
        self,
        solution: Solution,
        speed: float = 0.05,
    ) -> None:
        self.solution = solution
        self.speed = max(0.0, speed)

    @property
    def total_steps(self) -> int:
        return len(self.solution.path_cells)

    def steps(self) -> Iterator[Set[Tuple[int, int]]]:
        visited: Set[Tuple[int, int]] = set()
        for cell_coord in self.solution.path_cells:
            visited.add(cell_coord)
            yield set(visited)

    def animate_terminal(
        self,
        maze: Maze,
        entry: Tuple[int, int],
        exit_: Tuple[int, int],
        palette: ColorPalette,
        style: object,
        style_42: str,
    ) -> None:
        from .ascii_renderer import render as ascii_render, _clear as clear_screen
        from .ascii_renderer import RendererStyle

        if not isinstance(style, RendererStyle):
            return

        visited: Set[Tuple[int, int]] = set()
        path = self.solution.path_cells

        for step_idx, cell_coord in enumerate(path, start=1):
            visited.add(cell_coord)

            temp_solution = Solution(list(visited), [])

            clear_screen()
            print(ascii_render(
                maze, entry, exit_, palette, style, style_42,
                solution=temp_solution,
                show_solution=True,
            ))
            print(f"🧭 Step {step_idx}/{len(path)}  "
                  f"[{cell_coord[0]},{cell_coord[1]}]")

            if self.speed > 0.0:
                time.sleep(self.speed)

        if self.speed > 0.0:
            time.sleep(self.speed * 3)

    def get_step_cells(self, step: int) -> Set[Tuple[int, int]]:
        path = self.solution.path_cells
        if step <= 0:
            return set()
        limit = min(step, len(path))
        return set(path[:limit])
