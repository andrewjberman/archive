# Orion delta-6 drain -- WS-A1 leg-close record

**Serial:** 0.7.0_AE_CloudOps | **Date:** 2026-07-15 | **P0 workstream:** WS-A1 (OPAL_CONSOLIDATION)
**Closes:** orion silver parity leg (delta-6 STEP A4 drain, CTO GO 20260715T143910Z).

## Deploy chain (STEP A, CTO-ACCEPTED 154104Z)
- Source: 782001d30 (BUILD_MANIFEST + re-vendored mirror_conversion + stream_parquet.py vendored + source-map files[]).
- Build: write-VERIFIED artifact sha `rwI6QN5qzT30lWZrf87RlSOEl5XmSGkCTUTdlljqDPo=` (size 38193); ci-sha commit d9e24318d.
- Apply: TF plan 0/1/0 (module.silver_converter["orion"] source_code_hash only; memory/timeout/runtime UNCHANGED = 10240/600/py3.11); safe-apply; live sha == source-map == built zip; 0-diff re-plan; record-deploy 554518e12; tag **opal-assets-v0.16.0** pushed.

## STEP A3 runtime-confirm (envelope AC PASS, CTO-ACCEPTED)
Real conversions of the 1.39M-row 07-10 unit on the DEPLOYED artifact: **Max Memory Used 1131 / 1127 MB, Duration ~91 s** (CW REPORT). 1131 << 3008 (1877 MB headroom); 91 s << 600 s. Pre-streaming code OOM'd at BOTH 3008 and 10240 on this exact unit -- delta-6 streaming resolves it. Host->runtime deltas: +14% RAM, +93% wall vs DS dev-host (988 MB / 47 s).

## STEP A4 drain (this record)
- Mechanism: per-partition async event fan-out over all 58 orion `transactions` units (idempotent, force=False; a single run_sweep would self-timeout at 58 x ~91s >> 600s -- the Gap-A pattern now in the arch doc Section 5b).
- Result: **58/58 `fact_transactions` partitions landed.** Content census: byte sizes 27.2 MB (05-12) .. 31.3 MB (07-04), **min 27,183,918 B -- NO shell partitions** (every partition carries real ~1.3-1.4M-row content).
- DLQ: 5 transient throttle messages during the async flood **self-cleared to 0/0** (concurrency-2 back-pressure, not conversion errors); final `dlq_drained` = 0.

## Authoritative reconciliation (sweep 20260715T163036Z-d169038f)
The conservation instrument (contract Section 5 / V2-7 AC3), run AFTER the drain:
```
set_identity: verdict=PASS  expected=4640  landed=4640  matched=4640  missing=[]  alien=[]  holes=0
converted=0 (all landed via the event drain)  dlq_drained=0
backfill-status.json written (single-writer, sweep path)
```
**Orion silver = FULL PARITY 4,640/4,640.** Manifest: `orion/inflection/meta/conversions/20260715T163036Z-d169038f.json`.

## Leg-close bar (CTO 154104Z)
- [x] Full drain: 58/58 transactions converted, 0 named refusals.
- [x] set_identity PASS (independent sweep reconciliation, 4,640/4,640).
- [x] Content grounded (no shells; DS holds the 8th pin = 1.39M-row 07-10 content verify).
- [ ] CTO's own listing==4,640 census (his side).
- STEP C resize 10240->3008 rides the post-22:00Z batch (1131 MB runtime datapoint greenlights it).
