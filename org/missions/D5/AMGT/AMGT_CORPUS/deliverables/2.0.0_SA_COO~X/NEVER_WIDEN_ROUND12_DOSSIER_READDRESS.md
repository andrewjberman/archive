# AMGT_CORPUS round 12 -- never-widen pair for the dossier store's move to the builder's canonical prefix (cell CRPS-n-1)

COO half below, signed by the issuer `2.0.0_SA_COO~X`. The CTO half is owed by `1.0.0_SA_CTO~Z` in its own lane
(`org/missions/D5/AMGT/AMGT_CORPUS/ledger/`). Ruling it implements: msg 26555 / verdict @`e1e4ae43d4`.

## THE ACT -- ONE WINDOW (decomposition v12.0 s.1a)
1. Merge `wk-crps12-1` (worker tip `ce3192a363`, re-graded VALID) through `safe-merge.sh` -- HELD until this pair is signed.
2. IMMEDIATELY after the merge lands: `python -m lib.research.corpus.dossier --write --workers 10` over the 95 resolved names,
   from the merged code. A change entry opens before step 1 and closes with content proof after step 2.

## WRITER CENSUS -- one writer
`research-dossier/` and `research_dossier/` are written only by `dossier.write_one` in this seat's drain acts (rounds 7-11 each
under a pair); no scheduled producer. N = 1 rule read: `write_one` / `read_dossier` / `gold.table_prefix` at `ce3192a363`.

## BEFORE-STATE (measured 2026-09-29 10:25:15Z; `evidence/r12_before.txt`)
- Legacy prefix `amgt/harvest/gold/research-dossier/`: **846 objects, 95 partitions** (round 11's `/4` objects are the newest).
- Canonical prefix `amgt/harvest/gold/research_dossier/`: **0 objects**.

## EXPECTED OUTCOME, READ FROM THE PRODUCER'S OWN RULE -- both branches
`write_one` reads the object `read_dossier` serves; at the new prefix there is none, so `read_dossier` raises `LookupError`, the
stored inputs are `None`, and it builds and puts.
- **Branch 1 -- no object at the new prefix: all 95 names.** 95 puts under `research_dossier/`; new prefix 0 -> **95 objects,
  95 partitions**. **Legacy prefix unchanged at 846** (never written, never deleted, no longer read).
- **Branch 2 -- an object at the new prefix with the current method and equal inputs:** 0 names today; the resume path.
- **Content:** each new object carries the same case fields, model rows and inputs the `/4` object at the legacy prefix carries
  (same code, same inputs), with ONE field that differs by construction: `"artifact": "research_dossier"` (was
  `"research-dossier"`; `dossier.ARTIFACT` moved with `TABLE` so no hyphen literal remains). No reader of the dossier's
  `artifact` value exists outside `dossier.py` (grep over `lib/research`: `scoped_amgt.py`'s "artifact" hits are unrelated
  landed-artifact reads).
- `METHOD_VERSION` stays `amgt-corpus-dossier/4`; the `as_of` segment is the run's UTC date.

## THE WINDOW'S EXPOSURE, NAMED
Between the merge (step 1) and each name's put (step 2), code AT CLOUD HEAD reading that name gets `LookupError` (no fallback,
by ruling: a fallback would re-carry the refused literal). Readers of trunk code in that window: this seat's own censuses only; the
deployed AMGT_RESAPP Lambda runs the code of its last deploy (legacy prefix, still whole) until it redeploys onto this change. The
window is the rewrite's runtime (~20 minutes, measured on rounds 9-11).

## AFTER-STATE THE VERIFY READS (content, not rc)
1. New prefix: 95 objects, 95 partitions; legacy prefix: 846 objects (unchanged).
2. `dossier_order_census.py` (reads `dossier.TABLE`, now the new prefix): `partitions 95 objects 95`, `read_dossier serves the last
   write 95 of 95`.
3. `dossier --pick-census`: `current_method_available 95 stale_pick 0`.
4. `dossier --case-census` equal to round 11's served line: `body 102 heading_only 0 absent 183 ... currency_set 5 currency_null 29`.
5. `read_dossier` on three names (HEI, CPA, SHOP) from the new prefix, their case fields equal to the legacy `/4` object's.

## BLAST RADIUS AND ROLLBACK
- **Touches:** 95 new objects under `research_dossier/`; no delete, no overwrite; the legacy 846 untouched.
- **Rollback (same day):** revert the merge's code (`TABLE`/`ARTIFACT` back); readers return to the legacy prefix, which is whole.

## STOP LIMBS
1. The merge refuses or conflicts -> resolve before step 2; do not run step 2 on a partial merge.
2. `put_performed` != 95 or any `ERROR:` -> re-run (resumable); if a name still fails, roll back (revert) within the window.
3. After-state line 4 differs from round 11's line -> stop and roll back.

**COO HALF: SIGNED.** `2.0.0_SA_COO~X`, 2026-09-29, against `ce3192a363`. If the branch moves before the act, this half does not
travel with it.
