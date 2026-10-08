# WALK_ROUND78 -- AMGT-bb-19, worker 0.9.0_WK_AMGT_RESAPP~303

Records what was seen; no verdict on any act. The walker account is role admin, userType Dev: role-gated differences are NOT covered.

## Build, instrument, safety

- Build walked: local dev build `http://localhost:5174`, started by this worker with `bun run dev:live --port 5174` from `C:/tmp/r78-307/portal` (port 5174 read 000 before; no `bun install`). Portal ref `d1b21c97` (`git -C portal rev-parse HEAD` = d1b21c970ca00147e646d41e3c759a1edf52e048), branch `wk-AMGT_RESAPP-303-portal`. Live function per the GO: CodeSha256 `+s6R0/rcpQ6lJgYsX2JtxfgoFoCmiaozTtMreyyymTQ=`.
- Walker slot: `ui_walker_account.py status` read `status=disabled ... armed=no armedBy=none; SSM ABSENT` before each arm. Two arms (row `AMGT_RESAPP-Z-W303-S2`): run 1 holder `Opal_Bloomberg:39172:9bf49411` (stamp `20261008T083459Z`, disarmed 08:38:45Z) and run 2 holder `Opal_Bloomberg:39672:17e6ed9f` (stamp `20261008T084357Z`, disarmed 08:44:51Z). After each: `LOGIN WITH THE WALK PASSWORD AFTER DISARM: HTTP 401 ... REFUSED`. Status after run 2: `armed=no armedBy=none`.
- Instrument (`instrument/`): `walk_ay6.mjs` and `signin_detect.mjs` copied unchanged from round 77; this round's modules `bb19_walk.mjs` (run 1) and `bb19_ledger_walk.mjs` (run 2). GET only; guard unchanged: run 1 0 guard aborts, 3 API issues (three `/api/scoped/advisor-intelligence/platinum/firm/*.json` reads answered 500 while on the BA page, not an AMGT route), 5 console errors (two 401s on the sign-in page, three 500s for those reads), walk void: no. Third-party document requests are aborted in the browser context (one: the pressed item, see FWD-16); nothing left the device.
- Walk stamps (gitignored, never committed): run 1 `tmp/ui-walk/20261008T083459Z` (22 screenshots), run 2 `tmp/ui-walk/20261008T084357Z` (1 screenshot). Captures COPIED to `captures/`: 001-022 from run 1, 901 from run 2 = 23. `data/run1/` and `data/run2/` are the two runs' data folders.
- Positive control (`data/run1/captures.json`, run 1): 22 of 22 captures carry a route and 0 capture errors; 3 of 3 `/freshness` captures read `/freshness`; 18 of 18 `/security-analysis/<key>` captures carry all five tab labels `Thesis, Exec Management, Peers, Model, Posture`; 1 capture is the opened tab (`popup`, no tab labels by construction). Run 2's one capture is the BA Model tab (`data/run2/ledger/ba_model_ledger_wait.json`: 6 ledger rows read at the capture).
- What the page draws against what the SERVER sends: read from the dev build's own signed-in API client (`GET /api/scoped/amgt/security/<key>/overlay`, status 200 for all five names; `data/run1/api/overlay_*.json`). The served body carries the key `research_coverage` on BA, AMD, MSFT, HD and BP: MSFT `{"status":"outside_coverage","covered":false,"sentence":"We do not cover this company yet, so we hold no company figures or research for it. Any news or comparable companies shown here come from our wider market data.","covered_names":95}`; BA, AMD, HD, BP `{"status":"covered","covered":true,"sentence":null,"covered_names":95}`. The portal source at this ref has no reference to `research_coverage` under `portal/src/pages/SecurityAnalysis` (Grep over the folder, harness files excluded: 0 hits).
- PRD quotes at prd_version v0.41 (`org/missions/D5/AMGT/AMGT_RESAPP/prd/AMGT_RESAPP_PRD.md`).

## FWD-16

