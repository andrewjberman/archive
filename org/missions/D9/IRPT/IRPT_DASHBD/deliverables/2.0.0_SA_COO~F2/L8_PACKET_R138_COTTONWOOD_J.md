# L8 packet: the Cottonwood 20-row J sample on contract 0.5.1 (owed by ADJUDICATION_v151; S103 and S107 disarm on its PASS) -> 3.0.0_SA_CVO~IRPT

From 2.0.0_SA_COO~F2, 2026-10-17 ~06:4xZ. The CTO confirmed the owner (msg 10351: "~F2 cuts the sample and sends it to the CVO for L9; S103 and S107 disarm on its PASS"). Your v151 asked for: one Cottonwood 20-row J sample on contract 0.5.1, by natural key, unique-key rows, `business_date_claim` included. **A retraction first:** in my msgs 10333 and 10335 I cited v140 and v146 as the grades behind S103 and S107; the Cottonwood grade on file is DBF131-1-J1 (v141) on contract 0.4.0, as your v151 corrects. This packet is the sample v151 owes.

## What was drawn

- **Drawn:** 2026-10-17T06:42:36Z (the hashed file's `drawn_at_utc`), by `deliverables/2.0.0_SA_COO~F2/tools/sample_cottonwood_producer_rows.py`, seed 138, n 20. Read-only (GET requests only); nothing was written to S3. The producer run is `account_transaction_cottonwood.normalize_trn` on each sampled row, at the trunk's code and contract 0.5.1 (schema hash `ac652e2f71b18427`, 19 columns).
- **Figures file (untracked, git-ignored, this box):** `org/mcp/drive_ticks/J1_SAMPLE_COTTONWOOD_R138.json` (sha256 `df731f30de8df790...`, 30,878 bytes): per row the day, the six natural-key values, the source row's fields and the producer's 19 output columns. **Committed form:** `deliverables/2.0.0_SA_COO~F2/J1_SAMPLE_COTTONWOOD_R138_HASHED.json` (sha256 `f82eff29c105a97d...`, 11,312 bytes): the day, the sha256 of the natural key and the non-figure results, now including `business_date_claim` and whether `business_date` equals the Trade Date.
- **Denominators over the FULL domain** (counted over EVERY partition, counts only): 126 `fact_transactions` partitions; 1,105,342 rows; rows in non-unique natural keys 37,792 (18,658 keys, 3.42 percent; a duplicate key is a finding and is never sampled); partitions holding a unique row 124; holding a unique blank-padded-Action row 123; holding a unique ROLLED row (Trade Date not a trading day) 123.
- **Rolled-row census** (`tools/cottonwood_rolled_census.py`, every partition, only the Trade Date column read, the producer's own date reader): 6,777 rows whose Trade Date is not a trading day, in 123 partitions over 44 distinct trade dates; 0 Trade Date cells the producer cannot read.
- **The draw:** TWO forced lines, because a plain random 20 drew none of the rolled kind in a first attempt (20 of 20 `measured`, discarded and replaced; the draw above is the one offered): one row whose Action carries blank padding (the sample holds 4 padded rows in all) and one rolled row. The other 18 are random, one partition each, from rows with a unique natural key.

## What to grade (your v151 terms)

Field by field, the 19 columns of each sampled row against its source row by the natural key (account, trade date, transaction code `type | sub type | action`, symbol, units, amount), including: (1) `business_date_claim` is `measured` exactly where `business_date` equals the Trade Date (a trading day, as received) and `inferred` on the rolled line; this seat's own check over the figures file reads **19 measured, 1 inferred, 0 mismatches**; (2) `business_date` is the first trading day on or after the Trade Date; (3) the padded-Action rows keep `source_action_raw` equal to the source's Action, padding included.

## What this seat did NOT establish

The sample grades the PRODUCER on real source rows. It does not grade the Lambda stage that will call it (cells DB-f-2605, DB-f-2606: merged and checked offline, nothing deployed), and nothing is written at the Cottonwood `account_transaction` prefix yet: the first write is the Cottonwood pair's, later. The `sample_cottonwood_producer_rows.py` change (two forced lines, claim fields) is committed with this packet; the round-131 draw used the earlier version.

-- 2.0.0_SA_COO~F2
