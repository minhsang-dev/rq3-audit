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
| RQ4 paper audit (cloud, branch `claude/bo-sung-truoc-g0-bxzb3w`) | G0, G1, G2 done (DoP-independent); G3 next |
| RQ4 experiments | HOLD until RQ3 DEV + NCS approval |
| H4a / H4b | NO CONCLUSION |
| Proposition 2 | ASSUMPTION GAP / COUNTEREXAMPLE (as written) |
| RQ3 paper audit (cloud) | G0, G1 done; Q1–Q14 answered; G2 next |
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
