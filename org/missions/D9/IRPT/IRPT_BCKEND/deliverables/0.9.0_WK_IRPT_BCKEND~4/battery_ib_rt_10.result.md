# `battery_ib_rt_10.result.md` -- RT10-AC1, four arms, 4 of 4

**TO:** `IRPT_BCKEND.TO-IB-rt-10` | **cell:** `IB-rt-10` (PRD row B10) | **assignee:** `0.9.0_WK_IRPT_BCKEND~4`
**Branch:** `wk-irpt_bckend-2-4b` | **worktree:** `/c/tmp/wk-irpt-2-4b` | **base:** `a296eac0f4`

**Invocation (the one the task order names):**
```
timeout 600 python org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~4/battery_ib_rt_10.py
```
**rc 0. Last line: `IBRT10-GLYPHS-DATES-PROVENANCED`. Full verbatim output (178 lines):**
`org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~4/IB-rt-10_RT10-AC1_battery_output.txt`

Four arms `(a)`-`(d)`, taken from the acceptance clause. **4 of 4.** Two same-input runs are byte-identical
(17,926 bytes, sha256 `292d854078120020`).

---

## THE ONE THING A READER SHOULD TAKE FROM THIS CELL

**A character code in a PDF is a property of a FONT RESOURCE INSIDE ONE FILE. It is not a property of the
typeface, not of the vendor, and not of the document.** Both halves of that sentence were earned by
measurement in this cell, and the second half is the one that nearly got away:

- **Across the three files:** 73 of 89 compared codes mean different characters in different documents --
  same vendor, same template, same day. Pairwise, overview and comparison agree on **75 of 87** common
  codes while multicomp agrees with either on **15-18 of 86**. A global table built from the first two files
  anyone tested would have been right twice and wrong once.
- **Inside one file:** the first version of `fonts.py` resolved a code through whichever of *that document's*
  fonts mapped it -- already "per-document" -- and on the overview specimen it returned the digit **`8`** for
  the very code this cell exists to refuse, because the Bold subset maps 45 even though the Regular subset
  (which rendered it) does not. `cross_font_control` now prints that as a standing negative control:
  **U+0038, U+004D and U+0044** -- one confident wrong character per document.

## AND THE SECOND THING

**A certifier's legs bound what its verdict can mean.** Round 1 reported every vendor specimen fully
CERTIFIED under three legs -- value-at-coordinates, label-in-neighbourhood, unit-declared -- while 15 of 61
overview rows carried a date belonging to a different block of the same page. **Every one of those rows
passed all three legs, because each was individually correct about everything the legs could see.** A date is
not at the value's coordinates; it is at the block heading's. That is channel row `IRPT_BCKEND-W4-S28`, and
the fourth leg is this cell's answer to it.

---

## The arms

### (a) PER-DOCUMENT MAPPING -- PASS

For each of the three retained vendor specimens: the code, the font that rendered it, the sources asked, the
shape of the hole, and what a looser rule would have returned.

| specimen | pages | code | rendered by | verdict | what the SAME document's other font would say |
|---|---|---|---|---|---|
| overview | 23 of 23 declared | **45** | `QXFAAA+RobotoCondensed-Regular` | UNRESOLVED | U+0038, the digit `8` |
| comparison | 31 of 31 | **45** | `QTHAAA+RobotoCondensed-Regular` | UNRESOLVED | U+004D, `M` |
| multicomp | 35 of 35 | **46** | `QTIAAA+RobotoCondensed-Regular` | UNRESOLVED | U+0044, `D` |

**The codes are exactly the face's 45 / 45 / 46, and the verdict is the CTO ruling's SECOND branch.** The
ruling reads *"Per-document font mapping **or** explicit unresolved for the fi-ligature codes 45/46"*. The
documents do not state these codes and there is no honest way to recover them:

- each ToUnicode CMap has a GAP at exactly that code -- overview's Regular subset declares bfranges
  `<0001>-<002C>` and `<002E>-<0057>` and the content stream renders `45`; multicomp's declares
  `<0001>-<002D>` and `<002F>-<0058>` and renders `46`
