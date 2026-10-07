# AMGT_RESAPP round 78 -- what the drafting measured that the round-77 analysis did not know, and the issuer's defaults

`2.0.0_SA_COO~Z`, 2026-10-07 ~15:1xZ, for `1.0.0_SA_CTO~Z`. Source: the three group notes in this folder (@643863854d), each
figure from a read named there; the three read tables under `reads/` were re-run by this seat today.

**How to read this:** the build cells are NEW modules and are cut on the defaults below (a new module is LOCAL and changes
nothing served). The served shape is fixed only by the ADAPTER cell, which runs in wave 1 after its exporters drain. A ruling
that differs from a default changes the adapter cell's text, or one module, before anything is deployed. Two items are NOT cut
on a default, because the default would be a guess: they are marked HELD.

## A. Three reads the analysis asked for are DONE (no cell is cut for them)

| ruling | read | result |
|---|---|---|
| 2 | why a driver chart is served for 1 name of 95 | **83** covered names hold no filing analysis (41 read "no cik", 20 of those US tickers; 42 have no drafted document); **10** hold one with no table a driver could be drawn from; **2** hold a table (BA served, ASML NA refused). Sum 95. **The round-76 refusal removed 1 name, not 94: the gap is filing coverage.** `reads/DRIVER_CHART_COVERAGE.md` |
| 8 | the Recommendation cards | both labels on **3** (ASML NA, INTU, SAP GY); machine draft only 9; base case only 31; neither 52. Of the 12 cards with a drafted sentence, **12 of 12 face sentences carry no recommendation word; 0 of 63 sentences do.** `reads/RECOMMENDATION_CARDS.md` |
| 6 | the planted FWD-14 lapse | provable today with no build: on a COPY of the social list with a past review date, the route's own handler reads "The social account list is out of date: its review fell due on 2026-08-31." and "Andrew owns the publisher list and the social account list."; the unchanged copy reads in date; the packaged files' hashes did not move. `reads/PLANTED_LAPSE.json`. The organic arm falls due at 2026-10-10T22:42Z |

**What follows from the two counts, for the CTO to rule (not cut):**
- Ruling 2's follow-on cell is not a chart cell. 83 of 95 names have no filing analysis at all. FWD-18 needs filing coverage,
  which is a pipeline question (41 names have no CIK on file).
- Ruling 8's producer cell as written ("a drafted sentence that states no recommendation is refused") would empty all 12
  drafted cards. And the two labels are PAGE text (`ThesisCards.tsx`), switched by two served fields, so "one provenance label"
  is a page cell or a new served field. **HELD: no Recommendation cell is cut until this is ruled.**

## B. Defaults the build cells are cut on

