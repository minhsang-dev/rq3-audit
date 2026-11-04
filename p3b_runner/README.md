# p3b_runner — P3b (cost) + g(x) correctness tests (a)–(e)

Design source: `../05_FUTURE_PROBES.md` (P3b and "Kiểm thử độ đúng của g(x)"). Order approved by NCS: **P3b → tests (a)–(e) → P3a (τ = 0 first) → P3c.** This folder covers the first two steps only. CPU only; no GPU.

## What is here
| File | Role |
|---|---|
| `p3_lib.py` | Locked LightGBM (Bài 1 Bảng 2), weighted log-loss, naive EER `g(x)` of (2-6) — exact refit and leaf-refit variants — and stand-in data |
| `run_p3b.py` | Resumable runner. Units = (root, seed, grid point). Appends each finished unit to `units.jsonl` (fsync) |
| `summarize_p3b.py` | Writes `P3B_SUMMARY.md` (timing tables, daily-cost table, P3b rule outcome, test table) |
| `adapter_real_TEMPLATE.py` | Where the REAL DEV roots plug in (`--adapter your_adapter.py`) |

## Run (NCS machine)
```bash
pip install lightgbm numpy scipy scikit-learn        # tested with lightgbm 4.7.0, numpy 2.5.4, scipy 1.18.1, scikit-learn 1.9.1
python run_p3b.py --out runs/p3b_v1 --adapter my_adapter.py --roots ToN_2019-04-25,CIC_2018-02-21 \
       --seeds 1,2,3 --threads 1 --hw-note "CPU model, cores, RAM"      # P3b timing + tests (a)-(e)
python summarize_p3b.py runs/p3b_v1
```
* `--dry-run` lists the units. `--stage timing|tests|all`.
* **Resume**: run the same command again; finished units are skipped. Ctrl-C (or `kill`) finishes the current unit and stops; a hard kill loses only the unit in progress. `--max-units N` runs N units per invocation.
* The runner **refuses to resume** if `run_p3b.py`/`p3_lib.py`/adapter hashes or the design (roots, seeds, grid, criteria) changed; `--accept-script-change` overrides and logs it in `version_log.jsonl` (RQ2 log lesson 7).
* Use `--threads 1` for the CPU-hour budget (Q18); add e.g. `--threads 1,4` only to learn the scaling.
* **Hardware:** the manifest records `/proc/cpuinfo` model, core count and library versions. `--hw-note` is the free-text field NCS fills.

## What the tests check (criteria are constants in `run_p3b.py`, not CLI options)
| Test | Check | Pass |
|---|---|---|
| a | sign of g on a 2-class Gaussian task with known posterior, candidates in sparse regions | ≥ 90 % g > 0 and mean g > 0 |
| b | plumbing with a mock logistic-regression learner: zero-weight row ⇒ g = 0; p̂(y)=0 hypothesis drops out; Σp̂ = 1 enforced; candidate order irrelevant | all within 1e-8 |
| c | leaf-refit vs exact g on a candidate subsample | Spearman ≥ 0.9 and top-10 % Jaccard ≥ 0.7 |
| d | same seed ⇒ identical predictions; mean SD of g over bagging seeds / SD of g over candidates | deterministic and ratio ≤ 0.5 |
| e | 1/π-weighted L_V from a stratified over-sampled reserved sample is unbiased (Horvitz–Thompson) | \|bias\| ≤ 2 SE |

Why test b uses a mock learner: for LightGBM a zero-weight row is not guaranteed neutral (bagging draws, `min_child_samples` count rows, not weights).

## Known limits — read before trusting any number
1. **Default data is a SYNTHETIC STAND-IN.** The locked replay code (`replay/data.py`, SHA-256 `e2407dfa…3b21a`) and the DEV roots are not in this repository. Every record says `SYNTHETIC_STAND_IN` and the summary refuses to call it a verdict. Real P3b needs the adapter; DEV roots only (never CIDDS/UNSW/UGR'16).
2. `deterministic=True`, `force_row_wise=True` are added to the locked LightGBM parameters to remove nondeterminism (no hyper-parameter change). This is a **recorded diff** against the locked worker.
3. `--scorer nobag` (no bagging/column sampling) exists only to diagnose test d. It deviates from the lock and is recorded in the manifest; do not use it for the real run without NCS approval.
4. `Booster.refit` (leaf refit) is taken from the installed LightGBM 4.7.0 API (`decay_rate=0`: new leaf values only). Its suitability as the outline's "refit lá" is exactly what test c measures.
5. The naive g(x) adds the hypothetical row to C with no eviction and no HB2 admission (Q17).

## Smoke test done in the cloud session (code check only; stand-in data; 4 shared vCPU; NOT evidence)
* Resume works (run stopped after 4 units with `--max-units 4`, second invocation ran the remaining 4); a changed design (`--seeds`) is refused.
* Timing on the stand-in, 1 thread, k = 2000, 46 features: full refit ≈ 0.75 s per hypothesis (Bài 1 quoted ≈ 0.1 s — different hardware; do not use this box's number), leaf refit ≈ 0.05 s, predict V ≈ 0.001–0.008 s.
* Tests with the **locked** scorer on one stand-in seed with small candidate counts: b, e PASS; **a, c, d FAIL** (a: 40 % positive; c: Spearman 0.21, top-k Jaccard 0; d: noise/signal 1.6). With `--scorer nobag`: d passes trivially (no randomness), a and c still FAIL (a: 30 % positive; c: Spearman −0.02).
* Side check (scratch, not in the runner): on the Gaussian task, a logistic-regression learner gives 65–95 % positive g and the locked LightGBM 85–90 % with sparse candidates, but with random candidates the LightGBM share ranged 2–70 % across draws of C. So the code path is sound (b passes, LR behaves), and test a's outcome depends strongly on the draw of the 200-row context. The sample sizes here are tiny (15–40 candidates, 1 seed); the real run uses the declared sizes (a: 100, c: 300, d: 100 × 10 seeds) and several seeds. Criteria were not changed.
