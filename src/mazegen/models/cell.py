from dataclasses import dataclass
from .direction import Direction


@dataclass(repr=False)
class Cell:
    row: int
    col: int
    walls: int = 0b1111
    visited: bool = False

    def has_wal(self, direction: Direction) -> bool:
        return bool(self.walls & direction.value)

    def add_wall(self, direction: Direction) -> None:
        self.walls |= direction.value

    def remove_wall(self, direction: Direction) -> None:
        self.walls &= ~direction.value

    def to_hex(self) -> str:
        return f"{self.walls:X}"

    def from_hex(self, hex_char: str) -> None:
        self.walls = int(hex_char, 16)

    def __repr__(self) -> str:
        return f"Cell(row={self.row}, col={self.col}, hex='{self.to_hex()}')"