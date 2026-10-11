"""Seed helper shared by all challenges."""

import random

import numpy as np

DEFAULT_SEED = 42


def set_seed(seed: int = DEFAULT_SEED) -> int:
    """Fix Python's and NumPy's global random generators.

    Still pass `random_state=seed` to scikit-learn splits and models explicitly.
    PyTorch seeding gets added here in Challenge 10.
    """
    random.seed(seed)
    np.random.seed(seed)
    return seed
