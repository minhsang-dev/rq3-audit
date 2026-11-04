"""Template for plugging the REAL DEV roots into run_p3b.py (--adapter path/to/your_adapter.py).

The locked Bai 1 / RQ2 replay code (replay/data.py, SHA-256 e2407dfa2f2c1aaea020bf389ef1c33c7f01f85be45bd2ef52a076a129f3b21a)
is NOT in this repository, so this file cannot be completed here. Copy it, implement `load_world`, and verify:
  * roots are DEV roots only (ToN 2019-04-24/25/27/28/29, CIC 2018-02-21; DEV_REUSE). NEVER CIDDS, UNSW or UGR'16 (reserved for confirmation).
  * C has k = 2000 rows and is a context produced by the locked HB2 policy (or a FIFO/CBRS context for a pure timing probe: say which in meta).
  * V_* holds a reserved-label sample with inverse-probability weights V_w = 1/pi and |V| = n_V.
  * cand_X are unlabelled candidate rows from the POLICY part only (never EVAL).
"""
import numpy as np

from p3_lib import World


def load_world(root: str, seed: int, n_V: int) -> World:  # pragma: no cover - template
    raise NotImplementedError("Implement with the locked replay code; return p3_lib.World(...).")
