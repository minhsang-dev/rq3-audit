# Tabular Foundation Models versus LightGBM for NetFlow Intrusion Detection under Label Budgets and Drift: Consistent Gains, Day-Dependent Size, and Inflated Random-Split Estimates

Nguyễn Minh Sang¹, [co-authors and affiliations: to be inserted]

¹ Industrial University of Ho Chi Minh City, Vietnam



## Abstract

Tabular foundation models (TabFMs) classify new rows by reading a set of labelled rows as context, so an intrusion detector built on them can be updated by changing its context instead of retraining. We compare TabFM with LightGBM retrained daily on exactly the same context, under a leakage-controlled replay protocol that scores each NetFlow day before learning from it, limits labels to a daily budget with a reserved calibration share, and draws evaluation, policy and calibration rows from disjoint pools. In controlled-drift replay of 16 root days of NF-ToN-IoT-v3 and NF-CICIDS2018-v3 (378 evaluable days, no technical failure), TabFM ranked attacks better than LightGBM on 15 of 16 root days (Hodges–Lehmann difference +0.0098 AUPRC_w, 95 % CI [+0.003, +0.023]; exact Wilcoxon p = 3 × 10⁻⁵ against no difference; the preregistered practical-superiority criterion, a lower bound of at least 0.02, was not met), and the direction was the same under all four context policies tested (FIFO, DualFIFO, CBRS, CURE). Gains were large where LightGBM struggled: on a rare attack family (0.776 vs 0.371) and, in chronological replay of 14 real days, on CICIDS2018 days where LightGBM trained on earlier days ranked poorly — on 2018-02-20, TabFM reached 0.958 against 0.237 for LightGBM. Across real days the gain varied from −0.09 to +0.72, with a mean of +0.18 on CICIDS2018 and about zero on ToN-IoT. On the same evaluation rows, a conventional random split whose labelled context may include later flows raised mean AUPRC_w from 0.640 to 0.831 for TabFM and from 0.540 to 0.799 for LightGBM, so random-split evaluations describe a much easier task than day-by-day operation. A preregistered exploratory check on CIDDS-001 had too few evaluable days to be assessed. There, the chronologically fed LightGBM could not be trained on two of eight attack days because its context held no attack after attack-free days; in this setting, the random-split evaluation did not expose this one-class-context training failure. TabFM needed 58 GPU-seconds per day on an NVIDIA L4, against 0.36 CPU-seconds for LightGBM. The primary analysis and the prespecified addenda were locked before their respective results were examined; the CIDDS-001 untrainability analysis was explicitly post hoc. The real-day analyses are descriptive, and the H1 data are development data of two networks. The protocol, generator, policies, analyses and outputs are released with their hashes.

**Keywords:** network intrusion detection; NetFlow; tabular foundation model; in-context learning; concept drift; label budget; evaluation protocol; data leakage; preregistration

## 1. Introduction

A network intrusion detector that is trained once and left alone degrades. Hosts change their behaviour over the week and attack tools change [1], [2], [3]; the share of malicious flows also varies between days. The usual remedy is periodic retraining, which needs a fresh labelled sample. In a security operations centre, labels arrive slowly, in small numbers, and mostly for traffic that was already flagged [4].

Tabular foundation models change the form of this problem. TabPFN [5], TabICL [6] and TabFM [7] are transformers pre-trained on synthetic tables. At inference time they read a set of labelled rows as context and return class probabilities for new rows in one forward pass, without gradient steps. Updating such a model after drift means changing its context. If a few thousand labelled flows suffice to keep detection quality close to that of retraining, the update is cheap in labels, although not necessarily in compute [8].

In earlier work on the same NetFlow data [9], we compared TabFM context refresh with LightGBM retraining across day-to-day transitions. Two lessons from that study shape this one. First, the comparison that isolates the model class is the one in which LightGBM is trained on exactly the rows TabFM sees. Against this matched baseline, the macro-F1 advantage of TabFM was much smaller and could not be distinguished from zero under day-level inference. Second, the conclusion depended on the unit of inference: seed-level intervals looked decisive, while day-level intervals did not [10], [9]. That study also left three operational conditions uncontrolled:
- its labelled samples were stratified with ground-truth labels instead of being drawn under a daily label budget;
- labels were available immediately;
- the drift between consecutive days mixed every kind of change, so no result could be attributed to a particular kind of shift.

Several existing methods manage a bounded TabFM context on streams. Lourenço et al. [11] showed that a TabFM with a dual short-term/long-term memory (DualFIFO) can be an effective stream learner. Lee et al. [12] proposed CURE, which admits rows to the long-term memory by predictive entropy and evicts redundant rows. Class-balancing memories such as CBRS [13] come from continual learning. CURE was evaluated by prequential accuracy on general-purpose streams, with the context updated after every labelled example [12]. We are not aware of an evaluation of these policies that includes a daily label budget, a label delay, a separate calibration set for the alarm threshold, or network traffic. Studies of drift and labelling in security examine retrained classifiers rather than context management [14], [15], [16], [17]. Evaluations of TabFMs for intrusion detection have used random or stratified splits [18].

**What this paper is and is not.** We do not propose a new context selector; FIFO, DualFIFO, CBRS and CURE already exist and are used here as published or as close re-implementations. The contributions are:

1. **A leakage-controlled replay protocol with a label budget and label delay.** Each day of a NetFlow stream is scored before any of its labels are used ("score first, learn after"). Labels are queried under a budget *b*. A share η is reserved for a calibration set D_cal that no context policy sees. Labels can arrive after a delay τ. All context policies share one interface, and every policy and model scores the same evaluation rows. Section 3.2 states exactly which isolation properties the code guarantees in each replay mode and which it does not.
2. **A controlled-drift generator with disjoint pools.** Each real day is split once into disjoint evaluation, policy and calibration pools. Feature, class-prior and recurring-family drift is injected by weighted resampling within each pool, and every scenario is fixed in a hashed manifest.
3. **A preregistered, data-matched comparison of TabFM and LightGBM, with cost.** Both models receive the same context and the same evaluation rows on every day. Root days are the unit of inference. The hypothesis, decision rule, analysis script and missing-data rules were locked before the main run, and every deviation is reported. GPU and CPU seconds are recorded for every evaluated day, and the main run is governed by a cumulative compute budget with a pre-stated stop rule.
4. **A paired comparison of evaluation protocols on real days (descriptive).** On the same evaluation rows of 14 real days, we compare chronological replay with the conventional random split, whose labelled data are drawn from all days. Both analyses were fixed in addenda before the primary analysis was run.

In brief: TabFM beat LightGBM on almost every root day and under every context policy, but by a typical margin of about 0.01 AUPRC_w, below the conservative 0.02 we had preregistered. The size of the gain depends strongly on the day. It reached 0.4 on a rare attack family and 0.72 on a real CICIDS2018 day, and it was about zero on most ToN-IoT days. A random split, on the same evaluation rows, made the task look much easier for both models (mean AUPRC_w 0.640 → 0.831 for TabFM, 0.540 → 0.799 for LightGBM). On CIDDS-001, an independent check had too few evaluable days to be assessed. In this setting, random-split evaluation did not expose the one-class-context training failure observed under chronological replay.

The H1 test is preregistered, but it is run on development data that were also used for hyperparameter tuning, the cost pilot and the blinded variance pilot. It is therefore a preregistered test on development data, not an independent confirmation; confirmation of H1a on data not yet used is planned for later work . CIDDS-001 is no longer unused: it served the exploratory check of Section 4.11, and any later use of it must disclose this.

Section 2 reviews related work. Section 3 defines the protocol, Section 4 the experimental design (including the real-day addenda, Section 4.10) and Section 5 the locked analysis. Section 6 reports the results, Section 7 discusses them and their limitations, and Section 8 lists the deviations.

## 2. Related work

**Tabular foundation models.** TabPFN v2 [5] showed that a transformer pre-trained on synthetic tables can match tuned gradient boosting on small tabular tasks. TabICL [6] and TabICLv2 [19] scaled in-context learning to larger tables. TabFM [7] is a model of the same family, released as software with pretrained weights and described in a separate technical report [43]. Helli et al. [20] trained an in-context learner on priors that encode temporal shift; there the shift is modelled during pre-training rather than handled by changing the context. A hardware-oriented benchmark of TabPFN and TabICL documents their memory and latency cost [8].

**Context management for TabFMs on streams.** Lourenço et al. [11] used TabFMs as stream learners with a short-term FIFO memory whose overflow enters a long-term memory; on long-term overflow, the oldest row of the over-represented class is removed. Lee et al. [12] (CURE) keep the same two banks. They gate admission to the long bank by each row's normalised predictive entropy and evict one endpoint of the closest same-class pair within the most represented class. Their backbone is TabICLv2 [19], and they report prequential accuracy on seven streams, one of them synthetic, with a context budget of 1,000 rows . Chrysakis and Moens [13] proposed class-balancing reservoir sampling (CBRS) for online continual learning from imbalanced streams. We use these policies as comparators and do not modify their selection rules, except for the source of CURE's entropy (Section 3.5, DEV-005).

**Drift, labels and leakage in security.** TESSERACT [14] showed that ignoring time in train/test splits inflates malware-detection results. Arp et al. [15] list data snooping, including temporal snooping, and inappropriate baselines among common pitfalls of machine learning in security. INSOMNIA [16] studied concept drift in network intrusion detection and the labelling cost of model updates. Botacin and Gomes [17] showed that label delays change the conclusions of malware-detection evaluations. Žliobaitė [21] and Grzenda et al. [22] studied change detection and evaluation when labels arrive late. The prequential ("test-then-train") scheme of Gama et al. [23] is the basis of our score-then-learn order. Shyaa et al. [3] survey drift-aware intrusion detection.

**Data.** The NetFlow v3 datasets [24], [25] attach flow timestamps to the NetFlow v3 feature set [24], which extends the standard feature sets of [26] and makes day-level replay possible. They are derived from the ToN_IoT [27] and CSE-CIC-IDS2018 captures documented by the Canadian Institute for Cybersecurity [28]. The label errors documented for CSE-CIC-IDS2018 [30] apply to any conclusion drawn from them; for its predecessor CIC-IDS-2017 see [29].

**Evaluation practice.** Bouthillier et al. [10] showed that seed variation understates benchmark variance when other sources of variation are ignored. Preregistration separates confirmatory from exploratory analyses [31], and has been proposed for machine learning [32] and NLP [33]. Blinded variance estimates for sample-size review follow the internal-pilot literature [34], [35]. Our decision rule uses the Wilcoxon signed-rank test [36], the Hodges–Lehmann estimator with its exact rank-based bound [37], and the sign test [38]. The dependence check uses the moving-block bootstrap [39], [40].

## 3. Protocol

### 3.1 Day timeline: score first, learn after

A stream is a sequence of days. The first day of a run is warm-up; evaluation starts on the second day . For every day *t*:

1. **Score.** Day *t* is scored with the context and the calibration set D_cal built from labels that arrived before the end of day *t* − 1.
2. **Query.** At the end of day *t*, *b* labels are queried from day *t*. Which rows are eligible depends on the replay mode (Section 3.2).
3. **Reserve.** A share η of the queried labels is reserved for D_cal and is never shown to a context policy. The remaining (1 − η)·*b* go to the policy.
4. **Arrive.** All queried labels arrive at the end of day *t* + τ and are usable from day *t* + τ + 1: on day *t* + 1 for τ = 0, *t* + 2 for τ = 1, *t* + 8 for τ = 7 . Policy rows are passed to `policy.update(context, new_labelled_rows, unlabelled_stream)`, which returns a context of at most *k* rows . Reserved rows join D_cal.

