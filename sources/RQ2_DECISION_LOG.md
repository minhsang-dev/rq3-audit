# RQ2 DECISION LOG — memory policy for TabFM/LightGBM context (Bài 2)
Version 2, 2026-11-03 (v2: composition audit NO-GO, Codex reproduction, corrections). Owner: NCS Nguyễn Minh Sang. Audience: any AI agent picking up RQ2 work.
**Read this file in full before proposing or running anything for RQ2.** It is the single record of what was tried,
what was decided and why. Results listed here count as observed evidence; never treat them as unobserved.

## 1. Status in one line
ThreeBin (original, V3, Soft90, lending DC-11) = **CLOSED_AT_DEV**. No method contribution from ThreeBin so far.
A new proposal (section 6) is OPEN, not approved, and must start from section 5's rules.

## 2. Fixed context (do not change without a new decision)
- Thesis outline v14.3-2710 is submitted; it names the three-bin policy for RQ2 and cannot be revised for 6 months.
- Contribution standard (2026-11-01): a real technical change (not a renaming); measurable benefit on at least one
  RQ-relevant criterion; fair comparison with on/off ablation; distinguishable from prior art; independent check after
  development. Process: baseline → DEV → error analysis → small change → retry → save every version → lock candidate
  → independent check. Labels: GO DEVELOPMENT / GO CONTRIBUTION CANDIDATE / GO CONFIRMATION / NO-GO (or CLOSED_AT_DEV).
- Protocol: Bài 1 replay L5 (score first, learn after), k = 2,000, locked LightGBM, CPU only for DEV.
  replay/data.py (L4/L5) SHA-256 e2407dfa2f2c1aaea020bf389ef1c33c7f01f85be45bd2ef52a076a129f3b21a;
  generator 7148f6e5…843c. A hash 0fc82bb5… (old L1/L2) is wrong if it appears.
- Endpoint: returning-family vs benign AUPRC_w at reintroduction days t = 5, 6 (AP = mean of the two).
- Comparators (T1 decision): tier A = CURE, CBRS_FAMILY, ECBRS; FIFO as floor.
- Working folder (Windows): D:\Personal\PhD\IUH\bai2_rq2. Outputs under a_cpu_runs\. Every folder has SHA256SUMS.

## 3. Data exposure (important for any future claim)
- DEV-CHECK used 9 recurring roots: ToN 2019-04-24, 25, 27, 28, 29; CIC 2018-02-21 and two other CIC roots
  (AP = 1 for all policies, uninformative). Informative roots = 6.
- ToN 2019-04-26 was seen in earlier runs (STEP 0d). There are **no unused development roots left**: every further DEV
  run on these data is DEV_REUSE and cannot count as evidence for a contribution.
- Independent-check pool E1 (PENDING, do not open for development): NF-UNSW-NB15-v3 2015-01-22 and 2015-02-18 qualify
  (02-18 carries prior RQ2 label exposure; 01-22 was used by a Bài 3 model run, ledger PENDING_E1). [v2: year corrected
  from 2018 to 2015.] BoT 2018-06-04 = EXCLUDE_NOT_EVALUABLE. UGR'16 is the outline's planned
  confirmation set (attack-day count not yet checked).

