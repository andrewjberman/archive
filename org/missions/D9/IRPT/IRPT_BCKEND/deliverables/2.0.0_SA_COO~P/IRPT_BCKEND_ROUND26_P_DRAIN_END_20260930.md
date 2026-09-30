# IRPT_BCKEND round 26 (~P) -- the issuer's drain-end record (spine L8 input; the CVO's channel compile is its own artifact)

**Issuer:** `2.0.0_SA_COO~P`, 2026-09-30 ~17:0xZ. **Issuance:** @f54e17e4c6 (decomposition section 24, three cells). **Analysis it answered:**
`ledger/ROUND_ANALYSIS.round25P_sweep3_4.md` @dd4c69b696.

## The three cells, terminal

| cell | order | terminal state | evidence |
|---|---|---|---|
| `IB-pr-261` | TO-IB-pr-261 (WK~97) | COMPLETE @65144605a4 on `wk-IRPT_BCKEND-97`; drained into CLOUD at the hash stated in the slug | P26-1-AC1 PASS (2 targets sha-equal on S3, 6 collision probes 404); P26-1-AC2 PASS (run `chain_full_20260930_145412`: `INF_API_SILVER_REPS` ok, `INF_API_PULL_POSITIONS_DAILY` ok, `bronze/positions/2026-09-30.jsonl.gz` 2,309,545 bytes at 15:18:55Z); P26-1-AC3 PASS (ledger `inf-silver-ids-ship-20260930` CLOSED, 3 legs). The two readings the CTO required are in `deliverables/0.9.0_WK_IRPT_BCKEND~97/RESOLUTION_READINGS.json`: the deployed dispatch equals the repo (sha `d6b00f6fdd75...`), `sync_scripts()` flattens by basename into `/tmp/orion_gold_scripts`, and the traceback shows `lib` resolving as a namespace package with no `lib/` anywhere on the box's path -- so the ship is `code/silver/silver_ids.py` (a byte copy of `lib/silver_ids.py`) beside its importer, whose import reads `lib.silver_ids` first and falls back flat. `safe-deploy.sh` refused on its HALT gate (row W97-S2, the refusal text recorded); the order's `aws s3 cp` fallback was used and both objects read back sha-equal. |
| `IB-pr-262` | the issuer's served move | APPLIED 2026-09-30T16:19:48Z | packet `NEVER_WIDEN_SIGNOFF_PACKET_INF_LAUNCH_MONITOR_EMPTY_REASON_20260930.md` @e0a2f524e4 (blob 1bc65b9b16); CTO half @0386ab930c (six conditions), COO half in the packet; targeted safe-apply 0/1/0 on `module.inf_ec2_launch_monitor`; readback CodeSha256 `t1QrzaDeMtjGgnFL0oez1DGtL6vLVz7fgV0/BMVuIQo=`; re-plan No changes; apply ledger `inf-launch-monitor-empty-reason-served-20260930` CLOSED on its proven leg; observation ledger `inf-launch-monitor-empty-reason-a1-observation-20260930` HELD on the next real stopped event (CTO condition 4, by 2026-10-01 11:20Z), commit 5449e4ffcf. Row W86-S2 disarms on that observation, not before. |
| `IB-pr-263` | TO-IB-pr-263 (DS~S) | SUPERSEDED @ed0be5b557 | row S236 (@6b5755c32c): both gap partitions are zero-OK by `c02_twr_engine.py`'s own rule (2024-07-08 the series' first day; 2025-01-09 not a trading day), the four columns attach only on the OK branch, a re-emit at deployed bytes returns 11 columns with no S3 write. Issuer ruling inside the decomposition: the finding meets the need; no schema bump; S219 dispositioned by S236. The census the analysis asked for (readers of `twr_daily` at HEAD): 69 hits across 16,252 first-party files, DEF 2, SURFACED 19 (decomposition section 24). |

## The one real run of each outcome

