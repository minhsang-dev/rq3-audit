"""p3_lib.py -- shared code for the P3b cost probe and the g(x) correctness tests (a)-(e).

Design: 05_FUTURE_PROBES.md. This module contains NO experiment logic of its own beyond
(1) the locked LightGBM configuration, (2) the weighted log-loss, (3) the EER score g(x) of
outline eq. (2-6) in its naive form (Q17), exact (full refit) and leaf-refit variants,
(4) stand-in data generators.  It reads no real data.
"""
from __future__ import annotations

import dataclasses
import hashlib
import time
from typing import Callable, Optional

import numpy as np

# ---------------------------------------------------------------------------------------------
# Locked LightGBM configuration: Bai 1 Table 2 (sources/bai1_manuscript_v4_2_clean.md, Sec. 4.3).
# RUNNER_ADDITIONS are NOT hyper-parameter changes; they only remove run-to-run nondeterminism
# (needed by test d). They are a recorded diff against the locked worker.
# ---------------------------------------------------------------------------------------------
LOCKED_PARAMS = dict(
    n_estimators=300,
    learning_rate=0.02162,
    num_leaves=15,
    min_child_samples=5,
    subsample=0.886,
    subsample_freq=1,
    colsample_bytree=0.983,
    reg_lambda=0.26711,
    verbosity=-1,
)
RUNNER_ADDITIONS = dict(deterministic=True, force_row_wise=True)
# Optional EER-SCORING variant (NOT the deployed model): no bagging / no column sampling, so that adding one
# hypothetical row does not re-draw the random subsample. Default "locked" = exactly Bai 1 Table 2.
# Using "nobag" is a deviation from the lock and needs NCS approval; it is recorded in run_manifest.json.
VARIANT = {"v": "locked"}
NOBAG_OVERRIDES = dict(subsample=1.0, subsample_freq=0, colsample_bytree=1.0)

EPS = 1e-12


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def weighted_logloss(p1: np.ndarray, y: np.ndarray, w: Optional[np.ndarray] = None) -> float:
    """Weighted log-loss, normalised by sum of weights (Q25: L_V = log-loss with 1/pi weights)."""
    p = np.clip(np.asarray(p1, dtype=np.float64), EPS, 1.0 - EPS)
    y = np.asarray(y, dtype=np.float64)
    ell = -(y * np.log(p) + (1.0 - y) * np.log(1.0 - p))
    if w is None:
        return float(ell.mean())
    w = np.asarray(w, dtype=np.float64)
    return float((w * ell).sum() / w.sum())


# ---------------------------------------------------------------------------------------------
# Learners. A learner = fit(X, y, w) -> fitted object with .p1(X) (P(y=1|x)).
# ---------------------------------------------------------------------------------------------
class LGBFitted:
    def __init__(self, model):
        self.model = model

    def p1(self, X):
        return self.model.predict_proba(X)[:, 1]

    @property
    def booster(self):
        return self.model.booster_


class LGBLearner:
    """Locked LightGBM. `seed` fixes every internal RNG (bagging, feature fraction)."""

    name = "lightgbm_locked"

    def __init__(self, seed: int, n_jobs: int = 1):
        self.seed = int(seed)
        self.n_jobs = int(n_jobs)

    def fit(self, X, y, w=None):
        import lightgbm as lgb

        params = dict(LOCKED_PARAMS)
        if VARIANT["v"] == "nobag":
            params.update(NOBAG_OVERRIDES)
        m = lgb.LGBMClassifier(**params, **RUNNER_ADDITIONS,
                               random_state=self.seed, n_jobs=self.n_jobs)
        m.fit(X, y, sample_weight=w)
        return LGBFitted(m)


class LRFitted:
    def __init__(self, model):
        self.model = model

    def p1(self, X):
        return self.model.predict_proba(X)[:, 1]


class LRLearner:
    """Weighted logistic regression. Used ONLY to test the plumbing of g(x) (test b): a zero-weight
    row is exactly neutral for it, which is not guaranteed for LightGBM (bagging, min_data_in_leaf)."""

    name = "logreg_mock"

    def __init__(self, seed: int = 0, n_jobs: int = 1):
        pass

    def fit(self, X, y, w=None):
        from sklearn.linear_model import LogisticRegression

        m = LogisticRegression(C=1e6, tol=1e-12, max_iter=5000)
        m.fit(X, y, sample_weight=w)
        return LRFitted(m)


# ---------------------------------------------------------------------------------------------
# g(x), naive form of eq. (2-6): hypothetical row (x, y) is ADDED to C (no eviction, no HB2 admission).
# ---------------------------------------------------------------------------------------------
@dataclasses.dataclass
class EERState:
    learner: object
    X_C: np.ndarray
    y_C: np.ndarray
    w_C: Optional[np.ndarray]
    V_X: np.ndarray
    V_y: np.ndarray
    V_w: Optional[np.ndarray]
    base: object = None
    loss0: float = float("nan")

    def prepare(self):
        self.base = self.learner.fit(self.X_C, self.y_C, self.w_C)
        self.loss0 = weighted_logloss(self.base.p1(self.V_X), self.V_y, self.V_w)
        return self