DONE WHEN (quoted, v0.41 line 653): "EXERCISED -- an analyst has read the day's items at the top of a page and followed one out".

- BA, the top band (capture 005; page top 004): company line "The Boeing Company operates as an aerospace company. The Company develops, manufactures, and services commercial airplanes, defense products, and space systems. Boeing serves clients worldwide." Band: "In the news on October 6th, 2026" -- one item, "Stocks Are Ignoring the Bond Market Warning at Their Peril", "Barron's -- October 6th, 2026, 7:36a ET", "Mentioned 1 time"; "no social source is admitted yet". The band sits below the news timeline and above the tab strip. Newest news day October 6th, 2026 = 2 days before 2026-10-08, inside 30 days.
- Source name as the page shows it: "Barron's" (a plain publisher name, not a code). The served item also carries a `publisher_code` key (its value was not read).
- THE ONE PRESS (once, on that item; captures 005 before, 006 and 007 after; `data/run1/fwd16/BA_press.json`): the item is an anchor (`<a href=".../www.barrons.com/articles/..." target="_blank">`). The press opened a NEW BROWSER TAB for the link (pages in the context 1 -> 2); the page stayed on `/security-analysis/BA_US_Equity`; no dialog or panel opened (0 dialogs, 0 open details). The new tab's navigation to www.barrons.com was aborted by the walker's third-party document block, so the tab read `www.barrons.com is blocked ... ERR_BLOCKED_BY_CLIENT` (capture 006), and the article's text was not read. What opens, as built: a link out to the publisher's site in a new tab.

## FWD-12

DONE WHEN (quoted, v0.41 lines 611-615, the amended text): "DONE WHEN EXERCISED -- on a real name, each input's source, last-run time and run result are read on the page and agree with /freshness. No control on the page claims to re-run an input."

- The page half (one statement) is NOT on this ref as one statement: on BA the page states which inputs it used in TWO places that disagree (row `AMGT_RESAPP-Z-W303-S1`).
  1. The block "Where this page's data comes from", above the tabs, 4 rows (capture 008): "Bloomberg data pulls stored for this name -- October 7th, 2026, 9:02a ET -- Worked"; "Seeking Alpha articles and reports stored for this name -- September 11th, 2026, 12:03a ET -- Worked"; "web search results stored for this name -- nothing has been read from this input for this name yet"; "the research pack built for this name -- October 7th, 2026, 9:02a ET -- Worked". No filings row; 0 controls in the block. The block repeats under every tab (read on all five).
  2. The Model tab ledger "Where each input came from", 6 lines (captures 009, 901): "Market data: Bloomberg; last ran October 7th, 2026 and worked."; "Filings: no source set up yet; has not run yet."; "News: Articles we collect; last ran October 6th, 2026 and worked."; "Social: no source set up yet; has not run yet."; "Web: no source set up yet; has not run yet."; "Seeking Alpha: Seeking Alpha; has not run yet." In run 1 the ledger still read "Loading where each input came from" 3.5 s after the tab press (capture 009 shows that state); run 2 waited and read it drawn after 1,018 ms (row `AMGT_RESAPP-Z-W303-S2`).
- Places counted: 2 statements of the inputs (block and ledger). The two disagree on Seeking Alpha (block: September 11th, 2026 "Worked"; ledger: "has not run yet"). Also on the Thesis tab the page names a filing it used in its own source lines ("the 10-K filed January 30th, 2026 -- read from the research pool", "From the 10-K filed January 30th, 2026.", footer "Source: company filings and Form 10-K."); these are source lines of panels, counted separately from the two input statements, 3 lines.
- Against /freshness on BA (first visit, Boeing BA row): Seeking Alpha 2026-09-11, stale; the block's Seeking Alpha date is the same day.
- Served `input_provenance` for BA (`data/run1/api/overlay_BA.json`): 4 entries, input keys `bloomberg`, `seekingalpha`, `serp`, `pack`; no `filings` key.

## FWD-7

