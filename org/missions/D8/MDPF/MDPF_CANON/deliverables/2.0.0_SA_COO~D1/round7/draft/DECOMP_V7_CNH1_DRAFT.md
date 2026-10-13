# DRAFT -- NOT APPENDED. The v7 decomposition row for CN-h-1, to be appended to `decompositions/MDPF_CANON_DECOMP.md` at the issuance that cuts it
# (round 7, or a round-6 recut if the CTO so rules), after the fold's first scheduled fire is read. Written by a fork of 2.0.0_SA_COO~D1, 2026-10-13 ~11:4xZ.

| cell | serves (cell_refs) | candidate | owned files | depends on | actor |
|---|---|---|---|---|---|
| `CN-h-1` the frontier account counts read the newest A4 account-distribution at or before the axis date, never the staged runner object; no A4 -> the loader returns absent, never a fallback (S5 disarm; WORLD: a script shipped by a deploy) | FWD-5 (the lambda's inputs leave the runner-only objects); FWD-1 (the served counts are the day's roster) | M4 / S5 (MDPF_TAXSMA-S5) | `data/mdpf/scripts/gold/dim_mdpf_aggregate_aua_timeseries.py`, `data/mdpf/scripts/gold/tests/test_canplat_p1_1.py` and `test_global_fold_flag2.py` (one stub lambda each), `data/mdpf/tests/canon/test_frontier_counts_a4.py` (new) | -- (a deploy-order edge: after the fold's first scheduled fire is read; one change per fire) | ~17 (worker-light) |

**Fan-out:** 1 of 1 chains, cap 8. Reason: one behaviour, one file, about 40 product lines.

**Why this and not the nine-key sync / Stage 6:** the CTO's ADDENDA 4-5 ruled out a Stage 6 revival and moved the S5 disarm to the lambda's input. The
read `round6/TAXSMA_S5_STAGE6_READ.md` @7de2c1aa99 shows Stage 6 has been dead since 2026-08-14 for three stacked reasons; this cell removes the
lambda's dependence on its output instead.

**Close (carried to the CTO):** S5 reads DISARMED when, on the first scheduled fire after the deploy that mints a new date, every overridden key's
served frontier `account_count` equals the selected A4 map's value, the stamp's as-of is the A4's period, no staged object was requested, and the
per-scope moves equal the pair's table within the stated A4 key date.

**Not in this cell:** Stage 6 and everything that revives it; the nine `lib` keys; the IAM change on the runner role; `dim_mdpf_account_distribution.py`;
the staged object's retirement (M12); W2 L3's runner-log half (parked at M10 by the CTO).

**Checks:** `deliverables/2.0.0_SA_COO~D1/round7/checks/` (drafts at `round7/draft/checks/`). At base: `r6_cn_h_1.py reader` 1/8 (H0 a control), `seams`
1/4 (S4 a control), `comparator` 1/5 (K0 a control). A scratch reference tree (`checks/ref/make_reference_tree_h1.py`, never committed to product
paths) reads 8/8, 4/4, 5/5.