## 4. Evidence chain (chronological; details in each folder's report)
| Step | Folder / file | Result |
|---|---|---|
| T1 review | bai2_T1_decisions.md | REVISE: ThreeBin is an extension of DualFIFO/CURE; claimed parts = q_min*, trigger (only if ablation shows benefit), cluster fallback |
| T2 theory | bai2_T2_decisions.md | Prop. 1, q_min*, hybrid allocation k_F = max(w_F·k, G·q_min) done |
| T3 code | bai2_T3_review.md | GO DEVELOPMENT; synthetic demo shows retention, not benefit |
| STEP 0d | (ToN 2019-04-26) | trigger_off better than trigger on |
| ToN 24/04 telemetry | — | trigger helps overall AUPRC on that root only |
| Placebo A270 | — | trigger timing has no value (placebo ≈ real) |
| DEV-CHECK v1.2 | soft90_dev_check_v12\results (297 cells, parity PASS) | NO_GO_SOFT90. ThreeBin variants lose to CURE/CBRS_FAMILY on most informative roots (mean −0.03/−0.04). Family-aware memory beats FIFO on 8/9 roots (CURE − FIFO median +0.20) |
| Soft90 quick check | — | F identical in 165/189 pairs; acts only on reintro days (too late) |
| CURE diagnostic v1.1 | cure_failure_diagnostic_v11 (54 cells) | RETENTION_MECHANISM_NOT_SUPPORTED: CURE's edge is not explained by keeping more returning-family rows; entropy-gate rejection is the main removal route |
| Composition audit v1.2 | a_cpu_runs\rq2_final_memory_audit_v1_2 | MECHANISM_REQUIRES_PAPER_AUDIT: one signal: more benign / fewer other-attack rows ↔ higher AP; returning-family rows (V1) do not explain AP. Thin: 4 out-of-seed-spread pairs from 2 roots (ToN 25/04, 27/04) |
| Benign audit v1 | a_cpu_runs\rq2_threebin_benign_audit_v1 | Code: benign is not a group in F (threebin.py:143,312; adapter benign_group=False); benign lives only in R (≤1,000) and H (≤200). Strict ThreeBin context at end t=4 = 1,066–1,831 rows (not 2,000). S1 benign deficit 6/6 roots but SIZE_CONFOUND 12/12. S2 non-binding (design flaw of the criterion). Benign quota in F ≈ CBRS_FAMILY inside F → not novel |
| Prior probe | NO_GO_DC11_NEWEST_FIRST (sha256 596d41cd…b7; 1 seed, ToN, 2 days) | lending loses to random fill, size-matched strict, CURE, CBRS_FAMILY |
| Size diagnostic v1 | a_cpu_runs\rq2_threebin_size_diag_v1 | **CLOSED_AT_DEV.** Lending (dev_t3_dc11\threebin_dc11.py, sha256 876df7ab…d339) fills context to 2,000; parity lending=False vs locked A1 18/18 exact. W1 lending − CURE median −0.0108; W2 lending − CBRS_FAMILY −0.0354; L lending − strict −0.0076. Not a win under the DEV-CHECK rule. A5–A8 NOT_AVAILABLE (locked worker requires k = 2000). Deviation recorded: adapter "validator view" (true_* fields hold real values) |

## 5. Lessons that bind future RQ2 work
1. **The bottleneck is on the benign side**, not on keeping returning-family rows. Mechanisms that only protect attack
   families (family quota, q_min floor, trigger) did not help on the endpoint. Any new design must state how it treats
   benign rows.
2. **Never compare a policy that leaves slots empty against baselines that use full k.** Check actual context size per
   day for every arm first.
3. **Do not design a criterion that is capped by the quantity it is meant to test** (S2 of the benign audit).
4. **Trigger timing has shown no value** (placebo, STEP 0d, Soft90). Do not reopen trigger variants without new
   evidence.
5. **No robust complementarity between baselines.** [v2 correction] CBRS_FAMILY beats CURE robustly only on ToN 04-27
   (R = 4.0, same sign in 3/3 seeds). CURE's apparent wins (ToN 04-25 +0.011, R = 0.20; CIC 02-21 +0.036, R = 0.12,
   driven by one seed) are within seed spread. ToN 04-24, 04-27, 04-29 are near ceiling or tied. CBRS_FAMILY is the
   baseline to build on.
6. Locked runner/worker accepts only k = 2,000 and 11 known arms. New arms need a runner copy with a recorded diff;
   locked files are never edited.
7. Every new run: hash script before running, run once, append-only version_log.jsonl, report all roots/seeds/arms.

