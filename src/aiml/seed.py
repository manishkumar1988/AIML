"""Seed control for reproducible runs."""

from __future__ import annotations

import os
import random


def set_seed(seed: int) -> int:
    """Fix the Python RNG and hash seed.

    NumPy and PyTorch seeds belong in this function once those libraries are dependencies.
    """
    os.environ["PYTHONHASHSEED"] = str(seed)
    random.seed(seed)
    return seed
