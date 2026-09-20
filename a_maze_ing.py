from __future__ import annotations
import sys
import os
from typing import Optional

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from mazegen.rendering.color_palette import ColorPalette  # noqa: E402
from mazegen.rendering.ascii_renderer import AsciiRenderer  # noqa: E402

from mazegen.api.maze_generator import MazeGenerator  # noqa: E402
from mazegen.parser.validator import validate_config  # noqa: E402
from mazegen.parser.config_parser import parse_config  # noqa: E402


def main() -> int:
    if len(sys.argv) not in (2, 3):
        print("Use: python3 a_maze_ing.py <config_file>")
        print("Example: python3 a_maze_ing.py configs/config.txt")
        return 1

    config_path = sys.argv[1]

    if not config_path:
        print("Error: Config file not found.")
        return 1

    try:
        cfg = parse_config(config_path)
    except FileNotFoundError:
        print(f"Error: Config file not found: '{config_path}'")
        return 1
    except ValueError as e:
        print(f"Error (config format): {e}")
        return 1

    try:
        validate_config(cfg)
    except ValueError as e:
        print(f"Error (config validation): {e}")
        return 1

    width: int = cfg["WIDTH"]
    height: int = cfg["HEIGHT"]
    entry = cfg["ENTRY"]
    exit_ = cfg["EXIT"]
    output_file: str = cfg["OUTPUT_FILE"]
    perfect: bool = cfg.get("PERFECT", False)
    seed = cfg.get("SEED")
    algorithm: str = cfg.get("ALGORITHM", "recursive_backtracker")
    animation: bool = cfg.get("ANIMATION", False)
    animation_speed: float = cfg.get("ANIMATION_SPEED", 0.05)

    effective_speed: Optional[float] = animation_speed if animation else None

    mg = MazeGenerator(
        width=width,
        height=height,
        seed=seed,
        perfect=perfect,
        algorithm=algorithm,
        entry=entry,
        exit_=exit_,
    )

    mg.generate()
    mg.solve()

    try:
        mg.export(output_file)
        print(f"Output file written: {output_file}")
    except OSError as e:
        print(f"Warning: Output file could not be written: {e}")

    palette = ColorPalette()
    renderer = AsciiRenderer(mg, entry, exit_, palette,
                             animation_speed=effective_speed)

    _original_regenerate = renderer._regenerate

    def _regenerate_and_export(randomize_seed: bool = True) -> None:
        _original_regenerate(randomize_seed=randomize_seed)
        try:
            mg.export(output_file)
        except OSError:
            pass

    renderer._regenerate = _regenerate_and_export  # type: ignore[method-assign]

    renderer.run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
