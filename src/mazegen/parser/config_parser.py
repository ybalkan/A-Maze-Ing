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
                    f"Config format hatası: '=' işareti yok → '{line}'"
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
                f"{key} için geçersiz tamsayı değeri: '{value}'. "
                f"Tam sayı olmalı (örn: {key}=20)"
            )

    if key == 'PERFECT':
        if value.lower() not in ('true', 'false'):
            raise ValueError(
                f"PERFECT için geçersiz değer: '{value}'. "
                f"'True' veya 'False' olmalı."
            )
        return value.lower() == 'true'

    if key == 'ANIMATION':
        if value.lower() not in ('true', 'false'):
            raise ValueError(
                f"ANIMATION için geçersiz değer: '{value}'. "
                f"'True' veya 'False' olmalı."
            )
        return value.lower() == 'true'

    if key == 'ANIMATION_SPEED':
        try:
            speed = float(value)
        except ValueError:
            raise ValueError(
                f"ANIMATION_SPEED için geçersiz ondalık değer: '{value}'. "
                f"Sayısal bir değer olmalı (örn: 0.05)"
            )
        if speed < 0.0:
            raise ValueError(
                f"ANIMATION_SPEED negatif olamaz: {speed}. "
                f"0.0 veya daha büyük bir değer verin."
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
            f"Geçersiz koordinat formatı: '{value}'. "
            f"Beklenen format: 'x,y' (örn: 0,0)"
        )
