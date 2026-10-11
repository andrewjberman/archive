# AMGT_CORPUS round 46 -- never-widen pair for `CRPS-av-3`: re-write the 95 research dossiers at method version 12 (row classes and the team's own period values in `team_sheet`)

**Authority:** `1.0.0_SA_CTO~DELL1` round-45 analysis `ledger/ROUND_ANALYSIS.round45.md` @0d399ece09 s.2 item 1 and its ADDENDUM 1 (msg 3846): "The
values ride a dossier write at method /12 and one API redeploy. Each is its own never-widen pair, measured name by name." **Producer change:**
`CRPS-av-1`, drained @`f583a91842` (instance VALID rc 0; the issuer re-ran AC1-AC3 on the merged tree: `av1 build 4/4 control 2/2`, 111 passed,
the literal reads /12; the whole corpus directory 572 passed).

**Code:** box/dell1 at or after `f583a91842`: `lib/research/corpus/dossier.py` `METHOD_VERSION` = `amgt-corpus-dossier/12`; `build` stores
`fields["team_sheet"] = team_sheet.rows_for(security_key, client=client)`, which now carries `row_classes`, `row_numbers`, `row_values`,
`periods` and `row_counts` beside the six round-44 keys.
**Served today:** /11 (the deployed API's `dossier.py` is at /11; leg p of round 44, live at `l8egBo`, now `SOzAz9`). /12 is stored by nobody:
`av3_diff.py --pre` read 95 names, 95 with a /11 object, 0 with a /12 object (2026-10-11 ~13:3xZ).

## WHAT CHANGES AND WHY IT MOVES NOTHING SERVED

`build` stores one richer `team_sheet` field and the METHOD literal moves. `write_one` treats a stored object at a different method as
"not unchanged", so each of the 95 names writes ONE new write-once object at /12; /7 to /11 are kept.

**The pick rule (`read_dossier`, `dossier.py`):** if ANY stored object for the name carries the reader's current METHOD_VERSION, the pick is
made among those only; if none does, among all. The deployed API runs `dossier.py` at /11, so it picks among its /11 objects and ignores /12
until a redeploy carries /12 (leg p, `CRPS-av-4`, AMGT_RESAPP's window, its own pair). Between w and p the page serves /11 unchanged.

## PREDICTION OF THE WRITTEN CONTENT (read-only, this seat, ~13:3xZ; the reader's own census, the same function `build` calls)

| class | names | | row classes over the 32 own workbooks | rows |
|---|---|---|---|---|
| own_new | 21 | | FIGURE | 3381 |
| own_model | 11 | | HEADING | 316 |
| master | 0 | | CONTROL | 62 |
| master_absent | 63 | | sum (= the counted rows) | 3759 |
| sum / served | 95 / 95 | | largest field (AZN LN) / median / total | 33,942 / 25,226 / 796,077 bytes |

4,296 cells among the FIGURE rows' period values are text (for example `#VALUE!`), carried verbatim. The 63 `master_absent` names carry the new
keys empty. The master template is still not in the library (round-45 au-1/au-2 read).

## THE ACT, IN ORDER (one NEVER-2 entry, slug `amgt-corpus-r46-av3`, OPENED BEFORE leg w -- round 45's was opened late)

0. **Gate.** Both halves signed. `git diff f583a91842 HEAD -- lib/research/corpus/dossier.py lib/research/corpus/team_sheet.py` is empty.
   fitz asserted real in the write process (a stub aborts). `dossier_write_v12.py` leg 0 prints, per name, whether a /11 object exists (95
   of 95 at the pre-read); a name without one is listed and left out. `av3_diff.py --pre` reads 0 names with a /12 object.
1. **(w)** from dell1, `dossier.write_one` per name in 6 threads of one process (`checks/round46/dossier_write_v12.py`). Expected: 95 written.
2. **(v)** `checks/round46/av3_diff.py --post` on the WRITTEN /12 objects: every field of every name classed SAME / NEWFIELD / CHANGED /
   DROPPED against /11; the `team_sheet` arm: the six old keys equal /11's on every name (the field is additive), the shape holds
   (`row_classes`, `row_numbers`, `row_values` as long as `rows`, `row_counts` summing to it), the stored field equals a fresh
   `rows_for` on every name; per name FIGURE / HEADING / CONTROL and FIGURE rows with and without a team value; the by-source ESTIMATE.
   Expected: CHANGED on `team_sheet` and `model_rows` only; DROPPED 0; any other CHANGED is an input that moved (the au-1 ingest stored
   12 new bronze objects) and is printed WHOLE, named and read, or Branch C.
3. **(p) NOT SIGNED HERE.** AMGT_RESAPP's redeploy carries `dossier.py` at /12 (and `team_sheet.py` by blob, as the reader the build
   closes over). It is `CRPS-av-4`: its own pair, admitted by blob over the build's closure.

## EXPECTED OUTCOME (every branch)

- **Writers of the dossier object:** 1 (`dossier.write_one`; `continuation.write_one` writes the continuation artifact, a different
  object). **Pick rule:** 1 (`read_dossier`). **Scheduled callers:** none (the CTO half of round 45's au-1 read: no repo schedule writes a
  dossier; the site-Z task list names none that does).
- **Readers of the stored object outside the deployed API:** `backlog.py` and `base_census.py`, ad-hoc and read-only.
- **Branch A:** 95 written; leg v as stated; the page serves /11 unchanged until p.
- **Branch B:** a name fails to write, or a raised `rows_for` stores the old six-key answer (worker row `D1-W1-S7`: the fallback is not
  widened, and the page treats absent keys as the rows-only branch): listed; that name keeps serving /11 until a second write is ruled.
- **Branch C:** leg v reads DROPPED > 0, a changed old key inside `team_sheet`, a shape break, a stored field unequal to the reader, or a
  CHANGED outside `team_sheet` and `model_rows` that is NOT attributable to a moved input: listed, to the CTO, no second write without a ruling.
- **Between w and p:** the page serves /11 unchanged.

## BLAST RADIUS AND ROLLBACK (per key)

| what | may touch | rollback |
|---|---|---|
| gold research-dossier, `security_key=<KEY>/`, 95 partitions | ONE new write-once object per partition; nothing overwritten or deleted | before p nothing served moves; after p, re-deploying the API at /11 serves that method again; no delete |
| the Security Analysis page, ONLY after leg p | each served name's `model.team_sheet` gains the five keys (the payload grows by at most 34 KB per name) | as above |

Never touched: any Bloomberg or vendor call, the model blocks, field_map.json, the scheduled task, any portal file, any other firm.

**COO HALF: SIGNED** by `2.0.0_SA_COO~C1`, 2026-10-11 ~13:4xZ, for legs 0, w and v, covering branches A to C and the window between w and p.
Leg p is named and is not signed here.

**CTO HALF:** owed by `1.0.0_SA_CTO~DELL1`.
