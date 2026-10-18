# FEATURE RECEIPT -- AMGT-bv-1 (round 115), serial 0.9.0_WK_AMGT_RESAPP~508

## What the branch carries

- Branch: `cand/dell1/amgt-sa-remaining-date-bypasses` (portal repository, nested worktree `C:/dev/wk-resapp-508/portal`)
- Head commit: `aa20718421e537acf43fc58628d37dcbe545f984` (LOCAL, not pushed); the chain since the base: `4ba684ebeca8fda385ddb60599e0fcf99aa03817` (the four sites, first worker), `e68e03303de8ccf1d169f6c023970c674333479f` (D8 in the harness), `aa20718421e537acf43fc58628d37dcbe545f984` (amendment 1: the five further ModelTab sites and the fixture)
- Base: `26d998f7` (PROD)
- Every path changed since `26d998f7` (`git diff --name-only 26d998f7 HEAD`):
  - `src/pages/SecurityAnalysis/__harness__/basisAndReasons.harness.cjs`
  - `src/pages/SecurityAnalysis/__harness__/dateBypass.harness.cjs` (new)
  - `src/pages/SecurityAnalysis/__harness__/dateSites.fixture.json`
  - `src/pages/SecurityAnalysis/tabs/ModelTab.tsx`
  - `src/pages/SecurityAnalysis/tabs/PeersTab.tsx`
- `src/pages/SecurityAnalysis/dateWords.ts`: NOT touched (diff vs base: 0 lines).

## Pages changed

| page | route | class | gate |
|---|---|---|---|
| Security Analysis | /security-analysis | Opal-internal | internal |

## Shared files

- none

## Not carried

| path | `git diff 26d998f7 HEAD -- <path> \| wc -l` |
|---|---|
| package.json | 0 |
| bun.lock | 0 |
| src/lib/firmAccess.ts | 0 |
| src/App.tsx | 0 |

## How to look

- Dev build: `cd portal && bun run dev:live --port 5174`
- Page: `/security-analysis`, names ICT PM and RIO LN.
- Model tab: the price basis line under a historical P/E ("at the close of <long date>") and the gap-reason notes under the table.
- Peers tab: an absent-peers reason (basis absent) and a column tooltip (the column head hover).

## Harness run at the unedited head (`26d998f7` plus the new harness file, before any product edit)

Output saved at `.scratch/base_run.txt` (outer worktree, not committed):

```
CHECK D1 FAIL -- the line reads "at the close of 2026-09-30 -- the price is in GBp and consen"
CHECK D2 FAIL -- the list reads "1 No consensus estimate is served for this line 2 Price / reported EPS, FY2016, is not shown: the price is in GBp and reported EPS in USD, and a ratio of differ"
CHECK D3 FAIL -- the sentence reads "no peer set is served for this name; the universe was read at vintage 2026-10-02."
CHECK D4 FAIL -- 2 tooltips, 0 read the long form, 1 carry an ISO day
CHECK D5a PASS -- 0 bypass entries outside fixed_here or a named deferral (of 102 entries)
CHECK D5b PASS -- printed denominator.sites 102, entries 102
CHECK D5c FAIL -- C-18=deferred_to C-20=deferred_to C-33=deferred_to C-34=deferred_to
CHECK D6a PASS -- RIO LN Model rendered digest 1adca7de325af3f54c87b2e7dc79d861c403edea73615501b15c4697f5dcbdd2 (base 1adca7de...)
CHECK D6b PASS -- GOOGL Peers rendered digest 453a14ca8b199dabf64ca9cf0eb4726ed690bcc0612058c35eb81a4cb0bf68f4 (base 453a14ca...)
CHECK D7-dateRule PASS -- rc=0 "DATE RULE HARNESS: YES (7 of 7 checks)"
CHECK D7-gridScrollCue PASS -- rc=0 "GRID SCROLL CUE HARNESS: YES (5 of 5 checks)"
CHECK D7-modelTooltipRows PASS -- rc=0 "MODEL TOOLTIP ROWS HARNESS: YES (9 of 9 checks)"
CHECK D7-priceCurrencyRule PASS -- rc=0 "PRICE CURRENCY RULE HARNESS: YES (8 of 8 checks)"
DATE BYPASS HARNESS: NO (8 of 13 checks)
```

D1 to D4 and D5c fail at the base, as the order requires. D6 and D7 pass.

## Harness run after the edits (head `4ba684eb`)

