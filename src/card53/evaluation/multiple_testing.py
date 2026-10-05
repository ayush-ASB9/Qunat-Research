from __future__ import annotations

import numpy as np


def benjamini_hochberg_adjust(p_values: list[float] | np.ndarray) -> np.ndarray:
    p = np.asarray(p_values, dtype=float)
    if p.size == 0:
        return p
    n = p.size
    order = np.argsort(p)
    adjusted = np.empty(n, dtype=float)
    running = 1.0
    for rank, idx in enumerate(reversed(order), start=1):
        adjusted[idx] = min(1.0, running * p[idx] * n / rank)
        running = min(running, adjusted[idx])
    return adjusted[np.argsort(order)]