D_cal pools the reserved labels that arrived in the last W_V = 3 days, keeping at most the newest 5,000 rows . In this paper all of η·*b* goes to D_cal (`split_vt = False`) .

### 3.2 Sampling and isolation: what is and is not guaranteed

Every row carries an identity `rid`, the global index of its source flow in the dataset; a row read from a synthetic day carries the `rid` of the root-day flow it was resampled from . The replay checks three conditions on these identities :

- **I1.** When day *t* is scored, no `rid` of its evaluation sample is in the context or in D_cal.
- **I2.** After every policy update, the context holds at most *k* rows, no row that was ever reserved for D_cal, and only rows that were given to that policy with the same `rid`, label and features. This also stops a policy that reads the unlabelled stream (CURE may) from inserting unlabelled, fabricated or reserved rows. I2 is always checked and cannot be switched off.
- **I3.** At arrival, no `rid` is both reserved for D_cal and given to the policy, cumulatively over the run.

The guarantees differ between the two replay modes.

**(a) Real-day replay (used for LightGBM and τ_CURE tuning in Section 4.4 and chronological replay in DEV-011).**  The evaluation sample of day *t* is drawn from all rows of the day. At the end of the day, *b* labels are queried uniformly at random without replacement from all rows of the day, and the evaluation sample is not removed from this query pool. Removing it would take every flow of the rare families, which the sample keeps in full, out of the labelled data for good . Score-then-learn guarantees that an evaluation row of day *t* is not in the context or D_cal when day *t* is scored. I1 is asserted on every scored day; this is condition 3′ of the code audit . A row evaluated on day *t* can be queried at the end of day *t* and then serve as a context or D_cal row from day *t* + 1 on. The stricter condition that an evaluation row is never reused later therefore does not hold in this mode, by design. Real days hold distinct flows, so no flow is evaluated on two days, and I3 holds by construction (asserted).

**(b) Scenario replay (all pilot and H1 runs).**  Each root day is split once, stratified by label and attack family, into three disjoint pools: EVAL, POLICY and CAL . A synthetic day has three parts, each resampled with replacement from its own pool . The evaluation sample is drawn only from the evaluation part, policy labels only from the policy part, and D_cal labels only from the calibration part. The unlabelled stream passed to the policy contains only policy and calibration rows . Each root flow therefore has exactly one role for a whole chain: a flow used for evaluation is never labelled, and a labelled flow is never evaluated. This is stronger than condition 3′. Within its role, however, a root flow is not used only once:
- because synthetic days resample with replacement, the same root flow can appear on several days of a chain;
- it can appear more than once within one day's part; the evaluation sample draws positions without replacement, so repeated positions can hold the same flow ;
- a policy or calibration flow can be labelled more than once, on the same day or on different days, so the context and D_cal can hold several copies of one flow. I2 accepts such copies because each is a row the policy was given ;
- an evaluation flow can be evaluated on several days of a chain.

