from __future__ import annotations
import sys
import os
from typing import Optional

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

# Renk paleti ve ASCII çizim modüllerini içe aktarıyoruz.
from mazegen.rendering.color_palette import ColorPalette
from mazegen.rendering.ascii_renderer import AsciiRenderer

from mazegen.api.maze_generator import MazeGenerator
from mazegen.parser.validator import validate_config
from mazegen.parser.config_parser import parse_config


def main() -> int:
    if len(sys.argv) not in (2, 3):
        print("Kullanım: python3 a_maze_ing.py <config_dosyası>")
        print("Örnek:    python3 a_maze_ing.py configs/config.txt")
        return 1

    config_path = ""
    for arg in sys.argv[1:]:
        config_path = arg

    if not config_path:
        print("Hata: Config dosyası belirtilmedi.")
        return 1

    try:
        cfg = parse_config(config_path)
    except FileNotFoundError:
        print(f"Hata: Config dosyası bulunamadı: '{config_path}'")
        return 1
    except ValueError as e:
        print(f"Hata (config format): {e}")
        return 1

    try:
        validate_config(cfg)
    except ValueError as e:
        print(f"Hata (config doğrulama): {e}")
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
        print(f"Çıktı dosyası yazıldı: {output_file}")
    except OSError as e:
        print(f"Uyarı: Output dosyası yazılamadı: {e}")

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

    renderer._regenerate = _regenerate_and_export

    renderer.run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
