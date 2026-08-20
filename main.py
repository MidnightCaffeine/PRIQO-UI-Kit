"""PRISQO UI KIT — entry point.

Run with:
    python main.py
"""
import sys
from pathlib import Path

import flet as ft

# Make `src/` importable without installing the package.
sys.path.insert(0, str(Path(__file__).parent / "src"))
sys.path.insert(0, str(Path(__file__).parent))

from showcase.app import main  # noqa: E402

if __name__ == "__main__":
    ft.app(target=main)
