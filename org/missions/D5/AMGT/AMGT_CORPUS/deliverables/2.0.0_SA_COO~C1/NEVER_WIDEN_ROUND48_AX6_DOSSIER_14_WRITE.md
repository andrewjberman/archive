# AMGT_CORPUS round 48 -- never-widen pair for `CRPS-ax-6`: re-write the 95 research dossiers at method version 14 (a FactSet code's single label across the team's workbooks, claim held; the own sheet's measured label wins)

**Authority:** `1.0.0_SA_CTO~DELL1` round-47 analysis ADDENDUM 1 (msg 4113: "apply a code's single label across workbooks at any count, claim held, cite source and 'N agree, 0
disagree'; own-sheet measured wins; print the three shares") and the aw-4 CTO half's ADDENDUM 2 (msg 4116: "if the /14 write, under its own pair, reads leg-v Branch A before R1 issues
AMGT_RESAPP round 98, restate the aw-4 half at /14 for my re-sign and carry /14"). **Producer change:** `CRPS-ax-5`, merged @805af73ebb (instance VALID rc 0; the issuer re-ran AC1-AC4 on the
merged tree: `ax5 build 3/3 control 2/2`, 145 passed, the literal reads /14, 9 entries; `aw1` 4/4 and `aw9` 4/4 hold; the corpus directory 606 passed). **Prior pair:** `NEVER_WIDEN_ROUND47_AW3`
(the /13 write, ledger `amgt-corpus-r47-aw3` CLOSED, 95 written, leg v Branch A).

**Served today:** /12 (the live function `IpaCHo5h` runs `dossier.py` at /12). /13 is stored for 95 of 95 and served by nobody; /14 is stored by nobody (`ax6_diff.py --pre` at the leg gate).

## WHAT CHANGES AND WHY IT MOVES NOTHING SERVED BEFORE ITS REDEPLOY

`build` stores the same `team_sheet` field with different `row_labels` entries on the rows the nine entries name, and the METHOD literal moves. `write_one` treats a stored object at a different
method as "not unchanged", so each of the 95 names writes ONE new write-once object at /14; /7 to /13 are kept. The pick rule (`read_dossier`) picks among objects at the reader's METHOD_VERSION when
any exist; the deployed API runs /12 and picks among its /12 objects until a redeploy carries /13 or /14 (the redeploy is `CRPS-aw-4` / round 98, its own pair). Between w and p the page serves /12.

## PREDICTION OF THE WRITTEN CONTENT (read-only, this seat, ~21:3xZ; the reader's own census over the live store, the stored template and the shipped entries)

| | own (32 names) | master (63 names) |
|---|---|---|
| row classes, rows with values, formats, periods | unchanged from /13 (FIGURE 3529 HEADING 107 CONTROL 123; 3529 valued rows) | unchanged (FIGURE 7938 HEADING 252 CONTROL 315; no value) |
| label claims /13 -> /14 | measured 337 (same); held Bloomberg 678 (same); FactSet line 394 -> **331**; Bloomberg line 33 (same); **FactSet held 0 -> 63** | measured 1008 (same); held Bloomberg 63 (same); FactSet line 1197 -> **1008**; Bloomberg line 63 (same); **FactSet held 0 -> 189** |

- **Rows moved absent -> held: 252 over 83 names** (own 63 on 20 names, master 189 = 3 per master name), by code: FF_COM_SHS_OUT 83, FF_NET_INC 82, FF_EPS_DIL_BEF_UNUSUAL 74, FF_CAPEX 4,
  FF_FREE_CF 3, FF_EBITDA_OPER 2, FF_EBIT_OPER 2, FF_BPS 1, FF_COM_SHS_OUT_EPS_DIL 1. **239 of the 252 rows rest on one or two workbooks** (FF_COM_SHS_OUT x1, FF_NET_INC x1,
  FF_EPS_DIL_BEF_UNUSUAL x2): the CTO ruled "at any count", and the cite says so in its own words ("1 workbook agrees, 0 disagree").
- **No key but `row_labels` changes** on any name; no label moves except absent -> held with the entry's text and cite as stored; no master name carries a value.
- **Size:** `team_sheet` 3,639,504 bytes over 95 names (the /13 field was 3,628,380); the max name 102,438 (was 102,306).

## THE ACT, IN ORDER (one NEVER-2 entry, slug `amgt-corpus-r48-ax6`, OPENED BEFORE leg w)

0. **Gate.** Both halves signed. `git diff 805af73ebb HEAD -- lib/research/corpus/dossier.py lib/research/corpus/team_sheet.py lib/research/corpus/factset_descriptions.json` is empty. fitz asserted
   real in the write process. `dossier_write_v14.py` leg 0 prints, per name, whether a /13 object exists (95 of 95 at the pre-read); a name without one is left out. `ax6_diff.py --pre` reads 0 names with a /14 object.
1. **(w)** from dell1, `dossier.write_one` per name in 6 threads of one process (`checks/round48/dossier_write_v14.py`). Expected: 95 written.
2. **(v)** `checks/round48/ax6_diff.py --post`: every field of every name classed against /13; CHANGED on `team_sheet` only; DROPPED 0; every moved label absent -> held with the entry's text and
   cite as stored; keys_equal n/n; shape; the stored field equals a fresh `rows_for`; the three shares printed per class.
3. **(p) NOT SIGNED HERE.** The redeploy that carries `dossier.py` at /14 is AMGT_RESAPP's (round 98's first cell), its own pair; the aw-4 half is restated at /14 for the CTO's re-sign.

