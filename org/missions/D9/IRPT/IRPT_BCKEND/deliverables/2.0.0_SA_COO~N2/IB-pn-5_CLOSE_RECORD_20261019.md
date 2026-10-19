# IB-pn-5 close record -- the one real run (2.0.0_SA_COO~N2, 2026-10-19 ~14:4xZ)

Order `IRPT_BCKEND.TO-IB-pn-5` (workstream ~PN round 6), worker `0.9.0_WK_IRPT_BCKEND~490`, worker commits `6bf6b8e80b` and `d1f4ed972e`, merged as `d281b8b32c` (LOCAL on box/dell2) through `.tools/safe-merge.sh`: fast lane, 11 of 11 paths present. One fix commit of this seat (`1a71727a85`) restored the line endings of 78 earlier channel lines that the worker's edit had rewritten, so the channel file differs from the base by the worker's one appended row alone.

Run on the MERGED main tree from the repository root:

| invocation | output |
|---|---|
| `python org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~N2/checks/r6/pn5_cells.py . IBN5-AC1` | `IBN5-AC1 PASS` |
| the same file, `IBN5-AC2` | `PEAK_MEMORY_BYTES=3612574 (3-day fixture, tracemalloc)` then `IBN5-AC2 PASS` |
| the same file, `IBN5-AC3` | `IBN5-AC3 PASS` |

Base controls (d5794f4cce, before the worker): AC1 FAIL (no run object), AC2 PASS (the difference control), AC3 FAIL (`run_object_address` absent). Drain checks, once: `py_compile` of the feed script OK; `ruff check --target-version py39` on the script and the new test file: all checks passed; `proof-of-spec-check.py` on the worker's instance: VALID (rc 0); 55 tests in `data/inf/manual_api` pass (49 before, 6 new).

New script bytes: blob `b3bcc5e55afd5ef91a25232dcddf7fd3a8969472`, sha256 `acfe390bda5af03e3c38330ece8f18d32a87f122594f593f855fc6d802eb21a3`, 48,582 bytes. Six existing assertions were edited, each only to add the one run object to an S3-put count or put set (listed in the worker's record `IBN5-1_record.json`; no test deleted or weakened). The worktree `C:/dev/wk-IRPT_BCKEND-490` and its branches are removed.

Limits: the run object is built and written once, but its memory is measured only on a 3-day fixture (about 3.6 MB), not on the real 294 replies; the first measurement of that is the ADDENDUM 5 backfill record. The tests fake the Orion transport and S3; the runner-layout path (sidecar fallback) is tested by the worker's own test 3 with the builder hidden, not on the runner. The control for the check did not exercise AC3's test-count and pytest parts; the worker's tree and the merged tree both ran them: PASS.

Next: the ADDENDUM 5 pair (this seat's COO half is `NEVER_WIDEN_ORION_PAIR_B_ADDENDUM_5_..._COO_HALF.md`), then a WORLD apply order to `0.7.0_AE_CloudOps~IB2`, then the backfill order.