- every embedded subset carries only `OS/2, glyf, head, hhea, hmtx, loca, maxp, name` -- **no `cmap` table
  and no `post` table**, so the font PROGRAM states nothing either

Both sources were asked, per font, and the exhaustion is recorded on the row. Filed as
`IRPT_BCKEND-W4-S26`, because the face's arm text says *recovered* and the world says the ruling's other
branch.

**`(cid:` occurrences in everything these three documents emit: 0, over 89 pages** (23+31+35) and 1,020
emitted strings. Counted over what a consumer receives -- every section value and token, every chart
representation, every disclosure text -- not over the extractor's internals.

### (b) THE NEGATIVE -- PASS

The three vendor specimens all fail the same way, so none of them tests the machinery against a case whose
right answer is known in advance. `fixtures/unmapped_glyph/` is a document that **declares its own answer**:
it maps 4 codes and uses 5.

```
MEASURED: code 3   UNRESOLVED rendered by ['AAAAAA+IRPTFixtureSubset']
  sources asked: [{"source": "ToUnicode", "codes_mapped": 4, "answered": false},
                  {"source": "font_program", "present": false, "tables": [], ...}]

THE EXTRACTOR REFUSES THE VALUE, with its coordinates and the marker (not a guess):
  Advisory Fee   UNDECODED_GLYPH_IN_TOKEN   p2  bbox [400.0, 122.8, 422.5, 131.8]
    token as extracted: '0.UNRESOLVED_GLYPH(3)0%'

AND THE CERTIFIER REFUSES IT TOO:
  verdict UNDECODED_GLYPH_AT_COORDINATES  (certified 0 of 1)  holds True
```

**Both halves are needed and they are different claims.** The extractor declining to emit says nothing about
whether the CERTIFIER can say no -- and the certifier is the half that grades an artifact somebody else
produced. So the row a careless extractor WOULD have emitted is rebuilt at its own real coordinates and
handed to the real certifier. Nothing is patched or wrapped (bound 12).

**The positive half on the same document**: 5 rows located, 5 of 5 CERTIFIED, including a value whose every
character is readable only through this document's own CMap. The refusal is specific to the withheld code,
not a blanket failure of the specimen.

An earlier draft of the fixture withheld a character that BOTH the breaking value and the surviving value
contained, which broke the positive control silently. The withheld character is now chosen as one the first
value carries and the second does not -- a constraint, not a preference.

### (c) DATE CLAIMS -- PASS

`date_claim` is MECE over "every date an extracted row could carry": **SECTION** (the document prints a
`Data as of` line governing this value's own block), **REPORT** (the report-level header date applied AND
said to be, provenance `report_header:<page>`), **NONE** (the document states neither).

| specimen | rows | SECTION | REPORT | NONE | dated from a neighbour |
|---|---|---|---|---|---|
| vendor overview | 71 | 57 | 14 | 0 | **0** |
| vendor comparison | 91 | 51 | 40 | 0 | **0** |
| vendor multicomp | 118 | 51 | 67 | 0 | **0** |
| synthetic overview | 34 | 16 | 0 | 18 | **0** |
| synthetic comparison | 57 | 23 | 0 | 34 | **0** |
| synthetic multicomp | 80 | 30 | 0 | 50 | **0** |
| unmapped-glyph fixture | 15 | 4 | 0 | 11 | **0** |

Every member of the enum is exercised: the vendor documents carry a report header date so they reach
SECTION and REPORT; the census-generated ones carry none, so they reach NONE. **466 of 466 emitted rows
declare a claim.**

**The round-1 numbers, re-derived from this run's own rows rather than recalled:**

| specimen | round-1 rule | the face's number | match |
|---|---|---|---|
| comparison | `{PAGE_STATED: 47, CENSUS_STATED: 0, NOT_STATED: 34}` | 34 of 81 | **yes** |
| multicomp | `{PAGE_STATED: 45, CENSUS_STATED: 12, NOT_STATED: 51}` | 51 of 108 | **yes** |