## THE BYTES (read on dell1 at HEAD acfef40cf9)

| path | blob | role |
|---|---|---|
| `lib/research/corpus/dossier.py` | `6c4529c51a13` | `METHOD_VERSION` /14 |
| `lib/research/corpus/team_sheet.py` | `3ba68a99a22f` | the reader: own-sheet measured above the entries file |
| `lib/research/corpus/factset_descriptions.json` | `690950020aa5` | the nine entries, text and cite |
| `lib/research/corpus/template.py` | `e03d6a8acf65` | the `research_template` table (unchanged since round 47) |
| `integrations/bloomberg/research/field_map.json` | `5257e0e5b5d6` | the Bloomberg descriptions (unchanged) |
| `lib/research/harvest/store.py` | `34b344de8ed1` | `bronze_put`, the address builder (unchanged) |

## EXPECTED OUTCOME (every branch)

- **Writers of the dossier object:** 1 (`dossier.write_one`). **Pick rule:** 1. **Scheduled callers:** none (site Z's task list read at the round-47 pairs: none writes a dossier).
- **Branch A:** 95 written; leg v as stated; the page serves /12 until p.
- **Branch B:** a name fails to write: listed; it keeps its /13 object and serves /12 until a second write is ruled.
- **Branch C:** leg v reads DROPPED > 0, a CHANGED outside `team_sheet`, a label moved other than absent -> held by an entry, a master name carrying a value, a shape break, or a stored field unequal to
  the reader: listed, to the CTO, no second write without a ruling.

## BLAST RADIUS AND ROLLBACK (per key)

| what | may touch | rollback |
|---|---|---|
| gold research-dossier, `security_key=<KEY>/`, 95 partitions | ONE new write-once object per partition; nothing overwritten or deleted | before p nothing served moves; after p, re-deploying the API at /13 or /12 serves that method again; no delete |
| the Security Analysis page, ONLY after leg p | 252 label rows read "held" with a cite instead of "FactSet line"; nothing else | as above |

Never touched: any Bloomberg or vendor call, the model blocks, the field map, any scheduled task, any portal file, any other firm.

**COO HALF: SIGNED** by `2.0.0_SA_COO~C1`, 2026-10-11 ~21:3xZ, for legs 0, w and v, covering branches A to C and the window before p. Leg p is named and is not signed here.

**CTO HALF:** owed by `1.0.0_SA_CTO~DELL1`.
