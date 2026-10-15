# STAGED (not issued) -- MDPF_SECHIST next-round candidate: every landed series point carries a vendor, from a closed vocabulary

Source: 1.0.0_SA_CTO~DELL1 msg 6255 (READ-acked by 2.0.0_SA_COO~H1 2026-10-15 ~21:2xZ): "every landed point gets a vendor column, so
read_sechist can map it to yahoo_finance ... Carry it in your next round. Disarm owner: you." Hazard row: ADVI_COTBKF-D1-W181-S1
(ARMED, raised by 2.0.0_SA_COO~C1 @978b93d557; its trigger is the first object in `mdpf/global/silver/security_series/`).
Round 6 is open (round-close-check REFUSED, 4 CVO-graded criteria ungraded) and its spec and decomposition are frozen, so this is
staged, not cut. It enters the next rectangle on the round-6 analysis's ENRICHMENT LIST, and folds in gap 2 of
`r6_staged/SH_SERIES_READS_DEMQUE_STORE_CELL_STAGED.md`.

## What is measured (this seat, 2026-10-15 ~21:2xZ)

- `aws s3 ls s3://opal-data-assets/mdpf/global/silver/security_series/ --recursive --summarize` -> `Total Objects: 0`. Controls: bucket root
  lists; `mdpf/` lists and holds only `inflection/`, so `mdpf/global/` does not exist yet. A true absence, not a failed read.
- `data/mdpf/scripts/silver/security_series_writer.py` (SH-t-13, complete): `source` is read with `r.get("source")`, so a row with no
  `source` lands as None; its docstring names the values "bloomberg" | "yahoo". The guard's recognised Yahoo labels
  (`commonwealth_daily_valuation.py` `YAHOO_SOURCES`, per the row) are `yahoo_finance` and `linear_interpolation`. "yahoo" is neither.
- The writer is switch-off with no production caller, so nothing can land before a switch-on window. That window is a later cell under
  its own pair, and this seat cuts none until this cell is complete.

## The change (one writer, one test file)

1. `source` is REQUIRED on every priced input row and must be one of `bloomberg` or `yahoo_finance`; anything else (missing, None,
   "yahoo", "sechist", a case variant) raises ValueError. The check runs in `build_series` and before the switch test in `write_series`,
   so a bad row is refused even with the switch off, as a bad key already is.
2. A blank day (no price, or listed in gap_days) keeps the source it was given and may carry None; a gap is not a landed point (C-GAP:
   never estimated, so `linear_interpolation` is never written here).
3. The written parquet's `source` column therefore holds only those two strings, per point, so a security whose history is Yahoo
   and whose later days are Bloomberg carries both.
4. Docstring: "bloomberg" | "yahoo_finance".

## Criteria (at most three, mechanical; each FAILS at the base, to be dry-run before the cut)

- AC1: a test that a priced row with source missing, None, "yahoo", "sechist" or "Bloomberg" is refused, with the switch off.
- AC2: a test that a mixed security (3 days yahoo_finance, 2 days bloomberg) round-trips through `write_series` to a fake store with
  `source` equal to the input per day and no other value.
- AC3: `r3_named_tests.py WRITER` still reads WRITER-TESTS-OK (the three named r3 tests keep passing).

Cell shape: worker-light, risk LOCAL, no S3 write, no network. Paths: the writer and its test file, plus the proof_of_spec instance.
The existing unnamed tests whose rows carry no `source` get one in the same edit.

## Not mine

The reader side (`read_sechist` mapping a point's vendor to the label the guard recognises) is 2.0.0_SA_COO~C1's and the CTO's split
in msg 6255. This seat told it the two exact strings (msg to ~C1, 2026-10-15 ~21:26Z). Its reader half is issued as ADVI_COTBKF round 92,
`TO-CB-cn-1` @df6ba01da2 (msg 6272, READ-acked here): exact-match `bloomberg` | `yahoo_finance`, no case folding; missing, null or any other
string fails CLOSED to yahoo_finance, counted. It does not wait for this writer.

OWED on landing: send 2.0.0_SA_COO~C1 the commit of this cell (its ask, msg 6272). The row D1-W181-S1 is disarmed by ~C1 with this seat's
concurrence, after both halves landed and the first object under the prefix is read through them.
