from __future__ import annotations

import sys
import dataclasses
from typing import Optional, Set, Tuple, Any

from ..models.maze import Maze
from ..models.solution import Solution
from ..models.direction import Direction
from .color_palette import ColorPalette, RESET


@dataclasses.dataclass
class RendererStyle:
    name: str
    wall_h: str
    wall_v: str
    corner: str
    t_top: str
    t_bot: str
    t_left: str
    t_right: str
    tl: str
    tr: str
    bl: str
    br: str
    space_h: str = "  "
    space_v: str = " "
    sym_entry: str = "S "
    sym_exit: str = "E "
    sym_solution: str = "· "
    sym_empty: str = "  "


STYLE_LINE = RendererStyle(
    name="Classic",
    wall_h="──", wall_v="│", corner="┼",
    t_top="┬", t_bot="┴", t_left="├", t_right="┤",
    tl="┌", tr="┐", bl="└", br="┘", space_h="  ", space_v=" ",
    sym_solution="· "
)

STYLE_DUNGEON = RendererStyle(
    name="Dungeon",
    wall_h="🧱", wall_v="🧱", corner="🧱",
    t_top="🧱", t_bot="🧱", t_left="🧱", t_right="🧱",
    tl="🧱", tr="🧱", bl="🧱", br="🧱", space_h="  ", space_v="  ",
    sym_entry="🐁", sym_exit="🧀", sym_solution="🐾"
)

STYLE_ALL_BLOCK = RendererStyle(
    name="Full Block",
    wall_h="██", wall_v="██", corner="██",
    t_top="██", t_bot="██", t_left="██", t_right="██",
    tl="██", tr="██", bl="██", br="██", space_h="  ", space_v="  ",
    sym_entry="██", sym_exit="██", sym_solution="██"
)

STYLES = [STYLE_LINE, STYLE_DUNGEON, STYLE_ALL_BLOCK]

STYLES_42 = [
    "[36m# [0m",
    "💀",
    "[36m██[0m",
]


def _clear() -> None:
    print("[2J[H", end="", flush=True)


def render(
    maze: Maze,
    entry: Tuple[int, int],
    exit_: Tuple[int, int],
    palette: ColorPalette,
    style: RendererStyle,
    style_42: str,
    solution: Optional[Solution] = None,
    show_solution: bool = False,
) -> str:
    w = maze.width
    h = maze.height

    sol_cells: Set[Tuple[int, int]] = set()
    if show_solution and solution is not None:
        for col, row in solution.path_cells:
            sol_cells.add((col, row))

    wc = palette.wall
    ec = palette.entry
    xc = palette.exit
    sc = palette.solution

    lines: list[str] = []

    for row in range(h):
        top = ""
        for col in range(w):
            cell = maze.grid[row][col]
            if row == 0 and col == 0:
                top += wc + style.tl + RESET
            elif row == 0:
                top += wc + style.t_top + RESET
            elif col == 0:
                top += wc + style.t_left + RESET
            else:
                top += wc + style.corner + RESET

            if cell.has_wall(Direction.NORTH):
                top += wc + style.wall_h + RESET
            else:
                top += style.space_h

        if row == 0:
            top += wc + style.tr + RESET
        else:
            top += wc + style.t_right + RESET
        lines.append(top)

        mid = ""
        for col in range(w):
            cell = maze.grid[row][col]

            if cell.has_wall(Direction.WEST):
                mid += wc + style.wall_v + RESET
            else:
                mid += style.space_v

            if (col, row) == entry:
                mid += ec + style.sym_entry + RESET
            elif (col, row) == exit_:
                mid += xc + style.sym_exit + RESET
            elif (col, row) in sol_cells:
                mid += sc + style.sym_solution + RESET
            elif cell.is_42:
                mid += style_42
            else:
                mid += style.sym_empty

        mid += wc + style.wall_v + RESET
        lines.append(mid)

    bot = wc + style.bl + RESET
    for col in range(w):
        bot += wc + style.wall_h + RESET
        if col < w - 1:
            bot += wc + style.t_bot + RESET
    bot += wc + style.br + RESET
    lines.append(bot)

    return "\n".join(lines)


def print_maze(
    maze: Maze,
    entry: Tuple[int, int],
    exit_: Tuple[int, int],
    palette: ColorPalette,
    style: RendererStyle,
    style_42: str,
    solution: Optional[Solution] = None,
    show_solution: bool = False,
) -> None:
    print(render(maze, entry, exit_, palette, style, style_42, solution, show_solution))


