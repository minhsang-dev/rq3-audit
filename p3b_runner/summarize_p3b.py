#!/usr/bin/env python3
"""summarize_p3b.py -- read <out>/units.jsonl and write <out>/P3B_SUMMARY.md.
Applies the P3b rule fixed in 05_FUTURE_PROBES.md (no other thresholds):
  GO    : median time per hypothesis (full refit, 1 thread, |V|=90) <= 0.3 s AND EER_c at N_c=10b' for b=300 <= 1 CPU-h/day
  HOLD  : 0.3 s < t <= 1 s  (reduce N_c or use leaf refit; state the new N_c/b')
  NO-GO : t > 1 s, or even leaf refit cannot bring b=300 under 1 CPU-h/day at N_c >= 3b'
Prints the g(x) test table (a)-(e). Data marked SYNTHETIC_STAND_IN can never produce a P3b verdict.
"""
import json
import os
import sys
from collections import defaultdict

import numpy as np

CAP_H = 1.0     # CPU-hours per simulated day (Q18)


def load(path):
    out = []
    for line in open(path):
        line = line.strip()
        if line:
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return out


def q(v, p):
    return float(np.percentile(v, p)) if len(v) else float("nan")


def main(outdir):
    rows = load(os.path.join(outdir, "units.jsonl"))
    man = json.load(open(os.path.join(outdir, "run_manifest.json")))
    timing = [r for r in rows if r["kind"] == "timing"]
    tests = [r for r in rows if r["kind"].startswith("test_")]
    stand_in = any(r.get("data") == "SYNTHETIC_STAND_IN" for r in timing + tests)
    L = ["# P3B_SUMMARY (auto-generated)", ""]
    if stand_in:
        L += ["> **DATA = SYNTHETIC STAND-IN.** This verifies the code only. It is NOT P3b evidence and cannot yield a verdict.", ""]
    L += [f"- units done: timing {len(timing)}, tests {len(tests)}",
          f"- hardware: {json.dumps(man['hw'])}", ""]

    # ---- timing ----
    g = defaultdict(lambda: defaultdict(list))
    for r in timing:
        key = (r["n_V_requested"], r["threads"])
        for rep in r["reps"]:
            g[key]["full_wall"].append(rep["full_wall"]); g[key]["full_cpu"].append(rep["full_cpu"])
            g[key]["leaf_wall"].append(rep["leaf_wall"]); g[key]["leaf_cpu"].append(rep["leaf_cpu"])
            g[key]["predV"].append(rep["predV_wall"])
    L += ["## Time per hypothesis (seconds; median [IQR] over repeats x roots x seeds)", "",
          "| |V| | threads | full refit wall | full refit CPU | leaf refit wall | predict V | n |",
          "|---|---|---|---|---|---|---|"]
    med = {}
    for key in sorted(g):
        d = g[key]
        f = lambda k: f"{np.median(d[k]):.4f} [{q(d[k],25):.4f}-{q(d[k],75):.4f}]"
        med[key] = (float(np.median(d["full_wall"])), float(np.median(d["leaf_wall"])))
        L.append(f"| {key[0]} | {key[1]} | {f('full_wall')} | {f('full_cpu')} | {f('leaf_wall')} | {f('predV')} | {len(d['full_wall'])} |")
    L += ["", "## Daily EER cost = 2 * N_c * t  (CPU-hours/day, 1 thread, full refit, |V| from Q10)", "",
          "| b | b' | N_c=10b' | |V| | CPU-h/day | under 1 CPU-h? |", "|---|---|---|---|---|---|"]
    verdict = "INCONCLUSIVE (no 1-thread |V|=90 timing yet)"
    for b, nv in ((100, 30), (300, 90), (1000, 300)):
        bp, nc = int(0.8 * b), int(8 * b)
        if (nv, 1) in med:
            t = med[(nv, 1)][0]
            h = 2 * nc * t / 3600
            L.append(f"| {b} | {bp} | {nc} | {nv} | {h:.3f} | {'yes' if h <= CAP_H else 'NO'} |")
    if (90, 1) in med:
        tf, tl = med[(90, 1)]
        h300 = 2 * 2400 * tf / 3600
        if tf <= 0.3 and h300 <= CAP_H:
            verdict = "GO (PROVISIONAL, DEV)"
        elif tf <= 1.0:
            verdict = "HOLD: reduce N_c (state new N_c/b') or use leaf refit"
        else:
            h_leaf = 2 * 3 * 240 * tl / 3600
            verdict = "NO-GO (A2 'LightGBM feasible' falsified on DEV)" if h_leaf > CAP_H else "HOLD: only leaf refit fits the cap"
        L += ["", f"Max N_c under 1 CPU-h/day at |V|=90: {int(3600/(2*tf))} (full refit), {int(3600/(2*tl))} (leaf refit)."]
    L += ["", f"**P3b rule outcome: {verdict}**" + ("  <- stand-in data: not a verdict" if stand_in else ""), ""]

    # ---- tests ----
    L += ["## g(x) correctness tests (a)-(e)", "", "| test | unit | key numbers | passed |", "|---|---|---|---|"]
    for r in sorted(tests, key=lambda r: r["unit_id"]):
        keys = {"test_a": ("frac_pos", "mean_g"), "test_b": ("i_zero_weight_max_abs_g", "ii_abs_diff", "iii_rejects_bad_phat", "iv_perm_max_abs_diff"),
                "test_c": ("spearman", "jaccard_topk", "bias_mean_leaf_minus_exact"), "test_d": ("deterministic", "ratio"),
                "test_e": ("ht_bias", "ht_se", "selfnorm_bias")}[r["kind"]]
        num = ", ".join(f"{k}={r[k]:.4g}" if isinstance(r[k], float) else f"{k}={r[k]}" for k in keys)
        L.append(f"| {r['kind']} | {r['unit_id']} | {num} | {'PASS' if r['passed'] else '**FAIL**'} |")
    allp = all(r["passed"] for r in tests) if tests else None
    L += ["", f"All tests passed: {allp}. Any FAIL = stop P3a/P3c, fix the implementation, do not change the criteria (05 section 0)."]
    open(os.path.join(outdir, "P3B_SUMMARY.md"), "w").write("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main(sys.argv[1])
