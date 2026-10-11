# AMGT_CORPUS round 44 -- never-widen pair for `CRPS-at-10`: re-write the 95 research dossiers at method version 11 (team_sheet stored in the dossier)

**Authority:** `1.0.0_SA_CTO~DELL1` ruling msg 3213 ("team_sheet ... moves to /11") and msg 3196 ("precompute team_sheet into the gold
dossier; the API reads only served tiers"). The dell1 hold that parked this act (CTO msg 3317) was withdrawn by msg 3351 and msg 3380: Andrew
lifted it ~01:58Z, @`cbcfdc0c1c`. Producer change `CRPS-at-1` AMENDMENT 2, drained @`3bff293266` (instance VALID rc 0; 561 corpus and 908
API tests pass on the merged tree).

**Code:** box/dell1 at or after `3bff293266`: `dossier.py` `METHOD_VERSION` = `amgt-corpus-dossier/11`; `build` stores
`fields["team_sheet"] = team_sheet.rows_for(security_key, client=client)`; `scoped_amgt.py` reads the stored field and never calls the
team-sheet module (AC3 greps: 0).
**Served today:** /10 (AMGT_RESAPP mm-4, ledger CLOSED 20261011T022452Z; the deployed function carries `dossier.py` at /10). /11 is stored by
nobody: `at10_diff.py --pre` read 95 names, 0 with a /11 object (2026-10-11 ~02:4xZ).

## WHAT CHANGES AND WHY IT MOVES NOTHING SERVED

`build` gains one field, `team_sheet`, and the METHOD literal moves. `write_one` treats a stored object at a different method as "not
unchanged" (`dossier.py` `write_one`: `stored_method != METHOD_VERSION` sets `stored_inputs = None`), so each of the 95 names writes ONE new
write-once object at /11; /7 to /10 are kept.

**The pick rule, read at HEAD (`read_dossier`, `dossier.py:1623`):** "If ANY stored object for the name carries this module's current
METHOD_VERSION, the pick is made among those objects only; if none does, among all of them." The deployed API runs `dossier.py` at /10, so
it picks among its /10 objects and ignores /11 until a redeploy carries /11 (leg p). Between w and p the page serves /10 unchanged.

## PREDICTION OF THE WRITTEN CONTENT (read-only, this seat, 2026-10-11 ~02:4xZ)

`python -m lib.research.corpus.team_sheet --census` over the 95 served names (the same reader `build` calls):

| class | names |
|---|---|
| own_new (own `Model NEW VERSION` sheet) | 21 |
| own_model (own `Model` sheet) | 11 |
| master (the master template's rows) | 0 |
| master_absent (rows [], a reason in words; never invented) | 63 |
| sum / served | 95 / 95 |

The 63 are the names with no figure-carrying workbook of their own, and the master template
(`FactSet Based ONE PAGER TEMPLATE 2026 03 09_v2.xlsx`) is not in the store. CTO msg 3170: find and ingest, else no stand-in. The find is
`CRPS-at-4` (site-Z read, XB-7dd9: received in `0.7.0_AE_CloudOps~ZC`'s inbox 21:04Z 10-10, unacked, `~ZC` just spawned).

## THE ACT, IN ORDER (one NEVER-2 entry, slug `amgt-corpus-r44-at10`, opened before leg w)

0. **Gate.** Both halves signed. `git diff 3bff293266 HEAD -- lib/research/corpus/dossier.py lib/research/corpus/team_sheet.py` is empty.
   fitz asserted real in the write process (a stub aborts). `at10_diff.py --pre` reads 0 names with a /11 object.
1. **(w)** from dell1, `dossier.write_one` per name in 6 threads of one process (the round 41/42/44 driver). Expected: 95 written.
2. **(v)** `checks/round44/at10_diff.py --post` on the WRITTEN /11 objects: every field of every name classed SAME / NEWFIELD / CHANGED /
   DROPPED against /10; the stored `team_sheet` of each name compared to a fresh `team_sheet.rows_for`. Expected: NEWFIELD = `team_sheet` on
   all 95 and nothing else; CHANGED = only `model_rows` (the daily model block; each printed WHOLE); DROPPED 0; stored equals the reader 95/95;
   class counts equal the census above unless an input moved, in which case they are printed and read.
3. **(p) NOT SIGNED HERE.** AMGT_RESAPP redeploys the API carrying `dossier.py` at /11 and `scoped_amgt.py` reading the stored field. It waits
   on `CRPS-at-4`'s master-template read: **master absent** -> leg p carries /11; **master found** -> ingest, then a /12 write under its own
   pair, and ONE leg p carries /12. This keeps it to one redeploy either way. The /11 write moves nothing served, so it does not wait.

## EXPECTED OUTCOME (every branch)

- **Writers:** 1 for the dossier object (`dossier.write_one`; `continuation.write_one` writes the continuation artifact, a different object).
  **Pick rule:** 1 (`read_dossier`, the reader's own method). Both read above.
- **Readers of the stored object outside the deployed API:** `backlog.py:173` and `base_census.py:149`, both ad-hoc and read-only; they read
  /11 once written when run from box/dell1 code. Nothing scheduled reads it.
- **Branch A:** 95 written; leg v as stated; the page serves /10 unchanged until p.
- **Branch B:** a name fails to write: listed; it keeps serving /10.
- **Branch C:** leg v reads CHANGED outside `model_rows`, a NEWFIELD other than `team_sheet`, any DROPPED, or a stored `team_sheet` unequal to
  the reader: listed, to the CTO, no second write without a ruling.
- **Between w and p:** the page serves /10 unchanged.

## BLAST RADIUS AND ROLLBACK (per key)

| what | may touch | rollback |
|---|---|---|
| gold research-dossier, `security_key=<KEY>/`, 95 partitions | ONE new write-once object per partition; nothing overwritten or deleted | before p nothing served moves; after p, re-deploying the API at /10 serves that method again; no delete |
| the Security Analysis page, ONLY after leg p | each served name's `model.team_sheet` field (own_new / own_model rows, or the `master_absent` reason) | as above |

Never touched: any Bloomberg or vendor call, the model blocks, field_map.json, the scheduled task, any portal file, any other firm.

**COO HALF: SIGNED** by `2.0.0_SA_COO~C1`, 2026-10-11 ~02:5xZ, for legs 0, w and v, covering branches A to C and the window between w
and p. Leg p is named and is not signed here.

**CTO HALF:** owed by `1.0.0_SA_CTO~DELL1`.
