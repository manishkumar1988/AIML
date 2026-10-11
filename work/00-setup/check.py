"""Challenge 00 smoke check: environment versions and seed.

Run: uv run python work/00-setup/check.py
"""

import platform

import numpy as np
import pandas as pd
import sklearn

from common.seed import set_seed


def main() -> None:
    seed = set_seed()
    print(f"python={platform.python_version()}")
    print(f"numpy={np.__version__}")
    print(f"pandas={pd.__version__}")
    print(f"scikit-learn={sklearn.__version__}")
    print(f"seed={seed} first_draw={np.random.rand():.6f}")


if __name__ == "__main__":
    main()
