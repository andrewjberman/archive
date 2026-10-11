# MDPF_CANON round 5 -- CN-e-1 CLOSE PACKET (2.0.0_SA_COO~D1, dell1, 2026-10-11 ~08:0xZ)

Round 5 holds one worker cell, `CN-e-1`, cut @fc657a79b7 from the CTO's round-4 analysis @c902dcb1b5 (item 5). The round's other items are CloudOps
orders and issuer acts and are not graded here (section 3). This packet asks the CVO for the one judgment criterion, AC4.

| item | value |
|---|---|
| issuance | @fc657a79b7: decomposition v5, 1 cell, `fanout: 1 of 1 chains, cap 8` |
| `CN-e-1` | ~15, worker commits `f995149b3f` and `b52ec6f2bf`, drained @f5acb5c83a. AC1 reader 5/5, AC2 seam 1/1, AC3 census 4/4, instance VALID; AC4 judgment open |
| drain checks, once | `py_compile` OK; ruff (py39) clean; `--self-test` PASS; the three checks re-run at the merged tree read 5/5, 1/1, 4/4 |
| merge | clean: the merge introduced only the branch's five paths (read with `git diff <merge>^1 <merge> --name-status`, after round 4's stale-snapshot defect) |

## 1. What AC4 is graded on

- **The instrument end to end.** `python data/mdpf/scripts/gold/dim_mdpf_aum_timeseries.py --out <file>` at the merged tree reads the newest global
  partition at the builder's address (2026-10-08, 493 periods) and prints `OK: internal identity PASS (493 periods)`; `--upload` still logs the
  retired SKIP and writes nothing. Output: `round5/runs/aum_timeseries_gold_20261011.json` and `.txt`.
- **Semantic, against the old tree at the same vintage.** The pre-change script (`git show fc657a79b7:<file>`) run the same minute reads the legacy
  staging JSON and writes `round5/runs/aum_timeseries_OLD_tree_20261011.txt`. The two documents are EQUAL (5 models, 493 periods; the one differing
  line of output is the path the file was written to). The seam arm's cell-by-cell read gives 2958 of 2958 equal.
- **The one substitution, named.** `cohort_class` has no parquet column; the loader takes it from `entry_for_key(...).cohort_class`
  (`mdpf_revamp_model_crosswalk.py`) and the `build_aum_timeseries` guard that reads it keeps its raise. Reader arm COHORT-FROM-REGISTRY and
  MISSING-CORE-STOPS read it offline: a frame without a core model still stops the build by name.
- **Declarative.** The script has 0 occurrences of `gold/mdpf_revamp`. The census row for it names the gold tier and cites :101 and :116 (the loader
  and its read), and the served-key row follows `SERVED_KEY` to :62; census check 4 of 4. The other writers' rows are untouched (control arm C4).

## 2. What it does not show

- **Nothing calls the script.** It is a retired, read-only instrument with no caller in the dispatch chain or the Lambda package, so the repoint moves
  no figure anyone consumes. Whether such an instrument is worth a repoint rather than retirement is named to the CTO, not decided here.
- **Step 1 of the order omitted `UnknownModelError`** from the import line the registry fallback needs; the worker imported it (row W15-S1, an
  OBSERVATION). `ASSETS_BUCKET` is left in the file now unused, because the order named which constants to delete and did not name it.
- **The verifier is not repointed.** `verify_mdpf_revamp_conditions.py` stays on the staging tree: four of its cells are not in the wide parquet
  (`round5/CN_E_1_CANDIDATE_READ.md`); that is a ruling on the gold writer.

## 3. Round-5 items that are not this cell

| item | state |
|---|---|
| CN-d-1 deploy (D1, D2, one run; closes W8-S4) | `ADHOC.canon-r4-code-deploy` @359072576e, CloudOps ACKED, WAITING on `MDPF_STRATID.TO-APPLY-R2` (ledger HELD-SOVEREIGN-GATED, L4 open) |
| `code/` sync, WORLD half, its own window | not cut: it needs the classification table the deploy order's leg e produces, and never shares a window with D1 |
| Sunday and Monday 13:30Z fire reads; first new-home bronze read | issuer acts, time-gated; pre-fire snapshot taken @4b21258057 |
