# AMGT-rj-8 -- SESSION LOG (0.9.0_WK_AMGT_RESAPP~22, 2026-09-15, site Z)

Worktree `C:/tmp/wk-amgt-11-5`, branch `wk-amgt_resapp-11-5`, from tip `04b59f883c`
(the order's worker face at HEAD, amendment 1). RESPAWN: an earlier run on this
same order was terminated by an API limit before any edit or commit and left
five persisted filings pulled from the pool in `.scratch/src/`; those were reused
as offline fixtures for development and every graded run reads the POOL.

## THE BAR, FIRST

`git rev-parse --abbrev-ref HEAD` -> `wk-amgt_resapp-11-5`; `org/` and `.tools/`
present; `lib/research/identity/crosswalk.py`, `lib/research/filings/` and
`data/find/imo/scripts/_util/lusha_client.py` all present. TREE-OK, no blocking
row.

Premises re-grounded against live state before any build:
- `filings/v1/` in the pool holds exactly 10 objects = 5 `.source.json` + 5
  `.analysis.json`, for the five QA names. The issuer's statement that the five
  QA names are the whole set HOLDS.
- `universe/v1/2026-09-15.json` holds 256 names and carries NO domain field --
  which is why `domains.json` is a DECLARED table with its own denominator.
- rj-6's source object carries `officer_section: {item, text, chars, sha256,
  extracted: false, extraction_owner: "AMGT-rj-8"}` -- the section is persisted
  and UNPARSED, exactly as this cell assumes.
- Card 2 (`measure_lusha_csuite.py`, `boeing_csuite_prospecting.json`) read
  first: prospecting returns `firstName`/`lastName`/`jobTitle.title`/
  `socialLinks.linkedin`, 2 credits per page, and NO tenure field anywhere.

## WHAT WAS BUILT, AND THE THREE THINGS THAT WERE NOT OBVIOUS

`lib/research/management/` -- roster.py, enrich.py, batch.py, two schemas, the
declared domain table, the launcher, 26 tests.

1. **A BARE NUMBER IS NOT JUNK.** The first parser dropped numeric lines as page
   furniture. That silently deleted the AGE column of BABA's table and the YEAR
   FIRST APPOINTED column of SAP's -- the only role start a 20-F table carries --
   and both names read UNRESOLVED-SOURCE with a confident reason. Numbers stay; a
   table cycle can only be opened by a NAME, so a stray page number can never
   start one.
2. **SAP'S SUPERVISORY BOARD SITS ABOVE ITS EXECUTIVE BOARD.** Taking the first
   table in Item 6 publishes twenty non-executive people as the executive team,
   each with a plausible "year first elected". Every run is attributed to its
   nearest SHORT heading and a run under a non-executive heading is rejected BY
   NAME with its reason. The heading rule then needed a second correction: the
   introducing SENTENCE above a table names the same body the heading does, and
   taking it as the heading made every member's role the whole sentence, which
   then carried no executive title and rejected the run it was meant to accept
   (measured: 1 of 4 members survived). A heading is short, is not a sentence,
   and does not end in a colon or a period.
3. **THE TWO ESTATE SCRIPT SURFACES DISAGREE ABOUT ONE NAME.**
   `data/find/imo/scripts/_util` is a PACKAGE and
   `data/find/dualbiz/scripts/_util` is a MODULE, so whichever is imported first
   binds `_util` and the second fails -- and it failed AFTER the Lusha page was
   charged. Row `AMGT_RESAPP-Z-W22-S2`. The remedy is `_estate_module()`: purge
   every colliding name, restore sys.path BY VALUE (an estate script inserts its
   own directory, so removing one copy leaves the other), and resolve BOTH estate
   modules BEFORE the first billable call.

## ONE DELIBERATE DEPARTURE FROM THE MEASURED PATH, AND WHY

Card 2's own measurement noted the `c-suite` filter is LOOSE; the reason is that
the estate client applies `seniority` CLIENT-SIDE, which is to say not at all,
and the v3 API takes NUMERIC codes server-side (card 2 discovered c-suite = id
9). The unfiltered Boeing page is 50 rows of 103,753 and matched ONE officer of
twelve. This cell sends the filter server-side through the client's own
`_execute` seam and falls back to the estate client's unfiltered call if the API
refuses it -- a refused call returns no result and is charged nothing (billing is
per result), so the fallback cannot break the 2-credit bound. Measured on the
graded run: 50 of 739, and 4 of 12 officers matched.

## WHAT THE FILING WOULD NOT GIVE

`ceo_public_profile` is ABSENT on 5 of 5 names, with its reason on each object.
The cell NAMES `serp.py serp_brightdata()` as the instrument; that function
returns `item['link']` only (so `title` and `snippet` can never be filled from
it) and on the `serp_opal` zone those links come back as opaque Google redirect
wrappers, so even the HOST cannot be read. Row `AMGT_RESAPP-Z-W22-S1`, with both
diagnostic queries recorded in RUN_LOGS.md. The criterion admits ABSENT; what is
not reachable inside this cell is a RESOLVED profile.

## COMMITS (LOCAL, on `wk-amgt_resapp-11-5`)

- `a4270d3072` the package: roster, enrich, batch, the M-1 schema, the declared
  domains, the launcher, 25 tests.
- `deb16ee7d3` the POOL object's own closed schema + the write-time gate, the
  estate-module importer, and the two surprise rows.
- this commit: the proof-of-spec instance, RUN_LOGS.md, this log, and the task
  order's `<status>` flip.

Nothing was pushed, merged, rebased or stashed. No deploy. No portal edit. No
loop started. The weekly Windows task `OpalResearch-ExecManagement` exists and is
DISABLED; activating it is Andrew's word.