- FWD-3 (INF), the raw chain: the trigger's full run at 14:53Z reached the raw writers for the first time since 09-28 and landed
  `bronze/transactions/2026-09-30.jsonl.gz` (41,420,455 bytes, 15:03:57Z) and `bronze/positions/2026-09-30.jsonl.gz`; `INF_API_PULL_PERF`
  timed out at 600 s and was tolerated (row W97-S4); the 09-28 and 09-29 raw positions did NOT backfill (the daily pull is a snapshot of
  the run day; W97-S4). The run then FAILED at step 33 `INF_C_01` on the NNA partition coverage guard (row W97-S3, BLOCKING, ARMED to the
  issuer): accounts 866/769/1096 would lose $40,000 gross of served NNA from partition 2026-09-24; the guard names its remedy as a recorded
  excusal in `lib/nna_coverage_excusals.json` with a reason and a decider, and refuses until then.
- The S216 disarm read (the CTO's own condition, `fact_positions` frontier past 09-27), 16:3xZ: `orion/inflection/silver/fact_positions/`
  still ends at `date=2026-09-27` and `orion/inflection/bronze/positions/` at `2026-09-27.jsonl.gz`, so the mirror + `opal-assets-silver-orion`
  stage did not move on today's raw. **S216 stays ARMED**: the chain broke in two places, and the second (the ingest mirror and the
  silver-orion Lambda that logged only START on 09-28/29) is the round-27 diagnosis cell.
- IB-pr-262: the deployed function's behaviour is proven by the unit arms; its live observation is tomorrow's first stop event (held).

## Rows, dispositioned (this round's, plus those the analysis routed here)

| row | standing | disposition |
|---|---|---|
| S216 | BLOCKING, ARMED | stays ARMED (frontier read above); round 27 cell: the mirror + silver-orion no-op |
| W86-S1 | BLOCKING, ARMED | DISARMED by IB-pr-261: the chain passes step 3 and the raw writers ran (the worker's rows carry the run) |
| W86-S2 | ARMED | disarms on the held observation (a1 ledger), CTO condition 4 |
| S219 | ARMED (DS) | dispositioned by S236 (pr-263 superseded); the row's `surfaced_by` fixed per CTO 103314 in the commit named in the slug |
| S235 | ARMED (placement: CTO) | the Schwab silver 09-29 miss; the 49F r3 ledger A1 stays OPEN until a scheduled fire finds its silver |
| W97-S1, W97-S2, W97-S4 | INERT | observations (CLI flag; safe-deploy HALT gate; the 09-28/09-29 raw positions did not backfill and no performance raw landed) |
| W97-S3 | BLOCKING, ARMED (issuer) | ROUTED in the slug: the NNA excusal for accounts 866/769/1096 ($40,000 gross of served NNA dropped from 2026-09-24) is a served-data decision above this workstream; the guard's own remedy is the recorded excusal; round 27 records it once ruled |
| S236 | (DS~S) | closes pr-263 (above) |
| S237, S239 | BLOCKING, ARMED (issuer) | the retiring engine's skipped-day flow error (a bank-day deposit read as +56.10%; propagates into period returns by value-neutral linking): the engine is retired for 49F serving by IB-pr-201, so no IRPT_BCKEND cell; the CORRECT computation is written into IRPT_DASHBD DB-b-1's face (the skipped-day rule) @51c05d1530; the parity oracle's exposure is named for the CTO |
| S238 | ARMED (CTO) | ruled 103318: the API enforcement of allowedFirmIds for service principals is the TOP cell of ~P's next issuance (~Y's patch candidate @4a3cabe67d) |

## Enrichment the issuer proposes for round 27 (~P), for the CTO's analysis

1. `_authz/served.py`: a service principal's `selected_tenant` outside its `allowedFirmIds` answers 403, with the test (CTO 103318, ~Y's
   patch @4a3cabe67d) -- SERVED, packet + both halves, then ~Y's live negative control.
2. The second break in the INF chain: why the ingest mirror and `opal-assets-silver-orion` did not move `fact_positions` past 09-27 on
   today's raw (read-only diagnosis, then the repair under its own ledger); S216's disarm read stays the frontier.
3. The NNA excusal record for 866/769/1096, once ruled (W97-S3).
4. Carried: S132; the INF adapter switch under the every-period rule (after 2 lands and the INF holdings producer fires on its schedule);
   the 49F r3 ledger A1 (S235).
