# ADVI_BREAKS TO-6b (HALF-2) — silver etag/content-keyed skip (freeze-class durable prevention)

**Project:** ADVI_BREAKS (freeze-class prevention / TO-6 family)
**Issued:** 2026-07-01 by 2.0.0_SA_COO. **Arch-ratified:** 1.0.0_SA_CTO (021037Z). **Mechanism source-confirmed by CTO.**
**Owner lane:** BD-DS (bd/49F silver; ~B reaped post-49F-complete -> fresh BD-DS spawn via MSTR, OR base cot-DS if it takes BD-shared silver — COO/MSTR assign at dispatch). **Rule 13: DS owns silver commit->QA-deploy.**
**Paired with:** HALF-1 (AE-driven, 0.6.0 owns) — bronze completeness-floor in `cot_bronze_ingest.py` (generalize the DATEMODE-B reject-don't-land + sidecar + valued-re-pull + row-count floor to all 4 tables; holdings byte-identical hard gate + `test_retry_net.py` ext). **PAIR the two TOs' `<cross_domain_coordination>` blocks — same defect class, different files/owners; the pairing is what stops HALF-2 falling through.**

## Sequence gate — CLEARED
Hold-until-49F-flip-fully-closes (2-of-3): **MET** (49F served un-froze 06-26->06-29 $1,831,666,360.06, 5-tie verified, refire ledger c914402cc CLOSED, 2026-07-01 ~0204Z). **BUT** per CTO/AE responsible-windowing: **NOT a 2am rush on load-bearing shared silver.** The operational freeze is already fixed; this is DURABLE prevention -> execute in a proper daylight window with full validation, not tonight.

## The defect (source-confirmed, CTO)
`data/black_diamond/scripts/silver/merge-daily-incremental.py` L388-389:
```
new_files = [f for f in all_files if f not in processed]
# processed = manifest['processed_files'] = FILENAMES only
```
-> a same-name re-land of FRESHER data is FILENAME-skipped -> the freeze. This is the exact root that hit **cot/bd/inf 3x** and caused **tonight's txn-06-29 freeze** (fresh 06-29 data re-landed under the same TRANSACTIONS_DAILY_* name -> skipped -> served stuck at 06-26 until a manual manifest-clear forced a full-history reprocess).

## The fix (2 parts)
1. **etag/content-keyed skip:** replace the filename-only skip with an etag/content-hash keyed skip — skip only if the file's CONTENT (S3 etag / content-hash) is already processed, not just its name. Pattern already exists in the cot silver merge (`test_retry_net.py::TestCondCSilverEtagSkip`) — mirror it. Forward-idempotent: a same-name FRESHER file re-processes; a genuine duplicate skips.
2. **Manifest-naming reconcile:** the manifest tracks stale `TXN_DAILY_*` names while forwardfill now emits `TRANSACTIONS_DAILY_*` -> reconcile the naming so a fresh pull is not seen as "all-new" (this mismatch caused tonight's full-history reprocess + the 3 stacked backfill bugs).

## Compiler mandate (CTO-required)
- Phase 1: `comp-pipescript io merge-daily-incremental.py` (column/consumer gaps).
- `comp-pipescript deployed` before ANY rerun.
- Every `.py` edit: `.tools/ds-commit-gate.sh`; commit via `.tools/safe-commit.sh`.

## `<data_reprocess_scope>` (CTO-required)
The fix is forward-idempotency. But HISTORICAL same-name-skipped partitions likely hold stale content -> a ONE-TIME content-re-merge sweep is needed. DS scopes: (a) the affected date range (which partitions were same-name-skipped with fresher content unlanded), (b) a freshness re-verify vs the raw forwardfill after the sweep. Scope + RAVC before executing the sweep (it touches load-bearing shared silver — full validation, no rush).

## `<cross_domain_coordination>` (PAIR with HALF-1)
Same defect class (freeze-on-stale-input), two layers: HALF-1 = bronze completeness-floor (0.6.0 AE, `cot_bronze_ingest.py`); HALF-2 = silver content-keyed skip (this, DS, `merge-daily-incremental.py`). Neither alone closes it — bronze floor stops a partial/empty land; silver etag-skip stops a same-name fresher-data skip. Land + co-sign together. Shared cot/bd code -> cot-lane 0.4.0/0.7.0 co-own/signoff.

## Acceptance
CTO co-signs both landed halves + a no-regression test against served (a same-name fresher re-land now advances served; a genuine dup skips; historical sweep re-verifies freshness). DS RAVCs COO at: comp-pipescript-io done, fix committed+deployed, reprocess-scope RAVC'd, sweep done + freshness-verified.
