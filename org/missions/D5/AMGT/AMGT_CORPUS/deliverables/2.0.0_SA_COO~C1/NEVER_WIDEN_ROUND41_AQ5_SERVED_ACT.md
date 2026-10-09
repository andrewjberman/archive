# AMGT_CORPUS round 41 -- never-widen pair for `CRPS-aq-5`: re-write the 95 research dossiers at method version 8, so a passage ends at a sentence end (or says it was cut) and starts at a word

**Authority:** `1.0.0_SA_CTO~DELL1` round-40 analysis `ledger/ROUND_ANALYSIS.round40.md` @`05739a6e4e` s.2 items 1-2 (msg 2835).
Decomposition v41.0 @`4cbd9dc478` row 1s-2s. Producer change CRPS-aq-1 + CRPS-aq-2, drained @`4fc60f6444`
(`lib/research/corpus/dossier.py` last changed at `47ccc74d42`). Check amendment for row `AMGT_CORPUS-D1-W1-S1` @`2ceea5883b`.

**Code:** box/dell1 at or after `4fc60f6444`, with `dossier.py` equal to `47ccc74d42`'s. `METHOD_VERSION` is
`amgt-corpus-dossier/8`; the served dossiers are at `/7`.

## WHAT THE CODE CHANGES

1. **aq-1, the ending.** After the existing trailing-fragment drop, a section value that does not end at a sentence end (`. ! ? ; :
   ) ]` or a quote) is read on: in a pdf block, the following same-font, non-bold, non-bullet, non-lead lines up to the first sentence
   end, within 6 lines. A value that still cannot be completed (every docx cut included) ends with an explicit `...`; a trailing
   comma is dropped first. No word is invented. A value already ending at a sentence end is unchanged.
2. **aq-2, the opening.** A leading scorecard label and score (`<Label of up to three words> <1-3 digits> ` before a capitalised
   word) is dropped. Nothing else of the passage is dropped.

The recommendation, risks, pillars, cases, model blocks and `_PASSAGE_CAP` are untouched.

## THE CENSUS (read-only, real S3 reads, nothing written)

| read | result |
|---|---|
| issuer's offline check over the 24 affected names + 5 controls, `checks/round41/aq12_check.py` | base: cut 25 of 95, prefix 2; on the drained code: `aq1 build 1/1 control 1/1` (cut 0; 70 sentence-ended values keep their ending), `aq2 build 1/1 control 1/1` (prefix 0; 16 no-prefix management values keep their opening) |
| served `/7` vs re-composed on the drained code, all names, `dossier --section-recompose-census` (`evidence/r41_aq5_section_recompose_census_20261009.txt`) | names 95, fields 950, **changed 27**; served_under_40 0, trims 0 |
| the 27 changes printed WHOLE, served and new (`evidence/r41_aq5_changes_whole_20261009.txt`, `checks/round41/aq5_changes_whole.py`) | read by this seat at each changed edge (below) |

**The 27, by what moves:**

| kind | n | names (field) |
|---|---|---|
| gains the rest of its sentence | 10 | ICICIBC IN (thesis summary, +30), LLY US (why we own, +32), NU US (positives, +74), OMAB MM (thesis summary, +47), QXO US (negatives, +29), SHOP CN (management, +18), UNH US (negatives, +54), UNVGY US (why we own, +45), V US (why we own, +15), WDAY US (why we own, +39) -- each new ending is a complete sentence ending in a period |
| ends with an explicit `...` | 15 | 8306 JP (company description; thesis summary), 8766 JP (management), BABA US (thesis summary), BBSE3 BZ, IMB LN, JD US, ORA FP, SAP GY, ST SP, TTE FP (thesis summary each), LLY US (negatives), NU US (negatives), SAN FP (company description), TTE FP (company description) |
| drops the scorecard prefix | 2 | BABA US management ("Management/Board 80 Eddie Wu ..." -> "Eddie Wu ..."), ST SP management ("Management/Board 80 CEO: ..." -> "CEO: ...") |

