# THESIS AUDIT LOG — RQ3 / RQ4 paper audits and outline-revision items
Version 1, 2026-11-04. Owner: NCS Nguyễn Minh Sang. Audience: any AI agent working on RQ3, RQ4, the thesis outline
or the review essay. **Read in full before proposing anything for RQ3/RQ4.** Companion of `RQ2_DECISION_LOG.md`.

Authority: outline v14.3-2710 (50 refs), submitted, NOT amended. Nothing here changes it; items in §5 are a revision
list for the window ~6 months after submission. Verbatim outline excerpts: `outline_v14_3_RQ3_RQ4_verbatim.txt`,
`outline_v14_3_noidung5.txt`, `outline_v14_3_overview_KT.txt`, `outline_v14_3_references.txt`.
Labels: PROVED (paper proof, needs independent check) / DECISION (NCS) / PROPOSAL (not approved) / OPEN.

## 1. Status
| Item | State |
|---|---|
| RQ4 paper audit (cloud, branch `claude/bo-sung-truoc-g0-bxzb3w`) | CLOSED: G0–G4 approved 2026-11-04 (files 00–06) |
| RQ4 experiments | HOLD until RQ3 DEV + NCS approval |
| H4a / H4b | NO CONCLUSION |
| Proposition 2 | ASSUMPTION GAP / COUNTEREXAMPLE (as written) |
| RQ3 paper audit (cloud) | CLOSED: G0–G5 approved 2026-11-04. Prereg option (a): primary family m ≤ 3 cells, chosen after P3a on DEV roots, before any confirmation root is touched; P3a must not use the roots reserved for confirmation |
| RQ3 DEV probes | design only; run locally after approval |
| H3 | NO CONCLUSION |

## 2. RQ4 decisions (D1–D14 and G2)
- D1 ASR: ASR_raw = FNR (1 − recall) of the target family at the Definition 6 threshold λ_t; ASR_excess =
  FNR_attacked − FNR_clean (same trace, no defence). Report both. H4a's "50 % relative reduction" read on ASR_excess
  (PROPOSAL, fix in prereg). If ASR_excess without defence ≤ 0 or too small: RR undefined → HOLD_ASSUMPTION.
  Diagnostic variant ASR_excess_matched allowed.
