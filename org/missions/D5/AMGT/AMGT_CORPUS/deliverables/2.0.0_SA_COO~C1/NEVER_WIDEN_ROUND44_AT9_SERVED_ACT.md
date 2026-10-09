# AMGT_CORPUS round 44 -- never-widen pair for `CRPS-at-9`: re-write the 95 research dossiers at method version 10, restoring the PDF reads /9 lost (row D1-S2)

**Authority:** `1.0.0_SA_CTO~DELL1` ruling msg 3213 ("fix forward with a /10 now, decoupled from team_sheet; no /7 re-pin ... Pair shaped like
ar-2. Its leg v diffs EVERY dossier section of all 95 names against /7 and /9 ... Pre-write, assert fitz imports real (not stubbed) and
print the version"). Row `AMGT_CORPUS-D1-S2` (ARMED) @`f60af71c3f`. Producer change `CRPS-at-8` (METHOD literal only), drained
@`548315f918` (`lib/research/corpus/dossier.py` last changed at `54ffd435c7`).

**Code:** box/dell1 at or after `548315f918`, with `dossier.py` equal to `54ffd435c7`'s: the /9 method with `METHOD_VERSION` =
`amgt-corpus-dossier/10`; no logic change, no team_sheet (that is /11).
**Served today:** /9 (since 19:51:25Z). /7 and /8 stored, unserved.

## WHAT IS WRONG AND WHY /10 FIXES IT

`build` reads the team cases of a PDF pack through `_pdf_words_reader`, which uses fitz. The /8 (round 41) and /9 (round 42) writes ran on
dell1 with fitz STUBBED (its DLL did not load until 0.0.0_AB_MSTR~DELL1 placed msvcp140.dll at 20:03Z, msg 3108). So six PDF names were
written with no cases: 8035 JP, BZLFY US, HEI US, SNPS US, TSM US, V US (`evidence/r44_fwd16_census_v9_20261009.txt`; per method, TSM, V
and 8035 hold 3 cases at /6 and /7 and 0 at /8 and /9; ASML 3 at every method). An unchanged method with unchanged inputs writes nothing,
so the repair is a new method version written where fitz loads.

## PRE-WRITE (read-only)

- `import fitz` is real: `fitz real True version 1.28.2` (PyMuPDF bindings), and `METHOD_VERSION` reads `amgt-corpus-dossier/10`, on this
  box at HEAD after `548315f918`. Leg w asserts the same in-process before its first write and aborts if fitz is a stub.
- In-memory rebuild with the real fitz: TSM US and V US return upside / base / downside all with a value.
- The every-field diff in its pre-write form (`checks/round44/at9_diff.py --pre`) builds each name in memory at ~2 minutes a name, so it
  is run POST-write against the stored objects instead (identical content: the write stores exactly what `build` returns).

## THE ACT, IN ORDER (one NEVER-2 entry, slug `amgt-corpus-r44-at9`, opened before leg w)

0. **Gate.** Both halves signed. `git diff 54ffd435c7 HEAD -- lib/research/corpus/dossier.py` is empty. fitz real asserted.
1. **(w)** from dell1, `dossier.write_one` per name in 6 threads of one process (round 41/42's leg w), WITH THE REAL fitz (no stub in the
   driver; it asserts `hasattr(fitz, "open")` first). Each name writes ONE new write-once object at /10; /7, /8, /9 kept. Expected: 95
   written.
2. **(v)** `checks/round44/at9_diff.py --post` on the WRITTEN /10 objects: every field of every name classed SAME / GAIN9 / RESTORE7 /
   BOTH-DIFFER / ALL-DIFFER against /7 and /9. Expected: RESTORE7 = cases on the six names (and any pillars/management a stub dropped);
   GAIN9 = exactly the 12 /9 gains; BOTH-DIFFER 0 (nothing moved for no reason); ALL-DIFFER read line by line. Plus `--pick-census`
   current 95. Fields fed by inputs that changed since /7 (the daily model block) will read GAIN9 or ALL-DIFFER and are LISTED and read,
   not hidden; a field-level move other than those is Branch C.
3. **(p) NOT THIS SEAT'S LEG.** AMGT_RESAPP's mm-4 redeploy carries `dossier.py` at `54ffd435c7` (/10); the CTO amends that half when the
   /10 pin exists. Until p the page serves /9 (no cases on the six). After p: one live read of TSM US cases (three present).

## EXPECTED OUTCOME (every branch)

- **Writers:** 1 (`dossier.write_one`, only from a write run). **Pick rule:** 1 (`read_dossier`, newest of the reader's own method).
- **Branch A:** 95 written; leg v as stated; after p the TSM read shows three cases.
- **Branch B:** a name fails to write: listed; it keeps serving /9.
- **Branch C:** leg v reads BOTH-DIFFER above 0, a GAIN9 set unequal to the 12, or cases not restored on all six: listed, to the CTO,
  no second write without a ruling.
- **Between w and p:** the page serves /9 unchanged.

## BLAST RADIUS AND ROLLBACK (per key)

| what | may touch | rollback |
|---|---|---|
| gold research-dossier, `security_key=<KEY>/`, 95 partitions | ONE new write-once object per partition; nothing overwritten or deleted | before p nothing served moves; after p, re-deploying the API at /9 (or /7) serves that method again; no delete |
| the Security Analysis page, ONLY after leg p | the six names' team cases return; the 12 /9 gains stay | as above |

Never touched: any Bloomberg or vendor call, the model blocks, field_map.json, the scheduled task, any portal file, any other firm.

**COO HALF: SIGNED** by `2.0.0_SA_COO~C1`, 2026-10-09 ~21:5xZ, for legs 0, w and v, covering branches A to C and the window between w
and p. Leg p is named and is not signed here.

**CTO HALF:** owed by `1.0.0_SA_CTO~DELL1`.
