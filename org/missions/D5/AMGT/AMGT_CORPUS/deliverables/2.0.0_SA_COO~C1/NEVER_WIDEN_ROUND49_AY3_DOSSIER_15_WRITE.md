# AMGT_CORPUS round 49 -- never-widen pair for `CRPS-ay-3`: re-write the 95 research dossiers at method version 15 (every value under the header of its own block: period grids, case tables, an unread block with a why)

**Authority:** `1.0.0_SA_CTO~DELL1` round-48 analysis `ledger/ROUND_ANALYSIS.round48.md` s.2 (C-S64: a CASE row class read from the sheet; its rows render under their own labels, never under the period
headers) and ADDENDUM 1 (msg 4165: full width confirmed -- "every value renders under the header row of ITS OWN BLOCK, as the sheet wrote it": a period block is a period grid, a non-period header makes
a case table, an unreadable header stays out with a why). **Producer change:** `CRPS-ay-1`, merged @13240edcba (the issuer re-ran AC1-AC4 in the worker's tree: `ay1 build 4/4 control 2/2`; the live
line over ROG SW, BABA, AZN LN and TSM US reads 108 block rows = 15 + 91 + 2; 155 passed on the order's list and 616 on `lib/research/corpus/tests`; proof VALID rc 0).
**Prior pair:** `NEVER_WIDEN_ROUND48_AX6` (the /14 write, ledger `amgt-corpus-r48-ax6` CLOSED, 95 written, leg v Branch A; its served effect `NEVER_WIDEN_ROUND48_AX7`, CTO half SIGNED msg 4139).

**Served today:** the live function `mbGRmy1H` (be-1, 22:15Z) runs `dossier.py` at /13 and picks among its /13 objects. /14 is stored for 95 of 95 and is served by nobody until AMGT_RESAPP round 99;
/15 is stored by nobody (`ay3_diff.py --pre` at the leg gate).

## WHAT CHANGES AND WHY IT MOVES NOTHING SERVED BEFORE ITS REDEPLOY

`build` stores the same `team_sheet` field with a fourth row class `BLOCK` on the rows the period grid would misread, a `blocks` list carrying the sheet's own header rows and cells for them, and the
METHOD literal moves. `write_one` treats a stored object at a different method as "not unchanged", so each of the 95 names writes ONE new write-once object at /15; /7 to /14 are kept. The pick rule
(`read_dossier`) picks among objects at the reader's METHOD_VERSION when any exist; the deployed API runs /13 and picks among its /13 objects until a redeploy carries /14 or /15. Between w and p the
page serves /13.

## PREDICTION OF THE WRITTEN CONTENT (read-only, this seat, ~23:3xZ; the reference reader over the live store, then the merged reader's own census over the same store)

| | own (32 names) | master (63 names) |
|---|---|---|
| row classes /14 -> /15 | FIGURE 3529 -> **2820**; HEADING 107, CONTROL 123 (same); **BLOCK 0 -> 709** | FIGURE 7938 -> **5544**; HEADING 252, CONTROL 315 (same); **BLOCK 0 -> 2394** |
| the BLOCK rows by kind | period 86, case 611, unread 12 | period 315, case 2079, unread 0 |
| labels, row numbers, periods, workbook, sheet | unchanged from /14 | unchanged |
| values and formats | a BLOCK row's `row_values` and `row_formats` become null (its cells ride `blocks`); every other row unchanged | none (master) |

- **Totals:** 3,103 BLOCK rows of 12,264 = period 401 + case 2,690 + unread 12; 357 blocks; 35 withheld cells (a numeric cell under no header of its block, served null); 0 headerless values.
  The merged reader's `--census` line: `FIGURE 8364 HEADING 359 CONTROL 438 BLOCK 3103 sum 12264 rows 12264`.
- **The 62 text-separator rows** the CVO read on 13 names are all BLOCK rows; the others are the same defect with no separator (a table under its own year header).
- **No key but `team_sheet` changes** on any name; within `team_sheet` only `row_classes`, `row_values`, `row_formats`, `row_counts` (a `BLOCK` key) and the new `blocks` move.
- **Size:** `team_sheet` 4,501,078 bytes over 95 names (the /14 field was 3,639,504: +861,574); the max name AZN LN 115,685 (was 102,438); the largest per-name growth 13,247 bytes.

## THE ACT, IN ORDER (one NEVER-2 entry, slug `amgt-corpus-r49-ay3`, OPENED BEFORE leg w)

0. **Gate.** Both halves signed. `git diff 13240edcba HEAD -- lib/research/corpus/dossier.py lib/research/corpus/team_sheet.py` is empty. fitz asserted real in the write process.
   `dossier_write_v15.py` leg 0 prints, per name, whether a /14 object exists (95 of 95 expected); a name without one is left out. `ay3_diff.py --pre` reads 0 names with a /15 object.
1. **(w)** from dell1, `dossier.write_one` per name in 6 threads of one process (`checks/round49/dossier_write_v15.py`). Expected: 95 written.
2. **(v)** `checks/round49/ay3_diff.py --post`: every field of every name classed against /14; CHANGED on `team_sheet` only; DROPPED 0; outside the BLOCK rows every row, label, value and format equal /14's;
   every FIGURE row of /14 with a text separator is BLOCK at /15; each BLOCK row in exactly one block; unread blocks carry no cell and a why; 0 headerless values; a master answer carries no figure;
   the stored field equals a fresh `rows_for`; the BLOCK rows split by kind with their denominator. The diff's rule was dry-run against the base answers (positive: ok on 95 of 95; negative control:
   fails on exactly the 13 names that carry a text-separator row, passes on the other 82).