def _augment(state: EERState, x: np.ndarray, y: int, w_new: float):
    X = np.vstack([state.X_C, x.reshape(1, -1)])
    yy = np.append(state.y_C, y)
    if state.w_C is None and w_new == 1.0:
        w = None
    else:
        base_w = np.ones(len(state.y_C)) if state.w_C is None else state.w_C
        w = np.append(base_w, w_new)
    return X, yy, w


def hypothesis_loss_exact(state: EERState, x: np.ndarray, y: int, w_new: float = 1.0) -> float:
    X, yy, w = _augment(state, x, y, w_new)
    fitted = state.learner.fit(X, yy, w)
    return weighted_logloss(fitted.p1(state.V_X), state.V_y, state.V_w)


def hypothesis_loss_leaf(state: EERState, x: np.ndarray, y: int) -> float:
    """Leaf-refit approximation: keep the tree structure of the base LightGBM, re-estimate leaf values
    on C u {(x,y)} (decay_rate = 0, i.e. new leaf values only). Outline L64."""
    X, yy, _ = _augment(state, x, y, 1.0)
    booster = state.base.booster.refit(X, yy, decay_rate=0.0)
    return weighted_logloss(booster.predict(state.V_X), state.V_y, state.V_w)


def g_score(state: EERState, x: np.ndarray, p_hat: Optional[np.ndarray] = None,
            method: str = "exact", w_new: float = 1.0) -> float:
    """g(x) = sum_y p_hat(y|x) * (L_V(C) - L_V(C u {(x,y)})).  p_hat defaults to the base model."""
    if p_hat is None:
        p1 = float(state.base.p1(x.reshape(1, -1))[0])
        p_hat = np.array([1.0 - p1, p1])
    p_hat = np.asarray(p_hat, dtype=np.float64)
    assert abs(p_hat.sum() - 1.0) < 1e-9, "p_hat must sum to 1"
    total = 0.0
    for y in (0, 1):
        if p_hat[y] == 0.0:
            continue
        if method == "exact":
            loss = hypothesis_loss_exact(state, x, y, w_new)
        elif method == "leaf":
            loss = hypothesis_loss_leaf(state, x, y)
        else:
            raise ValueError(method)
        total += p_hat[y] * (state.loss0 - loss)
    return float(total)


# ---------------------------------------------------------------------------------------------
# Stand-in data (NOT real DEV roots). The real roots are plugged in through an adapter module,
# see adapter_real_TEMPLATE.py. Timing depends weakly on data, so results with the stand-in are
# a smoke test and an order-of-magnitude check only.
# ---------------------------------------------------------------------------------------------
@dataclasses.dataclass
class World:
    X_C: np.ndarray
    y_C: np.ndarray
    V_X: np.ndarray
    V_y: np.ndarray
    V_w: np.ndarray
    cand_X: np.ndarray
    meta: dict


def make_synthetic_world(root: str, seed: int, n_V: int, n_C: int = 2000, n_cand: int = 1500,
                         n_feat: int = 46, attack_rate: float = 0.08) -> World:
    """Benign ~ N(0, I); three attack families with shifted means on a few features.
    V is drawn by Poisson sampling with higher inclusion for attacks; weights = 1/pi."""
    rng = np.random.default_rng(int(hashlib.sha256(f"{root}|{seed}".encode()).hexdigest()[:8], 16))
    shifts = [rng.normal(0, 1.2, n_feat) * (rng.random(n_feat) < 0.15) for _ in range(3)]

    def draw(n):
        y = (rng.random(n) < attack_rate).astype(int)
        fam = rng.integers(0, 3, n)
        X = rng.normal(0, 1, (n, n_feat))
        for f in range(3):
            m = (y == 1) & (fam == f)
            X[m] += shifts[f]
        return X.astype(np.float64), y

    X_C, y_C = draw(n_C)
    pool_X, pool_y = draw(n_V * 40 + 1000)
    pi = np.where(pool_y == 1, 0.6, 0.6 / 10.0)  # oversample attacks 10x -> weights 1/pi
    pi = np.minimum(1.0, pi * n_V / (pi.sum()))
    keep = rng.random(len(pool_y)) < pi
    if keep.sum() < 2:
        keep[:2] = True
    cand_X, _ = draw(n_cand)
    return World(X_C, y_C, pool_X[keep], pool_y[keep], 1.0 / pi[keep], cand_X,
                 dict(kind="SYNTHETIC_STAND_IN", root=root, seed=seed, n_V=int(keep.sum())))


# ---------------------------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------------------------
class Timer:
    """Wall and process-CPU time of a block (CPU time covers all threads of this process)."""

    def __enter__(self):
        self.w0, self.c0 = time.perf_counter(), time.process_time()
        return self

    def __exit__(self, *exc):
        self.wall = time.perf_counter() - self.w0
        self.cpu = time.process_time() - self.c0


def spearman(a, b) -> float:
    from scipy.stats import spearmanr

    return float(spearmanr(a, b).correlation)


def jaccard_topk(a, b, k: int) -> float:
    ta = set(np.argsort(-np.asarray(a))[:k].tolist())
    tb = set(np.argsort(-np.asarray(b))[:k].tolist())
    return len(ta & tb) / len(ta | tb)
