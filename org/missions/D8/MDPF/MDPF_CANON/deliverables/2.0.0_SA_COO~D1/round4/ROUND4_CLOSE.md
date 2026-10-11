# MDPF_CANON round 4 -- CLOSE (2.0.0_SA_COO~D1, dell1, 2026-10-11 ~06:5xZ)

Round 4 is the CTO's round-3 analysis (msg 3530 @ae094ea51d) as re-cut by ADDENDUM 1 @187b53dbe6 (msg 3542), cut in one issuance @73fdbf8d0a
as five cells. Three judgment criteria are open; this packet asks the CVO for them. The Monday fire read and the first new-home bronze read
are the issuer's acts and are not graded here (section 4).

| item | value |
|---|---|
| issuance | @73fdbf8d0a: decomposition v4, 5 cells, `fanout: 5 of 5 chains, cap 8`; status staged -> pending @fdc574c044 |
| amendment | 1 @b184f33ea9 (row W13-S1): the proof instance is named beside the order's own file stem. Gate limb: none graded a modification (placeholders NONE) |
| `CN-d-1` served identity + cottonwood vintage | ~10, drained @9ecb1d4a66, closed @e539c44419. AC1 5/5, AC2 3/3, proof VALID, no judgment |
| `CN-d-2` the X2 basis counts carries | ~11, drained @24e8981f2f. AC1 4/4, proof VALID; AC2 judgment open |
| `CN-d-3` portal additive bands | ~12, outer record drained @54e1fc41d8; candidate on nested branch `wk-MDPF_CANON-12-portal` @133fb8af. AC1 4/4, AC2 5/5 (read in that worktree); AC3 judgment open |
| `CN-d-4` the audit reads the gold artifact | ~13, drained @68e13832ab. AC1 3/3, AC2 2/2 (3388 cells per firm DELTA=0), proof VALID; AC3 judgment open |
| `CN-d-5` the runner `code/` equality tool and step | ~14, drained @0468b6c8ba. AC1 5/5, AC2 2/2, proof VALID, no judgment |

Drain checks at the merged tree, once: `py_compile` on the 5 touched python files OK; `ruff --target-version py39` clean; `pytest
data/mdpf/tests/stratid data/mdpf/tests/taxsma data/mdpf/tests/canon` 272 passed. `round-close-check.py --round 4` is read below.

## The real runs (what each open criterion is graded on)

- **CN-d-2 AC2:** `deliverables/0.9.0_WK_MDPF_CANON~11/X2_GLOBAL_BASIS.md`. Entries read 41; held 37; carries 2 (`opal_growth_sma` 45 and
  `opal_div_sma` 40 accounts, `count_as_of` 2026-07-17, age 58 trading days, held by no firm); null 2. `by_model` min firms reads 1 over the
  held entries (it read 0 in the round-3 file). The ledger X2 row cites the new path; its status, decider and date are unchanged. The grade
  asks whether a seat that did not write the file reads back every `min firms` integer, each carry row and each single-firm count equal.
- **CN-d-3 AC3:** render of the candidate, `round4/runs/cn_d_3_global_trend_candidate_133fb8af.png`.
  - Instrument: the portal dev server on port 5174 from the candidate's worktree, `scripts/ui-smoke.mjs portfolios --click Trend`.
  - Fixture: one served object, global `aggregate-aua-timeseries` of 2026-10-08, read-only get, matched on the page's own URL (1 of 1).
    The page's other requests were not stubbed, so the category-views panel reads "could not be loaded"; that panel is not this cell's.
  - Read: the legend names `Additive SMA sleeves` and `Tax-Managed SMA` after Other AUA; the quarterly bars and the daily area show a thin
    band above Other AUA on the additive dates (24 non-null `sma_additive_aua`, from 2026-08-26; 7 non-null `tax_additive_aua`).
  - Not shown: the tooltip was not exercised in this render, so "tooltip rows add to the Total on a sampled additive date" is open for the
    grade. The two band colours resolve to #6366f1 and #ff4f1f (worker row W12-S1 notes no collision with another series' hex).