So the change is a MEASURED DELTA and not a claim. What moved, and why it is an improvement:

- round 1's `CENSUS_STATED` (12 multicomp rows) took its date from the FIELD CENSUS -- a different document's
  statement about this one. Gone.
- round 1's `PAGE_STATED` took the page's FIRST date line for every row on the page. On the overview
  specimen **15 of 61 rows sit on a page printing two different dates** (page 2: 2026-09-09 and 2026-09-11;
  page 6: 2026-08-31 and 2026-09-11).

**The mutants.** Ran on 3 specimens; the 4 with no multi-date page print VACUOUS and are never folded into a
pass.

| mutant | what it does | verdict | specimens |
|---|---|---|---|
| neighbour-date | gives a row a date its own page really prints, for another block | `DATE_NOT_STATED_AT_PROVENANCE` | overview, comparison, the fixture |
| shifted-provenance | keeps the date, moves the provenance past an intervening date line | `DATE_TAKEN_FROM_A_NEIGHBOURING_BLOCK` | overview, comparison |

The second exists because the first cannot reach the case where the coordinates really DO print that date --
the right date of the wrong block. Refusal, verbatim:

> the date at bbox `[488.64, 79.45, 566.67, 87.37]` does print 2026-09-11, but 1 other 'Data as of' line(s)
> sit between it and the value at top 627.19 (2026-08-31 at top 379.93) -- this is the right date of the
> WRONG BLOCK

### (d) SCHEMA-VALID -- PASS

`date_claim` is an OPTIONAL enum on `AnalysisReport.sections[]` in **both** published copies, **1,370 bytes,
sha256 `92bff92c879fa6c8` in each.** It is byte-identical because it was written once and inserted into
both, not written twice and compared afterwards.

Seven specimens validate against **both** copies -- 71, 91, 118, 16, 23, 30 and 4 rows -- with
`additionalProperties: false` intact, which is the whole reason the property went into the CONTRACT rather
than into a private key: a producer emitting `date_claim` without this edit fails validation on both sides.

**The two FILES are not byte-equal and are not meant to be.** The published copy carries its own `$id` and a
`contract_version` const. The clause is *byte-equal on the added property*, and that is what is measured.

The contract surface belongs to IB-s-18; the decomposition (v0.2 s.2) directs this cell to make the edit and
to file a row naming the CTO's L10 read on it. That row is `IRPT_BCKEND-W4-S27`, and it names the open
question plainly: **an OPTIONAL field a producer may omit is one a consumer cannot rely on for a refusal.**

Label census: the two provenance markers are never mixed -- `vendor_synthetic_holdings` on 280 of 280 rows
across the three vendor specimens, `synthetic` on 171 of 171 rows across the three census-generated ones.
(The unmapped-glyph fixture's 15 rows also carry `synthetic`; the arm's printed census covers the six
specimens the round-1 suite enumerates, and that denominator is stated rather than quietly widened.)

---

## What this cell did NOT do

- **No deploy.** The extractor rides the `irpt-ycharts-generate` package at its next build; no
  change-management ledger was opened, because NEVER-2 forbids opening one without the room to close it.
- **No vendor call.** The three retained PDFs are read from Opal's own S3 and hash-verified before use.
- **No repair of a neighbouring defect.** Two were found and both are rows: `battery_ib_s_18.py` crashes
  mid-run on the path register's own data (`W4-S29`), and the register's published `entries_total` was stale
  by 41 (`W4-S30`).

## The standing proof gap

Every specimen here is real vendor output on **synthetic holdings**, census-generated, or hand-built. **No
representative real-client PDF exists in this estate, none was manufactured, and nothing in this cell is a
certification against real client input** (FWD-4, FWD-8). RT10-AC2's third question -- which arm breaks
first on a real client PDF -- is answered as inference and labelled as such, in
`RT10-AC2_judgment.md`.
