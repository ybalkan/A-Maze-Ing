from enum import Enum

class Direction(Enum):
    NORTH = 0b0001
    EAST = 0b0010
    SOUTH = 0b0100
    WEST = 0b1000


    @property
    def opposite(self) -> 'Direction':
        _opposites: dict['Direction', 'Direction'] = {
            Direction.NORTH: Direction.SOUTH,
            Direction.EAST: Direction.WEST,
            Direction.SOUTH: Direction.NORTH,
            Direction.WEST: Direction.EAST,
        }
        return _opposites[self]

    @property
    def delta(self) -> tuple[int, int]:
        _deltas: dict['Direction', tuple[int, int]] = {
            Direction.NORTH: (0, -1),
            Direction.EAST: (1, 0),
            Direction.SOUTH: (0, 1),
            Direction.WEST: (-1, 0),
        }
        return _deltas[self]

    @property
    def dx(self) -> int:
        return self.delta[0]

    @property
    def dy(self) -> int:
        return self.delta[1]