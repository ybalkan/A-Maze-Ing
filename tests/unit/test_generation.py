from mazegen.models.maze import Maze
from mazegen.models.direction import Direction
from mazegen.generation.recursive_backtracker import RecursiveBacktracker
from mazegen.generation.braided import BraidedGenerator
from mazegen.api.maze_generator import MazeGenerator


def test_maze_bounds() -> None:
    m = Maze(5, 5)
    assert m.in_bounds(0, 0) is True
    assert m.in_bounds(5, 5) is False
    assert m.in_bounds(-1, 0) is False


def test_generator_seed_consistency() -> None:
    g1 = RecursiveBacktracker(10, 10, seed=42)
    m1 = g1.generate()

    g2 = RecursiveBacktracker(10, 10, seed=42)
    m2 = g2.generate()

    for row in range(10):
        for col in range(10):
            assert m1.grid[row][col].walls == m2.grid[row][col].walls


def test_maze_generator_api() -> None:
    mg = MazeGenerator(10, 10, seed=123, perfect=True, algorithm="prim")
    mg.generate()
    maze = mg.get_maze()
    assert maze.width == 10
    assert maze.height == 10
    assert maze.grid[0][0].walls != 0


def test_braided_generator() -> None:
    gen = BraidedGenerator(10, 10, seed=1)
    maze = gen.generate()

    dead_ends = 0
    for row in maze.grid:
        for cell in row:
            wall_count = sum(1 for d in Direction if cell.has_wall(d))
            if wall_count == 3:
                dead_ends += 1

    assert dead_ends == 0


def test_wall_consistency() -> None:
    gen = RecursiveBacktracker(10, 10, seed=99)
    maze = gen.generate()

    for row in range(maze.height):
        for col in range(maze.width):
            cell = maze.grid[row][col]
            if col + 1 < maze.width:
                neighbor = maze.grid[row][col + 1]
                assert cell.has_wall(Direction.EAST) == neighbor.has_wall(Direction.WEST), (
                    f"Wall consistency hatası: ({col},{row}).EAST != ({col+1},{row}).WEST"
                )
            if row + 1 < maze.height:
                neighbor = maze.grid[row + 1][col]
                assert cell.has_wall(Direction.SOUTH) == neighbor.has_wall(Direction.NORTH), (
                    f"Wall consistency hatası: ({col},{row}).SOUTH != ({col},{row+1}).NORTH"
                )


def test_perfect_maze_no_cycles() -> None:
    gen = RecursiveBacktracker(8, 8, seed=7)
    maze = gen.generate()

    from collections import deque
    from typing import Deque
    from mazegen.models.cell import Cell as _Cell
    start = maze.grid[0][0]
    visited = {start}
    queue: Deque[_Cell] = deque([start])

    while queue:
        current = queue.popleft()
        for _direction, neighbor in maze.get_accessible_neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    non_42_cells = [
        cell
        for row in maze.grid
        for cell in row
        if not cell.is_42
    ]
    assert len(visited) >= len(non_42_cells), (
        f"Bazı hücreler erişilemez: {len(non_42_cells) - len(visited)} hücre kayıp"
    )


def test_seed_reproducibility_api() -> None:
    mg1 = MazeGenerator(12, 8, seed=2024, perfect=True)
    mg1.generate()
    sol1 = mg1.solve()

    mg2 = MazeGenerator(12, 8, seed=2024, perfect=True)
    mg2.generate()
    sol2 = mg2.solve()

    assert sol1 is not None
    assert sol2 is not None
    assert sol1.to_string() == sol2.to_string(), (
        "Aynı seed ile farklı çözüm! Deterministiklik bozulmuş."
    )


def test_reusable_module_import() -> None:
    import mazegen
    assert hasattr(mazegen, "MazeGenerator")
    assert hasattr(mazegen, "Maze")
    assert hasattr(mazegen, "Cell")
    assert hasattr(mazegen, "Direction")
    assert hasattr(mazegen, "Solution")


def test_generator_all_algorithms() -> None:
    algorithms = ["recursive_backtracker", "prim", "braided"]
    for algo in algorithms:
        mg = MazeGenerator(6, 6, seed=1, perfect=True, algorithm=algo)
        mg.generate()
        maze = mg.get_maze()
        assert maze.width == 6
        assert maze.height == 6


def test_42_pattern_no_overlap_default() -> None:
    from mazegen.parser.validator import validate_config
    cfg = {
        "WIDTH": 20, "HEIGHT": 15,
        "ENTRY": (0, 0), "EXIT": (19, 14),
        "OUTPUT_FILE": "o.txt", "PERFECT": False,
    }
    validate_config(cfg)


def test_42_pattern_overlap_entry_raises() -> None:
    import pytest
    from mazegen.parser.validator import validate_config
    cfg = {
        "WIDTH": 20, "HEIGHT": 15,
        "ENTRY": (5, 5),
        "EXIT": (19, 14),
        "OUTPUT_FILE": "o.txt", "PERFECT": False,
    }
    with pytest.raises(ValueError, match="42"):
        validate_config(cfg)


def test_42_pattern_overlap_exit_raises() -> None:
    import pytest
    from mazegen.parser.validator import validate_config
    cfg = {
        "WIDTH": 20, "HEIGHT": 15,
        "ENTRY": (0, 0),
        "EXIT": (9, 7),
        "OUTPUT_FILE": "o.txt", "PERFECT": False,
    }
    with pytest.raises(ValueError, match="42"):
        validate_config(cfg)


def test_42_pattern_small_maze_no_check() -> None:
    from mazegen.parser.validator import validate_config
    cfg = {
        "WIDTH": 5, "HEIGHT": 5,
        "ENTRY": (2, 2), "EXIT": (4, 4),
        "OUTPUT_FILE": "o.txt", "PERFECT": True,
    }
    validate_config(cfg)
