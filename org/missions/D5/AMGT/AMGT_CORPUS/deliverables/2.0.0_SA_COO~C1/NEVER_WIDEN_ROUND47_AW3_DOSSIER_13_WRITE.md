# AMGT_CORPUS round 47 -- never-widen pair for `CRPS-aw-3`: re-write the 95 research dossiers at method version 13 (row labels in words, the corrected header, the by-name CONTROL rule, the team's number formats, the master template's rows)

**Authority:** `1.0.0_SA_CTO~DELL1` round-46 analysis `ledger/ROUND_ANALYSIS.round46.md` s.3 and ADDENDA 1 to 3 (msgs 3972, 3994, 4001): "the /13 write waits on [the
template cell]"; "each is its own never-widen pair". **Producer change:** `CRPS-aw-1` incl. AMENDMENTS 1 to 3, drained @7a58fb83fc (instance VALID rc 0; the issuer re-ran
AC1-AC4 on the merged tree: `aw1 build 4/4 control 2/2`, 143 passed, the literal reads /13, `aw9 build 4/4 control 2/2`; the whole corpus directory 604 passed).
**Input:** the master template stored write-once in `research_template` (ledger `amgt-corpus-r47-aw10` CLOSED, commit 3940506393): 1 key, 383839 B, sha256 `00bb23a6b08b35ca...`.

**Served today:** /12 (the deployed API's `dossier.py` is at /12: `l8egBo` -> `SOzAz9` -> `VNcX9ntm` -> `TmeKvn83`, which carries no round-47 file, R1 msg 4050). /13 is stored by
nobody: `aw3_diff.py --pre` read 95 names, 95 with a /12 object, 0 with a /13 object.

## WHAT CHANGES AND WHY IT MOVES NOTHING SERVED BEFORE ITS REDEPLOY

`build` stores one richer `team_sheet` field and the METHOD literal moves. `write_one` treats a stored object at a different method as "not unchanged", so each of the
95 names writes ONE new write-once object at /13; /7 to /12 are kept. **The pick rule (`read_dossier`):** if ANY stored object for the name carries the reader's current
METHOD_VERSION, the pick is made among those only; the deployed API runs `dossier.py` at /12 and picks among its /12 objects until a redeploy carries /13 (leg p, `CRPS-aw-4`,
AMGT_RESAPP's window, its own pair). Between w and p the page serves /12 unchanged.

## PREDICTION OF THE WRITTEN CONTENT (read-only, this seat, ~19:5xZ; the reader's own census over the live store and the stored template)

| class | names | | row classes | own (32) | master (63) |
|---|---|---|---|---|---|
| own_new | 21 | | FIGURE | 3529 | 7938 |
| own_model | 11 | | HEADING | 107 | 252 |
| master (was master_absent) | 63 | | CONTROL | 123 | 315 |
| sum / served | 95 / 95 | | rows | 3759 | 8505 (135 each) |

- **Own names, against the stored /12:** the six old keys (class, workbook_key, sheet, rows, model_rows_beside, reason) equal on 32 of 32. Row-class transitions over 32 names:
  HEADING>CONTROL 32 (`EQY_FUND_YEAR`), FIGURE>CONTROL 29 (`BEST_FPERIOD_OVERRIDE`), **HEADING>FIGURE 177** (CLX 65, ML FP 65, BABA 47: the round-46 header test took the
  `EQY_FUND_YEAR` row as the header and served those names' model rows as headings with no value; row D1-S7, the issuer's own reading, remedied in AMENDMENT 1). Rows carrying a
  team value: 3529, all own.
- **Master names (63):** class `master`, 135 rows each, the template's own rows and labels, cited; **no value, no number format, no period**: the template workbook is filled with one
  sample company's figures (`Ticker: CPA-US`) and AMENDMENT 3 serves none of them (measured before this write: 11467 rows with a value, 7938 of them the template's).
- **Labels (row_labels claims, by rows):** own 3759 rows: held 678, measured 337, absent 427 (394 `FactSet line`, 33 `Bloomberg line`), none 2317; master 8505 rows: held 63, measured 1008,
  absent 1260, none 6174. Measured labels are
  the team's own cells read from the workbook, cited `<sheet>!<cell>`; the 50 FactSet codes with no published description read "FactSet line", claim absent.
- **Size (a change for the API payload):** `team_sheet` per name: own 62,285 to 102,306 bytes (median 80,759), master 15,136; 3,628,380 bytes over 95 names. Round 46 stored at most
  33,942 bytes per name. The CTO half rules whether that size is accepted.

## THE ACT, IN ORDER (one NEVER-2 entry, slug `amgt-corpus-r47-aw3`, OPENED BEFORE leg w)

0. **Gate.** Both halves signed. `git diff 7a58fb83fc HEAD -- lib/research/corpus/dossier.py lib/research/corpus/team_sheet.py lib/research/corpus/template.py` is empty.
   fitz asserted real in the write process (a stub aborts). `dossier_write_v13.py` leg 0 prints, per name, whether a /12 object exists (95 of 95 at the pre-read); a name without one is
   listed and left out. `aw3_diff.py --pre` reads 0 names with a /13 object.
1. **(w)** from dell1, `dossier.write_one` per name in 6 threads of one process (`checks/round47/dossier_write_v13.py`). Expected: 95 written.
2. **(v)** `checks/round47/aw3_diff.py --post` on the WRITTEN /13 objects: every field of every name classed SAME / NEWFIELD / CHANGED / DROPPED against /12; the `team_sheet` arm
   by class as predicted above (own old keys 32/32; master 63/63 with no value; shape; the stored field equals a fresh `rows_for`). Expected: CHANGED on `team_sheet` and `model_rows`
   only; DROPPED 0; any other CHANGED is an input that moved (the daily Bloomberg pull) and is printed WHOLE, named and read, or Branch C.
3. **(p) NOT SIGNED HERE.** AMGT_RESAPP's redeploy carries `dossier.py` at /13 and the closure by blob (`team_sheet.py`, `template.py`, `factset_descriptions.json`, the field map
   `integrations/bloomberg/research/field_map.json`, `opal_naming.py`). It is `CRPS-aw-4`: its own pair.

