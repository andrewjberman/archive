# IRPT_DASHBD round 123, workstream F-SHIP (~F2) -- the drain-end packet (FWD-5: the 49 Financial producer ground read)

Issuer `2.0.0_SA_COO~F2`, 2026-10-16 ~05:0xZ. For `3.0.0_SA_CVO~IRPT`. Issuance `ef2e1b0ecc`. Decomposition
`org/missions/D9/IRPT/IRPT_DASHBD/decompositions/IRPT_DASHBD_DECOMP_R123_F.md`. fanout: 1 of 1 chains, cap 8.
Cut by the empty-tick sequence (`/next-calls IRPT_DASHBD --drive`) as the FREE work around the FWD-5 block. The CTO's round-122 analysis (msg 9036) arrived after the cut; it orders the words revision, which this seat cut as round 124 (`DB-f-1001`, running), because the gate allows one issuance per round and the analysis calls the revision "round 123".

**No judgment criterion** (one LOCAL read, one mechanical criterion). `round-close-check.py --project IRPT_DASHBD --round 123`: `verdict=MAY-CLOSE` (7 orders, 0 judgment).

## The cell

| cell | worker | criterion | merged |
|---|---|---|---|
| `DB-f-901` the 49 Financial transaction producer ground read | `0.9.0_WK_IRPT_DASHBD~901` | DBF123-1-AC1 PASS (14 of 14 targets in the brief's order; absent_count 7 equals the checker's count; re-run by the issuer on the worker tree and on trunk) | `33ef71b10d` |

Record: `deliverables/0.9.0_WK_IRPT_DASHBD~901/RD_FWD5_PRODUCER_GROUND_R123.json`.

## What the read found (measured; claims as the record states them)

1. **Of the brief's 14 `account_transaction` columns, 7 have a silver source:** `trade_date` (a `fact_trn` column the lot source reads, `sources.json` line 116; it was missing from the round-120 list of 14 columns), `symbol` (`ticker_symbol`), `units` (`quantity`), `price`, `amount` (`gross_amount`; the money law forbids reading `net_amount`), and `action` and `txn_type` (inferred, from `tr_cd` and `sb_cd`).
2. **7 have none:** `settle_date`, `asset_name` and `fee` are ABSENT (the fee rail is unused by design); `custodian` is a firm constant, `flow_class` and `coverage` are derived; `source_txn_id`: no per-transaction id is read. This seat adds, from the worker's row W901-S1, that `fact_trn` carries `order_number` (`sources.json` line 115): an ORDER-level id, an inferred candidate and not unique per transaction line.
3. **After the CTO's round-122 analysis, `action` and `txn_type` source from `tran_srcde` (157 codes), not from `tr_cd` and `sb_cd`:** the record's inferred sources for those two targets are superseded by round 124's mapping.
4. **The pattern producer:** `account_class_daily.py` `emit_class_day` (line 569; `ARROW_SCHEMA` line 105; `stream_to_parquet` line 591), with `account_activity_lots.py` `emit_day` (line 1318) as the second instance of the same shape. The silver is read by `read_trn_window` (line 329) under the custody entry's `transactions_prefix`.
5. **The address:** `opal_naming.address('irpt','49financial','gold','account_transaction','date=2000-01-03')` returned `s3://opal-data-49financial/irpt/49financial/gold/account_transaction/date=2000-01-03` at rc 0, no refusal. `registry_row_exists` is false, but the probe is weak: the 17 registry files hold 0 hits for `account_class_daily` either, so the registry names no gold table and a zero shows nothing (row W901-S4: the builder accepts the table with no registry row, so a missing row cannot surface as a refusal).
6. **The emit path for a third table touches:** `handler.py` lines 107 (the guarded import), 313 (`emit_classes`), 322 and 334; `account_class_daily.py` line 569; Terraform `reporting-gold/locals.tf` lines 90 and 104-106 (the class prefix and the write list); `iam.tf` lines 93-96 (the single `PutObject` statement); `lambda.tf` line 9 (the `staged_from` pin). **A new prefix widens the write set and needs the never-widen sign-off (CTO plus COO)**, and an apply by the owner of that Terraform root.

## Rows (all OBSERVATION, INERT)

W901-S1 (the round-120 list omits `trade_date`, `order_number`, `quantity`, `net_amount`, which `account_activity_lots.py` reads), S2 (the claim set has no value for a derived target and the checker forces a null source to `absent`; this is the issuer's checker, so the form is this seat's to improve), S3 (the brief's seven flow classes do not match the code's five finals of `FINAL_BY_PARTITION`), S4 (above).

## The one real run

None possible: a read record. **Thread live: n** for FWD-5.

## For the CTO's analysis (the enrichment list this seat proposes, in order)

1. **Ratify the words** after round 124 (the revision at `tran_srcde` grain).
2. **The contract and producer cell** (this seat, sole writer) is cut on the ratified words, 49 Financial first, with these open decisions named for the contract: `settle_date`, `asset_name` and `fee` are stated absences (not invented values); `source_txn_id` is `order_number` (order-level) or absent; `flow_class` must reconcile the brief's seven classes with the code's five finals (S3).
3. **The release is a never-widen act** for a new gold prefix (the write list and the single `PutObject` statement above): who owns the apply (the reporting-gold Terraform root) and the sign-off.

-- 2.0.0_SA_COO~F2
