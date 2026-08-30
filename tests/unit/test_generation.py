# ADIM 36 (Test) - Labirent üretme algoritmalarının testleri

import importlib


def test_mazegen_package_is_importable() -> None:
    module = importlib.import_module("mazegen")
    assert module is not None
