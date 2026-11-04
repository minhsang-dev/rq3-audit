#!/usr/bin/env python3
"""run_p3b.py -- P3b cost probe + g(x) correctness tests (a)-(e)  (design: 05_FUTURE_PROBES.md).

* CPU only. Resumable: every finished unit is appended (fsync) to <out>/units.jsonl; a restart skips
  finished units. Append-only <out>/version_log.jsonl records start / resume / stop / script changes.
* Refuses to resume if the script hashes or the design (roots, seeds, grid) changed, unless
  --accept-script-change is given (the change is then logged).
* Default data = SYNTHETIC STAND-IN (clearly labelled in every record). Real DEV roots: --adapter your_adapter.py
  (see adapter_real_TEMPLATE.py). The stand-in verifies the code and gives an order of magnitude; it is
  NOT P3b evidence about the real roots.
* Pre-declared pass criteria (05_FUTURE_PROBES.md, section 0) are constants below; they are not tunable by CLI.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import platform
import signal
import sys
import time
from datetime import datetime, timezone

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p3_lib as L  # noqa: E402

# ---- pre-declared criteria (05_FUTURE_PROBES.md) -------------------------------------------------
CRIT = dict(
    a_frac_pos=0.90,          # test a: >= 90 % of sparse-region candidates with g > 0, and mean g > 0
    b_tol=1e-8,               # test b: plumbing identities (mock learner)
    c_rho=0.90, c_jaccard=0.70,   # test c: leaf-refit vs exact on a subsample
    d_ratio=0.50,             # test d: mean SD(g over seeds) / SD(g over candidates)
    e_se=2.0,                 # test e: |mean HT estimate - truth| <= 2 SE
    noisy_factor=3.0,         # P3b stop rule: two consecutive repeats > 3 x median
)
V_SIZES = (30, 90, 300)
STOP = {"flag": False}


class StopRun(Exception):
    pass


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def hw_info(note: str) -> dict:
    model = ""
    try:
        with open("/proc/cpuinfo") as f:
            for line in f:
                if line.lower().startswith("model name"):
                    model = line.split(":", 1)[1].strip()
                    break
    except OSError:
        pass
    import lightgbm
    import scipy

    return dict(cpu_model=model or platform.processor(), nproc=os.cpu_count(),
                platform=platform.platform(), python=platform.python_version(),
                numpy=np.__version__, scipy=scipy.__version__, lightgbm=lightgbm.__version__,
                NCS_NOTE=note or "TODO: NCS fills CPU model / cores before the real run")


def append_jsonl(path: str, obj: dict):
    with open(path, "a") as f:
        f.write(json.dumps(obj, sort_keys=True) + "\n")
        f.flush()
        os.fsync(f.fileno())


def read_jsonl(path: str):
    if not os.path.exists(path):
        return []
    out = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    out.append(json.loads(line))
                except json.JSONDecodeError:
                    pass  # a torn last line from a hard kill: the unit is simply redone
    return out


def load_adapter(path):
    if not path:
        return None
    spec = importlib.util.spec_from_file_location("p3_adapter", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def get_world(adapter, root, seed, n_V):
    if adapter is None:
        return L.make_synthetic_world(root, seed, n_V)
    return adapter.load_world(root, seed, n_V)


# =================================================================================================
# P3b timing unit
# =================================================================================================
def unit_timing(adapter, root, seed, n_V, threads, repeats, K) -> dict:
    world = get_world(adapter, root, seed, n_V)
    learner = L.LGBLearner(seed, n_jobs=threads)
    with L.Timer() as t_base:
        state = L.EERState(learner, world.X_C, world.y_C, None, world.V_X, world.V_y, world.V_w).prepare()
    rng = np.random.default_rng(seed + 1000)
    reps = []
    for _ in range(repeats):
        idx = rng.integers(0, len(world.cand_X), K)
        ys = rng.integers(0, 2, K)
        with L.Timer() as tf:
            for i, y in zip(idx, ys):
                L.hypothesis_loss_exact(state, world.cand_X[i], int(y))
        with L.Timer() as tl:
            for i, y in zip(idx, ys):
                L.hypothesis_loss_leaf(state, world.cand_X[i], int(y))
        with L.Timer() as tp:
            for _ in range(K):
                state.base.p1(world.V_X)
        reps.append(dict(full_wall=tf.wall / K, full_cpu=tf.cpu / K,
                         leaf_wall=tl.wall / K, leaf_cpu=tl.cpu / K,
                         predV_wall=tp.wall / K))
    med = float(np.median([r["full_wall"] for r in reps]))
    noisy = any(reps[i]["full_wall"] > CRIT["noisy_factor"] * med and
                reps[i + 1]["full_wall"] > CRIT["noisy_factor"] * med for i in range(len(reps) - 1))
    return dict(kind="timing", root=root, seed=seed, n_V=int(len(world.V_y)), n_V_requested=n_V,
                threads=threads, k_context=int(len(world.y_C)), repeats=repeats, K=K,
                base_fit_wall=t_base.wall, base_fit_cpu=t_base.cpu, reps=reps, noisy=noisy,
                data=world.meta.get("kind", "REAL"))


# =================================================================================================
# Tests (a)-(e)
# =================================================================================================
def unit_test_a(seed, n_cands) -> dict:
    """Sign / generality on a 2-class Gaussian task with known posterior (adversarial: candidates in sparse regions)."""
    rng = np.random.default_rng(seed + 11)
    mu = np.array([[-1.0, 0.0], [1.0, 0.0]])

    def draw(n):
        y = rng.integers(0, 2, n)
        return mu[y] + rng.normal(0, 1, (n, 2)), y

    X_C, y_C = draw(200)
    V_X, V_y = draw(10_000)
    pool, _ = draw(2000)
    d = np.sqrt(((pool[:, None, :] - X_C[None, :, :]) ** 2).sum(-1)).min(1)
    cand = pool[np.argsort(-d)[:n_cands]]
    state = L.EERState(L.LGBLearner(seed), X_C, y_C, None, V_X, V_y, None).prepare()
    gs = []
    for x in cand:
        p1 = 1.0 / (1.0 + np.exp(-2.0 * x[0]))     # true posterior: logit = (mu1-mu0).x = 2 x0
        gs.append(L.g_score(state, x, p_hat=np.array([1 - p1, p1])))
    gs = np.array(gs)
    frac = float((gs > 0).mean())
    ok = frac >= CRIT["a_frac_pos"] and gs.mean() > 0
    return dict(kind="test_a", seed=seed, n_cands=int(len(gs)), frac_pos=frac, mean_g=float(gs.mean()),
                sd_g=float(gs.std()), passed=bool(ok))


def unit_test_b(seed) -> dict:
    """Plumbing identities of g(x) with a mock learner (weighted logistic regression)."""
    rng = np.random.default_rng(seed + 22)
    X_C = rng.normal(0, 1, (120, 3))
    y_C = (X_C[:, 0] + 0.5 * rng.normal(0, 1, 120) > 0).astype(int)
    V_X = rng.normal(0, 1, (400, 3))
    V_y = (V_X[:, 0] + 0.5 * rng.normal(0, 1, 400) > 0).astype(int)
    V_w = rng.uniform(1, 8, 400)
    state = L.EERState(L.LRLearner(), X_C, y_C, None, V_X, V_y, V_w).prepare()
    cands = rng.normal(0, 1, (12, 3))
    tol = CRIT["b_tol"]
    res = {}
    # (i) zero-weight hypothetical row => g == 0
    res["i_zero_weight_max_abs_g"] = float(max(abs(L.g_score(state, x, p_hat=np.array([.5, .5]), w_new=0.0))
                                              for x in cands))
    # (ii) p_hat(y=1) = 0  => g equals the single-hypothesis difference for y = 0
    x = cands[0]
    g_dir = state.loss0 - L.hypothesis_loss_exact(state, x, 0)
    res["ii_abs_diff"] = abs(L.g_score(state, x, p_hat=np.array([1.0, 0.0])) - g_dir)
    # (iii) p_hat must sum to 1
    try:
        L.g_score(state, x, p_hat=np.array([0.5, 0.4]))
        res["iii_rejects_bad_phat"] = False
    except AssertionError:
        res["iii_rejects_bad_phat"] = True
    # (iv) candidate order must not matter
    g1 = np.array([L.g_score(state, c) for c in cands])
    perm = rng.permutation(len(cands))
    g2 = np.array([L.g_score(state, cands[p]) for p in perm])
    res["iv_perm_max_abs_diff"] = float(np.abs(g1[perm] - g2).max())
    ok = (res["i_zero_weight_max_abs_g"] <= tol and res["ii_abs_diff"] <= tol
          and res["iii_rejects_bad_phat"] and res["iv_perm_max_abs_diff"] <= tol)
    return dict(kind="test_b", seed=seed, learner="logreg_mock", tol=tol, passed=bool(ok), **res)


def unit_test_c(adapter, root, seed, n_cands) -> dict:
    """Leaf-refit approximation vs exact refit on a candidate subsample (outline L64 asks for this deviation report)."""
    world = get_world(adapter, root, seed, 90)
    state = L.EERState(L.LGBLearner(seed), world.X_C, world.y_C, None, world.V_X, world.V_y, world.V_w).prepare()
    rng = np.random.default_rng(seed + 33)
    idx = rng.choice(len(world.cand_X), size=min(n_cands, len(world.cand_X)), replace=False)
    ge, gl, te, tl = [], [], 0.0, 0.0
    for i in idx:
        x = world.cand_X[i]
        with L.Timer() as a:
            ge.append(L.g_score(state, x, method="exact"))
        with L.Timer() as b:
            gl.append(L.g_score(state, x, method="leaf"))
        te += a.wall
        tl += b.wall
    ge, gl = np.array(ge), np.array(gl)
    k = max(1, int(round(0.1 * len(ge))))
    rho, jac = L.spearman(ge, gl), L.jaccard_topk(ge, gl, k)
    ok = rho >= CRIT["c_rho"] and jac >= CRIT["c_jaccard"]
    return dict(kind="test_c", root=root, seed=seed, n_cands=int(len(ge)), topk=k, spearman=rho, jaccard_topk=jac,
                bias_mean_leaf_minus_exact=float((gl - ge).mean()), sd_exact=float(ge.std()),
                time_exact_per_cand=te / len(ge), time_leaf_per_cand=tl / len(ge), passed=bool(ok),
                data=world.meta.get("kind", "REAL"))


def unit_test_d(adapter, root, seed, n_cands, n_seeds) -> dict:
    """Determinism (same seed => identical predictions) and noise-to-signal of g across bagging seeds."""
    world = get_world(adapter, root, seed, 90)
    f1 = L.LGBLearner(seed).fit(world.X_C, world.y_C).p1(world.V_X)
    f2 = L.LGBLearner(seed).fit(world.X_C, world.y_C).p1(world.V_X)
    deterministic = bool(np.array_equal(f1, f2))
    rng = np.random.default_rng(seed + 44)
    idx = rng.choice(len(world.cand_X), size=min(n_cands, len(world.cand_X)), replace=False)
    G = np.zeros((n_seeds, len(idx)))
    for s in range(n_seeds):
        st = L.EERState(L.LGBLearner(seed * 1000 + s), world.X_C, world.y_C, None,
                        world.V_X, world.V_y, world.V_w).prepare()
        for j, i in enumerate(idx):
            G[s, j] = L.g_score(st, world.cand_X[i])
    noise = float(G.std(axis=0, ddof=1).mean())
    signal = float(G.mean(axis=0).std(ddof=1))
    ratio = noise / signal if signal > 0 else float("inf")
    ok = deterministic and ratio <= CRIT["d_ratio"]
    return dict(kind="test_d", root=root, seed=seed, n_cands=int(len(idx)), n_seeds=n_seeds,
                deterministic=deterministic, noise_sd_over_seeds=noise, signal_sd_over_cands=signal,
                ratio=ratio, passed=bool(ok), data=world.meta.get("kind", "REAL"))


def unit_test_e(seed, n_resample, n_sample) -> dict:
    """Is the 1/pi-weighted L_V from a stratified, over-sampled reserved sample unbiased? (Horvitz-Thompson vs self-normalised)"""
    rng = np.random.default_rng(seed + 55)
    N = 50_000
    s = rng.beta(0.6, 6.0, N)                       # model score of the whole day (known here)
    y = (rng.random(N) < np.clip(s * 1.2, 0, 1)).astype(int)
    ell = -(y * np.log(np.clip(s, L.EPS, 1)) + (1 - y) * np.log(np.clip(1 - s, L.EPS, 1)))
    truth = float(ell.mean())
    q = np.quantile(s, [0.5, 0.8, 0.95, 0.99])
    stratum = np.searchsorted(q, s)                 # 0..4, higher = higher score
    rel = np.array([1.0, 2.0, 4.0, 8.0, 16.0])[stratum]
    pi = np.minimum(1.0, rel * n_sample / rel.sum())
    ht, sn = [], []
    for _ in range(n_resample):
        keep = rng.random(N) < pi                   # Poisson sampling, independent inclusion
        if keep.sum() == 0:
            continue
        w = 1.0 / pi[keep]
        ht.append(float((w * ell[keep]).sum() / N))
        sn.append(float((w * ell[keep]).sum() / w.sum()))
    ht, sn = np.array(ht), np.array(sn)
    se = ht.std(ddof=1) / np.sqrt(len(ht))
    ok = abs(ht.mean() - truth) <= CRIT["e_se"] * se
    return dict(kind="test_e", seed=seed, n_resample=int(len(ht)), n_sample_expected=n_sample, truth=truth,
                ht_mean=float(ht.mean()), ht_se=float(se), ht_bias=float(ht.mean() - truth),
                selfnorm_mean=float(sn.mean()), selfnorm_bias=float(sn.mean() - truth), passed=bool(ok))


# =================================================================================================
# Unit enumeration, manifest, main loop
# =================================================================================================
def enumerate_units(a):
    units = []
    if a.stage in ("timing", "all"):
        for root in a.roots:
            for seed in a.seeds:
                for nv in V_SIZES:
                    for th in a.threads:
                        units.append((f"timing|{root}|s{seed}|V{nv}|t{th}", "timing", dict(root=root, seed=seed, n_V=nv, threads=th)))
    if a.stage in ("tests", "all"):
        for seed in a.seeds:
            units.append((f"test_a|s{seed}", "test_a", dict(seed=seed)))
            units.append((f"test_b|s{seed}", "test_b", dict(seed=seed)))
            units.append((f"test_e|s{seed}", "test_e", dict(seed=seed)))
            for root in a.roots:
                units.append((f"test_c|{root}|s{seed}", "test_c", dict(root=root, seed=seed)))
                units.append((f"test_d|{root}|s{seed}", "test_d", dict(root=root, seed=seed)))
    return units


def design_of(a) -> dict:
    return dict(stage=a.stage, roots=a.roots, seeds=a.seeds, threads=a.threads, repeats=a.repeats, K=a.K,
                a_cands=a.a_cands, c_cands=a.c_cands, d_cands=a.d_cands, d_seeds=a.d_seeds,
                e_resamples=a.e_resamples, e_sample=a.e_sample, scorer=a.scorer, adapter=a.adapter or "SYNTHETIC_STAND_IN",
                crit=CRIT)


def run_unit(a, adapter, kind, p):
    if kind == "timing":
        return unit_timing(adapter, p["root"], p["seed"], p["n_V"], p["threads"], a.repeats, a.K)
    if kind == "test_a":
        return unit_test_a(p["seed"], a.a_cands)
    if kind == "test_b":
        return unit_test_b(p["seed"])
    if kind == "test_c":
        return unit_test_c(adapter, p["root"], p["seed"], a.c_cands)
    if kind == "test_d":
        return unit_test_d(adapter, p["root"], p["seed"], a.d_cands, a.d_seeds)
    if kind == "test_e":
        return unit_test_e(p["seed"], a.e_resamples, a.e_sample)
    raise ValueError(kind)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", required=True, help="output directory (created; holds units.jsonl, version_log.jsonl, run_manifest.json)")
    ap.add_argument("--stage", choices=["timing", "tests", "all"], default="all")
    ap.add_argument("--roots", default="SYN1,SYN2", help="comma list. Default = synthetic stand-ins; real DEV roots need --adapter")
    ap.add_argument("--seeds", default="1,2,3")
    ap.add_argument("--threads", default="1", help="comma list of n_jobs for the timing grid, e.g. 1,4. Use 1 for the CPU-hour budget")
    ap.add_argument("--repeats", type=int, default=20)
    ap.add_argument("--K", type=int, default=20, help="hypotheses per timing repeat")
    ap.add_argument("--a-cands", dest="a_cands", type=int, default=100)
    ap.add_argument("--c-cands", dest="c_cands", type=int, default=300)
    ap.add_argument("--d-cands", dest="d_cands", type=int, default=100)
    ap.add_argument("--d-seeds", dest="d_seeds", type=int, default=10)
    ap.add_argument("--e-resamples", dest="e_resamples", type=int, default=200)
    ap.add_argument("--e-sample", dest="e_sample", type=int, default=60)
    ap.add_argument("--scorer", choices=["locked", "nobag"], default="locked",
                    help="LightGBM variant used for everything here. 'locked' = Bai 1 Table 2 (default). 'nobag' = no bagging/column sampling "
                         "(deviation from the lock, for diagnosing test d; needs NCS approval)")
    ap.add_argument("--adapter", default="", help="path to adapter module with load_world(root, seed, n_V)")
    ap.add_argument("--hw-note", default="", help="free text: CPU model / cores (NCS fills this)")
    ap.add_argument("--max-units", type=int, default=0, help="stop after N units this invocation (0 = no limit)")
    ap.add_argument("--dry-run", action="store_true", help="list units and exit")
    ap.add_argument("--accept-script-change", action="store_true", help="resume although script/design hashes differ (logged)")
    a = ap.parse_args()
    a.roots = [r for r in a.roots.split(",") if r]
    a.seeds = [int(s) for s in a.seeds.split(",") if s]
    a.threads = [int(t) for t in a.threads.split(",") if t]

    L.VARIANT["v"] = a.scorer
    units = enumerate_units(a)
    if a.dry_run:
        for uid, kind, _ in units:
            print(uid)
        print(f"{len(units)} units", file=sys.stderr)
        return 0

    os.makedirs(a.out, exist_ok=True)
    unit_path = os.path.join(a.out, "units.jsonl")
    vlog = os.path.join(a.out, "version_log.jsonl")
    man_path = os.path.join(a.out, "run_manifest.json")
    here = os.path.dirname(os.path.abspath(__file__))
    scripts = {n: L.sha256_file(os.path.join(here, n)) for n in ("run_p3b.py", "p3_lib.py")}
    if a.adapter:
        scripts["adapter"] = L.sha256_file(a.adapter)
    manifest = dict(created=now(), scripts=scripts, design=design_of(a), hw=hw_info(a.hw_note))

    resumed = os.path.exists(man_path)
    if resumed:
        old = json.load(open(man_path))
        changed = old["scripts"] != scripts or old["design"] != manifest["design"]
        if changed and not a.accept_script_change:
            print("REFUSING to resume: script hashes or design differ from run_manifest.json.\n"
                  "Re-run with --accept-script-change only if the change is deliberate (it will be logged).", file=sys.stderr)
            return 2
        if changed:
            append_jsonl(vlog, dict(ts=now(), event="script_or_design_change_accepted", old=old["scripts"], new=scripts,
                                    old_design=old["design"], new_design=manifest["design"]))
    else:
        json.dump(manifest, open(man_path, "w"), indent=1, sort_keys=True)
    done = {r["unit_id"] for r in read_jsonl(unit_path)}
    todo = [u for u in units if u[0] not in done]
    append_jsonl(vlog, dict(ts=now(), event="resume" if resumed else "start", n_units=len(units),
                            n_done=len(done & {u[0] for u in units}), n_todo=len(todo), scripts=scripts,
                            hw_note=a.hw_note))
    print(f"{len(units)} units, {len(units) - len(todo)} already done, {len(todo)} to do", file=sys.stderr)

    def handler(signum, frame):
        if STOP["flag"]:
            raise KeyboardInterrupt
        STOP["flag"] = True
        print("\nStop requested: finishing the current unit (Ctrl-C again to abort it; it will be redone).", file=sys.stderr)

    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGTERM, handler)
    adapter = load_adapter(a.adapter)
    n_run, reason = 0, "completed"
    for uid, kind, p in todo:
        if STOP["flag"]:
            reason = "stop_requested"
            break
        if a.max_units and n_run >= a.max_units:
            reason = "max_units"
            break
        t0 = time.perf_counter()
        try:
            res = run_unit(a, adapter, kind, p)
        except KeyboardInterrupt:
            reason = "aborted_mid_unit"
            break
        res.update(unit_id=uid, finished=now(), unit_wall_s=time.perf_counter() - t0)
        append_jsonl(unit_path, res)
        n_run += 1
        flag = "" if res.get("passed", True) else "  FAIL"
        print(f"[{n_run}/{len(todo)}] {uid}  {res['unit_wall_s']:.1f}s{flag}", file=sys.stderr)
        if res.get("noisy"):
            reason = "noisy_machine_stop_rule"
            print("STOP RULE: two consecutive repeats > 3x median (machine noisy). Fix the machine load and re-run.", file=sys.stderr)
            break
    append_jsonl(vlog, dict(ts=now(), event="stop", reason=reason, units_run=n_run))
    return 0


if __name__ == "__main__":
    sys.exit(main())
