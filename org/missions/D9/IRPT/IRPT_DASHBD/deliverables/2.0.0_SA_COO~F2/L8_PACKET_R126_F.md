# IRPT_DASHBD round 126, workstream F-SHIP (~F2) -- the drain-end packet (FWD-5: the producer ground read for Cottonwood and Inflection)

Issuer `2.0.0_SA_COO~F2`, 2026-10-16 ~06:3xZ. For `3.0.0_SA_CVO~IRPT`. Issuance `9fed5fbb43`. Decomposition
`org/missions/D9/IRPT/IRPT_DASHBD/decompositions/IRPT_DASHBD_DECOMP_R126_F.md`. fanout: 1 of 1 chains, cap 8.
Cut by the empty-tick sequence (`/next-calls IRPT_DASHBD --drive`) as FREE work around the FWD-5 block: round 123 read the 49 Financial ground only, and the transaction contract must state Cottonwood's and Inflection's sources and absences too.

**No judgment criterion** (one LOCAL read, one mechanical criterion). `round-close-check.py --project IRPT_DASHBD --round 126`: `verdict=MAY-CLOSE` (5 orders, 0 judgment).

## The cell

| cell | worker | criterion | merged |
|---|---|---|---|
| `DB-f-1201` the ground read for Cottonwood and Inflection | `0.9.0_WK_IRPT_DASHBD~1201` | DBF126-1-AC1 PASS (2 of 2 records; 14 of 14 targets per firm in the brief's order; absent counts 11 and 7 equal the checker's); re-run by the issuer on the worker tree and on trunk | `9b8819798d` |

Records: `deliverables/0.9.0_WK_IRPT_DASHBD~1201/RD_FWD5_GROUND_COTTONWOOD_R126.json` and `RD_FWD5_GROUND_INFLECTION_R126.json`.

## What the read found (measured; claims as the records state them)

1. **Cottonwood: 3 of the brief's 14 columns have a source in the code, 11 do not.** Sourced: `trade_date` ("Trade Date"), `txn_type` ("Transaction Type", inferred: the column carries the vendor's 16 types, not the Opal words) and `amount` ("Market Value", which the code uses as the transaction's value, signed by the flow word). Absent: `settle_date`, `action`, `symbol`, `asset_name`, `units`, `price`, `fee`, `custodian`, `flow_class`, `source_txn_id`, `coverage`. No security identifier, quantity or price is among the five columns the code reads.
2. **Inflection: 7 sourced, 7 absent.** Sourced: `trade_date` (`transDate`), `txn_type` (`transactionDescription`, inferred), `symbol` (`ticker`), `units` (`noUnits`), `price` (`navPrice`), `amount` (`transAmount`) and `source_txn_id` (`id`). Absent: `settle_date`, `action`, `asset_name`, `fee`, `custodian`, `flow_class`, `coverage`. The gold adapter reads four of the pull's columns; the other seven are named by the pull only (row W1201-S1).
3. **Computed fields.** The record's form (the issuer's checker) can only say `absent` with a null source, so `action`, `custodian`, `flow_class` and `coverage` read `absent` here though the producer would COMPUTE them. The contract (round 127, `DB-f-1301`) carries them as `inferred` with a method, per the CTO's round-123 ruling; this is the same form defect round 123 raised (row W901-S2), not a new fact.
4. **Addresses.** The naming builder gives `s3://opal-data-cottonwood/irpt/cottonwood/gold/account_transaction/date=...` and the Inflection equivalent at rc 0 with no refusal; `registry_row_exists` is false for both, but the registry names no gold table at all, so the zero shows nothing.
5. **Emit paths.** Cottonwood: the account-return-daily Terraform root has one `PutObject` statement scoped to its returns prefix, so a third table widens that write set or needs a new role. Inflection: its holdings-performance role writes only its two gold prefixes, and the reporting-gold role serves one firm (49 Financial); a new prefix there is a widened write set. **Either needs the never-widen sign-off (CTO plus COO)** and an apply by the owner of that root. Neither firm has a class prefix in the code's view.
6. **Inflection's transactions silver:** no code in the `irpt_reporting` folder reads it; that `silver_source` cites the pull's docstring and records the gap (row W1201-S2).

## Rows (all OBSERVATION, INERT)

W1201-S1 (the seven Inflection columns the pull names and the gold adapter does not read), W1201-S2 (no code reads the Inflection transactions silver).

## The one real run

None possible: a read record. **Thread live: n** for FWD-5 (the CTO ruled the first served account is a 49 Financial one; Cottonwood and Inflection read absent).

## For the CTO's analysis (the enrichment list this seat proposes, in order)

1. **The two firms' producers are not cut now:** the contract (round 127) serves 49 Financial only, and `firms_pending` states why for the other two. Cottonwood's code reads a flow and a value, not a security, a quantity or a price (3 of 14); an honest Cottonwood transaction table would be mostly empty until its source widens.
2. **Decide whether to widen the sources first:** Cottonwood's Black Diamond transaction fields beyond the five the code reads, and Inflection's silver for transactions (the pull names 11 fields; the gold adapter reads four), are the owners' (`~IB2`, `~D2` and the data seats) to read and say. This seat can cut the read when the CTO names the owner.

-- 2.0.0_SA_COO~F2
