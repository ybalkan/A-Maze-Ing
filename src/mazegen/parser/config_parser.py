from typing import Any, Dict, Tuple


def parse_config(filepath: str) -> Dict[str, Any]:
    config: Dict[str, Any] = {}

    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()

            if not line or line.startswith('#'):
                continue

            if '=' not in line:
                raise ValueError(
                    f"Config format error: missing '=' sign → '{line}'"
                )

            key, _, value = line.partition('=')
            key = key.strip().upper()
            value = value.strip()

            config[key] = _parse_value(key, value)

    return config


def _parse_value(key: str, value: str) -> object:
    if key in ('ENTRY', 'EXIT'):
        return _parse_coord(value)

    if key in ('WIDTH', 'HEIGHT'):
        try:
            return int(value)
        except ValueError:
            raise ValueError(
                f"{key} has an invalid integer value: '{value}'. "
                f"Must be an integer (e.g. {key}=20)"
            )

    if key == 'PERFECT':
        if value.lower() not in ('true', 'false'):
            raise ValueError(
                f"Invalid value for PERFECT: '{value}'. "
                f"Must be 'True' or 'False'."
            )
        return value.lower() == 'true'

    if key == 'ANIMATION':
        if value.lower() not in ('true', 'false'):
            raise ValueError(
                f"Invalid value for ANIMATION: '{value}'. "
                f"Must be 'True' or 'False'."
            )
        return value.lower() == 'true'

    if key == 'ANIMATION_SPEED':
        try:
            speed = float(value)
        except ValueError:
            raise ValueError(
                f"Invalid decimal value for ANIMATION_SPEED: '{value}'. "
                f"Must be a numeric value (e.g. 0.05)"
            )
        if speed < 0.0:
            raise ValueError(
                f"ANIMATION_SPEED cannot be negative: {speed}. "
                f"Provide a value of 0.0 or greater."
            )
        return speed

    if key == 'SEED':
        return int(value) if value.lower() != 'none' else None

    return value


def _parse_coord(value: str) -> Tuple[int, int]:
    try:
        parts = value.split(',')
        if len(parts) != 2:
            raise ValueError
        return (int(parts[0].strip()), int(parts[1].strip()))
    except (ValueError, IndexError):
        raise ValueError(
            f"Invalid coordinate format: '{value}'. "
            f"Expected format: 'x,y' (e.g. 0,0)"
        )
