# IB163-1 -- what a column of a vendor section IS (IRPT_BCKEND.TO-IB-pr-469, read only)

Worker `0.9.0_WK_IRPT_BCKEND~324`, base `49fb205145273399947016d344cc4c3cbc93b7c4`. Data: `IB163-1_column_meaning.json` (same folder).
Nothing was invoked, no sign-in, no AWS write, no figure and no account or name recorded.

## The three answers

1. **Where the producer could know what a column is.** For S01, S03 and S18 the column is a compared security. The producer holds the
   primary portfolio name (`recipe.py:919`) and the chosen comparison names in request order (`recipe.py:306`, `publisher.py:88-100`)
   outside the page, and `extract.extract` is never handed them (`extract.py:623`); their only later use is a check that each name is
   printed somewhere in the PDF (`certify.py:120-133`). Verdict `HELD_ELSEWHERE_BY_THE_PRODUCER` for all three. For S14, S15 and S16 the
   column is a period. The census records the period headings the page prints (`axes.window` / `axes.lookback`, census lines 1433,
   1475, 1650) and no code reads `axes` (`extract.py:246-254` copies other keys). Verdict `ON_THE_PAGE_NEVER_READ`.
2. **One stored report.** NOT READ. The list of the `analysis_reports` prefix succeeded (21 objects over the 3 registered firm prefixes:
   1, 20, 0). The one get was refused: `AccessDenied`, the dell2 agent user may not `kms:Decrypt` the object. No other object, identity or
   path was tried. No section id was counted, so the S18 count against the rule's 36 is not established. Row `IRPT_BCKEND-D2-W324-S1`.
3. **Consumers of the id's shape.** None parses it. Three sites build it (`extract.py:705`, `:772`, `certify.py:632` control); the rest
   copy it, compare it whole (`publication.py:141` uniqueness; `ops/prospect_dates.py:46,369` length 1..200 and uniqueness) or declare a
   plain string (both copies of the contracts). Because the private `_column` key is dropped before the wire (`publication.py:215-216`),
   the id is the only carrier of the column. Census: 33 of 712 files hit `section_id` under the service and contracts roots; the portal
   checkout is an empty directory here (0 files).

## Column order claim

Not guaranteed to follow the request's security order (no code compares). It follows the page only partly: same-line cells are ranked left
to right by `x0` (`extract.py:597,603`), but only tokens that parse as a number, a missing mark or an undecoded glyph count
(`:587-595`), so one unreadable cell shifts later columns left; a value stacked below its label (`:598-599`) is ranked top to bottom;
the list stops at six.

## Not established

Any stored report's ids and counts; whether the page prints a heading over S01 and S18 columns (the census is silent); which entity the
single S14/S15/S16 row belongs to; whether S15 and S16 `Standard Deviation` collide on a real page (row `IRPT_BCKEND-D2-W324-S2`, from
source and census only); that c0 is the primary portfolio on the real page.
