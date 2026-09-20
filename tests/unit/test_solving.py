from mazegen.models.maze import Maze
from mazegen.generation.recursive_backtracker import RecursiveBacktracker
from mazegen.solving.bfs_solver import BFSSolver
from mazegen.api.maze_generator import MazeGenerator


def test_solvers_consistency() -> None:
    gen = RecursiveBacktracker(10, 10, seed=42)
    maze = gen.generate()

    entry = (0, 0)
    exit_ = (9, 9)

    bfs = BFSSolver(maze, entry, exit_)
    sol_bfs = bfs.solve()
    assert sol_bfs is not None


def test_unreachable_maze() -> None:
    maze = Maze(3, 3)
    solver = BFSSolver(maze, (0, 0), (2, 2))
    sol = solver.solve()
    assert sol is None


def test_seed_reproducibility_solution() -> None:
    def make_solution(seed: int) -> str:
        mg = MazeGenerator(10, 10, seed=seed, perfect=True)
        mg.generate()
        sol = mg.solve()
        assert sol is not None
        return sol.to_string()

    for seed in (0, 1, 42, 999, 12345):
        s1 = make_solution(seed)
        s2 = make_solution(seed)
        assert s1 == s2, f"Seed {seed} ile farklı çözümler üretildi!"


def test_solution_path_starts_at_entry() -> None:
    gen = RecursiveBacktracker(8, 8, seed=5)
    maze = gen.generate()
    entry = (0, 0)
    exit_ = (7, 7)
    solver = BFSSolver(maze, entry, exit_)
    sol = solver.solve()
    assert sol is not None
    assert sol.path_cells[0] == entry, "Çözüm giriş hücresinden başlamıyor!"


def test_solution_path_ends_at_exit() -> None:
    gen = RecursiveBacktracker(8, 8, seed=5)
    maze = gen.generate()
    entry = (0, 0)
    exit_ = (7, 7)
    solver = BFSSolver(maze, entry, exit_)
    sol = solver.solve()
    assert sol is not None
    assert sol.path_cells[-1] == exit_, "Çözüm çıkış hücresinde bitmiyor!"


def test_solution_animator_steps() -> None:
    from mazegen.rendering.animation import SolutionAnimator

    gen = RecursiveBacktracker(6, 6, seed=3)
    maze = gen.generate()
    entry = (0, 0)
    exit_ = (5, 5)
    solver = BFSSolver(maze, entry, exit_)
    sol = solver.solve()
    assert sol is not None

    animator = SolutionAnimator(sol, speed=0.0)
    assert animator.total_steps == len(sol.path_cells)

    prev_len = 0
    for step_cells in animator.steps():
        assert len(step_cells) > prev_len, "Animasyon adımı büyümedi!"
        prev_len = len(step_cells)

    assert prev_len == len(sol.path_cells), "Tüm hücreler gösterilmedi!"


def test_solution_animator_get_step_cells() -> None:
    from mazegen.rendering.animation import SolutionAnimator

    gen = RecursiveBacktracker(5, 5, seed=10)
    maze = gen.generate()
    solver = BFSSolver(maze, (0, 0), (4, 4))
    sol = solver.solve()
    assert sol is not None

    animator = SolutionAnimator(sol, speed=0.0)

    assert len(animator.get_step_cells(0)) == 0

    step1 = animator.get_step_cells(1)
    assert (0, 0) in step1

    full = animator.get_step_cells(animator.total_steps)
    assert len(full) == animator.total_steps