- **CN-d-4 AC3:** `round4/runs/count_source_audit_20261011.txt` (`--firm all`, the repointed audit at the merged tree) beside
  `count_source_audit_OLD_tree_20261011.txt` (the file as it stood at @73fdbf8d0a, same vintage, same minutes).
  - The two outputs are 91 lines each and differ on ONE line: the unaudited-firm line reads `['cottonwood']` where the old tree's listing
    read `['_aggregate_aua', '_audit', 'cottonwood']` (two staging-tree meta directories that were never firms), and its wording now says
    "the gold tier". Every audited-date denominator and DISAGREEMENT count is identical (36 of 93 and 38 of 39 audited).
  - Both runs end `AUDIT RESULT: DISAGREEMENT(S) FOUND` (exit 1). That verdict is the standing finding of the audit, present before this
    cell; the cell does not move it and does not claim to.
  - Not read: `verify_mdpf_revamp_conditions.py`, the census row's other reader, is not examined and is a later slice.
- **CN-d-1 and CN-d-5** carry no judgment criterion. Their real runs are `r4_cn_d_1.py` arm A4 (the new function over the served 2026-10-08
  global object: the 4-term identity holds on 484 non-null dates) and the tool's own whole-tree run:
  5 trees, 77 files, 48 equal, 29 not equal (gold 33 of 48 equal, backfill 7 of 11, feeders 4 of 5, bronze 2 of 2, config 2 of 4).

## For the CTO at L10 (not this packet's ask)

- **Item 4's close, restated.** "`code/` reads equal to the repo" is not a coherent close on measurement: the 29 non-equal names are mostly
  not runner members (QA tools, a bundle-shipped file, non-.py data). The close held is: every file the dispatch chain executes or reads is
  EQUAL, and every other non-EQUAL name is listed with its reason. The repo half is landed (`.tools/mdpf-code-equality.py`,
  `docs/deployment/MDPF_RUNNER_CODE_SYNC.md`); the WORLD half is a CloudOps order cut after `MDPF_STRATID.TO-APPLY-R2` reads CLOSED.
- **CN-d-1's deploy** carries a never-widen pair (CTO + COO): the global account-distribution gains `meta.cottonwood_fold.value_date` and
  `age_trading_days`; no served value moves. Rollback per key is the prior object's VersionId.
- **CN-d-3 is a portal candidate for the CTO's review before DEV** (a product file): nested branch `wk-MDPF_CANON-12-portal` @133fb8af, two
  files, +52 -3. Landing is the CTO's; it was not pushed.
- **Row D1-S16:** `safe-merge.sh --continue` committed a merge from a stale snapshot after a peer commit landed and reverted 7 of that
  peer's paths; restored byte-exact @c190e6faf8 under the audited lane override. The tool is `0.0.0_AB_MSTR`'s.
- **Rows carried:** W10-S1..S3 (docstring-by-addition under TXA1-AC4; the refusal's difference text; the order file outside the worker's
  paths), W12-S1 (the nested portal repo has no committer identity), W13-S1 (resolved by amendment 1), W14-S1 (the `--files` denominators).

## Carried (not this round's acts)

1. **Gold fire reads:** Sunday 2026-10-11 13:30Z and Monday 2026-10-12 13:30Z with `r2_daily.py read --fire <ISO>` after a snapshot taken
   before the fire. Monday is the first that builds global at Friday's frontier (D1-S10 ruling); its read grades FWD-1, CN-a-2 AC3 and
   closes D1-S9 and D1-S10.
2. **First new-home bronze delivery:** `round4/checks/r4_daily_bronze.py --run-date <D> --since <ISO>` after that day's dispatch.
3. **FWD-3** stays NOT REALIZED at Andrew's X2 call (open call fe9b).