## 6. CLOSED proposal: "ThreeBin as a composition of best baselines" — NO-GO (paper audit, 2026-11-03)
Folder a_cpu_runs\rq2_composition_paper_audit_v1 (COMPOSITION_AUDIT.md). C-1 (CURE with entropy-rejected rows
re-sampled family-balanced) DISTINGUISHABLE_WEAK but no robust component advantage; C-2 (FIFO + long CBRS_FAMILY) and
C-3 (C-1 with ECBRS) not distinguishable from their parts. Code note: runtime gamma = 1.0 (earlier files said 0.5).
Original conditions kept below for reference.
Idea (NCS): keep the physical three-bin structure; each bin runs the baseline algorithm that measures best for its
role; the composition is the method contribution. Bin algorithms must be chosen by measurement, not assumed.
Conditions any agent must respect before running it (see the assessment in the session of 2026-11-03):
- It counts only if the composite beats **each of its component baselines run alone at full k** (CURE, CBRS_FAMILY,
  ECBRS), under the DEV-CHECK rule, and each bin's contribution is shown by ablation (replace that bin's algorithm by
  FIFO, or merge the bin away). A composite that only lands between its components is NO-GO.
- Prior art to address: CURE and DualFIFO are already two-bin compositions; hybrid / partitioned buffers in continual
  learning. The novelty claim must name what the composition does that none of its parts does.
- Bin capacities and the candidate set are fixed by a written rule before any run (no grid search on DEV roots);
  at most 3 predeclared compositions.
