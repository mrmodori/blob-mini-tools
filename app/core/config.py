"""Application configuration loader.

This module exposes a single ``CONFIG`` dictionary loaded from the
``config.json`` file located at the root of the ``app`` package.  Using a
path derived from ``__file__`` ensures the configuration is found
regardless of the current working directory.
"""

from pathlib import Path
import json

# Resolve the path to ``config.json`` relative to this module's directory.
CONFIG_PATH = (Path(__file__).resolve().parent / ".." / "config.json").resolve()

with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    CONFIG = json.load(f)

