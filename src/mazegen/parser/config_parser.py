from typing import Tuple

def parse_config(filepath: str) -> dict:
    config: dict = {}

    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()

            if not line or line.startswith("#"):
                continue
            if '=' not in line:
                continue

            key, _, value = line.partition('=')
            key = key.strip()
            value = value.strip()

            config[key] = _parse_value(key, value)

        return config

def _parse_value(key: str, value: str) -> object:

    if key in ('ENTRY', 'EXIT'):
        return _parse_coord(value)
    if key in ('WIDTH', 'HEIGHT'):
        return int(value)
    if key == 'PERFECT':
        return value.lower == 'true'
    if key == 'SEED':
        return int(value) if value.lower() != 'none' else None
    return value

def _parse_coord(value: str) -> Tuple[int, int]:
    parts = value.split(',')
    return (int(parts[0].strip()), int(parts[1].strip()))