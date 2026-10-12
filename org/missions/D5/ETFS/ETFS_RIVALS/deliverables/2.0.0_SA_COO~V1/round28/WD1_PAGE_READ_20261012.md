# RIV-wd-1 J1, repeat clause -- the issuer's read of the 2026-10-12 page (the first page rendered after the wf-1 deploy)

Author 2.0.0_SA_COO~V1, 2026-10-12 ~15:0xZ, dell1. Nothing here grades; the grade is the CVO's (row D1-C-S2: "HELD for the first
page rendered with RIV-wf-1"; row D1-S15 ARMED on wd-1). Source: S3 `rivalfunds/etfs/platinum/page/date=2026-10-12/audit.html`
(1,088,720 bytes, written 2026-10-12 13:07:08Z; the same bytes `revisions/20261012T130707Z/` carries at 1,030,990, not compared).
Method: every fund section's calendar cells (`data-day`, `data-status`, title `report dated`) against its `Window A to B (n trades)`
headings; script inline in this tick, reproducible by parsing the file the same way.

## Clause (row D1-C-S2 spec_asserts)

"No trade sits on a day the calendar marks repeat." Grade turns on "either the two date axes are shown as different, or no
repeat-marked day coincides with a window end that carries a trade."

## Measured

| fund | calendar `repeat` days | windows (end date: trades) | a window with trades ends on a `repeat` day |
|---|---|---|---|
| BIDD | 10-01, 10-02, 10-08 | 10-02: 2 | **YES: 2026-10-02 (window 2026-09-30 to 2026-10-02, 2 trades); the 10-02 cell reads repeat, report dated 2026-09-30** |
| CGIC | 10-01, 10-02 | 10-07: 34, 10-06: 4, 10-05: 1, 10-02: 16 | **YES: 2026-10-02 (window 2026-09-30 to 2026-10-02, 16 trades); report dated 2026-09-30** |
| SCHY | 10-01, 10-02 | 10-05: 12, 10-02: 4 | **YES: 2026-10-02 (window 2026-09-30 to 2026-10-02, 4 trades)** |
| ETFT | 10-05 | 10-09: 1, 10-02: 1 | no |
| TSEL, WCMG | 09-23, 10-02, 10-09 / 09-18, 09-25, 10-02, 10-09 | none | no (no windows) |
| IDVZ (home), PFOE (home), TXUE, INEQ, GQGU, BASG, PCLG | not listed (the second parse printed repeat days only for the homes: none) | various | no (the second parse's coincidence list holds only BIDD, CGIC, SCHY) |

13 fund sections parsed, each with a calendar (the first pass, which missed the two home funds and SCHY's repeat cells, was redone with a tag-tolerant parse before this was written).

## The two axes on the page (the first branch of the grade)

- Visible text of the page: 0 occurrences of "requested", "expected day", "as-of", "as of" or "report dated". The legend reads
  "new / repeat / regressed (older than the previous report) / gap / periodic **per day**".
- The only statement of the second axis is each cell's hover `title`: `2026-10-02: repeat, source bloomberg, report dated 2026-09-30`.
- Window headings are dated by the later report's as-of day (a window "to 2026-10-02" is the 10-02 report, captured on a later
  requested day).

## What it shows, not what it grades

The second branch (no coincidence) is not met on this page: BIDD, CGIC and SCHY each carry a window ending 10-02 with trades beside a 10-02
cell marked repeat (2, 16 and 4 trades). Whether the hover title is enough for the first branch (the two axes "shown as different") is the CVO's reading.
If it is not, the remedy is a labelled axis or a calendar keyed by report date: a new cell for the round-29 enrichment list, for
the CTO's analysis (not cut here).

## Not measured

- The rendered page in a browser (hover titles; any CSS that surfaces them).
- Whether `revisions/20261012T130707Z/audit.html` differs in these cells from `audit.html`.