- D2 DoP spec missing → G2 run DoP-independent; f* and β HOLD.
- D3 Time order: RQ3 selects unlabelled rows → labels arrive after τ → RQ4 filter → HB2 loads. "lọc → chọn → nạp" is
  read functionally (RQ3's g(x) uses the filtered context).
- D4 The b daily labels are split across K simulated sources (each = one analyst); a source sees only its rows.
- D5 Outline: no change now; prepare options only.
- D8 UNCERTAIN sources: primary U1 (rows not auto-held; go through the row tier); U2 as sensitivity.
- D9 Honest-source noise: primary 0; one random-noise level as sensitivity, fixed in prereg (PROPOSAL).
- D10 V_t and D_cal come from the K sources' reserved η·b labels, unflagged sources only (outline Nội dung 3).
- D11 Attack (iv) flips target-family rows; daily flip rate = detection threshold − δ; δ HOLD until DoP spec.
- D12 Attacks (iii)/(v): attacker-trained surrogate (level K1: data it legitimately sees; no deployed-model weights or
  queries) — clarification of Definition 5, not an amendment.
- D13 Main H4a/H4b grid in mode A (exchangeable). Mode B (subnet): honest-only false-flag rate + attack (ii) secondary.
- D14 PROPOSAL: K ∈ {5, 10}; m ∈ {1, 2} (K=5), {1, 2, 4} (K=10); breakpoint curve m = 0..K−1; final after probe P4b
  (rows per source per day = b/K drives audit power).
- G2-1 Reading of f = R1 (flip rate over the source's labels of the day). R2 rejected (not observable by the audit).
- G2-2 Source flags: PROPOSAL primary = persistent until run end or verification, with retroactive hold of the
  source's rows in context, V_t and D_cal; non-retroactive as sensitivity. Conflicts with assumption A4 of RQ2 prop1
  (already OPEN there).
- G2-3 Reserved η·b labels: conservative — compromised sources flip them at the same rate (attacker cannot tell them
  apart).

- G3 approved 2026-11-04 (file 04_BASELINE_AND_NOVELTY.md; D15–D17 in 01_REQUIREMENT_TRACE.md §G):
  B1 = "RONI (Nelson-protocol adaptation)"; ART RONIDefense = reference only (5 differences; if used as-is, name
  "ART-RONI"). Oracle-clean V_t = diagnostic only, never in H4a/H4b decisions. Tuning: ≤ 12 configs on DEV for EVERY
  arm incl. S2/S3 (same budget). I_i: primary on TabFM; LightGBM with leaf-refit approximation as secondary, labelled
  approximate. Cost flag (extrapolation from Bài 1 coefficients, not measured): exact I_i on TabFM at b = 1,000 ≈ 800
  context re-runs/day ≈ 1+ GPU-h/day → needs an approximation (batch/group removal or scoring only rows of unflagged
  sources) decided in G4. "Better than RONI" margin for H4a: not fixed; set after P4a, before prereg. Bib: koh2022 →
  koh2021 (Machine Learning 2021); add mahloujifar2018multiparty, ezrielev2025patent (patent).
- G3 novelty: GAP_NARROW kept; theory (2′) low novelty, not the anchor; candidate anchor = source→row combination for
  tabular ICL context + defence-aware attacker + NIDS with delayed labels, conditional on P4a showing material harm.

- G4 approved 2026-11-04 (05_RQ3_INTERFACE_AND_FUTURE_GATES.md, 06_DECISION_MEMO.md; D18–D23 in 01 §H). RQ4 paper
  audit CLOSED (00–06). Q-G4-1: decide H4a per attack type (ii), (iii) separately; claim states which pass; "H4a fully
  supported" only if both. Q-G4-2: common daily inference cap B_pass for all arms accepted in principle, value after
  P4d; reduced-iteration B1 must be named. Q-G4-3: primary = HELD rows not verified in-run (excluded; report false-hold
  rate), no extra labels; variant = verification consumes labels from b, never extra labels. Q-G4-4: macro-F1 at λ_t,
  as H3. Q-G4-5: allowed variant HB2-R (removal hook + row telemetry) separate from LOCK_HB2; regression test: with no
  removals HB2-R output bit-identical to HB2; conflict with A4 of RQ2 prop1 stays OPEN. Statistics: Wilcoxon/HL by root
  day as primary (consistent with RQ2, RQ3 Q15 and revision item 4); mixed model only as sensitivity. P4a "material
  harm": CI over root days of ASR_excess excludes 0 AND median ≥ 2×SD seed noise. Proofs in 03 need an independent check
  (separate agent) before citation. Blockers: RQ3 DEV trace, DoP spec, P4d cost measurement.

- RQ4 D24–D30 applied by agent (01, 05, 06). Confirmed 2026-11-04: D29 (Wilcoxon/HL primary) is a declared deviation
  from v14.3 Nội dung 1 → kept as outline option O7 (= §5 item 4 here). Seed SD for D30 = within-root SD of ASR_excess
  across seeds, pooled over roots by root-mean-square. Tests one-sided in the preregistered direction (as RQ3 Q15);
  roots needed: 1/2^n < α/m for the declared family. False-hold rate of clean rows = primary reported metric (flags are
  persistent and HELD rows are excluded). HB2-R telemetry must not consume RNG nor reorder operations.

- D31–D34 recorded by RQ4 agent. P4a criterion (a) = one-sided Hodges–Lehmann lower confidence bound (level 1 − α)
  of ASR_excess over root days > 0, consistent with D34. Root-count rule 1/2^n < α/m binds the confirmatory family
  only; DEV probes (P3a–c, P4a–d) use uncorrected p, Holm descriptive (as RQ3 G4).

## 3. RQ4 findings (paper; DEV needed where marked)
- PROVED: rows of compromised sources in context ≤ min(k, m·s) (quota bound; no f).
- COUNTEREXAMPLE: m·s → m·f·s. One day: 10 flips of 1,000 labels (1 % < f = 0.2) can fill s = 10 slots. Accumulation:
  K=5, b=1,000 (200 labels/source/day), attacker (iv) flips just under threshold daily; if retention favours flipped
  rows, a source fills s = 400 in ~10–13 days; with m = 2, ρ = 40 % vs 8 % from (2-8).
- PROVED: without independence only P(all audits succeed) ≥ 1 − mβ (example m=2, β=0.1: 0.80 not 0.81); multi-day
  audits with non-persistent flags need 1 − mWβ (W = 13 makes the guarantee vacuous).
- PROVED (fixed rows, label-only flips): kNN certificate holds, but at k = 2,000, m·f·s = 160 needs vote margin ≥ 321 →
  rarely active. Not transferable to TabFM; label-dependent context needs cascade counting. [49] tie-break: check G3.
- Collusion (vi): per-source cap keeps the quota bound only, not the f factor.
- Proposition 2′ (CANDIDATE, requires proposal approval): cap s on each source's eligible pool (whole batches accepted
  by the audit), any retention allowed; guarantee 1 − |A_aud|·β'. Counting argument, low novelty; changes the loading
  design.
- Mode B identifiability lemma: if a source's feature region does not overlap any other source, "honest" and "flipped"
  worlds are observationally identical → UNCERTAIN is the correct output; f*, β meaningless without overlap.
- Mode A ceiling: attacker controls at most ~m/K of the target-family labels → attack may be too weak (probe P4a).
- Cross-RQ risk (inference, DEV needed): attack (ii) creates labelled-benign high-attack-score rows, exactly what HB2's
  H bin keeps → RQ4 must filter before HB2 loads. Outline Nội dung 5 already anticipates this interaction.
- D_cal risk: attack→benign flips in D_cal raise λ_t → FNR rises even with a clean context; the source tier must
  protect D_cal and V_t, not only C_t.
- V_t circularity: I_i signal shrinks ~ (1 − 2m/K), flips sign at m = K/2 (conjecture, DEV needed).
- Prior art (cloud task, 38 works + [34] Vejling, [35] Xu): GAP_NARROW — no source tier + row tier + per-source cap for
  tabular in-context models, no Prop-2-type bound, no adaptive attacker on this pairing. DoP was judged NO-GO for
  novelty (2026-10-24/25) → RQ4 novelty must rest on the combination, the (corrected) bound and adaptive evaluation.
  Key threats: Koh et al. (defence-aware attacks break row sanitizers), Miao et al. (disguise vs peer audit), RONI weak
  on focused attacks, Bilos et al. 2026 (TabFM hub-poison damage only −3–4 pp), AndroVenom (Deep k-NN hurt GBT −20 % TPR).

## 4. RQ3 decisions (Q1–Q14)
- Q1 Exposure primary E3 (flow-level, normalised, IPW), E1 (family time-to-first-detection) secondary; align with [2]
  Botacin & Gomes 2025 once opened (PROPOSAL). Q2 unit = days. Q3 clock resets at each appearance episode (first +
  each reappearance after ≥ 3 days absent) (PROPOSAL). Q4 flow detected if score ≥ λ_t on its evaluation day;
  never-detected capped at window end, censored share reported.
- Q5 F1-macro = 2 classes at λ_t; family metrics separate. Q6 binary → entropy/margin/least-confidence rank identically;
  use margin from the arm's own model; LightGBM-scored uncertainty for TabFM arm only as sensitivity; [30] separate arm.
- Q7 functional reading of "lọc → chọn → nạp". Q8 labels arriving end of day t used from day t+1 only.
- Q9 no-filter branch: V_t = reserved labels from all sources (compromised included).
- Q10 reserved η·b split 50/50 V_t/D_cal, seeded, disjoint; W_V = 3 (PROPOSAL). New assumption A6: at b = 100,
  D_cal is tiny and the α_eff floor (~8 %) may make threshold-dependent metrics too coarse.
- Q11 scenario replay: reserved rows from CAL part (stratified by arm model's score, 1/π); strategy picks from POLICY
  part only. Q12 pseudo-labels: BASE only, never HB2's H; ≤ 10 % of k; replaced on arrival; none for predicted-benign
  rows in drift regions. Q13 scenario replay (roles separated). Q14 staleness = mean and max age of V_t; reported only.
- Q15 (PROPOSAL) H3 decided per cell (b, τ, filter on/off): F1 supported if median over root days of ΔF1 ≥ ε₃ and
  one-sided Wilcoxon p < 0.05 (Holm over cells); exposure "lower" = one-sided test ΔE < 0, no margin (outline gives
  none), HL estimate + CI reported. Claim states exactly which cells pass; no pooled verdict, no mixed model.
- Q16 V_t membership by arrival day (last W_V days of arrivals; otherwise empty at τ = 7); reported age = t − query
  (observation) day.
- Q17 Primary g(x) = naive (2-6) as written; diagnostic: share of selected rows actually loaded by HB2 within W days;
  HB2-aware variant only as DEV if that share is low (PROPOSAL).
- Q18 Pseudo-labels only for rows already queried and awaiting labels, replaced on arrival; drift region = feature-only
  kNN distance to context above the 95th percentile of D_cal distances (PROPOSAL). Budget (PROPOSAL): selection cost per
  simulated day ≤ 1 GPU-hour (TabFM) / ≤ 1 CPU-hour (LightGBM); total experiment budget fixed after P3b, before prereg.
- G2 approved 2026-11-04 → G3 (web allowed; only opened sources count as VERIFIED).
- G3 approved 2026-11-04 (04_BASELINE_AND_NOVELTY.md, RQ3_REFS.bib): novelty GAP_NARROW; EER-for-LightGBM is a
  baseline, not a contribution; candidate contribution = EER on ICL context + delayed labels + HB2 + exposure, only if
  P3a passes at matched cost. Q19 density baseline = GMM selection stage of NetGuard only, named "NetGuard-style density
  selection (no generation)". Q20 (PROPOSAL) STRAL and [30] mapped to b/day by a shared banking rule: unspent b' carries
  over, daily spend cap 3b', total labels over the run equal to other arms; η·b reserve fixed every day; report daily
  spend. STRAL: ADWIN (δ = 0.002, 2,000-event grace) decides spending days, hybrid near-threshold + high-score pick.
  [30]: RandVarUncertainty, budget fraction b'/|U_t|, arrival order, stop at b'. Q21 cite the arXiv version actually
  read (stamp on PDF page 1). Q22 GAP_NARROW wording accepted for the audit; before writing any contribution claim:
  extended search + NCS downloads Botacin & Gomes [2], Pham et al. 2022, Žliobaitė et al. 2014 via library access.
- G4 (RQ3) approved 2026-11-04 (05_FUTURE_PROBES.md): P3b (~2 CPU-h) → g(x) correctness tests (a)–(e) → P3a
  (~74 CPU-h; arms R, U, U_c, EER_c; b 100/300 × τ 0/1; 6 roots × 5 seeds) → P3c (~67 CPU-h, τ = 7, b = 300).
  Versions read: NetGuard v3, STRAL v2, Tab-AICL v1, Castellani v2, Cacciarelli v4.
  Findings: (1) Q15 Holm rule unattainable with 6 roots (min one-sided Wilcoxon p = 1/2^n; 1/64 > 0.05/4) — error in
  my Q15 proposal. DEV probes: uncorrected p as criterion, Holm descriptive. Main study must pick in prereg: Holm over a
  small predeclared primary family, or enough roots (n ≥ log2(m/0.05): 18 cells need ≥ 9 roots). (2) τ = 7 needs label
  warm-up: Q23 allowed — labelled pre-stream history for initial context, identical for all arms; warm-up τ + 2 days
  excluded from evaluation. (3) TabFM EER under 1 GPU-h/day is nearly non-selective at b ≥ 300 (extrapolation):
  decide after real GPU measurement (with P4d) between raising the cap (allowed; report cost) and a two-stage shortlist
  (U_c arm controls the shortlist effect). Q24 same cap for all arms, actual spend reported, no forced equal spend.
  Q25 L_V = log-loss weighted 1/π (0-1 as sensitivity); N_c = 10·b′ and U_c accepted. Q26 informative root = random arm
  F1-macro < 0.95, computed from the random arm only, fixed before EER results, excluded roots reported.
- Bài 1 source for protocol/cost: v4.2 (438d5b44…) or its clean copy (e25f39ee…), same content minus comments.

## 5. Outline v14.3 revision list (for the window ~6 months after submission; nothing changed now)
1. Drop CIDDS-001 as secondary confirmation set (now also used as RQ2 HB2 confirmation; exposure).
2. Avoid H2 name clash (Bài 1 renamed to PC1).
3. ε₁ = 0.02 only for Bài 1's preliminary H1; Chapter 6 uses ε₁ from the two-criteria rule.
4. Statistics of Nội dung 1: Wilcoxon/HL by root day instead of mixed model.
5. Plan more root days for H2 power.
6. Check UGR'16 attack days — now: UGR'16 unsuitable as main confirmation set ('background' unlabelled; 9/46 common
   features, ~6 independent; one cluster).
7. RQ2/H2: rewrite for HB2 (ThreeBin evaluated, negative with diagnosis); fix ε₂ (HB2 median ~0.012 < planned 0.03);
   add the 10 % label-noise test; fix the order RQ3 → labels → RQ4 filter → HB2 load.
8. Proposition 2 (RQ4): wrong as written (§3); replace by the quota bound m·s or Proposition 2′; union bound instead
   of (1−β)^m unless independence is assumed and justified.
9. ASR definition direction (use target-family FNR; 50 % on attack-induced excess).
10. Notation f vs f* in Proposition 2.
11. Source tier must protect D_cal and V_t, not only the context.
12. Citation fixes: [10] Google blog does not state the 10-class / 500-feature limits or the licence attributed to it;
    [16] authors Grinsztajn et al. (not "Prior Labs"); [19], [20] cite journal versions (Comput. Secur. 156, 104510;
    IEEE Access 12:144489–144508); [40] DOI 10.1109/rivf55975.2022.10013926; [41] year 2025; [44] IEEE IoT-J
    10(10):8578–8589, 2023; [46] vol./no. unverified; KT4 add bilos2026 (context manipulation without defence).
13. H3 (RQ3 G5, options S1–S6, unapproved): S1 small predeclared primary family (m ≤ 3); S2 EER approximated by
    candidate sampling, two-stage EER for TabFM; S3 formal definitions of exposure E3, F1-macro, ℒ_V, V_t; S5 at b = 100
    report AUPRC_w and recall at fixed false alerts, or drop the cell from the primary family. ε₃ not relaxed.
14. Root-day supply: confirmation roots must be disjoint from DEV roots; current CIDDS (7, one environment) + UNSW (2)
    are not enough for 18 cells → add root days/datasets before the main RQ3/RQ4 study.
15. KT3 wording: "EER chưa được khảo sát cho TFM" → "chưa thấy trong phạm vi đã tìm"; cite Tab-AICL and
    Castellani 2022 as closest prior work.
