from typing import Tuple

def validate_config(config: dict) -> None:
    _check_required_keys(config)
    _check_dimensions(config)
    _check_coords(config)

def _check_required_keys(config: dict) -> None:
    required = ['WIDTH', 'HEIGHT', 'ENTRY', 'EXIT', 'OUTPUT_FILE']
    for key in required:
        if key not in config:
            raise ValueError("Config is missing: '{key}' not found")

def _check_dimensions(config: dict) -> None:
    if config['WIDTH'] < 1:
        raise ValueError(f"WIDTH should be at least one, given: {config['WIDTH']}")
    if config['HEIGHT'] < 1:
            raise ValueError(f"HEIGHT should be at least one, given: {config['HEIGHT']}")
    #TODO width <= 1000

def _check_coords(config: dict) -> None:
     width: int = config['WIDTH']
     height: int = config['HEIGHT']
     entry: Tuple[int, int] = config['ENTRY']
     exit_: Tuple[int, int] = config['EXIT']

     if not _in_grid(entry, width, height):
         raise ValueError(f"ENTRY {entry} out of the grid"
                      f"0..{width - 1}, 0..{height - 1}.")

     if not _in_grid(exit_, width, height):
              raise ValueError(f"EXIT {exit_} out of the grid"
                           f"0..{width - 1}, 0..{height - 1}.")

def _in_grid(coord: Tuple[int, int], width: int, height: int) -> bool:
     col, row = coord
     return 0 <= col < width and 0 <= row < height
        