DONE WHEN (quoted, v0.41 line 549): "EXERCISED -- (v0.39) a seat opens the one place on demand, sees every covered company with its last-refreshed date, and finds a stale one without opening any folders. Adam's own use stays the ACCEPT".

- First visit (the first page opened after the sign-in landing on `/market`): `/freshness`, 95 rows; columns Company, Oldest input, Bloomberg, Seeking Alpha, Research pack, Stale. The column header reads "Seeking Alpha" (not "Seeking Alpha last read"); the words "Seeking Alpha last read <date>" appear in the Stale column on stale rows. Summary: "3 of 95 covered companies have an input older than 7 trading days."
- Seeking Alpha cell on 5 rows, exactly as read (capture 002, `data/run1/fwd7/fwd7-first.json`): Alibaba BABA `2026-09-11` (stale, "Seeking Alpha last read 2026-09-11"); Boeing BA `2026-09-11` (stale, same words); Costco COST `2026-09-11` (stale, same words); Adobe ADBE US `Not collected` (not stale); AIA Group `Not collected` (not stale). Over all 95 rows: `Not collected` 92, a date 3 (all `2026-09-11`).
- Whether any row reads stale: yes, 3 of 95 (the three above, the same three names as round 77), each stale on Seeking Alpha only.
- First paint (navigation start to the first table row): first visit 4,580 ms (DOMContentLoaded 166 ms); second visit in the same session 2,019 ms (DOMContentLoaded 170 ms). Round 77 read 3,495 / 2,044 ms.
- Page end: "End of Freshness. Data as of October 8th, 2026, 5:00p ET."
- Captures: 001, 002, 003.

## FWD-1

DONE WHEN (quoted, v0.41 line 493): "EXERCISED -- (v0.40) a seat opens, on demand, a covered company the grading seat names, and the model numbers, the business description and the segment breakdown are on screen with no spreadsheet or data terminal opened. An analyst's own use stays the ACCEPT".

### AMD US -- SEGMENT TABLE NOT SERVED THIS ROUND

- Segment panel (`data-segment-state="REASON"`, 0 rows, 0 headings) under the heading "Business segments -- from the filing": "No filing analysis is stored for this name yet, so no segment breakdown is shown. A segment table with figures needs a separate segment data pull." Capture 011.
- Business description: "About the company" opened, 401 characters, "Advanced Micro Devices, Inc. (AMD) produces semiconductor products and devices. ... AMD serves customers worldwide." with "Company description from Bloomberg"; the company line at the top of the page ends in an ellipsis ("... assembling, testing, and..."). Captures 010, 012.
- Model numbers: the header figures read Price USD 649.42, Market cap USD 1.06T, Enterprise value USD 1.05T, Net debt USD -6.71B, Beta 1.55, Average volume 20.42M, Short interest 2.5% (capture 010/013). The Model tab holds two tables (read from the page, `data/run1/fwd1/AMD_model_tab.json`): a version comparison "Figure | Before, October 6th, 2026 | After, October 7th, 2026 | Change | Change, % | Detail | Consensus estimate of the price/earnings ratio (fiscal year 2026)", 16 rows; and "Consensus (Bloomberg) | Financial Summary" with fiscal-year columns 2016 to 2025, 65 rows. Capture 013 is the viewport after the tab press and shows the page top (header figures), not the table body: the tables are in the data file.

## COVERAGE

Order text: "Record every place the page says, or implies, that the company is not covered, and every empty panel that gives another reason ... The repair is one plain statement in one place. Then open BA and record that no such statement is drawn." (No PRD DONE WHEN line is named by the order for this act.)

