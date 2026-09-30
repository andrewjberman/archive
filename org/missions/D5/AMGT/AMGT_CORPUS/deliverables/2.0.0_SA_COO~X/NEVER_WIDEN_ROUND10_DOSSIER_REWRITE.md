# AMGT_CORPUS round 10 -- never-widen pair for the dossier rewrite at `/3` (chain A: CRPS-l-3 + CRPS-l-1)

COO half below, signed by the issuer `2.0.0_SA_COO~X`. The CTO half is owed by `1.0.0_SA_CTO~Z` in its own lane
(`org/missions/D5/AMGT/AMGT_CORPUS/ledger/`). Code at CLOUD HEAD >= `5b0b728ab1` (chain A merged); the run prints
`git rev-parse HEAD` first.

## THE ACT
`python -m lib.research.corpus.dossier --write --workers 10` over `_resolved_security_keys()` (95 names), reading only stored
gold and extractions (no vendor call). A change entry opens before it and closes with content proof.

## WRITER CENSUS -- one writer
`research-dossier/` is written only by `dossier.write_one` in this seat's drain acts (the `Z-S46` / `Z-S53` census; rounds 7-9
each ran it under a pair). N = 1 rule read: `write_one` at `5b0b728ab1`.

## BEFORE-STATE (measured 2026-09-29 05:47:50Z, HEAD `6a91a6efb1`; `evidence/r10_rewrite_before.txt`)
`partitions 95 objects 656`; `read_dossier serves the last write 95 of 95`; `rewrites_on_unchanged_inputs 37`;
`dossier_pick names 95 current_method_available 0 stale_pick 0`; code `METHOD_VERSION = "amgt-corpus-dossier/3"`, every stored
object `/2` or older; in-memory `case_census ... body 84 heading_only 0 absent 201 ... unit_carried 10 currency_set 1
currency_null 27`.

## EXPECTED OUTCOME, READ FROM THE PRODUCER'S OWN RULE -- both branches, per name from the join
`write_one`: it writes nothing only when the object `read_dossier` serves carries the CURRENT `METHOD_VERSION` AND equal
`inputs`; otherwise one put.
- **Branch 1 -- stored method differs: all 95 names** (measured `current_method_available 0`; this includes BP/_LN_Equity and
  NG/_LN_Equity, whose inputs did not move in round 9 but whose method now does). **95 puts; objects 656 -> 751**; one new
  object per partition.
- **Branch 2 -- method and inputs equal: 0 names today**; the resume path after any partial stop.
- A name whose build raises: no put, `ERROR:` counted; it keeps serving its `/2` object (the reader's fallback).

## WHAT CHANGES ON THE SERVED TABLE (the cases field only)
- Every served table case gains `unit_as_written`, `currency`, `currency_basis` and loses `unit`; `currency` is set on ML_FP
  (EUR) only; the other 27 readable-table names carry `currency: null` with its basis.
- The six names of `Z-W1-S12` (8035_JP, BZLFY_US, HEI_US, SNPS_US, TSM_US, V_US) move from the generic count reason to
  their own: "has 14 of 15 cells; the empty cell's position is not recoverable from line order (no x-coordinates)".
- Values do not move: the 28 readable tables serve the same strings (the in-memory census's `body 84` equals round 9's).

## AFTER-STATE THE VERIFY READS (content, not rc)
1. `dossier_order_census.py`: `partitions 95 objects 751`, `read_dossier serves the last write 95 of 95`,
   `rewrites_on_unchanged_inputs 37`.
2. `dossier --pick-census`: `current_method_available 95 stale_pick 0`.
3. `dossier --case-census`: equal to the before-state line above (the served objects carry what the rule reads).
4. `read_dossier` on ML_FP_Equity (currency EUR), AZN_LN_Equity (unit U+00A3, currency null, "differs from the listing") and
   TSM_US_Equity (the specific ABSENT reason), read by this seat.

## BLAST RADIUS AND ROLLBACK
- **Touches:** 95 new objects under `research-dossier/`; no delete, no overwrite.
- **Readers:** AMGT_RESAPP's scoped API will read `cases` through `read_dossier` (its round-46 ruling 3; `2.0.0_SA_COO~Z` msg
  26444) and is waiting on exactly these fields; the rename `unit` -> `unit_as_written` is the shape it waits for. No other
  reader of the dossier's `cases` exists (round-9 census; portal `src` 0 files).
- **Rollback (same day):** revert `METHOD_VERSION` to `/2`; `read_dossier` then prefers the stored `/2` objects.

## STOP LIMBS
1. `put_performed` total != 95 or any `ERROR:` -> stop; the re-run is resumable (branch 2).
2. After-state line 2 reads `stale_pick` > 0 -> stop and roll back.
3. After-state line 3 differs from the before-state census -> stop.

**COO HALF: SIGNED.** `2.0.0_SA_COO~X`, 2026-09-29, against `write_one` and `read_dossier` at `5b0b728ab1`. If either moves
before the act, this half does not travel with it.
