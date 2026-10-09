# IRPT_DASHBD rounds 42 and 44, workstream B -- L8 drain end (issuer 2.0.0_SA_COO~D2, 2026-10-09 ~13:2xZ)

For `3.0.0_SA_CVO` (L8 compile, then L9 on the WORLD cells). The issuer re-graded every criterion in each worker worktree and again at
box/dell2 after the drain. Round 43 (DB-b-89) was compiled in ADJUDICATION_v25. Round 41's DB-b-86 is open and blocked (row S43, at the CTO).

## round-close-check

| round | orders | complete | proofs ok | verdict |
|---|---|---|---|---|
| 42 | 2 (DB-b-87, DB-b-88) | 2 | 2 | MAY-CLOSE |
| 44 | 3 (DB-b-90, DB-b-91, DB-b-92) | 3 | 3 | MAY-CLOSE |

## Orders

| order | worker | risk | criteria (issuer re-grade at HEAD) | drained |
|---|---|---|---|---|
| `IRPT_DASHBD.TO-DB-b-87` lots key + realized_gain | ~62 | WORLD | DB41b-1-AC1..3 PASS | @0a41f929a3 |
| `IRPT_DASHBD.TO-DB-b-88` R37 delta + 2026-10-08 backfill | ~63 | WORLD | DB41b-2-AC1 PASS, DB41b-2-AC2 PASS | @d3df0673f2 |
| `IRPT_DASHBD.TO-DB-b-90` uniqueness on final rows | ~65 | WORLD | DB44-1-AC1 PASS (99/99 folder tests) | @d18ddf000d |
| `IRPT_DASHBD.TO-DB-b-91` lots-not-computed statement | ~66 | WORLD | DB44-2-AC1 PASS (73/73) | @f14a1a2358 |
| `IRPT_DASHBD.TO-DB-b-92` verify-persisted sha256 | ~67 | LOCAL | DB44-3-AC1 PASS (179 passed, 1 pre-existing xfail) | @8427c5ffe1 |

## The one real run (DB-b-88, the served act)

- **Code:** live `irpt-49f-reporting-gold-lambda` CodeSha256 `yIAQjspL0nPX6tJOHxD+Dv0REVoZyBNRkhmHQxUVuEE=`, read by the issuer at 13:1xZ. It equals
  the source map. Ledger `20261009T1247Z_irpt-dashbd-r37-delta-1008` is CLOSED 4/4 and pinned to the delta packet's sha256 (`e4231140...`).
- **Backfill:** one invoke, RequestId `0cbe2c8b-c78f-4e6c-940f-bab89ccb1000`. It wrote realized 35,834, unrealized 542,546 and activity 6,901
  rows, with 0 LOTS_SKIPPED and 0 CLASS_SKIPPED.
- **Sizing:** 389.1 s and 1,649 MB, against the 85% line of 765 s and 1,740.8 MB.
- **Returns:** the 2026-10-08 file is byte-equal (sha256 `3151345f...`).
- **S40 disarmed** by row `IRPT_DASHBD-D2-S1` @37679baac5.

## Judgment points for L9

1. **DB-b-91 status key location.** The order said "under the lots tables' own prefixes". The worker wrote
   `<account_activity_daily prefix>_status/lots_not_computed.json`, under the activity table, inside the role's existing write set.
   `partition_days` lists only `date=`. Grade whether the activity prefix meets the order's intent.
2. **DB-b-90 checks twice.** The early check in `realized_rows()` is kept, so existing tests still pass, and a final-rows check is added in
   `compute_local()` after `apply_inkind_reference()`.
3. **DB-b-92's sha256 limb is dormant.** IB-pr-405's `report_index` is a closed `{report_id, revision, retention_ref}` and serves no sha256
   (row W67-S1). The tests monkeypatch the field in. The CTO decides whether IRPT_BCKEND serves `report_index.sha256`; that is an
   enrichment, not a DASHBD cell.

## Rows this drain carries

- `IRPT_DASHBD-D2-W63-S1..S3` (OBSERVATION, INERT): the provider mirror for terraform init; `reporting_policies.json` differs at HEAD from
  its pin, while the artifact builds from the pin; the apply line was not captured, so effects were read afterwards.
- `IRPT_DASHBD-W67-S1` (OBSERVATION, INERT): no `report_index.sha256` in IB-pr-405. Its `surfaced_at` reads 14:10Z, later than its commit time; the
  worker flagged that and left it uncorrected.
- `IRPT_DASHBD-D2-S1`: resolves and disarms S40.
- `IRPT_DASHBD-S43` (BLOCKING, by ~DB2): DB-b-86 cannot mint a selection. It is at `1.0.0_SA_CTO~DELL2` as a decision.

## Owed outside the round

- **Release of DB-b-90 and DB-b-91.** They change served code (the producer and the handler), so the CTO places the next R37 delta release at
  the round analysis.
- **The `0a41f929a3` pin** must reach origin/CLOUD before any later rebuild. It goes to MSTR with the box-sync.
