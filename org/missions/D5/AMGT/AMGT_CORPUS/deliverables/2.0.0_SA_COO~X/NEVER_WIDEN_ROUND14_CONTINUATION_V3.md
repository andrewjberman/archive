# AMGT_CORPUS round 14 -- never-widen pair for the continuation /3 rewrite and the dossier re-derive (cell CRPS-p-5)

COO half below, signed by the issuer `2.0.0_SA_COO~X`. The CTO half is owed by `1.0.0_SA_CTO~Z` in its own lane
(`org/missions/D5/AMGT/AMGT_CORPUS/ledger/`). Ruling it implements: round-13 analysis s.4 item 5 @`f1c482d24f` (msg 26603);
order amendment 1 @`af9e934ae2` (row `Z-W5-S5`).

## THE ACT -- ONE WINDOW
1. Merge `wk-crps14-5r` (worker tip `a53f4c4bfc`, re-graded VALID by the issuer: AC1 44 passed, AC2 `p5 ML_FP_Equity pillars 5
   empty_text 0 | IMB_LN_Equity pillars 6 empty_text 0 | ADBE_US_Equity pillars 2 empty_text 0`, AC3 455 passed) through
   `safe-merge.sh` -- HELD until this pair is signed.
2. `python -m lib.research.corpus.continuation --write` over the 95 resolved names, from the merged code.
3. `python -m lib.research.corpus.dossier --write --workers 10` over the 95 resolved names, from the merged code.
A change entry opens before step 1 and closes with content proof after step 3.

## WRITER CENSUS -- one writer per table
`research-continuation/` is written only by `continuation.write_one` (via `--write`) and `research_dossier/` only by
`dossier.write_one`, both in this seat's drain acts under pairs; no scheduled producer. N = 2 rules read at `a53f4c4bfc`:
`continuation.write_one` + `_inputs_sha16` + `_select_stored`; `dossier.write_one` + `read_dossier` + `_build_inputs`.

## BEFORE-STATE (measured 2026-09-29T19:28:18Z, bucket opal-data-harvest)
- `amgt/harvest/gold/research-continuation/`: **225 objects, 95 partitions**, newest 2026-09-26 21:58:02Z (method /1 and /2).
- `amgt/harvest/gold/research_dossier/`: **95 objects, 95 partitions**, newest 2026-09-29 11:09:15Z (round 12, method dossier/4).

## EXPECTED OUTCOME, READ FROM THE PRODUCERS' OWN RULES -- both branches
**Continuation (step 2).** The object name is `_inputs_sha16(document["inputs"])`, and that hash covers `METHOD_VERSION`
(`continuation.py:161-162`), so `/3` names a new key for every name; `gold_put` never overwrites.
- Branch 1 -- no `/3` object for the name: **all 95 today**. 95 puts; table 225 -> **320 objects, 95 partitions**. Body per name:
  `method_version` `/3`; `thesis_pillars` byte-identical to `/2` for 94 names, ML_FP 1 empty pillar -> **5 pillars with text**
  (worker's read-only census over 95 names at `a53f4c4bfc`: 34 PDF-sourced, 94 unchanged, other four fields 95 of 95 equal).
- Branch 2 -- a `/3` object with an equal body already stored (the resume path): 0 names today; a no-op put.
**Dossier (step 3).** `_build_inputs` carries the continuation object's key and sha256; substrate picks the input-matching
continuation object with the CURRENT method (`_select_stored`), which after step 2 is the `/3` object -- so every name's dossier
inputs change and `write_one`'s unchanged-inputs no-op does not fire.
- Branch 1 -- stored inputs differ: **all 95**. 95 puts, `as_of=2026-09-29.<new hash>.json`; table 95 -> **190 objects, 95
  partitions**. `read_dossier` serves the new object (same `as_of` date as round 12, greater LastModified). Case fields equal
  the round-12 object's for 94 names; ML_FP's `thesis_pillars` goes from 1 empty pillar to 5 with text.
- Branch 2 -- stored inputs equal (step 2 skipped or failed for a name): that name writes nothing and serves unchanged.

## THE WINDOW'S EXPOSURE, NAMED
- Merge -> step 2: trunk code reading continuation picks the `/2` object (no `/3` exists; `_select_stored` falls back), so
  every read still serves. The deployed AMGT_RESAPP function reads stored dossier objects and is untouched by the merge.
- Step 2 -> step 3: the dossier served is still round 12's; nothing unserved.
- After step 3: the served move is ML_FP's page gaining 5 pillars; 94 names serve equal case content under new objects.

## AFTER-STATE THE VERIFY READS (content, not rc)
1. continuation: 320 objects, 95 partitions; dossier: 190 objects, 95 partitions.
2. `read_dossier` ML_FP_Equity: `thesis_pillars` 5 items, every `text` non-empty, leads the five named in order amendment 1.
3. `read_dossier` IMB_LN_Equity and ADBE_US_Equity: `thesis_pillars` equal to round 12's served object (6 and 2).
4. `dossier --pick-census`: `current_method_available 95 stale_pick 0`.
5. `dossier --case-census` equal to round 12's served line apart from ML_FP's pillar count.

## BLAST RADIUS AND ROLLBACK
- **Touches:** 95 new continuation objects and 95 new dossier objects; no delete, no overwrite; the 225 + 95 existing untouched.
- **Rollback, next UTC day or later:** revert the merge (`METHOD_VERSION` back to `/2`, reader back), then `dossier --write`:
  substrate picks `/2` again, inputs revert, and the object written under the new date serves round 12's content.
- **Rollback, SAME UTC day -- NOT AVAILABLE BY WRITE:** the reverted code's dossier key `as_of=2026-09-29.<round-12 hash>` already
  exists, so `gold_put` does not re-write it and the step-3 object stays the newest pick. A same-day un-serve would need a
  DELETE of the 95 step-3 objects, which is Andrew's act (CLAUDE.md Agent Autonomy). The served delta is one name's pillars
  (ML_FP 0 -> 5 real pillars); 94 names serve equal content, so the exposure of the no-same-day-rollback leg is that one field.

## STOP LIMBS
1. The merge refuses or conflicts -> resolve before step 2; never run step 2 on a partial merge.
2. Step 2 `put_performed` != 95 or any `ERROR:` -> re-run (resumable); a name still failing -> stop before step 3, revert the
   merge (continuation readers fall back to `/2`, nothing served moved).
3. Step 3 `put_performed` != 95 or after-state 2/3 differs -> stop; report the served state per name; no further write.

**COO HALF: SIGNED.** `2.0.0_SA_COO~X`, 2026-09-29, against `a53f4c4bfc`. If the branch moves before the act, this half does not
travel with it.