```
CHECK D1 PASS -- the line reads "at the close of September 30th, 2026 -- the price is in GBp"
CHECK D2 PASS -- the list reads "1 No consensus estimate is served for this line 2 Price / reported EPS, FY2016, is not shown: the price is in GBp and reported EPS in USD, and a ratio of differ"
(the note is cut at 160 characters; the check tests the whole list for "October 2nd, 2026" and no ISO day)
CHECK D3 PASS -- the sentence reads "... the universe was read at vintage October 2nd, 2026."
CHECK D4 PASS -- 2 tooltips, 1 read the long form, 0 carry an ISO day
CHECK D5a PASS -- 0 bypass entries outside fixed_here or a named deferral (of 107 entries)
CHECK D5b PASS -- printed denominator.sites 107, entries 107
CHECK D5c PASS -- C-18=fixed_here C-20=fixed_here C-33=fixed_here C-34=fixed_here
CHECK D6a PASS -- RIO LN Model rendered digest 1adca7de325af3f54c87b2e7dc79d861c403edea73615501b15c4697f5dcbdd2 (base 1adca7de...)
CHECK D6b PASS -- GOOGL Peers rendered digest 453a14ca8b199dabf64ca9cf0eb4726ed690bcc0612058c35eb81a4cb0bf68f4 (base 453a14ca...)
CHECK D7-dateRule PASS -- rc=0 "DATE RULE HARNESS: YES (7 of 7 checks)"
CHECK D7-gridScrollCue PASS -- rc=0 "GRID SCROLL CUE HARNESS: YES (5 of 5 checks)"
CHECK D7-modelTooltipRows PASS -- rc=0 "MODEL TOOLTIP ROWS HARNESS: YES (9 of 9 checks)"
CHECK D7-priceCurrencyRule PASS -- rc=0 "PRICE CURRENCY RULE HARNESS: YES (8 of 8 checks)"
DATE BYPASS HARNESS: YES (13 of 13 checks)
```

Digests: the two base digests were recorded before the product edit and are unchanged after it, so the RIO LN Model text (and the B5 digest in `modelTooltipRows`) did not move. No digest constant was re-recorded.

## Date census re-run

Sites read at the new head (the four AMGT-bv-1 sites):

| census | file:line now | reads | helper |
|---|---|---|---|
| C-18 | tabs/ModelTab.tsx:199 | served PX_LAST `period_end_date` / `fiscal_period_end` (read at 196-197) | `longDate` (bare day); non-date prints as it came |
| C-20 | tabs/ModelTab.tsx:973 | gap reason, served prose | `daysInWords` |
| C-33 | tabs/PeersTab.tsx:407 | `data.reason` (absent-peers reason), served prose | `daysInWords` |
| C-34 | tabs/PeersTab.tsx:235 | `column.reason` in the HelperTip, through `guardedReason` | `daysInWords(guardedReason(...))` |
| C-103 | tabs/ModelTab.tsx:697 | served gap reason (withheld P/E reason, else cellReasons) in the summary dash | `daysInWords` (amendment 1) |
| C-104 | tabs/ModelTab.tsx:710 | "P/E not shown" sentence (`plainPeReason` output) | `daysInWords` around the sentence (amendment 1) |
| C-105 | tabs/ModelTab.tsx:932 | served gap reason (cellReasons) in the grid dash | `daysInWords` (amendment 1) |
| C-106 | tabs/ModelTab.tsx:832 | team-sheet reason paragraph | `daysInWords` (amendment 1) |
| C-107 | tabs/ModelTab.tsx:155 | check reason passed to `displayValue` ("[REFUSED: ...]") | `daysInWords` before `displayValue` (amendment 1); see surprise row S8 |

Re-search of the two files for `_date`, `as_of`, `vintage`, `period_end`, `slice(0, 10)`, `toISOString`, `toLocaleDateString`, `Date(` and `reason`, with each hit read in context: 59 hit lines in ModelTab.tsx and 28 in PeersTab.tsx (87 hit lines read).

Classification of the visible prints:

- ModelTab.tsx, routed: 199 (C-18), 622 (C-19, already routed), 973 (C-20), 1065 (C-21, etDay).
- ModelTab.tsx, data attribute only (not visible text): 421-422 (`data-model-line-reason`, `data-model-line-refusal`), 477 (`data-team-case-reason`), 1037 (C-23). The visible team-case and refusal text are fixed words (425, 468-490).
- ModelTab.tsx, served reason printed raw in the first worker's run, ROUTED by amendment 1 through `daysInWords` (display only, no sentence reworded): 155 (`[REFUSED: <reason>]`, C-107), 697 (summary dash, C-103), 710 ("P/E not shown", C-104), 832 (team-sheet reason, C-106), 932 (grid dash, C-105). No served reason in the two files is printed raw any more.
- PeersTab.tsx, routed: 202-203 (C-28, C-29, longDate), 215 (C-30, longStamp), 217 (C-31, longStamp), 235 (C-34), 278 (C-32, longDate), 407 (C-33).
- PeersTab.tsx, data attribute only: 214 (C-35), 355-356 (`data-absent-column-reason`, `data-absent-reason-class`), 398 (`data-peers-absent-reason`).
- PeersTab.tsx, fixed words or comments: 55-58 (`absentReasonClass` clause, a fixed sentence), 13-16, 36, 51, and the comment lines.

