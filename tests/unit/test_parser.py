import pytest
from mazegen.parser.config_parser import parse_config
from mazegen.parser.validator import validate_config
from mazegen.models.cell import Cell

from typing import Any


def test_parse_valid_config(tmp_path: Any) -> None:
    config_file = tmp_path / "valid.txt"
    config_file.write_text(
        "WIDTH=10\nHEIGHT=15\nENTRY=0,0\nEXIT=9,14\nPERFECT=True\nOUTPUT_FILE=out.txt\n")

    cfg = parse_config(str(config_file))
    assert cfg["WIDTH"] == 10
    assert cfg["HEIGHT"] == 15
    assert cfg["ENTRY"] == (0, 0)
    assert cfg["EXIT"] == (9, 14)
    assert cfg["PERFECT"] is True


def test_parse_invalid_config(tmp_path: Any) -> None:
    config_file = tmp_path / "invalid.txt"
    config_file.write_text("WIDTH=abc\n")
    with pytest.raises(ValueError):
        parse_config(str(config_file))


def test_validator_missing_keys() -> None:
    cfg = {"WIDTH": 10}
    with pytest.raises(ValueError, match="Config eksik"):
        validate_config(cfg)


def test_validator_out_of_bounds_entry() -> None:
    cfg = {
        "WIDTH": 10, "HEIGHT": 10,
        "ENTRY": (15, 0), "EXIT": (9, 9),
        "OUTPUT_FILE": "o.txt", "PERFECT": False
    }
    with pytest.raises(ValueError, match="grid dışında"):
        validate_config(cfg)


def test_cell_hex_conversion() -> None:
    c = Cell(0, 0, walls=10)
    assert c.to_hex() == "a"
    c.from_hex("f")
    assert c.walls == 15


def test_parse_animation_config(tmp_path: Any) -> None:
    config_file = tmp_path / "anim.txt"
    config_file.write_text(
        "WIDTH=5\nHEIGHT=5\nENTRY=0,0\nEXIT=4,4\n"
        "OUTPUT_FILE=out.txt\nPERFECT=False\n"
        "ANIMATION=true\nANIMATION_SPEED=0.1\n"
    )
    cfg = parse_config(str(config_file))
    assert cfg["ANIMATION"] is True
    assert abs(cfg["ANIMATION_SPEED"] - 0.1) < 1e-9


def test_parse_animation_false(tmp_path: Any) -> None:
    config_file = tmp_path / "noanim.txt"
    config_file.write_text(
        "WIDTH=5\nHEIGHT=5\nENTRY=0,0\nEXIT=4,4\n"
        "OUTPUT_FILE=out.txt\nPERFECT=False\n"
        "ANIMATION=false\nANIMATION_SPEED=0.05\n"
    )
    cfg = parse_config(str(config_file))
    assert cfg["ANIMATION"] is False


def test_parse_invalid_animation_speed(tmp_path: Any) -> None:
    config_file = tmp_path / "badspeed.txt"
    config_file.write_text(
        "WIDTH=5\nHEIGHT=5\nENTRY=0,0\nEXIT=4,4\n"
        "OUTPUT_FILE=out.txt\nANIMATION_SPEED=-1.0\n"
    )
    with pytest.raises(ValueError, match="negatif"):
        parse_config(str(config_file))


def test_parse_invalid_animation_value(tmp_path: Any) -> None:
    config_file = tmp_path / "badanim.txt"
    config_file.write_text("ANIMATION=maybe\n")
    with pytest.raises(ValueError):
        parse_config(str(config_file))


def test_comment_lines_skipped(tmp_path: Any) -> None:
    config_file = tmp_path / "comments.txt"
    config_file.write_text(
        "# Bu bir yorum\n"
        "WIDTH=7\n"
        "# Başka bir yorum\n"
        "HEIGHT=7\n"
        "ENTRY=0,0\nEXIT=6,6\nOUTPUT_FILE=out.txt\nPERFECT=False\n"
    )
    cfg = parse_config(str(config_file))
    assert cfg["WIDTH"] == 7
    assert cfg["HEIGHT"] == 7


def test_empty_lines_skipped(tmp_path: Any) -> None:
    config_file = tmp_path / "empty.txt"
    config_file.write_text(
        "\n\nWIDTH=4\n\nHEIGHT=4\n\nENTRY=0,0\nEXIT=3,3\nOUTPUT_FILE=o.txt\nPERFECT=False\n\n"
    )
    cfg = parse_config(str(config_file))
    assert cfg["WIDTH"] == 4
    assert cfg["HEIGHT"] == 4


def test_validator_animation_speed_negative() -> None:
    cfg = {
        "WIDTH": 5, "HEIGHT": 5,
        "ENTRY": (0, 0), "EXIT": (4, 4),
        "OUTPUT_FILE": "o.txt", "PERFECT": False,
        "ANIMATION_SPEED": -0.5,
    }
    with pytest.raises(ValueError, match="ANIMATION_SPEED"):
        validate_config(cfg)