- All DEV roots are exposed: development results are DEV_REUSE. GO CONTRIBUTION CANDIDATE needs a locked version and
  an independent check on unexposed data (E1 / UGR'16).
- Benign handling must be explicit (lesson 1).

## 7. Additional records (v2)
- Codex independent reproduction of composition audit v1.2: same decision and counts (11 material, 7 within spread,
  4 outside from ToN 04-25/04-27; ten-row 10 cells, mean AP 0.644). Codex screened one direction only, so V3 FAIL
  there vs inverse PASS here; consistent given dV4 = 0.
- Confirmation data status: UGR'16 has 13 root-days meeting the Bài 1 recurring label rule (2016-07-28 to 08-09),
  but they are one network with daily injected attacks = ONE cluster, not 13 independent units. Raw flows are not
  on disk (site returned 403 to the agent); NetFlow-v3 46-feature schema does not match UGR'16 CSV. Practical status
  for any RQ2 confirmation: HOLD_DATA until raw data and a common feature schema exist.
- Campus access log (DS1) considered and set aside by the NCS (2026-11-03).
- Dataset choice rule (NCS, 2026-11-03): the only hard constraint is no fabricated data; choosing datasets/settings
  favourable to the proposed model is allowed. Claims must state the scope actually measured.
- Next candidate (proposed, not approved): "hard-benign bin" on top of unchanged CBRS_FAMILY: H holds benign rows the
  current model scores near the threshold / previously flagged, k-center for diversity; total k = 2,000; ablations:
  H random benign, H hardness without k-center; baseline alone at full k. Prior art: hard-negative mining, CURE
  entropy gate, uncertainty-based replay.

## 8. Hard-benign bin (HB) — DEV results (2026-11-03)
- HB v1 (a_cpu_runs\rq2_hard_benign_dev_v1): CBRS_FAMILY locked + H = 200 benign rows chosen by model attack score
  (top 400) + k-center. SIGNAL by locked rule but thin (M1 median +0.0048; 2 roots within seed spread). k-center did not
  help (HB_NOKC >= HB) -> HB2 = hardness top-k only, chosen after seeing v1 on the same roots (recorded).
- Seed extension (a_cpu_runs\rq2_hard_benign_seedext_v1; SEED_EXTENSION, guard override in memory, DEV only; path-identity
  and parity PASS; 66 locked files unchanged): 10 seeds x 6 roots. ROBUST_SIGNAL by fixed rule.
  M1 = HB2 - CBRS_FAMILY median: ToN 04-25 +0.0299 (10/10 seeds +), ToN 04-28 +0.0283 (8/10), ToN 04-27 +0.0015 (10/10,
  near ceiling), CIC 02-21 +0.0930 (6/10, SD ~0.31), ToN 04-24 -0.0046 (2/10), ToN 04-29 -0.0001 (4/10).
  A1 = HB2 - HB_RANDOM: ToN 04-25 +0.030 (9/10), ToN 04-28 +0.015 (8/10). No harm flag. R < 1 on every root (unpaired SD).
- Status: GO DEVELOPMENT -> candidate for locking. Not a contribution candidate until an independent check on data not
  used to develop HB.
- Confirmation data notes: UGR'16 is a poor fit for HB: 'background' is unlabelled (contamination would make "hard
  benign" select mislabelled attacks), common schema 9/46 features (~6 independent), one cluster, ~236 GB. Prefer
  clean-benign sources with the Bài 1 schema (NF-UNSW-NB15-v3) or an existing cache (CIDDS-001, not used for RQ2).
- CURE τ note (2026-11-03): τ is the entropy threshold for entry to CURE's long bank (cure_ref/cure.py:274). Bài 1
  locked τ = 0.1 (grid on ToN 04-24..26). Every RQ2 CURE cell (A270 config: DEV-CHECK, size_diag, HB, seedext) used
  τ = 0.5; reason not documented. RQ2 conclusions "vs CURE" therefore refer to CURE τ = 0.5, not the Bài 1-locked CURE.
  HB2 decisions use CBRS_FAMILY and HB_RANDOM, so they are unaffected. Confirmation adds CURE τ = 0.1 as a reference arm.
- HB2 locked: a_cpu_runs\rq2_hb2_lock_v1 (LOCK_HB2.json sha 9d8f6d49…1612). Eligible confirmation roots:
  NF-UNSW-NB15-v3 2015-01-22 (EXPOSED_OTHER), 2015-02-18 (EXPOSED_RQ2); CIDDS-001-internal 03-15, 16, 17, 20, 21, 23, 24
  (EXPOSED_OTHER). ~2 independent clusters. Decision READY_TO_PREREGISTER.

## 9. HB2 preregistered confirmation (LightGBM, CPU) — 2026-11-04
- Prereg v1.1 sha 4449de16…64e8 (v1 bc3033ac…; v1.1 changed only the CPU cap 6 → 12 h before any run). Runner
  run_conf_v1_1.py. 540/540 cells COMPLETE, 0 failed, 7,922 s wall. Folder a_cpu_runs\rq2_hb2_conf_prereg_v1.
- Label: SUPPORTED_ONE (CIDDS-001-internal).
  CIDDS-001 (7 roots, all evaluable): M1 = HB2 − CBRS_FAMILY median > 0 on 7/7 roots; root medians 03-15 +0.0096 (8/10),
  03-16 +0.0004 (6/10), 03-17 +0.0168 (9/10), 03-20 +0.0178 (9/10), 03-21 +0.0050 (8/10), 03-23 +0.0116 (8/10),
  03-24 +0.0686 (8/10); median of roots +0.0116. A1 = HB2 − HB_RANDOM > 0 on 7/7 roots (≥ 8/10 seeds on 6). SUPPORT met
  via 03-17 and 03-20. No harm (overall AUPRC_w deltas ≈ 1e-4).
  NF-UNSW-NB15-v3 2015-01-22: NO_SUPPORT; all three decision arms median AP 0.974 (M1 = 0), near ceiling.
  Sensitivity UNSW 2015-02-18 (EXPOSED_RQ2): M1 +0.0014 (5/10), A1 +0.0095 (6/10); not in decision.
- Status per prereg item 9: GO CONTRIBUTION CANDIDATE, LightGBM scope, claim limited to CIDDS-001 (one environment,
  EXPOSED_OTHER, 19 features); DEV signal on ToN 04-25/04-28. Next: TabFM phase addendum (GPU), prior-art positioning.

## 10. HB2 post-confirmation audits (2026-11-04)
- Duplicate/weighting audit (a_cpu_runs\rq2_hb2_dup_audit_v1; one pre-outcome parser fix, NCS-approved rerun):
  NOT_COMPUTABLE — BASE/H row ids and per-row H scores were not logged. Reference arms (descriptive): HB2 > CURE τ=0.1
  on 7/7 CIDDS roots (median +0.003..+0.055), > CURE τ=0.5 and > FIFO on 7/7; UNSW 01-22 all arms 0.974.
  Next (proposed): telemetry-only rerun with identity gate; de-dup ablation only if confounded/mixed.
- Novelty audit (cloud): NARROW_REQUIRED. Closest: UGSR, HCIL, MADAR, Tab-AICL, GRASP, MES/BAEP; none ranks only the
  benign class by attack score in a bounded memory. Contribution narrowed to "class-directed adaptation of
  hard-negative retention ... evaluated on roots not used for development" (manuscript v0.2).
