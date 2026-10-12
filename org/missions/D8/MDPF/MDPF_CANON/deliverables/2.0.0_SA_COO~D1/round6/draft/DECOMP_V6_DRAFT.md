# DRAFT -- NOT APPENDED. This is the section text to append to `decompositions/MDPF_CANON_DECOMP.md` at the round-6 recut, after the
# CTO's round-5 analysis lands. Items in [AT RECUT] are filled from that analysis; nothing else here waits on it.

## v6 -- ROUND 6 (issuer 2.0.0_SA_COO~D1 on DELL1, [AT RECUT: date/time])

**Rectangle:** `ledger/ROUND_ANALYSIS.round5.md` [AT RECUT: @hash, msg] section 3 (the CTO's enrichment list) and, for the fold cell, the CTO's
record `org/tier1_exec/1.0.0_SA_CTO/deliverables/RECORD_FE9B_RULED_BY_CLUSTER_LEAD_20261012.md` ADDENDA 1-4 (cluster lead ruling (A) on open call
`dell1-20261011T053810Z-fe9b`; msgs 4393, 4398, 4414, 4418, 4422), read with the issuer's design `deliverables/2.0.0_SA_COO~D1/round6/FOLD_DESIGN.md`
@2f702bb7ff and `FOLD_ADDENDUM2_READ.md` @01b9e95401 and the corrections in the order's ISSUER NOTES.
- The fold is ONE cell, `CN-f-1`: the Global min-firms fold. It serves FWD-3 (the X2 grant's basis, "aggregate counts only"); row `D1-W8-S5`
  disarms on its read-back, and open call fe9b closes on it.
- [AT RECUT: the analysis's other enrichment items, one line each; the CloudOps orders are not cells.]

| cell | serves (cell_refs) | candidate | owned files | depends on | actor |
|---|---|---|---|---|---|
| `CN-f-1` the Global min-firms fold: per date, a model-class line is shown only where >= 2 firms hold it; the rest fold into `other_models`, itself shown only where >= 2 firms hold it; the differential identity asserted fail-closed (WORLD: scripts shipped by a deploy; an `infra/` file) | FWD-3 | M7 / fold (fe9b) | `data/mdpf/scripts/gold/{mdpf_gold_consolidator,dim_mdpf_account_distribution,dim_mdpf_aum_metrics,mdpf_revamp_model_crosswalk}.py`, `infra/aws/lambda/opal-assets/opal-assets-daily-emitter/mdpf_revamp_model_crosswalk.py` (second home, byte-equal), `data/mdpf/tests/canon/test_global_min_firms_fold.py` (new) | -- (a deploy-order edge, not a data edge: see below) | ~16 (worker) |

**Fan-out:** 1 of 1 chains, cap 8. Reason: one behaviour with a cross-file contract (`fold_keys` / `fold_emit` between the consolidator and the
distribution builder); splitting would put that contract between two workers who share the consolidator.

**Why not split the document half:** the account-distribution pooling and the aum-metrics row are consumers of the fold set the consolidator
computes; each is ten to forty lines. Three workers on three files would need the function names fixed first, which is what the order does.

**What the cell is, in one paragraph:** `apply_global_min_firms_fold(arts, firm_scopes, min_firms=2) -> (arts_out, report)` in the consolidator,
called through `guard_global_min_firms_fold(arts, _isolated)` directly after `guard_global_served_identity`, so a refusal refuses Global alone.
The held predicate is the firm's own `model_value > 0` on that date; the as-of fold set is computed from the objects on every run; per date, a
line held by fewer than two firms goes to the pool; the pool is emitted as `other_models` only where two firms hold it; the dollars that leave
are suppressed, never redistributed; the differential identity `model_aua - sum(by_model)` moves by exactly the suppressed dollars on every
valued date or the build refuses. SMA-class lines and `tax` are untouched (the SMA tree already serves `by_firm` by Andrew-direct ruling).

**Deploy at the drain** (CloudOps ~DELL1, a WORLD order the issuer cuts after the drain; never a worker): the code lands by the CN-d-1 deploy
order's own shape (named files through `safe-deploy.sh`, the gold package through `build_package.py --pin <the merge commit>` and a targeted
`safe-apply` on `mdpf-gold-lambda`, one on-demand run read before and after) AFTER `ADHOC.canon-r4-code-deploy` reads CLOSED (both change
`mdpf_gold_consolidator.py`; two acts never copy one key in one window), in its OWN window, touching none of the router, guard, CloudFront
behaviours, `bronze_homes.json`, `firm-config.mjs` or the WAF rider before FIRMBKTS's flip receipt passes ownership (PRD v2.11 R2). It carries a
never-widen pair (CTO + COO) whose blast radius is the four global aggregate objects and the global gold parquet partitions FROM THE FIRST
NEW-DATE FIRE ONWARD; no firm scope, no staged object, no dated key already served (they are immutable and keep their one-firm lines; the reader
read found no served reader of a pre-fold dated object, so no retro-fold). The pair names the writer count (N = 8 across 7 leaf classes), the
three branches (flips-and-identity pass publishes; a refusal leaves the prior Global object served and the firm scopes publish; a fault is the
same), the per-key rollback (the version id of the prior object) and the client-visible deltas the CTO accepted: Total Holdings -185, archetype
cards -$43.16M in all, per-model trend and the core models' quarter cells beginning 2026-05-15 (the quarter cells are an open item, below).

**The close, restated (carried to the CTO in the L10 message):** FWD-3 reads REALIZED when (a) the first scheduled run after the deploy serves a
global aggregate-aua-timeseries on which no model-class line is held by fewer than two firms on any date it carries a value (the comparator's
K6 and K7 on that object), (b) the identity differential read-back holds on every valued date, (c) the in-band statement is present and names
no model, and (d) the round-4 close stands (every file the dispatch chain executes or reads is EQUAL; every other non-EQUAL name is listed with
its reason).

**Open items carried to the CTO with this draft (not decided here):**
1. ADDENDUM 1's refusal on a non-zero flip count and ADDENDUM 3 (b) cannot both bind: on the real 2026-10-09 object each core line has 392 earlier
   dates held by fewer firms while the as-of holds >= 2, which under (b) are simply the folded dates. The cell reports flips and refuses on
   the identity and the >= 2 assertions.
2. ADDENDUM 4's "model_aua - sum(by_model) == suppressed to the cent" read absolutely cannot pass on today's object (208 of 485 valued dates carry
   a pre-existing residual of a cent or two, max 0.02). The cell asserts the DIFFERENCE the fold makes.
3. The core models' aum-metrics quarter cells follow the per-date rule: q2 (2026-03-31) and q3 (2025-12-31) of the 2026-10-09 object fall before
   2026-05-15, so 10 of the 20 core quarter cells render absent (an existing honest-None state). The accepted deltas named the trend and Total
   Holdings, not these.
4. The union predicate would emit a pool of one firm's per-date-folded core dollars plus a trace of a second firm's custom line (measured: 0
   dates on the real history). Say whether that is intended.
5. The second crosswalk home is a deployed package read by the emitter lambda (`channel_sources.py`, `lambda_function.py`): the CloudOps order
   names whether the emitter is re-packaged or the home lands as repo parity only.

**Checks:** `deliverables/2.0.0_SA_COO~D1/round6/checks/` (drafts at `round6/draft/checks/`). At base (HEAD of box/dell1): `r6_cn_f_1.py contract`
0/10, `seams` 0/6, `r6_cn_f_1_comparator.py` 1/11 (K0 is a control and passes: the served objects read and the pre-fold residual is within $0.02
on every valued date). A reference tree (`checks/ref/make_reference_tree.py`, never committed to product paths) reads 10/10, 6/6 and 11/11 (the
arms can pass; the comparator on the REAL 2026-10-09 objects reads fold set 11, other_models emitted on 47 dates and not shown on 438, per-model
detail beginning 2026-05-15, identity checked on 485 dates with 0 gaps). Three planted defects turn it red: the fold line never suppressed (K6;
contract C2, C3, C4, C10), pooled dollars dropped with the cell's own identity refusal disabled (K4, K5; contract C2, C3, C10), and a removed
model's name left in free text (K7).

**Not provable offline (graded after the deploy, AC4 and the pair's read-back):** the pooled account-distribution statistics (need the
account-level vectors from silver), the category-views Custom node, the gold parquet column set, and the Model Portfolios page on a missing key.

**Not in round 6:** [AT RECUT: from the analysis]. M3's full-history clause; M6 (HELD on `LGIC_NAMING-S7`); M9 and M10 (`ADVI_FIRMBKTS`); M11-M17.