- MSFT US (`MSFT_US_Equity`; capture 014 page top, 015 Thesis tab full page; five tabs' text in `data/run1/coverage/`): the page does NOT draw the served sentence "We do not cover this company yet, ..." anywhere: the words "do not cover" occur 0 times on any of the five tabs. The page draws this instead, 10 places on the Thesis tab and the other tabs:
  1. Header: "sector and country are not in this security's data".
  2. "no company description is held for this name yet, so no one-line description is shown".
  3. "We hold no stored company data for this name yet." (plain, below the header, every tab).
  4. Block "Where this page's data comes from", 4 rows, each "nothing has been read from this input for this name yet" (every tab).
  5. "Earnings dates are not on file for this company yet, so no earnings marker is drawn."
  6. Thesis tab: "The research team's thesis pillars: no research dossier exists for this name." and "No drafted prose for this name yet."
  7. Thesis tab: "BUSINESS SEGMENTS -- FROM THE FILING: No filing analysis is stored for this name yet, so no segment breakdown is shown. A segment table with figures needs a separate segment data pull."
  8. Exec Management tab: "The research team on management: no research dossier exists for this name." and "No officer list could be shown for this name. Company filing: No filing could be matched to msft; ... Research notes: no research notes exist for this name. Bloomberg: no Bloomberg officer list is stored for this name, and getting one needs a new Bloomberg request, which this page does not make".
  9. Posture tab: "No fund of record and no last stated position: no research dossier exists for this name."
  10. Peers tab: three peer rows read "This listing has only an exchange number; we have no company match for it yet."
- Empty-panel reasons on MSFT other than coverage: the news band and the news timeline DO draw articles (newest item "Stocks Are Ignoring the Bond Market Warning at Their Peril", Barron's, October 6th, 2026, "Expand (61 more)"; the band "In the news on October 6th, 2026"). The words "No articles collected" did not occur in any tab's text; the closed "Posture, research dossier and readings" disclosure was not opened.
- BA US (`data/run1/coverage/BA_scan.json`, five tabs; capture 017): no statement that the company is not covered is drawn ("do not cover", "not covered", "outside coverage": 0 occurrences on all five tabs). Other absence lines on BA: "The research team's thesis pillars: no research pack for this security.", "web search results stored for this name -- nothing has been read from this input for this name yet", "Earnings dates are not on file for this company yet ...", "THE RESEARCH TEAM'S BASE CASE IS NOT IN THIS PACK". The served BA `research_coverage` is `covered: true`, `sentence: null`.

## OFFICERS

Order text: "The repair puts a chief executive first, then a chief financial officer, where the list holds them." (No PRD DONE WHEN line is named by the order for this act.)

First three rows of the Exec Management list as drawn (`data/run1/officers/`):

- BA US (captures 016, 018): 12 officers, "from Item 10. Directors, Executive Officers and Corporate Governance, the 10-K filed January 30th, 2026, as of September 15th, 2026"; 1. Robert K. Ortberg -- "President and Chief Executive Officer, and a member of the Board"; 2. Jesus Malave, Jr. -- "Executive Vice President and Chief Financial Officer"; 3. Uma M. Amuluru -- "Executive Vice President and Chief Human Resources Officer".
- HD US (captures 019, 020): 10 officers, "from Item 10 ... the 10-K filed March 18th, 2026, as of September 15th, 2026"; 1. EDWARD P. DECKER -- "Chair, and as our President and Chief Executive Officer"; 2. RICHARD V. McPHAIL -- "Executive Vice President and Chief Financial Officer"; 3. WILLIAM D. BASTEK -- "Executive Vice President - Merchandising".
- BP/ LN (`BP/_LN_Equity`, URL `/security-analysis/BP%2F_LN_Equity`; captures 021, 022): the management list IS drawn (status SERVED, 10 officers), captioned "10 officer(s) from Bloomberg officer list (no filing roster could be read), as of October 7th, 2026", with the note "This table is the Bloomberg fallback: the filing roster did not resolve."; 1. Katherine Anne Thomson "Kate" -- "Chief Financial Officer"; 2. Marguerite Eileen O'Neill "Meg" -- "Chief Executive Officer"; 3. Sonya Adams -- "Exec VP:People & Culture". On BP the chief financial officer is drawn before the chief executive.

## Not walked

Nothing named by the order was left unwalked. Not walked outside the order: the non-Dev negative arm (the account is Dev only), any role-gated view, and the closed "Posture, research dossier and readings" disclosure on MSFT.
