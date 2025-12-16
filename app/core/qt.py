from __future__ import annotations

from pathlib import Path


def ui_path(*relative_parts: str) -> str:
    """Return absolute path to a ui file located inside the app package.

    Paths are resolved relative to the repository's app/ directory, so it works
    regardless of the current working directory.
    """

    app_dir = Path(__file__).resolve().parents[1]
    return str(app_dir.joinpath(*relative_parts))