The replay runs in `filter` mode with zero tolerated drops: any row that would violate I1 (against that day's evaluation identities) or I3 stops the run . A completed scenario run therefore shows that I1–I3 held on every day of every chain. The disjoint pools make this hold by construction; the filter confirms it for the actual run.

**What these checks do not show.** The identity checks concern flow identities only. In scenario replay, evaluation and labelled flows come from the same root day, the same network and, for the most part, the same hours. A scenario therefore measures detection of held-out flows of a root day under injected drift, not prediction of a later real day. Near-duplicate flows with different identities are not detected by any check. The code and its audits support no stronger or weaker claim about leakage than the properties above.

### 3.3 Controlled drift

**Synthetic sequences.** A scenario is a short sequence of synthetic days built from one real *root day* by seeded resampling, with drift weights that change over the days. The days of a chain differ in two ways: by the injected drift, and by sampling variation, because each synthetic day is a new random resample of the same pools. Real changes between days, such as new hosts, new attack tools or schedule effects, are not present within a chain. They enter the study only through the differences between the 16 root days. Scenarios built from the same root day are correlated, so the root day, not the scenario, is the independent unit .

**Pools.** Rare families (fewer than 1 % of the day's attack flows) are split 50/50 between the evaluation pool and the stream pool (policy + calibration). Every other stratum sends 0.35 of its flows to the evaluation pool . The value 0.35 is the smallest multiple of 0.05 that gives the smallest root day (329,487 flows) an evaluation pool of at least 100,000 rows . The stream pool is split again: a share η = 0.2 goes to CAL and the rest to POLICY . A synthetic day has an evaluation part of 200,000 rows from the evaluation pool. Its policy and calibration parts have at most 200,000 rows together, 20 % of them from CAL .

**Kinds of drift** :

- *Feature shift.* Two unchanged days, then three days in which each row is resampled with weight exp(β · mean_j(s_j · z_j)). Here z_j is the rank of feature *j* rescaled to [−1, 1] and s_j is a random sign. The grid is |J| ∈ {1, 2, 3} features × β ∈ {0.5, 1, 2, 3}. Features are drawn from columns with at least 20 distinct values in a 100,000-row sample of the root day.
- *Class-prior shift.* Two unchanged days, then three days in which the attack odds are multiplied by λ ∈ {1/8, 1/4, 1/2, 2, 4, 8}. The attack-family temper is 0 or 0.5; 0.5 is used only if the root day has at least 2 attack families.
- *Recurring family.* Two unchanged days, then *d* ∈ {3, 4, 5} days without attack family *f*, then 2 days with *f* again. Generated only when the root day has at least 2 attack families with at least 1,000 flows each.

Drift weights are computed within each pool, so all three parts of a day carry the same kind and intensity of drift . At most 10 scenarios per kind and root day are drawn without replacement from the grid cells, with a seed derived from the dataset, root day and kind. *Rare* and *recurring* were defined before any run: a family is rare if it has fewer than 1 % of the day's attack flows, and recurring if it is absent for at least 3 days .

**Manifest.** For every scenario, the manifest stores its root day, kind, parameters and seed. Rows are rebuilt deterministically, and the stream adapter refuses to build a stream whose pools do not match the pool hashes in the manifest . The generator (SHA-256 7148f6e5…843c) and the manifest (SHA-256 207817c6…ed08) were hashed before any model was run on any scenario . The manifest holds 363 scenarios (160 feature, 140 prior, 63 recurring) with 2,004 synthetic days . A first version of the generator drew all parts of a synthetic day from the whole root day and could not guarantee I1 and I3. It was replaced before any model run (DEV-001, Section 8) .

### 3.4 Context policies

All policies implement `update(context, new_labelled_rows, unlabelled_stream) → context` with |context| ≤ *k* .

- **FIFO.** Keeps the newest *k* labelled rows.
- **DualFIFO** [11], [12]. A short FIFO bank holds the newest B_S = round(ρ*k*) rows and a long bank holds B_L = *k* − B_S rows, with ρ = 0.75 as in the CURE paper . Short-bank overflow enters the long bank without a gate. When the long bank overflows, the oldest long-bank row of the most represented class is removed. We follow the DualFIFO paragraph of App. B.1 ("Controlled Policy Variants") of the CURE paper . Ties between equally represented classes go to the largest label, as in the reference code . With *k* = 2,000, B_S = 1,500 and B_L = 500 .
- **CBRS** [13]. Class-balancing reservoir sampling, with the binary label as the class. While the memory is not full, every row is stored. After that:
  - a row of a class that is not *full* overwrites a random row of the currently largest class;
  - a row of a full class replaces a random stored row of its own class with probability m_c/n_c, and is otherwise ignored.

  A class becomes full when it is, or has been, the largest class, and it stays full. Fullness is evaluated only after the memory is filled. Under this reading the paper's Property 1 holds, and the paper's supplement (Lemma A.1) supports it .
- **CURE** [12]. The same two banks as DualFIFO.
  - *Admission.* A short-bank overflow candidate enters the long bank while the long bank is not yet full (warm-fill). After that, it enters only if its stored normalised predictive entropy is at least τ_CURE; otherwise it is discarded.
  - *Eviction.* When the long bank overflows, CURE takes the most represented class and finds its closest pair of long-bank rows in z-scored feature space. It removes the endpoint farther from the centroid of that class's short-bank rows .
  - *Entropy.* A row's entropy is computed once, on the day the row is queried, by the model conditioned on that day's context, and is stored with the row. A row without a prediction gets entropy 0: this happens when the context has fewer than 2 rows or fewer than 2 classes, or when the row falls within the 100-arrival warm-up . In this paper the locked LightGBM computes the entropy for both models, so that TabFM and LightGBM are compared on the same context (DEV-005). CURE as published uses the entropy of its own TabFM backbone .
  - *Threshold.* τ_CURE was selected on the grid {0.1, …, 0.5} with the locked LightGBM in real-day replay (Section 4.4)  and is 0.1 (the lowest grid value).

The harness also contains CBRS-family (CBRS with the attack family as the class). It is not part of the H1 design .

| Policy | Source | Reproduction check |
|---|---|---|
| FIFO | Written for this protocol | Unit test (newest *k*, order)  |
| DualFIFO | Re-implemented from [12], App. B.1 (no official code) | Hand-worked unit test; same retained rows as the reference DualFIFO after every batch for *k* ∈ {4, 10, 40, 100} × 3 seeds  |
| CBRS | Re-implemented from [13], Alg. 1 (no official code found) | Reference implementation, synthetic streams: Property 1 held in all 12,000 Monte Carlo runs with 0 violations, and Property 2 (uniform within-class subset) passed . On a Fig. 1-like stream (class sizes partly assumed), classes 0 and 2 were stored whole and the other three balanced, as in the paper's figure. The *m* = 255 perfect-balance remark was also reproduced . The harness CBRS was slot-by-slot IDENTICAL to the reference on 7 streams × 30 seeds (*m* = 1,000, batch 10), and a negative control (fill-phase variant) was detected as DIFFERENT . |
| CURE | Copy of a reference implementation that follows the official code (commit f7c6b2f), wrapped in the harness interface | Reference vs official `CUREMemoryPolicy`: 0 mismatching steps out of 10,500 over 4 configurations . Reference test suite 20/20; the adapter returns the same rows as the reference  |

*Table 1. Context policies, sources and reproduction checks. The CBRS and CURE checks are made at the level of the memory policy; no classifier-accuracy result of the original papers was reproduced* .

### 3.5 Models

A model receives the context and a set of query rows and returns an attack score in [0, 1] . TabFM [7] uses the context as in-context examples. LightGBM [41] uses the same context as its training buffer and is retrained every day with locked hyperparameters (Section 4.4). FIFO, DualFIFO and CBRS never read model output, and CURE's gate is driven by the locked LightGBM for both arms (DEV-005). Both models therefore see exactly the same context on every evaluated day, and they score exactly the same evaluation rows . Because the context is computed once with LightGBM in the loop, the CURE comparison measures the two models under a LightGBM-gated CURE context. It does not measure CURE as it would run with TabFM.

### 3.6 Metrics and thresholds

**Evaluation sample.** On every evaluated day, the protocol draws a sample of 10,000 rows, stratified by attack family. It keeps every row of the rare families, and each row carries the weight 1/π, the inverse of its inclusion probability . In scenario replay the sample is drawn from the evaluation part of the synthetic day, so the weights refer to that part . The same sample is used for every policy and model.

**Primary metric.** The primary metric is AUPRC weighted by 1/π (AUPRC_w). The sample over-represents rare families, so only the weighted AUPRC estimates the AUPRC of the day .

**Threshold rule (A_FP), as defined by the protocol.** The protocol sets the operating threshold from a false-alarm budget A_FP, in false alarms per day. For evaluated day *t* :
1. N̂_t = (number of flows of the real root day) × (benign share of D_cal);
2. α_t = A_FP / N̂_t;
3. α_eff = max(α_t, 5 / n_benign_cal), and days where the floor applies are flagged;
4. the threshold is the (1 − α_eff) quantile of the benign D_cal scores.

**Not used for the H1 comparison (DEV-010).** The threshold needs each model's scores on the D_cal rows. In the main run, TabFM scored only the evaluation rows. Scoring the D_cal rows as well would have cost about one more GPU-hour, and this was declined . Threshold metrics and per-family recall are therefore not reported for the TabFM–LightGBM comparison. They are replaced by a descriptive per-family AUPRC_w, fixed before any H1 result was seen (Section 5.5). Even if D_cal had been scored, A_FP = 1,000 alarms per day  could not have been met with a D_cal of about 1,200 rows: the 5 / n_benign_cal floor binds .

## 4. Experimental design

### 4.1 Data and root days

Only development data are used: NF-ToN-IoT-v3 and NF-CICIDS2018-v3 [24], [25] . The v3 paper calls them NF3-ToN-IoT and NF3-CSE-CIC-IDS2018 . Both have 46 numeric features . Days are UTC days of the flow start time with at least 100,000 flows .
- NF-ToN-IoT-v3 contributes 7 consecutive root days, 2019-04-23 to 2019-04-29.
- NF-CICIDS2018-v3 has 10 valid days between 2018-02-14 and 2018-03-02. 2018-02-23 has no attack flow: it stays in the stream but is not a root day. This leaves 9 root days .

In total R = 16 root days . They range from 329,487 to 6,373,074 flows . Rare families occur on one root day only: 2018-02-21 (LOIC-UDP, 0.33 % of attack flows) .

The same development data were used for three things before the main run:
- tuning LightGBM and τ_CURE, on four NF-ToN-IoT-v3 days that are also root days (Section 4.4);
- the cost pilot;
- the blinded variance pilot, on feature scenarios of all 16 root days (Section 4.6).

UGR'16 is not opened in this paper. CIDDS-001 was opened only for the exploratory check of Section 4.11, after the H1 analyses, and played no part in tuning or in H1 .

### 4.2 Units, chains and outcomes

A *chain* is one scenario replayed with one policy and one seed. One scenario per kind and root day is used (scenario index 0, S = 1). The primary analysis therefore contains 16 feature chains, 16 prior chains and 10 recurring chains . Recurring chains exist for 6 ToN-IoT and 4 CICIDS2018 root days. The other 6 root days do not have two attack families with at least 1,000 flows each . Feature and prior chains have 5 days, of which 4 are evaluated. Recurring chains have 2 + *d* + 2 days, of which 7 are evaluated on average (*d* = 4) .

On every evaluated day, d = AUPRC_w(TabFM) − AUPRC_w(LightGBM), computed on the same evaluation rows. A chain outcome is the mean of d over its evaluable days, and a root-day outcome x is the mean over its chains . With S = 1 and one seed there is one chain per kind and root day, so each available kind contributes equally to x .

### 4.3 Fixed settings

| Item | Value |
|---|---|
| Label budget *b*; reservation η | 2,000 labels per day; 0.2, all to D_cal  |
| Context size *k*; label delay τ | 2,000; 0 days  |
| D_cal window W_V | 3 days  |
| Evaluation sample | 10,000 rows per day, stratified, all rare-family rows, weights 1/π  |
| A_FP (protocol setting; not used for H1, DEV-010) | 1,000 alarms per day  |
| Seed | 42  |
| LightGBM | `n_estimators=300`, `learning_rate=0.02162`, `num_leaves=15`, `min_child_samples=5`, `subsample=0.886`, `subsample_freq=1`, `colsample_bytree=0.983`, `reg_lambda=0.26711`, `verbosity=-1` (Section 4.4) |
| TabFM | `tabfm` library 1.0.1; weights `google/tabfm-1.0.0-pytorch` at revision 77cb9cc1b4fd3a9c77fbb9552c218200bb4dab83 with pinned file hashes; the 8-member ensemble of the released TabFM software; bfloat16; ensemble batch 1; query batch 4,096  |
| CURE | ρ = 0.75; warm-up 100 arrivals; warm-fill 1.0; τ_CURE = 0.1; entropy from the locked LightGBM  |
| Isolation | Filter with zero tolerated drops (stops the run on any I1/I3 collision); I2 always checked  |

*Table 2. Settings fixed before the main run.*

### 4.4 Locking LightGBM and CURE

LightGBM hyperparameters were chosen by a seeded random search over 50 configurations, with mean AUPRC_w as the criterion. Configuration 0 was the Study 1/2 setup . The search used real-day replay (Section 3.2(a)) of NF-ToN-IoT-v3, 2019-04-23 to 2019-04-26, under these settings :
- FIFO, *b* = 2,000, η = 0.2, *k* = 2,000, τ = 0;
- a 10,000-row evaluation sample;
- seeds 42 and 123;
- day 23 as warm-up and days 24–26 evaluated.

The registered plan specified Bayesian search; a random search with the same budget was used instead (DEV-002) . τ_CURE was then selected on the grid {0.1, …, 0.5} (5 of the 12 configurations allowed per policy), with the locked LightGBM on the same days . FIFO, DualFIFO and CBRS have no tuned parameter .

The four tuning days are also root days of the scenarios. This shared use is a risk of bias of unknown direction. LightGBM may be favoured on those root days because it was tuned on their flows. It may also be overfitted to the real-day setting, which differs from the scenario setting. We do not assume either direction, and Section 5.5 reports results per dataset.

### 4.5 Cost pilot

Before the main design was fixed, TabFM and LightGBM were timed on an NVIDIA L4 GPU on development data . With a 2,000-row context:
- TabFM took 9.6 s to score 1,000 query rows and 56.8 s to score 10,000;
- peak GPU memory stayed at or below 5.0 GB for contexts of up to 8,000 rows;
- a LightGBM retrain on 2,000 rows took about 0.1 s .

A linear fit to the two TabFM timings gives 4.36 s plus 5.25 s per 1,000 query rows per evaluated day . A separate speed test scored the same three pilot days with faster batching settings and the same model, weights and 8 ensemble members . The faster settings changed scores by up to 0.0075, so the pilot settings were kept . The pilot also measured the time to re-score after removing one context row (a full context recompute) . At k = 2,000 with 1,000 query rows, the full recompute took 9.61 s.

### 4.6 Blinded variance pilot

To size the main run without seeing the effect, a pilot scored 48 units (192 evaluated days) with both models, using 3.03 GPU-hours (median 58.4 s per day) . Its design :
- FIFO, feature scenarios, τ = 0, *k* = *b* = 2,000, η = 0.2;
- a 10,000-row evaluation sample;
- seeds 42 and 123;
- scenario 0 for every root day, plus scenarios 1 and 2 for four root days (ToN-IoT 23 and 24 April, CICIDS2018 14 and 15 February).

The analysis wrote only standard deviations and counts of d, estimated by the method of moments for the nested design (root day > scenario > seed, dataset as a fixed effect). No mean, sign or per-unit value was printed or written  (compare blinded sample-size review [34], [35]). The root-day standard deviation was 0.071 by moments but 0.0024 by a robust MAD-based estimate. The scenario and seed standard deviations were 0.0008 and 0.0021 . The gap between the two root-day estimates is compatible with a heavy-tailed distribution in which one root day lies far from the others.

After this pilot, the primary test was changed from a *t* test in a linear mixed model to the Wilcoxon signed-rank test (DEV-004). No mean or direction had been seen . In the blinded simulation under the heavy-tailed model, a one-sample *t* test against 0 had power of about 0.50 at θ = 0.02 and 0.03, against 1.00 for the Wilcoxon test . Scenario and seed variation were small relative to root-day variation, so the main run uses S = 1 and one seed .

### 4.7 Power

The power of the locked decision rule (exact one-sided 95 % HL lower bound ≥ ε₁) was simulated with 4,000 replicates and seed 20261028, under two models of the 16 root-day outcomes built from the blinded standard deviations :
- **(A) heavy tail.** 15 root days follow N(θ, 0.0024²) and one lies at θ ± 0.274, so the moment SD equals 0.071 .
- **(B) normal.** All root days follow N(θ, 0.071²).

| θ | 0.02 (= ε₁) | 0.03 | 0.05 | 0.07 |
|---|---|---|---|---|
| (A) heavy tail | 0.056 | 1.00 | 1.00 | 1.00 |
| (B) normal | 0.046 | 0.126 | 0.506 | 0.848 |

*Table 3. Probability that the decision rule is met . At θ = ε₁ the entries are type I error rates.*

The preregistration attributes its power figures to `power_v2.py`. That script tests against 0, not against ε₁. The figures in the preregistration come from the exact rule and are reproduced by `power_v3.py` within Monte Carlo error (DEV-009) . Both models assume that the 16 root-day outcomes are independent, and both are built from blinded variance estimates of feature-shift chains only. Under (A), the design detects θ ≥ 0.03 with near certainty. Under (B), it is underpowered unless θ is well above ε₁. Which model is closer to the truth is not known before the analysis. If root days are positively dependent, the effective sample is smaller than 16, and the power figures are optimistic. For reference, Study 1 made the same comparison under a different protocol and observed differences of about 0.07–0.09 .

### 4.8 Run plan and compute budget (design P2)

| Part | Policies | Kinds | Evaluated days |
|---|---|---|---|
| Primary (H1a) | FIFO | feature, prior, recurring | ≈ 198  |
| Secondary | DualFIFO, CBRS, CURE | feature | 192  |

*Table 4. Main-run design P2* .

Design P2 was chosen from three candidates, costed with the pilot model at 10,000 query rows per day :

| Design | Description | TabFM-days | GPU-hours |
|---|---|---|---|
| P1 | FIFO × 3 kinds, S = 2, plus the secondary part | 588 | 9.3 |
| P2 | As P1, with S = 1 for the primary part | 390 | 6.2 |
| P3 | 4 policies × 3 kinds, S = 2 | 1,584 | 25.0 |

The projection for P2, 6.2 GPU-hours, corresponds to about 10 Colab compute units at 1.62 units per hour .

**Budget rule** :
- The cap is 12 compute units, cumulative over all Colab sessions of the main run and never reset at reconnection.
- A ledger records each stage's wall time × 1.62 × 1.1. A 60-second heartbeat updates it, so a disconnected session is still counted. It also records the "available units" reading entered at the start of each session. Spent units are the larger of the two figures.
- Before the run, after the first scored day and every 10 days after that, the run stops if spent plus projected remaining units would exceed the cap. It continues only if the cap is raised explicitly, recorded in the ledger and as a deviation.

### 4.9 Procedure, blinding and integrity

The preregistration (v4), the analysis script, the export script and the Colab script were hashed and locked on 2026-10-28, before any main-run output existed. 27 synthetic tests passed on a copy with a synthetic cache, and a static audit of the export and Colab scripts passed . The run proceeds in fixed stages :

1. **Export (local CPU).** Every unit is replayed with the locked LightGBM. For every evaluated day the package stores:
   - the context and the evaluation rows;
   - the labels, families and weights;
   - the LightGBM scores, in float64.

   Every unit records the hashes of its inputs. No metric of either model is written to the package (DEV-007, DEV-008).
2. **Colab: verify, dry run, run.** The package, the analysis script and the preregistration are checked against the locked hashes. TabFM then scores every evaluable day. Each score file stores the SHA-256 of its exact inputs; a checkpoint whose inputs no longer match stops the run.
3. **Results.** Status and counts per day only; no AUPRC is computed.
4. **Analyze, once.** A marker is written first. AUPRC_w is then computed for both models, and the locked analysis script runs on the result.

The descriptive per-family analysis of DEV-010 (`secondary_h1.py`, SHA-256 05de983f…c561) runs once, after the primary analysis, and refuses a second run .

### 4.10 Real-day addenda (DEV-011, DEV-012, DEV-013)

Three addenda were written and hashed during the main run, after its GPU scoring had started and before the primary analysis was run. They do not change the preregistration, H1a, H1b, the analysis script or the main data .

**DEV-011: chronological replay of the real days.** The same replay code, locked LightGBM, FIFO, *b*, η, *k*, τ = 0, evaluation sample and TabFM settings as the main run are applied to the real development days in time order. These are 7 days of NF-ToN-IoT-v3 and 10 of NF-CICIDS2018-v3, including 2018-02-23, which has no attack. The first day is warm-up. Replay mode (a) of Section 3.2 is used, with I1 asserted, and seeds 42, 123 and 2026 apply to label queries and LightGBM. The unit is the day transition, with d averaged over valid seeds. The analysis reports the mean, the HL estimate with a nominal two-sided 95 % interval and a nominal one-sided lower bound, the number of positive transitions, and per-dataset means. The intervals are nominal because they assume independent transitions. Consistency with H1a was defined in advance as the same sign of the two HL estimates and the same side of ε₁ for the two lower bounds. A difference between the settings is not attributed to the protocol, because the settings also differ in drift, evaluation rows and time structure .

**DEV-013: conventional random split.** For every chronological day and seed, the evaluation rows are those of DEV-011. Rows, row identities, labels, families and weights are checked to be identical, and any difference stops the export. The context is replaced by 2,000 rows drawn uniformly from all flows of the dataset, past, same-day and future, excluding that day's evaluation rows. There is no time order, label budget or label delay. This is a future-informed evaluation, not a deployable setting. The analysis pairs (dataset, day, seed) triples that are valid under both protocols. It reports, for each protocol, the mean AUPRC_w of each model and the HL estimate of d. It also reports the paired day-level change of d and of each model's AUPRC_w, with nominal intervals and no test .

**DEV-012: cost reporting.** The report gives measured TabFM GPU-seconds per evaluated day on the L4, ledger Colab wall hours and estimated compute units (CU), the cross-session CU balance delta, and LightGBM retrain and prediction latency on CPU, measured with the locked parameters and 2 threads. GPU and CPU seconds are reported side by side and never converted into each other. TabFM GPU-seconds per +0.01 AUPRC_w are computed only if the H1a exact lower bound is above 0 and the HL estimate is at least ε₁ .

All three analyses ran once, from hashed scripts, after the primary analysis. The DEV-011 and DEV-013 GPU scoring had finished before the primary analysis was run .

### 4.11 Independent check on CIDDS-001 (PC1; exploratory)

*Naming.* PC1 (protocol check 1) is called "H2" in its preregistration, scripts and output files (`prereg_h2_cidds.md`, `analysis_h2.py`, `h2_out.json`); DEV-PC1-001 is DEV-H2-001 in the deviation log and `dev_h2_001.py`. The names were changed in this paper only, so that PC1 is not confused with hypothesis H2 of the wider research plan; the locked files are unchanged.

After DEV-013, we fixed a further question in a separate preregistration, before CIDDS-001 was downloaded: does the
inflation of the random split replicate on data that played no part in forming the question? The preregistration and
its scripts were hashed before the data were opened .

- **Data.** The CIDDS-001 OpenStack (internal) NetFlow data [42], about 31 million flows over four weeks [44].
- **Features.** 19 features: flow counts, protocol and TCP-flag bits. No IP address or time is used as a feature.
- **Model and settings.** The locked LightGBM, not retuned, with the same evaluation sample, *b*, η, *k* and seeds as
  DEV-011.
- **Arms.** Three arms share the same evaluation rows:
  - chronological replay (the DEV-011 code);
  - random split over all days (the DEV-013 code);
  - random split over earlier days only ("random-past").
- **Quantity.** Δ = AUPRC_w(random split) − AUPRC_w(chronological), per day.
- **Why the check is exploratory.** In the pre-lock simulation, the candidate rules did not consistently control the
  nominal error rate across the day counts and dependence settings evaluated. We therefore treat PC1 as an independent
  exploratory check. It reports effect sizes, nominal intervals, a bootstrap sensitivity to dependence and a
  descriptive outcome label fixed in advance. It uses no test or *p*-value.
- **Minimum data.** Fewer than 8 days valid in all three arms gives the label INSUFFICIENT_DATA.

## 5. Statistical analysis

The preregistration and the analysis script are locked and unchanged. This section describes them .

### 5.1 Hypotheses

- **H1a (primary).** Under FIFO, TabFM detects attacks better than LightGBM retrained daily on the same context, by at least ε₁ = 0.02 AUPRC_w. The parameter θ is the pseudo-median over root days of d. H0: θ ≤ ε₁; H1: θ > ε₁. A conclusion of superiority requires the one-sided 95 % lower bound of θ to be at least ε₁ . The preregistration labels H1a "confirmatory". Here this means that the hypothesis, decision rule and analysis were fixed before the main run. It does not mean that the data are independent of tuning and piloting (Section 4.1). The value ε₁ = 0.02 is a convention fixed before the run. It was the smallest effect in the power grid of the study plan, about ten times the blinded seed-to-seed standard deviation (0.0021) and well below the 0.07–0.09 seen in Study 1. It was not derived from the operational cost of an alarm or of GPU time; no such anchor exists for AUPRC in this setting. Section 6.2 therefore also reports the range of effects compatible with the data, so that readers can apply their own margin.
- **H1b (quality–cost).** H1b would have been tested only if λ (VND per +0.01 AUPRC_w) and the unit prices per GPU-hour and CPU-hour had been written into the analysis script before the lock, and only after H1a was supported (fixed sequence). They were not written in, so H1b is descriptive: it reports the extra seconds per +0.01 AUPRC_w and supports no claim . The addendum DEV-012 (Section 4.10) further restricts the seconds-per-gain ratio to the case HL ≥ ε₁ with a positive lower bound.

### 5.2 Primary decision

On the 16 root-day outcomes x :

1. **Exact test.** An exact one-sided Wilcoxon signed-rank test of x − ε₁ at α = 0.05. Equivalently, the exact one-sided 95 % lower bound of the Hodges–Lehmann (HL) estimate, obtained by inverting the signed-rank test. The HL estimate is the median of the Walsh averages (x_i + x_j)/2, i ≤ j. The lower bound is the Walsh average whose rank corresponds to the 5 % quantile of the exact null distribution .
2. **Dependence sensitivity check.** A moving-block bootstrap with blocks of 3 consecutive root days within each dataset, 10,000 resamples and seed 20261028. The one-sided 95 % lower bound is the 5 % quantile of the bootstrap distribution of the HL estimate of the pooled resample .

| Verdict (label of the locked script) | Rule |
|---|---|
| CONFIRMED | exact lower bound ≥ ε₁ and block-bootstrap lower bound ≥ ε₁ |
| SUPPORTED_DEPENDENCE_SENSITIVE | exact lower bound ≥ ε₁, block-bootstrap lower bound < ε₁ |
| SUPERIOR_BELOW_EPS1 | the Wilcoxon test against 0 rejects and the exact lower bound is < ε₁ (no claim of practical superiority) |
| NOT_ESTABLISHED | otherwise |
| NO_CONFIRMATORY_CLAIM | technical failures > 5 % of the primary evaluable days (Section 5.4) |

*Table 5. Preregistered verdicts for H1a* . The labels are fixed by the locked script. A CONFIRMED verdict would mean that the preregistered decision rule was met on these 16 development root days. It would not be an independent confirmation, and it would not show that the result holds for other NetFlow networks.

### 5.3 Assumptions

**Symmetry.** The Wilcoxon test and its HL bound assume that root-day outcomes are symmetric about θ. Without symmetry, they refer to the pseudo-median. The exact sign test [38] of x − ε₁ concerns the median and needs no symmetry; it is reported next to the verdict. If the two tests disagree, we say so .

**Dependence.** The 16 root days are calendar days of the same two networks: consecutive for ToN-IoT, close for CICIDS2018. Their outcomes may be dependent. The exact test assumes independence. The block bootstrap allows dependence within three neighbouring days, but with 7 and 9 days per dataset it is a sensitivity check, not a correction. The lag-1 autocorrelation of root-day outcomes within each dataset is reported. A CONFIRMED verdict requires both bounds. Even so, 16 possibly dependent days are a smaller effective sample than 16 independent ones .

### 5.4 Days that cannot be scored

Every evaluated day is kept in the results with a status :
- *not_evaluable*: by design, decided before TabFM is run. The day has a one-class context or no attack in its evaluation sample. Such days are excluded for both models, and their counts and reasons are reported.
- *tech_fail*: a TabFM error after 3 attempts with the same settings. The scorer may halve the query batch on out-of-memory errors; this does not change the scores. The error type is recorded, and no day is dropped silently.

The primary analysis uses the available evaluable days, which assumes that failures are unrelated to the outcome. Whenever any technical failure exists, three sensitivity analyses are reported:
- **S1:** worst case for TabFM, with AUPRC_w(TabFM) = 0 on failed days;
- **S2:** complete chains only;
- **S3:** root days without any failure only.

If technical failures exceed 5 % of the primary evaluable days, the verdict is NO_CONFIRMATORY_CLAIM. The cause is then fixed, a new version is locked as a deviation, and the whole run is repeated .

### 5.5 Secondary and descriptive analyses

All of these are reported in full, and no claim rests on any of them alone :
- the mean of the root-day outcomes with a *t* confidence interval, raw and adjusted for dataset;
- the same per dataset and per kind of drift;
- for each secondary policy (DualFIFO, CBRS, CURE, on feature scenarios), the HL estimate with its 95 % confidence interval;
- every root day more than 5 MAD from the median, listed with its value.

**Per-family AUPRC_w (descriptive; replaces threshold metrics and per-family recall, DEV-010)** . The calculation:
1. For every evaluated day with status ok and every attack family *f* in that day's evaluation sample, take the benign rows plus the rows of *f*, with label 1 = *f*.
2. On these rows, compute AUPRC_w of each model with the locked inverse-inclusion weights. Both models use the same rows.
3. If a (day, family) pair has fewer than 10 rows of *f* or fewer than 10 benign rows, list it as not_evaluable with its reason.
4. For each (policy, dataset, family), compute the root-day value as the mean over that root day's evaluable days.

The report gives the number of root days and days, the median and interquartile range of the root-day TabFM − LightGBM differences, and the mean AUPRC_w of each model. Every family is reported, with no test and no p-value .

### 5.6 Deviation policy

Any change after the lock is recorded as a deviation: what changed, why, when, and whether main-run output had been seen. A change made after results are seen is reported as such, together with the preregistered analysis. A code defect found after the run is fixed, a new version is locked, everything is rerun, and both runs are reported .

## 6. Results



### 6.1 Run accounting

| Quantity | Primary (FIFO) | Secondary (DualFIFO / CBRS / CURE) |
|---|---|---|
| Chains | 42 (16 feature, 16 prior, 10 recurring) | 48 (16 per policy, feature) |
| Evaluated days | 188 | 192 |
| ok / not_evaluable / tech_fail | 186 / 2 / 0 | 192 / 0 / 0 |
| not_evaluable reasons | one-class context: 2 days of the prior chain of CICIDS2018 2018-02-22 | — |
| Share of technical failures (primary evaluable days) | 0.0000 | — |
| Rows dropped by the isolation filter | 0 (zero tolerance; any drop stops the export) | 0 |

*Table 6. Run accounting* . Because no technical failure occurred, the missing-data sensitivity analyses S1–S3 (Section 5.4) were not triggered . Cost and compute units are reported in Section 6.5.

### 6.2 Primary hypothesis H1a

| Statistic | Value |
|---|---|
| Root days (n) | 16 |
| HL estimate of θ | +0.0098 |
| Exact one-sided 95 % lower bound | +0.0038 |
| Two-sided 95 % interval | [+0.0030, +0.0232] |
| Wilcoxon *p* vs ε₁ / vs 0 (exact, one-sided) | 0.948 / 3.1 × 10⁻⁵ |
| Block-bootstrap one-sided 95 % lower bound (block 3, 10,000 resamples) | +0.0036 |
| Sign test *p* vs ε₁ | 0.989 |
| Lag-1 autocorrelation (ToN-IoT / CICIDS2018) | −0.352 / −0.116 |
| Root days with x > 0 | 15 / 16 |
| **Verdict** | **SUPERIOR_BELOW_EPS1** |

*Table 7. H1a, preregistered primary analysis: TabFM − LightGBM in AUPRC_w under FIFO, root-day outcomes* . (The output file of the locked report script labels this table "confirmatory"; in the sense of Section 5.1 it is the preregistered primary analysis on development data.)

TabFM ranked attacks better than LightGBM on 15 of the 16 root days; the one exception, CICIDS2018 2018-02-16, differs by −0.0004 . The Hodges–Lehmann estimate is +0.0098 AUPRC_w and the exact Wilcoxon test against no difference gives *p* = 3.1 × 10⁻⁵ . The preregistered decision rule for practical superiority was not met. The exact lower bound (+0.0038) and the block-bootstrap lower bound (+0.0036) are both below ε₁ = 0.02, and the Wilcoxon and sign tests against ε₁ agree in not rejecting . The locked script therefore returns SUPERIOR_BELOW_EPS1: the root-day differences lie above zero (15 of 16 root days positive; Wilcoxon against 0, *p* = 3.1 × 10⁻⁵), but the estimated advantage of about 0.01 AUPRC_w is smaller than the margin fixed as practically relevant before the run. We therefore make no claim of practical superiority of TabFM. The test against 0 assumes independent root days, so its *p*-value is optimistic; the lag-1 autocorrelations within each dataset are negative (−0.35 and −0.12), which gives no sign of positive serial dependence in these short series .

**Effects compatible with the data.** The exact one-sided lower bound was +0.00376 AUPRC_w and the block-bootstrap one-sided lower bound was +0.00360. At the preregistered margin of 0.02, the locked verdict was `SUPERIOR_BELOW_EPS1`. The nominal two-sided interval [+0.0030, +0.0232] contains ε₁ = 0.02, so the data do not exclude an advantage of 0.02 either.

[Figure 1: root-day outcomes x by dataset in calendar order, with ε₁ and the HL estimate marked — bai1_results/fig1_root_days.png.]

### 6.3 Secondary and descriptive analyses (scenario replay)

| Analysis | Estimate | 95 % interval | n |
|---|---|---|---|
| Mean of root-day outcomes | +0.0233 | [−0.0044, +0.0509] | 16 |
| Mean, dataset-adjusted | +0.0233 | [−0.0050, +0.0515] | 16 |
| NF-ToN-IoT-v3 (mean) | +0.0121 | [−0.0015, +0.0258] | 7 |
| NF-CICIDS2018-v3 (mean) | +0.0319 | [−0.0207, +0.0846] | 9 |
| Feature shift (mean) | +0.0237 | [−0.0141, +0.0615] | 16 |
| Class-prior shift (mean) | +0.0182 | [−0.0007, +0.0372] | 16 |
| Recurring family (mean) | +0.0178 | [−0.0076, +0.0431] | 10 |
| DualFIFO, feature (HL) | +0.0056 | [+0.0008, +0.0158] | 16 |
| CBRS, feature (HL) | +0.0061 | [+0.0005, +0.0164] | 16 |
| CURE, feature (HL) | +0.0046 | [+0.0012, +0.0147] | 16 |

*Table 8. Secondary analyses of TabFM − LightGBM in AUPRC_w (means with t intervals; secondary policies with HL and exact intervals). No claim rests on them alone* .

The mean (+0.023) is more than twice the HL estimate because two root days lie beyond 5 MAD of the median: CICIDS2018 2018-02-22 (x = +0.213; feature +0.287, prior +0.138) and ToN-IoT 2019-04-29 (x = +0.044, driven by its recurring chain, +0.115) . The other 14 root days lie between −0.0004 and +0.026 . The sign of the difference is the same under the three secondary policies, with HL estimates of +0.005 to +0.006 . Under CURE, this holds for the LightGBM-gated variant only (Section 3.5).

**Per family (DEV-010, descriptive).** Under FIFO, the median root-day difference is close to zero for families that both models rank almost perfectly (for example DoS-Hulk, SSH-Bruteforce and HOIC in CICIDS2018, with AUPRC_w ≈ 1.000 for both) . The larger differences occur for families that LightGBM ranks less well: LOIC-UDP, the rare family of CICIDS2018 2018-02-21 (TabFM 0.776 vs LightGBM 0.371; one root day, 11 days), and in ToN-IoT mitm (0.784 vs 0.686), ransomware (0.636 vs 0.549) and dos (0.802 vs 0.721) . Each of these rests on one or two root days. Three CICIDS2018 families (Brute Force-Web, Brute Force-XSS, SQL Injection) were never evaluable, because they have fewer than 10 rows in every evaluation sample .

| Dataset | Family | Root days / days | Median root-day TabFM − LightGBM | Mean AUPRC_w TabFM / LightGBM |
|---|---|---|---|---|
| CIC | DDoS LOIC-UDP (rare) | 1 / 11 | +0.405 | 0.776 / 0.371 |
| CIC | DoS Slowloris | 1 / 14 | +0.049 | 0.983 / 0.934 |
| CIC | DoS GoldenEye | 1 / 11 | +0.022 | 0.992 / 0.970 |
| CIC | Infiltration | 2 / 16 | +0.020 | 0.276 / 0.256 |
| ToN | mitm | 1 / 14 | +0.098 | 0.784 / 0.686 |
| ToN | ransomware | 1 / 11 | +0.087 | 0.636 / 0.549 |
| ToN | dos | 2 / 25 | +0.080 | 0.802 / 0.721 |
| ToN | backdoor | 2 / 25 | +0.024 | 0.993 / 0.968 |

*Table 9. Per-family AUPRC_w under FIFO, families with |median difference| ≥ 0.02 (descriptive, no test).* Supplementary Table S6 is listed among the pending release items.

### 6.4 Real days: chronological replay and random split (DEV-011, DEV-013; descriptive)

These analyses use real days, not synthetic scenarios, and were fixed in two addenda before the primary analysis was run (Section 4.10). They are descriptive.

**Chronological replay (DEV-011).** Over 14 day transitions (8 CICIDS2018, 6 ToN-IoT; 45 day×seed records: 41 evaluable, 4 not evaluable), the HL estimate of d was +0.034, with a nominal two-sided 95 % interval of [+0.001, +0.166] and a nominal one-sided lower bound of +0.003; d was positive on 11 of 14 transitions . The mean, +0.100, is again pulled up by large values. In CICIDS2018 the mean d was +0.180. On three transitions LightGBM ranked far worse than TabFM: 2018-02-20 (TabFM 0.958 vs LightGBM 0.237), 2018-02-15 (0.978 vs 0.674) and 2018-02-21 (1.000 vs 0.770) . In ToN-IoT the mean d was −0.007, with transitions between −0.086 (2019-04-25) and +0.034 . Under the consistency criteria fixed in the addendum, the chronological replay and the scenario H1a agree: the two HL estimates have the same sign, and both lower bounds lie below ε₁ . Neither setting supports a lower bound of 0.02.

**Random split (DEV-013).** The random split keeps the evaluation rows of every chronological day and changes only the context. The context holds 2,000 rows drawn uniformly from all flows of the dataset, including flows recorded after the evaluated day. This is the usual random-split evaluation. It is future-informed and not a setting that could be deployed. 41 (day, seed) pairs were valid under both protocols; one pair (CICIDS2018 2018-02-28, seed 123, one-class chronological context) was excluded .

| Quantity | Random split | Chronological | Random − chronological (paired, per day) |
|---|---|---|---|
| Mean AUPRC_w, TabFM | 0.831 | 0.640 | HL +0.118, nominal 95 % [+0.012, +0.372]; 11 / 14 days > 0 |
| Mean AUPRC_w, LightGBM | 0.799 | 0.540 | HL +0.207, nominal 95 % [+0.076, +0.416]; 13 / 14 days > 0 |
| d = TabFM − LightGBM: HL (nominal one-sided LB) | +0.009 (+0.005) | +0.034 (+0.003) | HL −0.005, nominal 95 % [−0.142, +0.040]; 7 / 14 days > 0 |
| Days with d > 0 | 14 / 14 | 11 / 14 | — |

*Table 10. Random split vs chronological replay on the same evaluation rows (14 real days; means over the seeds valid under both protocols; nominal intervals assume independent days; no test)* .

Two observations follow, and the data support them to different degrees.

1. *Absolute levels.* With a future-informed random context, both models reach a clearly higher AUPRC_w than in chronological replay on the same rows. The increase is +0.12 (HL) for TabFM and +0.21 for LightGBM, and it occurs on most days . Several days that are hard in chronological order are almost solved under the random split. For example, on ToN-IoT 2019-04-28 TabFM scores 0.996 under the random split and 0.287 in chronological order, and on CICIDS2018 2018-03-02 it scores 1.000 and 0.123 . An evaluation that draws its labelled data without regard to time would therefore report a much easier task than the one a deployed detector faces.
2. *The gap between the models.* Under both protocols, the HL estimate of d is positive and its nominal lower bound is far below 0.02 (Table 10). The paired change in d between the protocols is centred near zero (HL −0.005), its interval is wide and covers both signs, and it is positive on half the days . These data therefore do not show that the random split consistently changes the relative standing of the two models. What they do show is that the gap varies strongly between days and datasets. The largest chronological gaps (CICIDS2018 2018-02-15, 02-20 and 02-21) almost vanish under the random split, where both models score above 0.96. On CICIDS2018 2018-02-22, by contrast, the gap is larger under the random split (+0.335 vs +0.187) .

[Figure 2: AUPRC_w of both models per real day under the two protocols — bai1_results/fig3_protocols_per_day.png.]

### 6.5 Cost (H1b and DEV-012, descriptive)

| Quantity | Value |
|---|---|
| TabFM on NVIDIA L4, GPU-seconds per evaluated day (median; IQR) | 58.4 (55.7–58.5) |
| TabFM on NVIDIA L4, GPU-seconds per 1,000 evaluation rows (median; fit + predict, *k* = 2,000) | 5.84 |
| LightGBM on CPU (2 threads), retrain seconds per day (median; IQR) | 0.36 (0.27–0.53) |
| LightGBM on CPU, prediction seconds per 1,000 rows (median over 20 days) | 0.0074 |
| TabFM GPU-seconds per day per +0.01 AUPRC_w (DEV-012 rule) | not computed: HL below ε₁ |
| Main run: Colab wall-clock hours (ledger, all stages and sessions) | 6.12, of which 5.97 in the scoring stage |
| Main run: ledger CU estimate (sum(wall_seconds) × 1.62 × 1.1 / 3600) | 10.90 |
| Cross-session CU balance decrease | 9.94 (18.55 → 8.61) |
| DEV-011 / DEV-013: compute units, ledger estimate | 1.31 / 1.37 |

*Table 11. Measured GPU and CPU time, Colab wall time and compute units.* TabFM GPU-seconds per evaluated day and LightGBM CPU-seconds are reported separately. The ledger CU estimate uses Colab wall time across stages and sessions. The balance decrease spans the first main-run session and the start of the chronological replay session. It includes idle runtime and can be attributed to the main run only if there was no other Colab use in that interval. The chronological and random-split sessions overlapped. Their costs are reported as separate ledger estimates. The 12-unit cap was not reached, changed or invoked.

Under the DEV-012 rule, fixed before the analysis, the GPU-seconds per +0.01 AUPRC_w are computed only if the H1a lower bound is above 0 and the HL estimate is at least ε₁. The second condition fails, so the quantity is not computed . The locked analysis script, written before DEV-012, also prints the descriptive H1b ratio of preregistration v4: 59.0 extra seconds per +0.01 AUPRC_w . It is reported here only for completeness, because it divides by an estimate (0.0098) whose interval reaches 0.003. In plain terms, TabFM needs about one GPU-minute per day where LightGBM needs under half a CPU-second, for a typical gain of about 0.01 AUPRC_w in the scenario replay.

### 6.6 Independent check on CIDDS-001 (PC1 and DEV-PC1-001; exploratory)

**PC1: insufficient data.** 
- **Attack days.** Attacks occurred on 9 of the 28 valid days. Weekends, the day of the OpenStack network failure
  (2017-03-22), and weeks 3–4 contained no attacks.
- **Realized sample.** The matched sample contained 6 days and 17 day×seed triples.
  Chronological untrainability accounted for 7 exclusions (6 across fully untrainable days and 1 on a partially untrainable day).
- **Label.** The preregistered label is INSUFFICIENT_DATA. PC1 is not assessed, and no size label or interval is
  reported. This outcome is neither evidence for nor against inflation on CIDDS-001.
- **Anticipated vs actual days.** The preregistration anticipated up to about 13 evaluable days. After warm-up,
  8 attack-bearing days remained as the ceiling before checking trainability and pairing.

The day values are shown descriptively:

| Day | Seeds | Chronological | Random (all days) | Random (past days) |
|---|---|---|---|---|
| 2017-03-16 | 3 | 0.988 | 0.973 | 0.980 |
| 2017-03-17 | 3 | 0.998 | 0.999 | 0.999 |
| 2017-03-21 | 3 | 0.996 | 0.992 | 0.997 |
| 2017-03-23 | 2 | 0.970 | 0.999 | 0.999 |
| 2017-03-24 | 3 | 0.999 | 0.999 | 0.999 |
| 2017-03-28 | 3 | 0.656 | 0.774 | 0.831 |

*Table 12. CIDDS-001: LightGBM AUPRC_w on the 6 days valid in all arms (descriptive; PC1 not assessed)* .

On five of the six days, all arms rank attacks almost perfectly (0.97–0.999), so there is little room for inflation.
On the one day with a clear difference (2017-03-28), the random split over past days only scored higher than the
random split over all days. On that day, the gain over chronological replay did not depend on future information.

**DEV-PC1-001: untrainable chronological contexts (post hoc, descriptive).** This analysis was added after the PC1
output had been seen. It is exploratory .
- *Observed one-class contexts.* After attack-free periods, some chronological FIFO contexts contained only benign flows.
  FIFO can carry rows over from earlier days. On the observed one-class records, LightGBM could not train under the
  protocol, so those records had no valid chronological predictor.
- *How often this happened.*
  - On 2 of the 8 attack days (2017-03-20 and 2017-03-27), the chronological arm was untrainable for all three seeds.
    On a third (2017-03-23), it was untrainable for one seed.
  - It was also untrainable on 13 of the 14 attack-free days of weeks 3–4 for at least one seed (12 days for all seeds).
  - Neither random arm was untrainable on any day.

| Day (seeds untrainable, chronological) | Chronological | Random (all days) | Random (past days) | Constant-score reference (hypothetical) |
|---|---|---|---|---|
| 2017-03-20 (3/3) | untrainable | 0.998–0.999 | 0.997–0.999 | 0.216 |
| 2017-03-23 (1/3: s42) | untrainable (s42); 0.970 (other seeds) | 0.999 | 0.999 | 0.266 |
| 2017-03-27 (3/3) | untrainable | 0.735–0.858 | 0.723–0.779 | 0.006 |

*Table 13. Attack days on which the chronological context held one class: what the random splits reported (LightGBM
AUPRC_w, range over seeds)* . The last column is a hypothetical reference: the AUPRC_w of a
scorer that ranks every row equally, which equals the weighted attack prevalence. It is not a LightGBM result.

In this setting, random-split evaluation did not expose the one-class-context training failure observed under
chronological replay: on those days the random splits reported near-perfect or good ranking. This is not a failed
prediction but the absence of a valid predictor under the protocol. We report it as an observation on one dataset
with one context size and one label budget, not as a general law; we do not claim that random splits always hide
this failure.

## 7. Discussion and limitations

### 7.1 What the results show

**TabFM is consistently better, by a small typical margin.** On the same context and the same evaluation rows, TabFM ranked attacks better than a daily-retrained LightGBM on 15 of 16 root days and under all four context policies. This is a positive result, and the protocol makes it hard to attribute to leakage or to a better context: both models saw identical labelled rows. Its typical size, about 0.01 AUPRC_w, did not meet the conservative preregistered margin of 0.02, and we do not claim practical superiority on that criterion. The interval reaches 0.023, so a gain of that order is not excluded.

**Where the advantage is large.** In both the scenario and real-day analyses, the advantage is concentrated in a few days and families. In scenario replay it comes from an attack-scarce CICIDS2018 day (2018-02-22) and from the recurring chain of ToN-IoT 2019-04-29. Per family, it comes from families that LightGBM ranks poorly, including the one rare family (LOIC-UDP). In chronological real-day replay it comes from three CICIDS2018 transitions on which LightGBM's ranking collapsed while TabFM's did not. The published CSE-CIC-IDS2018 attack schedule shows that the scheduled attack types vary across days [28], so the context built from earlier days may hold few or no rows of the attack being evaluated; we did not measure this per day. In ToN-IoT the chronological difference is close to zero on average. We did not test why TabFM degrades less on these days, and we do not claim a mechanism. A plausible reading is that a model conditioned on a small context generalises differently from a tree ensemble fitted to that context when the evaluated attack is absent from, or rare in, the context. Confirming this would need a design built for it.

**What the protocol comparison shows.** The random-split comparison supports one clear statement. Drawing the labelled context from all days, including later ones, raises the absolute AUPRC_w of both models substantially on the same evaluation rows (+0.12 for TabFM and +0.21 for LightGBM, HL). Results from such evaluations therefore overstate how well either model would rank attacks in day-by-day operation. The comparison does not show a consistent change in the TabFM–LightGBM gap. The paired change in the gap is centred near zero and varies in both directions across days. The gap itself, under any protocol, varies strongly between days and datasets. A single pooled number from one protocol therefore hides most of what matters for choosing between the models.

**What the CIDDS-001 check adds (exploratory).** The preregistered replication could not be assessed (Section 6.6).
In this setting, random-split evaluation did not expose a training failure that chronological replay revealed. When the labelled context follows time and attacks are
absent for a day or more, a bounded context loses every attack example, and a retrained classifier cannot be built.
On those same days, the random split reported AUPRC_w of up to 0.999. Whether this matters in practice depends on
how often attack-free periods occur, on the context size and on the label budget. A context policy that keeps
minority-class rows (DualFIFO, CBRS or CURE) might avoid it, but we did not test this on CIDDS-001.

**Practical reading.** The results suggest when TabFM is worth its cost. On stable traffic, which here means within-day scenarios and most ToN-IoT days, both models rank attacks almost equally well. The small gain of TabFM there costs about one GPU-minute per day on an L4, while LightGBM needs under half a CPU-second. On real days where a model fitted to earlier days ranks poorly, the picture changes. On CICIDS2018 2018-02-20, LightGBM's ranking collapsed to 0.237 while TabFM kept 0.958; on 02-15 and 02-21 the gaps were 0.30 and 0.23; on the rare family LOIC-UDP it was 0.40. For a detector that must cope with such days and has a GPU available, these results favour TabFM. For stable traffic on CPU-only hardware, LightGBM gives almost the same ranking for a fraction of the cost. How often such days occur, and whether they can be recognised in advance, depends on the network; our evidence comes from two testbed networks.

### 7.2 Scope of the contribution

This paper adds no new context selector; FIFO, DualFIFO, CBRS and CURE are existing methods. Its contributions are:
- the replay protocol, with its label budget, label delay and stated isolation guarantees;
- the controlled-drift generator;
- a preregistered, data-matched comparison of TabFM and LightGBM, reported with its cost;
- a descriptive comparison, on the same evaluation rows, of chronological replay and a conventional random split.

The last comparison covers one alternative protocol on 14 dependent days of two networks. It does not cover a day-to-day split with oracle-stratified labels or a setting without a calibration reservation, and it does not establish that either protocol is better in general.

### 7.3 Limitations stated before the run

The preregistration recorded these limitations before the main run :
- **Development data only.** There are 16 root days from two datasets, and they are not independent.
- **No label delay in H1.** The protocol supports τ > 0, but H1 is tested only at τ = 0.
- **One seed and one scenario per kind** (S = 1).
- **The variance pilot covered the feature kind only**, so the power analysis rests on feature-shift variation.
- **CURE is gated by LightGBM entropy**, not by the entropy of the model it serves (DEV-005). The CURE results here are not results of CURE as published.
- **A_FP is not attainable.** With D_cal of about 1,200 rows, the α floor binds.
- **Root days, not scenarios, are the independent units**, because each synthetic day is resampled from one root day.

Added before any H1 result was seen (DEV-010) :
- **No threshold metrics or per-family recall for H1.** TabFM did not score the D_cal rows, so no TabFM threshold exists. The comparison covers ranking quality (AUPRC_w and the descriptive per-family AUPRC_w) and says nothing about operating-point behaviour or alarm load.

### 7.4 Threats to validity

**Construct validity.** AUPRC_w measures ranking quality over a day; it does not measure behaviour at an operating threshold, which is not reported here. The controlled drift is a resampling-based perturbation of real days. It changes the weights of existing flows, but it creates no new flows, new attack families or new network behaviour, and successive synthetic days also differ by sampling variation (Section 3.3). In scenario replay, evaluation and labelled flows are disjoint but come from the same root day (Section 3.2), so the task is easier in this respect than predicting a later real day.

**Internal validity.** Both models see the same context and score the same evaluation rows on every day. Pool disjointness enforces isolation of flow identities, and the run stops on any violation (Section 3.2). LightGBM and τ_CURE were tuned on four root days in real-day replay, a risk of bias whose direction we do not assume (Section 4.4). The analysis is computed once, from a locked script, after a blinded run (Section 4.9).

**Statistical conclusion validity.** The exact test assumes independent, symmetric root-day outcomes, and neither is guaranteed (Section 5.3). The block bootstrap is a sensitivity check for short-range dependence within a dataset; it does not correct for dependence in general. The power figures assume independence and come from two blinded variance models with very different implications (Section 4.7).

**External validity.** Both datasets are testbed captures with scheduled attacks. CICIDS2018 runs largely one attack type per day, and its flows inherit the label errors documented for CSE-CIC-IDS2018 [30]. Two root days are thin in specific ways :
- on ToN-IoT 2019-04-28, the 200,000-row evaluation part is resampled from an evaluation pool of 115,321 rows, so its evaluation sample contains repeated flows;
- on CICIDS2018 2018-02-22, the CAL pool holds only 329 attack flows.

**CIDDS-001 check (PC1, DEV-PC1-001).** PC1 had too few evaluable days to be assessed, because the attacks of
CIDDS-001 are concentrated in nine weekdays. DEV-PC1-001 was defined after the PC1 output had been seen. It covers one
dataset, one policy (FIFO), one context size and one label budget.

**Real-day analyses (DEV-011, DEV-013).** These cover 14 transitions of two networks. Transitions of one network are dependent, and three CICIDS2018 transitions dominate the chronological mean. The intervals are nominal and no test was made. The analyses are therefore descriptive: they show what happened on these days, not how often such days occur elsewhere. The random split compares one alternative protocol only, and its context is drawn from the same dataset as the evaluation rows. Part of its advantage may come from flows of the evaluated day that sit in the context (same hosts and attack sessions), not only from later days. We did not separate these sources.

One context size, one label budget, one TabFM configuration and one LightGBM configuration are tested. Whatever the verdict, it concerns these development root days and these settings. It does not establish that the result holds for other NetFlow networks; independent confirmation on unused data is planned separately.

## Data and code availability

The NetFlow v3 datasets are public [24], [25]. Planned release materials and their recorded hashes are listed below. [RELEASE: NCS TO ADD]
- the preregistration (v4, SHA-256 5c9d428d…3d16) and the analysis script (SHA-256 914c5400…2b77);
- the descriptive secondary script (SHA-256 05de983f…c561) and the power script `power_v3.py` (SHA-256 2bb9f3e3…ff9d);
- the export and Colab scripts;
- the drift generator (SHA-256 7148f6e5…843c) and the scenario manifest (SHA-256 207817c6…ed08);
- the replay harness with its tests, and the policy implementations with their reproduction reports;
- the deviation log;
- the real-day addenda with their export and analysis scripts (DEV-011: `export_realday.py` 766bab32…, `analysis_realday.py` 6fce0e4e…, addendum 8218d182…; DEV-012/013: `export_random.py` 192764a3…, `analysis_random.py` 7d41cd53…, `cost_report.py` d72ea1a0…, addendum 9c8ff697…);
- the outputs of every single-run analysis, with the SHA-256 recorded by their once-markers: `results_h1.jsonl` e93bbeb9…, `out_h1.json` 37fa539d…, `secondary_h1.json` f4748817…, `cost_report.json` b4609de6…, `realday_results.jsonl` 84d01ecb…, `realday_out.json` 15b9a576…, `random_results.jsonl` 519dc01d…, `random_out.json` e6108b16…;
- the PC1 preregistration and scripts for CIDDS-001 (`prereg_h2_cidds.md` 247d4f16…, `analysis_h2.py` bbf8c34e…, `export_h2.py` c5b9552a…, `build_cidds_cache.py` 247c25c4…, `cidds_stream.py` 3ebbdafd…, `dev_h2_001.py` acfb3a96…) and their outputs (`h2_out.json` 1d6f4c4a…, `h2_results.jsonl` c8c2e835…, `dev_h2_001_out.json` 9565f8b0…);
- the report scripts that print every table of Section 6 from these outputs (`make_results_bai1.py`, `make_results_addenda.py`).

Code: [RELEASE: NCS TO ADD]

## Declarations

**Funding.** [NCS TO ADD]
**Competing interests.** The authors declare no competing interests.
**Author contributions (CRediT).** [NCS TO ADD]
**Use of generative AI.** [NCS TO ADD per journal policy]

## 8. Deviations from the plan

DEV-001 to DEV-008 predate the lock of 2026-10-28. DEV-009 to DEV-013 were recorded during the main run, before any H1 result existed; DEV-011 to DEV-013 add descriptive analyses and change nothing that was preregistered. No entry was made after main-run results were seen . No entry changes H1a, H1b, the data or the primary endpoint, and the preregistration and the analysis script are unchanged .

| ID | What changed | Why | When / what had been seen |
|---|---|---|---|
| DEV-001 | Drift generator v1 replaced by v2 (disjoint EVAL / POLICY / CAL pools); the replay filter kept only as a zero-tolerance check  | v1 resampled every synthetic day from the whole root day. The same flow could be an evaluation row of one day and a labelled row of an earlier day (I1), or be reserved on one day and given to the policy on another (I3). Estimated at up to about 2.4 % of the evaluation sample on the smallest root day  | 2026-10-27, before any model was run on any scenario  |
| DEV-002 | Step C: seeded random search (50 configurations) instead of Bayesian search. Tuning on NF-ToN-IoT-v3 2019-04-23..26, which are also root days  | No additional dependency. Shared tuning and root days are a risk of bias of unknown direction (Section 4.4) | 2026-10-27, before any scenario model run  |
| DEV-003 | Pilot GPU budget variable of 5 h instead of 3 h. Measured: 3.03 GPU-hours of scoring (192 days, median 58.4 s per day) plus about 0.7 h of cost measurements  | Scoring plus cost measurements exceeded the 3 h allowance of the request  | 2026-10-27/28, pilot  |
| DEV-004 | Primary test changed from a mixed-model *t* test to the Wilcoxon signed-rank test with the Hodges–Lehmann bound  | Blinded root-day SD of 0.071 by moments vs 0.0024 by MAD (heavy tail)  | 2026-10-28, after the blinded pilot; no mean or direction seen  |
| DEV-005 | CURE's entropy gate driven by the locked LightGBM for both arms  | Same context for both models under every policy  | 2026-10-28, before the main run  |
| DEV-006 | Amendments 1–4: decision rule with ε₁ = 0.02; dependence and symmetry checks; H1b descriptive unless λ and prices are locked; failure classes with S1–S3 and the 5 % limit; cumulative 12-unit budget  | Review of the preregistration draft | 2026-10-28, before the main run  |
| DEV-007 | Audit fixes M2: no AUPRC before the single analysis; checkpoints bound to their inputs; ledger heartbeat; LightGBM scores in float64; synthetic tests (25)  | First audit of the run scripts | 2026-10-28, before the main run  |
| DEV-008 | Audit fixes M3: no metric of either model in the export package; full content hash of every cache file in the inputs of a resumed export; package scan test; `check_lock.py` (27 synthetic tests)  | Second audit of the run scripts | 2026-10-28, before the main run  |
| DEV-009 | Source of the power figures corrected: they come from the exact rule (HL lower bound ≥ ε₁), not from `power_v2.py` (which tests against 0), and are reproduced by `power_v3.py` (4,000 simulations, seed 20261028; Table 3)  | Mislabelled source in the preregistration text | 2026-10-28, during the main run, before the analysis; no change to design or analysis  |
| DEV-010 | Threshold metrics and per-family recall not reported for the H1 comparison; replaced by a descriptive per-family AUPRC_w (`secondary_h1.py`, locked)  | Both need a threshold calibrated on D_cal, and TabFM did not score the D_cal rows. Scoring them would have cost about one more GPU-hour, which was declined  | 2026-10-28, during the main run, before any H1 result; approved 14:09  |

| DEV-011 | Added a descriptive chronological replay of the real development days (14 transitions, 3 seeds)  | Reviewer request: show the TabFM–LightGBM difference on real day-to-day change, not only on synthetic scenarios | 2026-10-28, during the main run, before the primary analysis; addendum and scripts hashed before export |
| DEV-012 | Cost reporting rule: GPU and CPU seconds side by side, never converted; seconds per +0.01 AUPRC_w only if HL ≥ ε₁ and lower bound > 0  | Reviewer: the ratio is unstable near 0, and GPU and CPU time are different hardware | as DEV-011 |
| DEV-013 | Added a descriptive random-split comparison on the DEV-011 evaluation rows  | Reviewer request: compare the protocol with a conventional evaluation on the same rows | as DEV-011 |

| PC1 | Independent exploratory check on CIDDS-001 (separate preregistration; option B: no test, descriptive label)  | Test whether the random-split inflation of DEV-013 replicates on unused data | 2026-10-28, after DEV-013 results; preregistration and scripts hashed before CIDDS-001 was opened; the decision rule was replaced by descriptive reporting before the lock, after a simulation showed that error control was not possible |
| DEV-PC1-001 | Post hoc descriptive analysis of untrainable chronological contexts on CIDDS-001  | Explain why PC1 had too few days, and report what the random splits showed on those days | 2026-10-28, after the PC1 output had been seen; no change to PC1 |

*Table 14. Deviations DEV-001 to DEV-013, the PC1 check and DEV-PC1-001. DEV-001 is in DEVIATIONS.md; DEV-002 to DEV-009 are in the append file prepared for it; DEV-010 is in DEV-010_and_lock.md; DEV-011 to DEV-013 are in the two prereg addenda* .

## References

[1] J. Gama, I. Žliobaitė, A. Bifet, M. Pechenizkiy, and A. Bouchachia, "A survey on concept drift adaptation," *ACM Comput. Surv.*, vol. 46, no. 4, Art. no. 44, Apr. 2014, doi: 10.1145/2523813. 
[2] J. Lu, A. Liu, F. Dong, F. Gu, J. Gama, and G. Zhang, "Learning under concept drift: A review," *IEEE Trans. Knowl. Data Eng.*, vol. 31, no. 12, pp. 2346–2363, Dec. 2019, doi: 10.1109/TKDE.2018.2876857. 
[3] M. A. Shyaa, N. F. Ibrahim, Z. Zainol, R. Abdullah, M. Anbar, and L. Alzubaidi, "Evolving cybersecurity frontiers: A comprehensive survey on concept drift and feature dynamics aware machine and deep learning in intrusion detection systems," *Eng. Appl. Artif. Intell.*, vol. 137, Art. no. 109143, 2024, doi: 10.1016/j.engappai.2024.109143. 
[4] B. A. Alahmadi, L. Axon, and I. Martinovic, "99% false positives: A qualitative study of SOC analysts' perspectives on security alarms," in *Proc. 31st USENIX Security Symp.*, Boston, MA, USA, Aug. 2022, pp. 2783–2800. 
[5] N. Hollmann, S. Müller, L. Purucker, A. Krishnakumar, M. Körfer, S. B. Hoo, R. T. Schirrmeister, and F. Hutter, "Accurate predictions on small data with a tabular foundation model," *Nature*, vol. 637, no. 8045, pp. 319–326, Jan. 2025, doi: 10.1038/s41586-024-08328-6. 
[6] J. Qu, D. Holzmüller, G. Varoquaux, and M. Le Morvan, "TabICL: A tabular foundation model for in-context learning on large data," in *Proc. 42nd Int. Conf. Machine Learning (ICML)*, PMLR vol. 267, 2025, pp. 50817–50847. 
[7] Google Research, "TabFM: Tabular foundation models," software, version 1.0.1, Jul. 2026, https://github.com/google-research/tabfm. Weights: "TabFM 1.0.0 (PyTorch)," Hugging Face model `google/tabfm-1.0.0-pytorch`, revision 77cb9cc1b4fd3a9c77fbb9552c218200bb4dab83. 
[8] I. Gangwani and A. Bansal, "Light-weight benchmarks reveal the hidden hardware cost of zero-shot tabular foundation models," arXiv:2512.00888, 2025. 
[9] Nguyễn Minh Sang et al., "Reassessing tabular foundation models for network intrusion detection under temporal distribution shift: A preregistered evaluation," manuscript under review (v8), 2026. 
[10] X. Bouthillier et al., "Accounting for variance in machine learning benchmarks," in *Proc. MLSys*, vol. 3, 2021. 
[11] A. Lourenço, J. Gama, E. P. Xing, and G. Marreiros, "In-context learning of evolving data streams with tabular foundational models," in *Proc. 32nd ACM SIGKDD Conf. Knowledge Discovery and Data Mining (KDD)*, 2026, pp. 973–982, doi: 10.1145/3770854.3780305. arXiv:2502.16840. 
[12] J. Lee, D. Choi, M. Choi, and J. Yoo, "Bounded context management for tabular foundation models on stream learning," in *Proc. 2nd ICML Workshop on Foundation Models for Structured Data*, Seoul, South Korea, 2026. arXiv:2606.18677. Code: https://github.com/morcellinus/CURE-ICML-FMSD (commit f7c6b2f). 
[13] A. Chrysakis and M.-F. Moens, "Online continual learning from imbalanced data," in *Proc. 37th Int. Conf. Machine Learning (ICML)*, PMLR vol. 119, 2020, pp. 1952–1961. 
[14] F. Pendlebury, F. Pierazzi, R. Jordaney, J. Kinder, and L. Cavallaro, "TESSERACT: Eliminating experimental bias in malware classification across space and time," in *Proc. 28th USENIX Security Symp.*, 2019, pp. 729–746. 
[15] D. Arp et al., "Dos and don'ts of machine learning in computer security," in *Proc. 31st USENIX Security Symp.*, Boston, MA, USA, 2022, pp. 3971–3988. 
[16] G. Andresini, F. Pendlebury, F. Pierazzi, C. Loglisci, A. Appice, and L. Cavallaro, "INSOMNIA: Towards concept-drift robustness in network intrusion detection," in *Proc. 14th ACM Workshop Artif. Intell. Secur. (AISec '21)*, Nov. 2021, pp. 111–122, doi: 10.1145/3474369.3486864. 
[17] M. Botacin and H. Gomes, "Towards more realistic evaluations: The impact of label delays in malware detection pipelines," *Computers & Security*, vol. 148, Art. no. 104122, Jan. 2025, doi: 10.1016/j.cose.2024.104122.
[18] P. García, J. de Curtò, I. de Zarzà, J. C. Cano, and C. T. Calafate, "Foundation models for cybersecurity: A comprehensive multi-modal evaluation of TabPFN and TabICL for tabular intrusion detection," *Electronics*, vol. 14, no. 19, Art. no. 3792, Sep. 2025, doi: 10.3390/electronics14193792. 
[19] J. Qu, D. Holzmüller, G. Varoquaux, and M. Le Morvan, "TabICLv2: A better, faster, scalable, and open tabular foundation model," in *Proc. 43rd Int. Conf. Mach. Learn. (ICML)*, PMLR vol. 306, 2026, pp. 102477–102555, arXiv:2602.11139. 
[20] K. Helli, D. Schnurr, N. Hollmann, S. Müller, and F. Hutter, "Drift-resilient TabPFN: In-context learning temporal distribution shifts on tabular data," in *Advances in Neural Information Processing Systems 37*, 2024. 
[21] I. Žliobaitė, "Change with delayed labeling: When is it detectable?" in *Proc. IEEE Int. Conf. Data Mining Workshops (ICDMW)*, 2010, pp. 843–850, doi: 10.1109/ICDMW.2010.49. 
[22] M. Grzenda, H. M. Gomes, and A. Bifet, "Delayed labelling evaluation for data streams," *Data Min. Knowl. Discov.*, vol. 34, no. 5, pp. 1237–1266, 2020, doi: 10.1007/s10618-019-00654-y. 
[23] J. Gama, R. Sebastião, and P. P. Rodrigues, "On evaluating stream learning algorithms," *Mach. Learn.*, vol. 90, no. 3, pp. 317–346, 2013, doi: 10.1007/s10994-012-5320-9. 
[24] M. Luay, S. Layeghy, S. Hosseininoorbin, M. Sarhan, N. Moustafa, and M. Portmann, "Temporal analysis of NetFlow datasets for network intrusion detection systems," arXiv:2503.04404, Mar. 2025. 
[25] The University of Queensland, "Machine learning-based NIDS datasets." [Online]. Available: https://staff.itee.uq.edu.au/marius/NIDS_datasets/ (accessed Oct. 28, 2026). 
[26] M. Sarhan, S. Layeghy, and M. Portmann, "Towards a standard feature set for network intrusion detection system datasets," *Mobile Netw. Appl.*, vol. 27, no. 1, pp. 357–370, Feb. 2022, doi: 10.1007/s11036-021-01843-0. 
[27] N. Moustafa, "A new distributed architecture for evaluating AI-based security systems at the edge: Network TON_IoT datasets," *Sustainable Cities and Society*, vol. 72, Art. no. 102994, 2021, doi: 10.1016/j.scs.2021.102994.
[28] Canadian Institute for Cybersecurity, “CSE-CIC-IDS2018 on AWS,” University of New Brunswick, dataset description and attack schedule. [Online]. Available: https://www.unb.ca/cic/datasets/ids-2018.html
[29] G. Engelen, V. Rimmer, and W. Joosen, "Troubleshooting an intrusion detection dataset: The CICIDS2017 case study," in *Proc. IEEE Secur. Privacy Workshops (SPW)*, 2021, pp. 7–12, doi: 10.1109/SPW53761.2021.00009. 
[30] L. Liu, G. Engelen, T. Lynar, D. Essam, and W. Joosen, "Error prevalence in NIDS datasets: A case study on CIC-IDS-2017 and CSE-CIC-IDS-2018," in *Proc. IEEE Conf. Commun. Netw. Secur. (CNS)*, Oct. 2022, pp. 254–262, doi: 10.1109/CNS56114.2022.9947235. 
[31] B. A. Nosek, C. R. Ebersole, A. C. DeHaven, and D. T. Mellor, "The preregistration revolution," *Proc. Natl. Acad. Sci. USA*, vol. 115, no. 11, pp. 2600–2606, Mar. 2018, doi: 10.1073/pnas.1708274114. 
[32] L. Bertinetto, J. F. Henriques, S. Albanie, M. Paganini, and G. Varol, Eds., *NeurIPS 2020 Workshop on Pre-registration in Machine Learning*, PMLR vol. 148, 2021. 
[33] E. van Miltenburg, C. van der Lee, and E. Krahmer, "Preregistering NLP research," in *Proc. 2021 Conf. NAACL-HLT*, 2021, pp. 613–623, doi: 10.18653/v1/2021.naacl-main.51. 
[34] M. Kieser and T. Friede, "Simple procedures for blinded sample size adjustment that do not affect the type I error rate," *Statist. Med.*, vol. 22, no. 23, pp. 3571–3581, 2003, doi: 10.1002/sim.1585. 
[35] T. Friede and M. Kieser, "Sample size recalculation in internal pilot study designs: A review," *Biometrical J.*, vol. 48, no. 4, pp. 537–555, 2006, doi: 10.1002/bimj.200510238. 
[36] F. Wilcoxon, "Individual comparisons by ranking methods," *Biometrics Bull.*, vol. 1, no. 6, pp. 80–83, Dec. 1945, doi: 10.2307/3001968. 
[37] J. L. Hodges, Jr. and E. L. Lehmann, "Estimates of location based on rank tests," *Ann. Math. Statist.*, vol. 34, no. 2, pp. 598–611, Jun. 1963, doi: 10.1214/aoms/1177704172. 
[38] W. J. Dixon and A. M. Mood, "The statistical sign test," *J. Amer. Statist. Assoc.*, vol. 41, no. 236, pp. 557–566, Dec. 1946, doi: 10.1080/01621459.1946.10501898.
[39] H. R. Künsch, "The jackknife and the bootstrap for general stationary observations," *Ann. Statist.*, vol. 17, no. 3, pp. 1217–1241, 1989, doi: 10.1214/aos/1176347265. 
[40] R. Y. Liu and K. Singh, "Moving blocks jackknife and bootstrap capture weak dependence," in *Exploring the Limits of Bootstrap*, R. LePage and L. Billard, Eds. New York, NY, USA: Wiley, 1992, pp. 225–248. 
[41] G. Ke, Q. Meng, T. Finley, T. Wang, W. Chen, W. Ma, Q. Ye, and T.-Y. Liu, "LightGBM: A highly efficient gradient boosting decision tree," in *Advances in Neural Information Processing Systems 30 (NIPS 2017)*, 2017, pp. 3146–3154. 
[42] M. Ring, S. Wunderlich, D. Grüdl, D. Landes, and A. Hotho, "Flow-based benchmark data sets for intrusion detection," in *Proc. 16th European Conf. Cyber Warfare and Security (ECCWS)*, Academic Conferences and Publishing International, 2017, pp. 361–369.
[43] W. Kong, E. Louidor Ilan, S. Nie, T. Narayan, R. Sen, Y. Zhou, D. Fu, S. Oymak, and A. Das, “TabFM: A Zero-Shot Foundation Model for Tabular Data,” arXiv:2609.37959, Sep. 2026. [Online]. Available: https://arxiv.org/abs/2609.37959
[44] M. Ring, S. Wunderlich, and D. Grüdl, "Technical report CIDDS-001 data set," Coburg Univ. Appl. Sci., Apr. 2017. [Online]. Available: https://hs-coburg.de/wp-content/uploads/2024/11/WISENT_cidds_Technical_Report.pdf (accessed Nov. 3, 2026).