AMENDMENT 1 (round 115, head `aa207184`): the five sites above are routed in place, so the count still bypassing in these two files is 0 (ModelTab.tsx 0, PeersTab.tsx 0). The earlier deferral to AMGT-bu-4 is superseded. Re-search on aa207184 with the same pattern: ModelTab.tsx 59 hit lines, PeersTab.tsx 28 hit lines (the line numbers are unchanged by the amendment, which edits five lines in place); the five changed lines were read in context at the new head.

Harness at head `aa207184`: `DATE BYPASS HARNESS: YES (23 of 23 checks)` (D1 to D4, D5a to D5c, D6a, D6b, D7 x4, D8a to D8e and their no-date controls); the run on the unedited head before the edits (`4ba684eb` plus the D8 harness) read `NO (16 of 23 checks)`, failing D5a, D5c and D8a to D8e.

NEW denominator: 107 sites (was 102), `files_with_hits` 37, `files_read` 37. Bypass entries 35, all `fixed_here` after amendment 1 (before it: fixed_here 30, deferred 5). Entries reading `bypass: true` with a disposition other than `fixed_here`: 0 (in ModelTab or PeersTab: 0). `denominator.sites` equals the entry count (107).

Surprise row for the census item (c): `AMGT_RESAPP-D1-W508-S8` OBSERVATION, INERT. The REFUSED branch at ModelTab.tsx:155 is reached by no page render (rowRefusal collapses a refused row before any ModelCell is built; a team cell is routed to TeamModelCell, which reads no verdict). It is routed as ordered; D8e grades it on the component itself through a test-only export appended to the transpiled ModelTab.

## Harness and fixture changes beyond the four sites

- `basisAndReasons.harness.cjs` B1b: the expected string moves from the raw day to the long form (`2025-12-31` -> `December 31st, 2025`). The check's intent is unchanged. Without this change, the sibling harness reads `NO (9 of 10)` at head (AC2 regression 1 on the first run).
- `dateSites.fixture.json`: the four AMGT-bv-1 entries read `fixed_here` (`bypass` stays `true`, the same convention as C-08). Five entries C-103 to C-107 are appended. The header note now names the round-115 re-run. The denominator moves from 102 to 107.
- The first run of the new harness put the five residual entries under surprise-row deferrals. `dateRule.harness.cjs` E5 (an older harness) accepts `deferred_to` only from AMGT-bu-1 or AMGT-bu-4 and read 6 of 7. The entries now defer to AMGT-bu-4, the census owner of ModelTab.tsx, with the row as the reason. Row S7 records this. D5a stays the strict cell rule.

## Surprise rows (investigation file, appended; no existing row edited)

`org/missions/D5/AMGT/AMGT_RESAPP/surprise-channel/investigations/INVESTIGATION_v1.md`

- `AMGT_RESAPP-D1-W508-S1` OBSERVATION, INERT: ModelTab summary dash (697) and grid dash (932) print a served gap reason raw.
- `AMGT_RESAPP-D1-W508-S2` OBSERVATION, INERT: ModelTab "P/E not shown" sentence (710) and team-sheet reason (832) print served text raw.
- `AMGT_RESAPP-D1-W508-S3` OBSERVATION, INERT: ModelTab REFUSED figure cell (155) prints the check reason raw.
- `AMGT_RESAPP-D1-W508-S4` OBSERVATION, INERT: the premise of C-34 fails at the base. The PRESENT_NOT_CARRIED reason is fixed text (cscTable.ts:188-196). D4 injects a served-shaped reason at the buildCscTable boundary.
- `AMGT_RESAPP-D1-W508-S5` OBSERVATION, INERT: the schema path the order names (`org/surprise_channel/schemas/investigation_item.schema.json`) is absent in this worktree. Rows follow the channel's existing form.
- `AMGT_RESAPP-D1-W508-S6` OBSERVATION, INERT: the D5 strict cell rule cannot name a cell for the residual entries. Its world_is is superseded by S7.
- `AMGT_RESAPP-D1-W508-S7` OBSERVATION, INERT: dateRule E5 hard-codes the owners (AMGT-bu-1, AMGT-bu-4). The residual entries defer to AMGT-bu-4 with the row as reason.

Each row carries `disarm_owner` `2.0.0_SA_COO~R1`.

## Approval row check (`--check-only`, not registered)

```
APPROVAL-REGISTER result=OK row=- head_sha=4ba684eb (full 4ba684ebeca8fda385ddb60599e0fcf99aa03817) commits=1 check-only=yes waived=0
```

No `org/devices/` file was committed. The approval row was not registered.
