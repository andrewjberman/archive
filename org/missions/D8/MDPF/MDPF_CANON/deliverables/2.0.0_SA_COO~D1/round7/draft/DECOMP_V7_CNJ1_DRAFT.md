# DRAFT -- NOT APPENDED. The v7 decomposition row for CN-j-1 (the FWD-9 history leaf), to be appended to `decompositions/MDPF_CANON_DECOMP.md` at the round-7
# issuance, after the CTO's round-6 analysis. Written by a fork of 2.0.0_SA_COO~D1, 2026-10-13 ~21:2xZ.

| cell | serves (cell_refs) | candidate | owned files | depends on | actor |
|---|---|---|---|---|---|
| `CN-j-1` the history leaf: one read-only served series per scope (`platinum/mdpf/{scope}/category-views-history.json`: `dates[]` plus the two Client aum arrays) assembled by the publisher from the dated category-views objects it already lists; absent is null, a malformed dated object is omitted and named (WORLD: a publisher package deployed by CloudOps; four new served keys) | FWD-9 | M7 / FWD-9 Client chips (history route; CTO msgs 5086-5088) | `infra/aws/lambda/opal-assets/opal-assets-mdpf-portal-publisher/lambda_function.py`, `.../tests/test_completeness.py` (three serve-write filters only), `.../tests/test_history_leaf.py` (new) | -- (a deploy-order edge to `CN-i-1`: its Client chips draw the history from this leaf once served; `CN-i-1` ships as-of first without it) | ~17 (worker) |

**Fan-out:** 1 of 1 chains beside `CN-h-1` and `CN-i-1` (no shared file: `CN-h-1` owns `dim_mdpf_aggregate_aua_timeseries.py` and its tests; `CN-i-1` owns portal files); 3 of 3
independent chains if the three are issued in one round, cap 8.

**What it is not:** the portal fetch and the chips (`CN-i-1`); any consolidator, gold-lambda or edge change; a change to the artifact-type axis or `a4_expected` (the leaf is not a gold
type); a repair of the publisher's unreadable pointer (a separate finding, its own pair).

**Close (carried to the CTO):** FWD-9's Client-chip history reads exercised when the four leaves are served and equal the dated Client nodes, every existing served leaf is unchanged
apart from `_provenance.written_at`, and the Trend (`CN-i-1`) draws the chips on the leaf's dates and absent elsewhere on `bun run dev:live` at a stated portal commit.

**Checks:** `deliverables/2.0.0_SA_COO~D1/round7/checks/` (drafts at `round7/draft/checks/`). At base: `r7_cn_j_1.py unit` 0/6, `seam` 3/8 (S2 pairs unchanged, S7 no served-plane read
beyond the pointer, S8 the publisher's own 12 tests are controls that hold), `real` 2/6 (R0, R2 controls: the 91 dated objects read; both Client nodes on every one). A scratch reference
(`checks/ref/make_reference_publisher_j1.py`, never committed to product paths) reads 6/6, 8/8 and 6/6; `selftest` prints OK with two planted mutants RED (a missing node read as 0.0 -> U3;
a leaf that ignores the pointer -> S3).

**Not in this cell:** the portal side; the readback script `round7/checks/r7_history_readback.py` (owed before issuance); the CloudOps deploy order and the pair's CTO half.
