from __future__ import annotations

from typing import Dict

RESET = "[0m"


class Ansi:
    BLACK = "[30m"
    RED = "[31m"
    GREEN = "[32m"
    YELLOW = "[33m"
    BLUE = "[34m"
    MAGENTA = "[35m"
    CYAN = "[36m"
    WHITE = "[37m"

    BRIGHT_BLACK = "[90m"
    BRIGHT_RED = "[91m"
    BRIGHT_GREEN = "[92m"
    BRIGHT_YELLOW = "[93m"
    BRIGHT_BLUE = "[94m"
    BRIGHT_MAGENTA = "[95m"
    BRIGHT_CYAN = "[96m"
    BRIGHT_WHITE = "[97m"

    BOLD = "[1m"


_PALETTES: Dict[str, Dict[str, str]] = {
    "default": {
        "wall": Ansi.WHITE,
        "entry": Ansi.BRIGHT_GREEN,
        "exit": Ansi.BRIGHT_RED,
        "solution": Ansi.BRIGHT_YELLOW,
    },
    "blue": {
        "wall": Ansi.BRIGHT_BLUE,
        "entry": Ansi.BRIGHT_GREEN,
        "exit": Ansi.BRIGHT_RED,
        "solution": Ansi.BRIGHT_YELLOW,
    },
    "magenta": {
        "wall": Ansi.BRIGHT_MAGENTA,
        "entry": Ansi.BRIGHT_GREEN,
        "exit": Ansi.BRIGHT_RED,
        "solution": Ansi.BRIGHT_YELLOW,
    },
    "cyan": {
        "wall": Ansi.BRIGHT_CYAN,
        "entry": Ansi.BRIGHT_GREEN,
        "exit": Ansi.BRIGHT_RED,
        "solution": Ansi.BRIGHT_YELLOW,
    },
    "red": {
        "wall": Ansi.BRIGHT_RED,
        "entry": Ansi.BRIGHT_GREEN,
        "exit": Ansi.BRIGHT_CYAN,
        "solution": Ansi.BRIGHT_YELLOW,
    },
}

PALETTE_NAMES = list(_PALETTES.keys())


class ColorPalette:

    def __init__(self, name: str = "default") -> None:
        self._idx = PALETTE_NAMES.index(name) if name in PALETTE_NAMES else 0

    @property
    def name(self) -> str:
        return PALETTE_NAMES[self._idx]

    @property
    def wall(self) -> str:
        return _PALETTES[self.name]["wall"]

    @property
    def entry(self) -> str:
        return _PALETTES[self.name]["entry"]

    @property
    def exit(self) -> str:
        return _PALETTES[self.name]["exit"]

    @property
    def solution(self) -> str:
        return _PALETTES[self.name]["solution"]

    def next(self) -> "ColorPalette":
        self._idx = (self._idx + 1) % len(PALETTE_NAMES)
        return self