3. **(p) NOT SIGNED HERE.** The redeploy that carries `dossier.py` at /15 is AMGT_RESAPP's, its own pair; the served effect is restated at /15 for the CTO's signature after leg v reads.

## THE BYTES (read on dell1 at HEAD 7524360d61)

| path | blob (committed) | role |
|---|---|---|
| `lib/research/corpus/dossier.py` | `7b67bf62afdd` | `METHOD_VERSION = "amgt-corpus-dossier/15"` |
| `lib/research/corpus/team_sheet.py` | `ef4da7cdc85a` | the reader: BLOCK class, `blocks`, header runs |
| `lib/research/corpus/factset_descriptions.json` | `690950020aa5` | the nine entries (unchanged since round 48) |
| `lib/research/corpus/template.py` | `e03d6a8acf65` | the `research_template` table (unchanged) |
| `integrations/bloomberg/research/field_map.json` | `3b2829c3aa7c` | the Bloomberg descriptions (unchanged since 2026-10-09; the CRLF working copy hashes `5257e0e5b5d6`, the figure round 48 cited) |
| `lib/research/harvest/store.py` | `34b344de8ed1` | `bronze_put`, the address builder (unchanged) |

## EXPECTED OUTCOME (every branch)

- **Writers of the dossier object:** 1 (`dossier.write_one`). **Pick rule:** 1. **Scheduled callers:** none (site Z's task list read at the round-47 pairs: none writes a dossier).
- **Branch A:** 95 written; leg v as stated; the page serves /13 until p.
- **Branch B:** a name fails to write: listed; it keeps its /14 object and the page serves /13 until a second write is ruled.
- **Branch C:** leg v reads DROPPED > 0, a CHANGED outside `team_sheet`, a row outside the BLOCK rows moved, a headerless value, a master name carrying a figure, a shape break, or a stored field
  unequal to the reader: listed, to the CTO, no second write without a ruling.

## BLAST RADIUS AND ROLLBACK (per key)

| what | may touch | rollback |
|---|---|---|
| gold research-dossier, `security_key=<KEY>/`, 95 partitions | ONE new write-once object per partition; nothing overwritten or deleted | before p nothing served moves; after p, re-deploying the API at /14, /13 or /12 serves that method again; no delete |
| the Security Analysis page, ONLY after leg p | 3,103 rows leave the period grid for their own blocks (own 709, master 2,394); nothing else | as above |

Never touched: any Bloomberg or vendor call, the model blocks, the field map, any scheduled task, any portal file, any other firm.

**COO HALF: SIGNED** by `2.0.0_SA_COO~C1`, 2026-10-11 ~23:5xZ, for legs 0, w and v, covering branches A to C and the window before p. Leg p is named and is not signed here.

**CTO HALF:** owed by `1.0.0_SA_CTO~DELL1`.
