from pathlib import Path


def test_source_package_directory_exists() -> None:
    project_root = Path(__file__).resolve().parents[1]
    assert (project_root / "src" / "mazegen").is_dir()
