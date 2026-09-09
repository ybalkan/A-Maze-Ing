from dataclasses import dataclass
from .direction import Direction


@dataclass(repr=False, unsafe_hash=True)
class Cell:
    col: int
    row: int
    walls: int = 0b1111
    visited: bool = False

    def has_wall(self, direction: Direction) -> bool:
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
        return f"Cell(col={self.col}, row={self.row}, hex='{self.to_hex()}')"