def _menu(
    palette: ColorPalette, style: RendererStyle,
    show_solution: bool, seed: Optional[int],
    perfect: bool = False
) -> None:
    seed_str = str(seed) if seed is not None else "random"
    path_str = "HIDE" if show_solution else "SHOW"
    mode_str = "PERFECT (Single Path, No Loops)" if perfect else "PAC-MAN (Multi-Path, Braided)"
    print()
    print("  ==========================================")
    print(f"   ACTIVE THEME: {style.name}")
    print("  ==========================================")
    print("   Status:")
    print(f"   - Mode  : {mode_str}")
    print(f"   - Color : {palette.wall}{palette.name}{RESET}")
    print(f"   - Path  : {path_str}")
    print(f"   - Seed  : {seed_str}")
    print()
    print("   Controls:")
    print("   [T] Change Full Theme (Recommended)")
    print("   [R] Generate New Maze")
    print("   [M] Toggle Mode (Perfect <-> Pac-Man)")
    print("   [P] Toggle Solution Path")
    print("   [A] Start Solution Animation")
    print("   [C] Change Wall Color")
    print("   [S] Change Wall Style (Custom)")
    print("   [N] Change 42 Pattern (Custom)")
    print("   [Q] Quit")
    print("  ==========================================")
    print("  > ", end="", flush=True)


class AsciiRenderer:

    def __init__(
        self,
        maze_generator: Any,
        entry: Tuple[int, int],
        exit_: Tuple[int, int],
        palette: Optional[ColorPalette] = None,
        animation_speed: Optional[float] = None,
    ) -> None:
        self._mg = maze_generator
        self.entry = entry
        self.exit_ = exit_
        self.palette = palette or ColorPalette()
        self._animation_speed: float = animation_speed if animation_speed is not None else 0.0
        self._style_idx = 0
        self._42_idx = 0
        self._show_solution = False

        try:
            mg = self._mg
            self._maze = mg.get_maze()
            self._solution = mg.get_solution()
        except (RuntimeError, AttributeError):
            self._maze = None
            self._solution = None

    def _draw(self) -> None:
        _clear()
        if self._maze is None:
            return
        print_maze(
            self._maze,
            self.entry,
            self.exit_,
            self.palette,
            STYLES[self._style_idx],
            STYLES_42[self._42_idx],
            self._solution,
            self._show_solution,
        )
        perfect = getattr(self._mg, "perfect", False)
        _menu(
            self.palette, STYLES[self._style_idx],
            self._show_solution, self._mg.seed,
            perfect=perfect
        )

    def _regenerate(self, randomize_seed: bool = True) -> None:
        if randomize_seed:
            import random
            self._mg.seed = random.randint(0, 999999)

        if self._animation_speed > 0:
            from .animation import animate_generation
            gen = self._mg.prepare_generator()
            generated_maze = animate_generation(
                generator=gen,
                delay=self._animation_speed,
                palette=self.palette,
                entry=self.entry,
                exit_=self.exit_,
            )
            self._mg._maze = generated_maze
        else:
            self._mg.generate()

        self._maze = self._mg.get_maze()
        self._solution = self._mg.solve()
        self._show_solution = False

    def _animate_solution(self) -> None:
        if self._solution is None or self._maze is None:
            return

        from .animation import SolutionAnimator
        animator = SolutionAnimator(
            solution=self._solution,
            speed=self._animation_speed if self._animation_speed > 0 else 0.05,
        )
        animator.animate_terminal(
            maze=self._maze,
            entry=self.entry,
            exit_=self.exit_,
            palette=self.palette,
            style=STYLES[self._style_idx],
            style_42=STYLES_42[self._42_idx],
        )
        self._show_solution = True

    def run(self) -> None:
        try:
            import tty
            import termios
            _has_tty = sys.stdin.isatty()
        except ImportError:
            _has_tty = False

        if self._animation_speed > 0:
            self._regenerate(randomize_seed=False)
            self._animate_solution()
        elif self._maze is None:
            self._regenerate(randomize_seed=False)

        while True:
            self._draw()

            if _has_tty:
                fd = sys.stdin.fileno()
                old = termios.tcgetattr(fd)
                try:
                    tty.setraw(fd)
                    ch = sys.stdin.read(1).lower()
                finally:
                    termios.tcsetattr(fd, termios.TCSADRAIN, old)
            else:
                try:
                    ch = input().strip()[:1].lower()
                except EOFError:
                    ch = "q"

            if ch == "r":
                self._regenerate(randomize_seed=True)
                if self._animation_speed > 0:
                    self._animate_solution()
            elif ch == "m":
                self._mg.perfect = not self._mg.perfect
                self._regenerate(randomize_seed=False)
                if self._animation_speed > 0:
                    self._animate_solution()
            elif ch == "p":
                if self._solution is not None:
                    self._show_solution = not self._show_solution
            elif ch == "a":
                self._show_solution = False
                self._animate_solution()
            elif ch == "c":
                self.palette.next()
            elif ch == "t":
                self._style_idx = (self._style_idx + 1) % len(STYLES)
                self._42_idx = self._style_idx
            elif ch == "s":
                self._style_idx = (self._style_idx + 1) % len(STYLES)
            elif ch == "n":
                self._42_idx = (self._42_idx + 1) % len(STYLES_42)
            elif ch in ("q", "", ""):
                _clear()
                print("Goodbye!")
                break
