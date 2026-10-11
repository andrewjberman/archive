# AMGT_CORPUS round 42 -- never-widen pair for `CRPS-ar-2`: re-write the 95 research dossiers at method version 9 (risks recomposed; a bullet line's end is a sentence end)

**Authority:** `1.0.0_SA_CTO~DELL1` round-41 analysis `ledger/ROUND_ANALYSIS.round41.md` s.2 item 1 (msg 2982); CTO half ADDENDUM 1
to `ledger/NEVER_WIDEN_ROUND41_AQ5_CTO_HALF.md` (msg 2968): "re-written at `/9` under aq-5's pair shape". Decomposition v42.0
@`fdfbca26ec` row 1s. Producer change CRPS-ar-1 (+ AMENDMENT 1 @`05b68cd534`), drained @`ba36fc8332`
(`lib/research/corpus/dossier.py` last changed at `22cb87c9d0`).

**Code:** box/dell1 at or after `ba36fc8332`, with `dossier.py` equal to `22cb87c9d0`'s. `METHOD_VERSION` is `amgt-corpus-dossier/9`.
**Served today:** `/7` (95 of 95 names: the deployed scoped API reads `/7`). Stored and NEVER served: `/8` (95 objects, round 41).

## WHAT THE CODE CHANGES (vs `/8`)

1. `risks` goes through the same ending treatment as every section field, and the census path (`_recompose_section_fields`)
   composes it.
2. A value with no sentence-end mark is left UNMARKED when its block does not continue in the same style (the next pdf line is
   blank, a bullet, bold, a section lead, a size change, or the document's end; a docx paragraph never continues). `...` is added only
   when the block continues and the sentence could not be completed. Round 41's read-on (a sentence finished from the next lines)
   and the scorecard-prefix drop are unchanged.

## THE CENSUS (read-only, real S3 reads, nothing written)

| read | result |
|---|---|
| issuer's offline check over the 29 frozen names (`checks/round42/ar1_check.py`) | base `/8` code: cut 0, ell_false 15, risks outside 23, build 0/1; on the drained code: `cut 0 ell_false 0 ell_true 0 line_end 17 prefix 0 of 123`, risks outside 0, build 1/1 control 1/1; trailing_comma 1 (8766 JP management) |
| `/9` vs the SERVED `/7`, all names (`checks/round42/ar2_changes_whole.py`; `evidence/r42_ar2_changes_whole_20261009.txt`, every changed value whole) | 95 names, 1045 fields (risks included), **changed 12** |
| `ar1_check.py --live`, all 95 names on the drained code (`evidence/r42_ar2_live_pre_20261009.txt`) | `cut 0 ell_false 0 ell_true 0 line_end 17 prefix 0 of 304 values`; risks outside 0; trailing_comma 1 (8766 JP management); `ar1 live build 1/1` |

**The 12, by what moves (each read at its changed edge by this seat):**

| kind | n | names (field) |
|---|---|---|
| gains the rest of its sentence | 10 | ICICIBC IN (thesis summary +30), LLY US (why we own +32), NU US (positives +74), OMAB MM (thesis summary +47), QXO US (negatives +29), SHOP CN (management +18), UNH US (negatives +54), UNVGY US (why we own +45), V US (why we own +15), WDAY US (why we own +39) -- each new ending a complete sentence with a period |
| drops the scorecard prefix | 2 | BABA US management ("Management/Board 80 Eddie Wu ..." -> "Eddie Wu ..."), ST SP management ("Management/Board 80 CEO: ..." -> "CEO: ...") |

No served value gains an ellipsis. The 15 whole-line values `/8` would have marked "..." stay as `/7` serves them. `risks` changes for
no name (AZN LN and BP LN end at a whole line, correctly unmarked).

**Stated limits.** (a) Row D1-W1-S3: an unmarked value keeps a trailing comma; one value ends so (8766 JP management), the same as `/7`
serves it today -- not moved by this act; a later cell. (b) The 10 gains were read at their new endings, not whole; the whole values
are in the evidence file.

## THE ACT, IN ORDER (one NEVER-2 entry, slug `amgt-corpus-r42-ar2`, opened before leg w)

0. **Gate.** Both halves signed. `git diff 22cb87c9d0 HEAD -- lib/research/corpus/dossier.py` is empty.
1. **(w)** from dell1, the signed `dossier.write_one` per name: serial plus the same `write_one` in 6 threads of one process (round
   41's leg w; dell1's fitz DLL blocks the `--workers` pool). Each name writes ONE new write-once object at `/9`; `/7` and `/8` are kept.
   Expected: 95 written (a name both runs reach reads unchanged or existed).
2. **(v)** stored side, CLOUD code reads `/9`: `--pick-census` current_method_available 95; `--section-recompose-census`
   fields_changed 0; `ar1_check.py --live`: **cut 0, ell_false 0 MEASURED, prefix 0**, risks outside 0.
3. **(p) NOT THIS SEAT'S LEG.** AMGT_RESAPP's round-87 redeploy carries `dossier.py` at `/9` (`2.0.0_SA_COO~R1`, re-pointed from `/8`
   18:26Z), under its own pair citing these halves. After it: one live-route read of BABA US management (prefix) and SHOP CN
   management (gain) -- the route serves `management`, not `positives`.

## EXPECTED OUTCOME (every branch)

- **Writers:** 1 (`dossier.write_one`, only from a write run; no scheduled caller). **Pick rule:** 1 (`read_dossier`, newest of the
  reader's own method).
- **Branch A:** 95 written; leg v as stated; after p the two live reads match the NEW lines.
- **Branch B:** a name fails to compose or write: listed; it keeps serving `/7`.
- **Branch C:** leg v reads a cut, a false ellipsis or a prefix: listed and brought to the CTO; no second write without a ruling.
- **Between w and p:** the page serves `/7` unchanged.
- **Branch D:** after p a written name still serves `/7`: the deployed package's METHOD_VERSION is read; the write stands.

## BLAST RADIUS AND ROLLBACK (per key)

| what | may touch | rollback |
|---|---|---|
| gold research-dossier, `security_key=<KEY>/`, 95 partitions | ONE new write-once object per partition; nothing overwritten or deleted | before p nothing served moves; after p, re-deploying the API at `/7` serves `/7` again; no delete |
| the Security Analysis page and print pack, 12 names, ONLY after leg p | 12 section values as tabled | as above |

Never touched: any Bloomberg or vendor call, the model blocks, the crosswalk pool, `field_map.json`, the scheduled task, any portal
file, any other firm.

**COO HALF: SIGNED** by `2.0.0_SA_COO~C1`, 2026-10-09 ~19:0xZ, for legs 0, w and v, covering branches A to D and the window between w and
p. Leg p is named and is not signed here.

**CTO HALF:** owed by `1.0.0_SA_CTO~DELL1`.
