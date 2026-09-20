from typing import Any, Dict, FrozenSet, Tuple

_PATTERN_42 = [
    "X...X XXXX",
    "X...X ...X",
    "XXXXX XXXX",
    "....X X...",
    "....X XXXX",
]
_PATTERN_42_W = len(_PATTERN_42[0])
_PATTERN_42_H = len(_PATTERN_42)


def _compute_42_cells(width: int, height: int) -> FrozenSet[Tuple[int, int]]:
    if width < _PATTERN_42_W + 2 or height < _PATTERN_42_H + 2:
        return frozenset()

    start_col = (width - _PATTERN_42_W) // 2
    start_row = (height - _PATTERN_42_H) // 2

    cells: set[Tuple[int, int]] = set()
    for r, row_str in enumerate(_PATTERN_42):
        for c, char in enumerate(row_str):
            if char == 'X':
                cells.add((start_col + c, start_row + r))
    return frozenset(cells)


def validate_config(config: Dict[str, Any]) -> None:
    _check_required_keys(config)
    _check_dimensions(config)
    _check_coords(config)
    _check_42_overlap(config)
    _check_animation(config)


def _check_required_keys(config: Dict[str, Any]) -> None:
    required = ('WIDTH', 'HEIGHT', 'ENTRY', 'EXIT', 'OUTPUT_FILE', 'PERFECT')
    for key in required:
        if key not in config:
            raise ValueError(f"Config is missing required key: '{key}'.")
    if not isinstance(config['PERFECT'], bool):
        raise ValueError("PERFECT must be a boolean (True or False).")


def _check_dimensions(config: Dict[str, Any]) -> None:
    if config['WIDTH'] < 1:
        raise ValueError(
            f"WIDTH must be at least 1, got: {config['WIDTH']}"
        )
    if config['HEIGHT'] < 1:
        raise ValueError(
            f"HEIGHT must be at least 1, got: {config['HEIGHT']}"
        )


def _check_coords(config: Dict[str, Any]) -> None:
    width: int = config['WIDTH']
    height: int = config['HEIGHT']
    entry: Tuple[int, int] = config['ENTRY']
    exit_: Tuple[int, int] = config['EXIT']

    if not _in_grid(entry, width, height):
        raise ValueError(
            f"ENTRY {entry} is outside the grid "
            f"(0..{width - 1}, 0..{height - 1})."
        )
    if not _in_grid(exit_, width, height):
        raise ValueError(
            f"EXIT {exit_} is outside the grid "
            f"(0..{width - 1}, 0..{height - 1})."
        )
    if entry == exit_:
        raise ValueError(
            f"ENTRY and EXIT must not be the same: both are {entry}."
        )


def _check_animation(config: Dict[str, Any]) -> None:
    if 'ANIMATION_SPEED' in config:
        speed = config['ANIMATION_SPEED']
        if not isinstance(speed, (int, float)) or speed < 0.0:
            raise ValueError(
                f"ANIMATION_SPEED must be 0.0 or greater, got: {speed}"
            )


def _check_42_overlap(config: Dict[str, Any]) -> None:
    width: int = config['WIDTH']
    height: int = config['HEIGHT']
    entry: Tuple[int, int] = config['ENTRY']
    exit_: Tuple[int, int] = config['EXIT']

    cells_42 = _compute_42_cells(width, height)
    if not cells_42:
        return

    if entry in cells_42:
        raise ValueError(
            f"ENTRY {entry} overlaps with a '42' pattern cell. "
            f"This cell is unreachable — the maze would have no solution. "
            f"For a {width}x{height} maze the '42' pattern occupies "
            f"col[{(width - _PATTERN_42_W) // 2}.."
            f"{(width - _PATTERN_42_W) // 2 + _PATTERN_42_W - 1}], "
            f"row[{(height - _PATTERN_42_H) // 2}.."
            f"{(height - _PATTERN_42_H) // 2 + _PATTERN_42_H - 1}]. "
            f"Please choose a different ENTRY coordinate."
        )
    if exit_ in cells_42:
        raise ValueError(
            f"EXIT {exit_} overlaps with a '42' pattern cell. "
            f"This cell is unreachable — the maze would have no solution. "
            f"Please choose a different EXIT coordinate."
        )


def _in_grid(coord: Tuple[int, int], width: int, height: int) -> bool:
    col, row = coord
    return 0 <= col < width and 0 <= row < height