## THE BYTES (read on dell1 at HEAD c691f46640)

| path | blob | role |
|---|---|---|
| `lib/research/corpus/dossier.py` | `13463426d0da` | `METHOD_VERSION` /13, `build` stores `team_sheet.rows_for` |
| `lib/research/corpus/team_sheet.py` | `956e69d7be7e` | the reader: year-row header, by-name CONTROL, labels, formats, the master arm, no master values |
| `lib/research/corpus/template.py` | `e03d6a8acf65` | the `research_template` table |
| `lib/research/corpus/factset_descriptions.json` | `76faa8d6a708` | FactSet description entries (empty) |
| `integrations/bloomberg/research/field_map.json` | `5257e0e5b5d6` | the Bloomberg field descriptions the labels cite |
| `lib/research/harvest/store.py` | `34b344de8ed1` | `bronze_put`, the address builder |

## EXPECTED OUTCOME (every branch)

- **Writers of the dossier object:** 1 (`dossier.write_one`). **Pick rule:** 1 (`read_dossier`). **Scheduled callers:** none (round 45's and this round's CTO halves read the site-Z
  task list: none writes a dossier or a `research_template` object). **Readers of the stored object outside the deployed API:** `backlog.py` and `base_census.py`, ad-hoc and read-only.
- **Branch A:** 95 written; leg v as stated; the page serves /12 unchanged until p.
- **Branch B:** a name fails to write, or a raised `rows_for` stores a narrower answer: listed; that name keeps serving /12 until a second write is ruled.
- **Branch C:** leg v reads DROPPED > 0, a master name carrying a value, a changed old key on an own name, a shape break, a stored field unequal to the reader, or a CHANGED outside
  `team_sheet` and `model_rows` not attributable to a moved input: listed, to the CTO, no second write without a ruling.
- **Between w and p:** the page serves /12 unchanged.

## BLAST RADIUS AND ROLLBACK (per key)

| what | may touch | rollback |
|---|---|---|
| gold research-dossier, `security_key=<KEY>/`, 95 partitions | ONE new write-once object per partition; nothing overwritten or deleted | before p nothing served moves; after p, re-deploying the API at /12 serves that method again; no delete |
| the Security Analysis page, ONLY after leg p | each served name's `model.team_sheet` gains row_labels and row_formats, the corrected classes, and (63 names) the template's rows; the payload grows (size above) | as above |

Never touched: any Bloomberg or vendor call, the model blocks, the field map, any scheduled task, any portal file, any other firm.

**COO HALF: SIGNED** by `2.0.0_SA_COO~C1`, 2026-10-11 ~19:5xZ, for legs 0, w and v, covering branches A to C and the window between w and p. Leg p is named and is not signed here.

**CTO HALF:** owed by `1.0.0_SA_CTO~DELL1`.
