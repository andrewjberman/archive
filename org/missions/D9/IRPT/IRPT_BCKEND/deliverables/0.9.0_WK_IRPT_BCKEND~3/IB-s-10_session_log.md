# Session log -- `0.9.0_WK_IRPT_BCKEND~3` on `IRPT_BCKEND.TO-IB-s-10`

Worktree `/c/tmp/wk-irpt-1-3`, branch `wk-irpt_bckend-1-3`, re-cut from `7799dcfb10` (the IB-s-9
drain). Fifth and last order in slot `~3`, after IB-s-9.

## Order of acts

1. **The bar.** `git rev-parse --abbrev-ref HEAD` -> `wk-irpt_bckend-1-3`;
   `test -d org && test -d .tools` -> `TREE-OK`; then every path this face names, checked one by
   one rather than taken from the hand-off message.

2. **Re-grounded the premises BEFORE taking the order,** and took it only after they held:
   - the field census, present, 201,817 bytes -- 33 sections, 118 field rows, and the shape that
     drives everything: the rows come in **three** forms (53 `field/unit/values`, 19 with a
     `group`, 46 glossary `term/definition`), which is what makes the routing a reading of the
     data rather than a preference.
   - the variants packet, **on the branch this time** -- row `W3-S7`'s shape does not recur.
   - the three retained vendor PDFs, fetched under this serial and hash-verified `3 of 3`,
     **plus** page counts against `pdf_validation.json`. KMS resolved with no refusal, so arm
     (v0.11) was executable and no BLOCKED row was needed.
   - PDF tooling: pdfplumber / pypdf / pdfminer / PyMuPDF import; **reportlab does not**, so the
     specimens are generated with PyMuPDF.
   - the one thing the hand-off named that does not exist here (the "gitignored session-serial
     line") -- recorded in the take-the-order commit rather than silently skipped, and **not**
     filed as a row, because no premise of the FACE asserts it.

3. **Built the extractor and the certifier as two modules with a deliberate wall between them.**
   `certify.py` is handed only the emitted rows and the original bytes; it is given no extractor
   state, because a checker that can re-derive the answer it grades is a tautology.

4. **Built the specimens from the census**, deterministically, labelled `synthetic: true` in
   metadata, in a page banner and in the path, with the multicomp third column a **declared
   replica** of entity 2 rather than three invented numbers.

5. **Ran the vendor specimens through the same code path,** verified before use, labelled
   `vendor_synthetic_holdings: true` -- a different marker, never mixed with the first.

6. **Wrote the battery, watched it FAIL, and fixed the predicate rather than the measurement**
   (see below). Then the four mutants, the determinism pair, the proof instance, the flip.

## What went wrong, and what each cost

Six of these are the substance of the cell; they are recorded because the rule each produced is
only trustworthy if its incident is visible.

- **The census's page numbers are a HINT, not an INDEX.** They describe the one report the CRO
  scraped; the same section sits on a different page in a 23-page Overview and a 35-page Multi.
  Treating them as an index cost the first run **58 of 58 fields UNLOCATED** on a document that
  plainly contained them. Now: census pages first, then the rest of the document.
- **My own specimen's banner contained `--`.** The em-dash pair is how YCharts prints an absent
  cell, so the extractor read the banner as a missing-value token, put a phantom candidate on the
  top row of every page, and broke the label tie on the nearest section heading. A fixture's own
  chrome must not be readable as data.
- **A date is not a measurement.** A section heading matched as a label, and the "BELOW" rule
  harvested `9,` and `2026` off the "Data as of:" line -- **9.0 and 2026.0 as values, certifying
  happily**, because the digits really are at those coordinates. Rows that *are* a date line are
  now excluded from value candidacy. This removed 16 bogus rows per synthetic variant.
- **A list is not a value.** A `list`-unit census field rendered as a long bracketed string ran
  across the next column's x position; the overlapping glyph runs handed the extractor fragments
  like `8,` and `6,` **which also certified**. Two fixes: the extractor refuses `list`/`table`
  units outright (`NON_SCALAR_UNITS`), and the generator prints `[see table]` with no digits.
  **The certifier cannot catch this class -- only refusing to ask can.**
- **A fixed-size label neighbourhood cannot span two real layouts.** 260pt label-to-value gap in
  the synthetic specimens, ~60pt in the vendor tables. A box sized for the second failed **30 of
  34** correctly-located rows. The neighbourhood is now the value's own text row plus a shallow
  band above it -- the document's structure, not a constant.
- **My own scaling predicate was over-strong, and the battery caught it.** `arm (a): FAIL`,
  `24 / 47 / 70` against an asserted `24 / 48 / 72`, token withheld. The code was right: a field
  absent for one entity and present for another yields a different row count per column. Exact
  scaling was a property of an imagined dataset, not of this one.

And two defects **in the controls themselves**, which are the more instructive half:

- **The M4 probe shared a dependency with what it graded** -- it called the very function M4
  patches out, so it went blind in the one run it existed to measure and reported a clean `0` on a
  mutant that had just harvested 17 extra values. Reference set now captured pre-mutation.
- **The first M4 probe detected dates by token shape** and returned 4 false positives on the
  baseline, which turned out to be a **second, different** real defect hiding behind noise
  attributed to the first. A probe whose positives you have to explain away is not measuring the
  thing it names.

## Surprise rows filed on this order

| id | class | hazard | one line |
|---|---|---|---|
| `IRPT_BCKEND-W3-S10` | OBSERVATION | ARMED | Real vendor PDFs lose the `fi` ligature to a font-subset glyph on 89 of 89 pages, and the glyph's code differs between documents of the same run -- so no cid-to-letter mapping is safe. The synthetic specimens cannot reproduce the class at all. |
| `IRPT_BCKEND-W3-S11` | OBSERVATION | ARMED | `AnalysisReport.sections[].as_of_date` is REQUIRED; the documents state no date for 34 of 81 and 51 of 108 rows. Closing that means fabricating a date or holding rows out, and the contract has no field in which a fallback could be declared as one. |
| `IRPT_BCKEND-W3-S12` | OBSERVATION | ARMED | `_keys.s3_evidence_key` accepts a client display name and an e-mail address as a path segment, against its own docstring, while `cache_key` in the same module refuses both -- and it is the one that mints DURABLE S3 keys. |

All three ARMED, each with a `disarm_owner` naming what this cell disarmed for itself and what is
the issuer's, the CVO's or the CTO's. None was worked around silently; none widened this order.

**`W3-S12` is the one to read first.** It was found only because this cell needed exactly one
firm-scoped key and **probed the grammar before trusting it** rather than calling the function and
believing its docstring. The issuer amendment this face carries says to find refusals "through the
public `cache_key`" -- correct guidance that happens to route a reader around the function that
does not check, so following the amendment exactly would not have surfaced it.

## Bounds honoured

- **No deploy in this cell.** Nothing was applied, no ledger entry opened, no `.tf` touched. The
  extractor rides IB-s-9's package at that package's next build.
- **No live vendor call.** The only network read is `s3api get-object` against Opal's own
  `opal-data-ycharts`, hash-verified before use.
- **No number from a visual guess** -- arm (d), `0` emitted values across 10 chart regions on all
  six specimens, with a mutant proving the check can fail.
- **Synthetic is labelled synthetic** in metadata, in a page banner, in every artifact path, and
  in a per-row marker that is censused `N of N`; `vendor_synthetic_holdings` is a different string
  and the two are never mixed.
- **`_keys`, `_contracts` and `_authz` were READ, never edited** -- none is in this order's
  `<paths>`. Both contract frictions found there are rows, not edits.

## Commits on this order (all LOCAL on `wk-irpt_bckend-1-3`)

| hash | subject |
|---|---|
| `8c230cc89b` | IB-s-10: take the order -- status staged -> pending, after re-grounding its premises against live state |

Plus the closing commit that carries the package, the fixtures, the battery, this log, the result
document, the proof instance, the three channel rows and the `<status>` flip.
