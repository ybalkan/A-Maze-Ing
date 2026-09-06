from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from mazegen.models.maze import Maze

def hex_string_to_row(hex_line: str) -> List[int]:
    return (int(ch, 16) for ch in hex_line.strip())

def maze_to_hex_lines(maze: 'Maze') -> List[str]:
    lines: List[str] = []
    for row_index in range(maze.height):
        row_str = ''
        for col_index in range(maze.width):
            cell = maze.grid[row_index][col_index]
            row_str += cell.to_hex()
        lines.append(row_str)
    return lines

def apply_hex_lines_to_maze(maze: 'Maze', hex_lines: List[str]) -> None:
    for row_index, line in enumerate(hex_lines):
        for col_index, ch in enumerate(line.strip()):
            maze.grid[row_index][col_index].from_hex(ch)