| cell | what was measured | the default |
|---|---|---|
| bb-1 segments reader (ruling 3) | the stored object carries NO fiscal period and NO currency; ruling 3 asks for both. 76 names carry revenue rows, 9 none, 50 operating income; a missing period arrives as about -2.4e-14 in 2,564 of 9,410 cells; 1,324 of 1,882 metric names carry an indent of non-breaking spaces; `table_class.segment_refusal` refuses 0 of the 76 | serve Bloomberg's period numbers as "Period 1..5" with a plain note that the vendor's table does not state the fiscal period, `currency` null with its note, near-zero cells as absent, the indent as a level. Naming the period needs a second field on a second call per name: a vendor use, not taken |
| bb-2 one statement of inputs (ruling 4) | THREE statements are served, not two: `input_provenance` (95 of 95, no filings row), the overlay's `provenance` ("no filings run is recorded" on 95 of 95 while 12 theses cite a filing), and the `/ledger` route | one function builds the statement with a filings row that says what the page used; the adapter serves it wherever inputs are stated. `/ledger` is NOT retired by this round (removing a route is an endpoint change): it is named here for a ruling |
| bb-8 peer price currency (FWD-8) | round 69 already serves `price_currency`, on 25 of 676 priced rows; **3 of those 25 are wrong** (Taiwan Semiconductor's Taiwan price served "USD" on 2 rows, Petrobras's Brazil price on 1) | the cell refuses the 3 and adds about 50 US rows. **It does not close FWD-8:** about 600 rows have no currency in any stored file (scanner file 0 of 10 fields, pool 0 of 243). Closing it is a vendor pull or the scanner's producer. A row is filed for the 3 wrong rows |
| bb-9 country | all capitals on 95 of 95, 22 distinct values | `value` re-cased, the stored text kept as `value_as_stored`; "BRITAIN" becomes "Britain", no rename |
| bb-10 coverage marker | no marker on any of 97 overlays; pool 243 = 95 covered + 148 outside | field `research_coverage` with `covered`, `outside_coverage`, `not_known`. An older field `covered_no_block` calls scanner-list names such as Deere "covered"; the new marker follows `covered_security_keys()` (the 95) |
| bb-11 source names | the top band already serves plain names (69 of 69); 640 feed items carry a code only (5 codes); five storage-word strings are served | the feed and those strings |
| bb-13 Peers V below three peers (row Z-S162) | round-77 cell ba-16 did not do it. Floors today are 6 peers per measure and 8 for the score. All 35 stored scores date from 2026-09-17 | a distinct plain reason below 3 peers; the 6 and 8 floors are left alone. If Andrew's word means LOWER a floor to 3, that is a different cell. Neither reaches a page until `run_scores` is re-run, a store write under its own pair |
| bb-7 name search | 100 of 243 pool records carry a name; "apple" and "microsoft" answer nothing; AMGT_HARVST's 234 legal names are not readable by search | the cell COPIES that file (dated 2026-10-05) into a generated names module: 238 of 243. The alternative is the pool carrying legal names at its next mint |
| bb-3 officer rank (ruling 9) | a chief-executive row is present and not first in 17 of 93 served rosters; 3 stored lists carry no chief-executive title | the rank is order only; a list with no such title is left as served |
| bb-14, bb-15, bb-4 | as the notes state | cut as drafted |

## C. HELD, not cut on a default

1. **The hygiene cell (ruling 12) cannot land as ruled.** Measured today: 45 files (41 `.py`, 4 `.tf`), the same count as row
   Z-S362. **34 of the 41 `.py` files FAIL `.tools/commit-gate.sh` as they stand** (CLAUDE.md rule 14: every `.py` edit passes
   it), so a renormalising commit of them is refused unless each is also rewritten for lint, which is not "bytes equal after CR
   is stripped". 7 `.py` pass it; the 4 `.tf` were not run through the gate. Also: 7 of the 45 are Lambda sources under `infra/aws/lambda/`
   (`smartx_query`, `smartx_ingestion_pipeline`, `daily_agenda_generator`, `trending_image_generator`); a renormalised source
   moves that function's package hash at its module's next apply, by any seat. The file list is
   `CRLF_UNDER_EOL_LF_45_FILES_20261007.txt`. Options: (a) the 7 `.py` that pass and the 4 `.tf`, now; (b) all 45 under an audited gate override for
   a line-ending-only commit; (c) leave it. The issuer recommends (a) with the Lambda sources excluded.
2. **The Seeking Alpha reader (ruling msg 31034) has two halves in two projects.** `FRESHNESS_COLUMN_READERS_READ_20261007.md`
   (@b824708cf4): the article-to-security join exists only in silver parquet (`discovered_for`), which the deployed reader
   cannot open, and the collector's job records are files on the collector's box. So terms 1 and 2 need AMGT_HARVST's collector
   to land a small JSON record per finished job in the store. The reader cell (bb-16) IS cut this round: it reads that record,
   is proved on fixtures, and from the day it deploys it stops serving the three pilot objects as a last-read date. The page is
   right only when the collector's half lands. **The collector's half is `2.0.0_SA_COO~H`'s cell, for the CTO to route.**

## D. Issuer acts of the round (no order file; each under its own pair where it moves anything)

- ABNB's model-block pull (ruling 7).
- The eleven ARMED rows, read one by one (ruling 11).
- `run_scores` re-run, only if the Peers V reason is wanted on a page this round.
