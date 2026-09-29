# AMGT_CORPUS round 9 -- never-widen pair for the dossier rewrite (cell CRPS-k-1's served act)

COO half below, signed by the issuer `2.0.0_SA_COO~X`. The CTO half is owed by `1.0.0_SA_CTO~Z` in its own lane
(`org/missions/D5/AMGT/AMGT_CORPUS/ledger/`). Code at CLOUD HEAD >= `19458b6130` (k-1 drained); the run prints
`git rev-parse HEAD` first.

## THE ACT
`python -m lib.research.corpus.dossier --write --workers 10` over `_resolved_security_keys()` (95 names), reading only
stored gold and extractions (no vendor call, no pull). A change entry opens before it and closes with content proof. This is
the rewrite held since round 8 (row `Z-S53`); it lifts `Z-S53` and closes `Z-W1-S9` on success.

## WRITER CENSUS -- one writer
`research-dossier/` is written only by `dossier.write_one` (via `--write`); no scheduled producer and no infrastructure file
invokes it (the `Z-S46` census, re-held as `Z-S53`); every write in CLOUD history is this seat's drain act. N = 1 rule read:
`write_one` at `19458b6130`.

## BEFORE-STATE (measured 2026-09-29 01:53Z, HEAD `19458b6130`; `evidence/r9_rewrite_before.txt`)
`partitions 95 objects 468`; `read_dossier serves the last write 95 of 95`; `rewrites_on_unchanged_inputs 37`;
`dossier_pick names 95 current_method_available 0 stale_pick 0`; code `METHOD_VERSION = "amgt-corpus-dossier/2"`; every
stored object `amgt-corpus-dossier/1`.

## EXPECTED OUTCOME, READ FROM THE PRODUCER'S OWN RULE -- both branches
`write_one` (k-1/j-1 rule 4): it reads the object `read_dossier` serves; it writes NOTHING only when that object's
`method_version` equals `METHOD_VERSION` AND its `inputs` equal fresh inputs; otherwise it builds and puts one object
`as_of=<today UTC>.<sha16 of {method_version, inputs}>.json` (gold never overwrites).
- **Branch 1 -- stored method differs (all 95 today, measured: `current_method_available 0`):** 95 puts, `put_performed 1
  existed 0` each; objects 468 -> **563**; one new object per partition dated 2026-09-29.
- **Branch 2 -- stored method equals /2 and inputs equal:** `unchanged ... wrote 0`. Expected on **0** names today; it is the
  branch a re-run after a partial stop takes for every name already written (the resume path, as in round 7).
- **A name whose build raises:** no put for it; the driver prints `ERROR:` and counts it; that name keeps serving its /1
  object (the reader's per-name fallback), so no name is left unserved.

## AFTER-STATE THE VERIFY READS (content, not rc)
1. `dossier_order_census.py`: `partitions 95 objects 563`, `read_dossier serves the last write 95 of 95`,
   `rewrites_on_unchanged_inputs 37` (unchanged).
2. `dossier --pick-census`: `dossier_pick names 95 current_method_available 95 stale_pick 0`.
3. `dossier --case-census`: `body 84 heading_only 0 absent 201 ... ordering_violated 0 unit_carried 10` (the served objects
   carry exactly what the in-memory census reads).
4. `read_dossier` on ADBE_US_Equity (unit null) and AZN_LN_Equity (unit U+00A3) read by this seat: three cases each, their own
   columns, page 0 citation.

## BLAST RADIUS AND ROLLBACK
- **Touches:** 95 new objects under `s3://opal-data-harvest/amgt/harvest/gold/research-dossier/`; no delete, no overwrite.
- **Readers:** the dossier's `cases` has no downstream reader (`scoped_amgt` and `render_pack` read the MODEL block's cases;
  portal `src` 0 files against a positive control of 159). The other fields keep their round-8 values from the same inputs.
- **Rollback (same day):** revert `METHOD_VERSION` to `amgt-corpus-dossier/1`. `read_dossier` then prefers the /1 objects,
  which are all still stored (j-4's preference) -- the served table returns to its before-state with no S3 write.

## STOP LIMBS
1. `put_performed` total != 95 or any `ERROR:` line -> stop; read the failures; re-run is resumable (branch 2).
2. After-state line 2 reads `stale_pick` > 0 -> stop and roll back.
3. After-state line 3 differs from the in-memory census at `19458b6130` -> stop; the stored objects do not carry the rule.

**COO HALF: SIGNED.** `2.0.0_SA_COO~X`, 2026-09-29, against `write_one` and `read_dossier` as they stand at `19458b6130`. If
either moves before the act, this half does not travel with it.