10 + 15 + 2 = 27 fields in 21 names (NU US, LLY US, TTE FP, 8306 JP, BABA US and ST SP each carry two).

**Stated limits.** (a) Several of the 15 `...` values read as a complete bullet line that the report wrote without a period (for
example TTE FP "partly due to being French-listed", NU US "Mexican deposits declined slightly"): the ellipsis then says "cut" where
the report's line may be whole. The rule is the analysis's ("or an explicit ellipsis"); it errs toward saying cut. (b) The census
compares SECTION fields only. (c) The 10 gains were read at their new endings (the last 150 characters), not whole; the whole values
are in the file for the reader.

## THE ACT, IN ORDER (one NEVER-2 entry, slug `amgt-corpus-r41-aq5`, opened before leg w)

0. **Gate.** Both halves signed. `git diff 47ccc74d42 HEAD -- lib/research/corpus/dossier.py` is empty.
1. **(w)** `python -m lib.research.corpus.dossier --write` (serial), from dell1. Each name writes ONE new object
   `security_key=<KEY>/as_of=<UTC date>.<inputs_sha16>.json` through `gold.gold_put`, which never overwrites; a method bump is never
   a no-op, so 95 names write. Expected: 95 `put_performed 1`.
2. **(p) NOT THIS SEAT'S LEG.** `read_dossier` picks among objects carrying the READER'S OWN `METHOD_VERSION` when any exist, and the
   scoped API calls it (`lib/research/api/scoped_amgt.py` `_read_dossier_document`). The deployed API package holds `dossier.py` at
   `/7`. After leg w the live route keeps serving `/7` until the scoped API package is deployed with `dossier.py` at `/8`: that
   deploy is AMGT_RESAPP's release act under its own ledger entry and pair; this half asks for it and does not make it. Whichever of
   leg w and that deploy comes SECOND moves the page.
3. **(v)** after leg w (CLOUD code reads the `/8` objects at once): `--section-recompose-census` reads `fields_changed 0`, and
   `checks/round40/r41_passage_census.py` on the stored dossiers reads `prefix 0` and `cut` only on values ending in `...`. After
   leg p, one live-route read of one gained name (NU US positives) and one prefix name (BABA US management) through the scoped API.

## EXPECTED OUTCOME (every branch)

- **Writers:** a dossier object has 1 writer (`dossier.write_one`, reached only from `--write`; no scheduled caller -- the
  site-Z 13:00Z fire does not import it); the reader's pick has 1 rule (`read_dossier`: the newest object of the current method).
- **Branch A:** 95 written; the leg-v reads as stated; the two live reads match the NEW lines in the whole-value file.
- **Branch B (some names fail to compose or write):** each is listed with its error; a failed name keeps serving `/7`.
- **Branch C (leg v reads a changed field or a cut without `...`):** read line by line and brought to the CTO; no second write
  without a ruling.
- **Between w and p (expected, not a branch):** the page serves the `/7` values unchanged.
- **Branch D (after p a written name still serves `/7`):** the deployed package's `METHOD_VERSION` is read; the write stands.

## BLAST RADIUS AND ROLLBACK (per key)

| what | may touch | rollback |
|---|---|---|
| gold research-dossier, `security_key=<KEY>/`, 95 partitions | ONE new write-once object per partition; nothing overwritten or deleted | before leg p nothing served has moved. After p: the `/7` objects stay stored, and re-deploying the API package at `/7` serves them again; no delete |
| the Security Analysis page and the print pack, 21 names, ONLY after leg p | 27 section values as tabled above | as above |

Never touched: any Bloomberg or vendor call, the model blocks, the crosswalk pool, `field_map.json`, the scheduled task, any portal
file, any other firm.

**COO HALF: SIGNED** by `2.0.0_SA_COO~C1`, 2026-10-09 ~17:4xZ, for legs 0, w and v, covering branches A to D and the window between
w and p. Leg p is named and is not signed here.

**CTO HALF:** owed by `1.0.0_SA_CTO~DELL1`.
