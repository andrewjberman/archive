# WALK_ROUND77 -- AMGT-ba-24, worker 0.9.0_WK_AMGT_RESAPP~286

Records what was seen; no verdict on any judgment read. The walker account is role admin, userType Dev (status line below), so role-gated differences are NOT covered.

## Build, instrument, safety

- Build walked: local dev build `http://localhost:5174`, started by this worker with `bun run dev:live --port 5174` from `C:/tmp/r77-286/portal` (port 5174 read 000 before). Portal ref `8ddfe409` (origin/DEV at the GO; `git -C portal rev-parse HEAD` = 8ddfe409948cc79bb45e5ac27a8136264ce8c9d4). Page as deployed to DEV plus the live data front door.
- GO facts (AMENDMENT 2): DSGN round 45's page work is on the ref (walked FWD-16 and FWD-12); the AMD segment pull has NOT run; no name carries a planted read; DEV-ONLY act added.
- Walker slot: `ui_walker_account.py status` read `status=disabled role=admin userType=Dev armed=no armedBy=none; SSM ABSENT` before each run. Three runs (see row `AMGT_RESAPP-Z-W286-S1`): holders `Opal_Bloomberg:34652:95f23092` (armed 06:02:22Z, disarmed 06:04:13Z), `Opal_Bloomberg:45220:e9ceb16d` (disarmed 06:09:00Z), `Opal_Bloomberg:32264:6914d4d4` (disarmed 06:12:31Z). After every run: `LOGIN WITH THE WALK PASSWORD AFTER DISARM: HTTP 401 ... REFUSED`. Final status read in the AC2 output of the proof.
- Instrument (`instrument/`): `walk_ay6.mjs` and `signin_detect.mjs` copied unchanged from round 76; this round's module `ba24_walk.mjs` (GET only; guard unchanged). Final run: 0 guard aborts, 1 API issue (the RESOLVE control read without headers, 401, by design), 3 console errors (two 401s on the sign-in page, one 401 on that same control read), walk void: no. Third-party document requests are aborted in the browser context.
- Walk stamps (gitignored, never committed): run 1 `tmp/ui-walk/20261007T060222Z` (35 screenshots), run 2 `20261007T060715Z` (36), **run 3 `20261007T061041Z` (40) = the record**; the 40 run-3 screenshots are copied to `captures/` as 001-040, plus 041 from run 1 (the accidental press, S1). `data/` beside this file is run 3's data folder.
- Positive control on every capture (`data/captures.json`, run 3): 40 of 40 carry a route and 0 capture errors; 8 of 8 `/freshness` captures read `/freshness`; 29 of 29 `/security-analysis/<key>` captures carry all five tab labels `Thesis, Exec Management, Peers, Model, Posture`; 2 on `/market` (the sign-in landing and its hover), 1 on `/security-analysis` (the RESOLVE read's page context).
- PRD quotes at prd_version v0.41 (`org/missions/D5/AMGT/AMGT_RESAPP/prd/AMGT_RESAPP_PRD.md`): FWD-1 line 493, FWD-7 line 549, FWD-12 line 599 (amended text lines 607-615), FWD-14 line 629, FWD-16 line 653, FWD-18 line 678.

## DEV-ONLY

- Sign-in landed on `/market`. The sidebar draws a `Freshness` entry (`a[href="/freshness"]`, visible; 18 sidebar links read, `data/misc/dev_only_nav.json`). The rail shows icons only; hovering the entry shows its label "Freshness" (`data/misc/dev_only_hover.json`). `/freshness` opens (h1 "Freshness", 95 rows).
- Captures: `001-devonly-nav-with-freshness-entry`, `002-devonly-nav-freshness-entry-hovered` (the label shown).
- The walker account reads role admin, userType Dev. It cannot sign in as a non-Dev user; the negative arm (a non-Dev user: no nav entry, no route) is NOT walked, and no other account was tried.

## FWD-7 -- the closing visit on /freshness

DONE WHEN (quoted, v0.41 line 549): "EXERCISED -- (v0.39) a seat opens the one place on demand, sees every covered company with its last-refreshed date, and finds a stale one without opening any folders. Adam's own use stays the ACCEPT". The task order adds CTO ruling 2: one visit with a NOT-stale row beside a stale one, the stale one found from the page.

- FIRST VISIT (the first page opened after the sign-in landing; the page had not been read before): 95 rows; columns Company, Oldest input, Bloomberg, Seeking Alpha, Research pack, Stale. Summary: "3 of 95 covered companies have an input older than 7 trading days." Default sort pressed: Stalest first.
- STALE rows seen (3, all found from the page by the default sort and the Stale column; flag `data-stale=true`): Alibaba BABA, Boeing BA, Costco COST -- each Oldest input 2026-09-11, Seeking Alpha 2026-09-11, Stale text "Seeking Alpha last read 2026-09-11". NOT-stale rows seen: 92, e.g. Adobe ADBE US, AIA Group, Air Liquide AI FP -- Oldest input 2026-10-06, Seeking Alpha "Not collected", Stale text "All inputs current".
- The two together: capture `005-fwd7-stale-beside-not-stale-default-sort` shows the three stale rows directly above the first not-stale rows. The step that found the stale ones: open /freshness, read the default Stalest-first order and the Stale column. Sorts pressed: Stalest first (stale 3 of first 3 rows), Freshest first (first ten all not stale), Company name (captures 006-008).
- PLANTED: no. All three stale reads are organic (the same three names as round 76); nothing was planted by this worker or named in the GO. The GO named no planted name, so this was not needed.
- Date against flag on 5 rows (capture `009-fwd7-date-vs-flag-five-rows`, `data/fwd7/date_vs_flag.json`): Alibaba, Boeing, Costco show Oldest input 2026-09-11 equal to the oldest date among their input columns and are flagged stale; Adobe and AIA show 2026-10-06 equal to their oldest input date and are not stale. Over all 95 rows the Oldest input equals the oldest dated input cell on 95 of 95; 0 mismatches.
- Never-collected input: Seeking Alpha reads "Not collected" on 92 of 95 rows and a date on 3; Bloomberg and Research pack read a date on 95 of 95. The word "stale" is not applied to a "Not collected" cell (`data-state` `not_collected` 92, `stale` 3, `collected` 190 across the three inputs). The Web search column is gone (headers above); one sentence states "Web search is not collected yet."
- First paint (navigation start to the first table row): first visit **3,495 ms** (DOMContentLoaded 193 ms; the `/api/scoped/amgt/freshness` read took 542 ms, 5,244 bytes encoded, 66,341 decoded); second visit in the same session **2,044 ms**. The same measure in the two earlier runs: 3,654 / 1,578 ms and 5,491 / 1,606 ms. Round 76 read 4,116 / 1,591 ms.
- Page end line: "End of Freshness. Data as of October 7th, 2026, 5:00p ET."
- Captures: 003, 005, 006, 007, 008, 009, 010 (second visit).

## FWD-14 -- the owner line on /freshness

DONE WHEN (quoted, v0.41 line 629): "EXERCISED -- a list has actually gone out of date and somebody was told by the system rather than by a wrong page".

- Under the summary the page reads: "Andrew owns the publisher list and the social account list." and "The publisher list is in date: reviewed 2026-09-10, next review due 2026-12-09. The social account list is in date: reviewed 2026-09-10, next review due 2026-10-10."
- So: owner for each of the two lists = Andrew (one sentence for both); last reviewed 2026-09-10 for both; neither reads out of date. Capture `004-fwd14-freshness-owner-line`.

## FWD-1 -- model numbers, business description, segment breakdown

DONE WHEN (quoted, v0.41 line 493): "EXERCISED -- (v0.40) a seat opens, on demand, a covered company the grading seat names, and the model numbers, the business description and the segment breakdown are on screen with no spreadsheet or data terminal opened. An analyst's own use stays the ACCEPT"

- **AMD US -- SEGMENT PULL NOT YET RUN.** The segment panel (`data-segment-state="REASON"`, 0 rows) reads under the heading "Business segments -- from the filing": "No filing analysis is stored for this name yet, so no segment breakdown is shown. A segment table with figures needs a separate segment data pull." That is a reason, not a breakdown of segments with figures. Capture `028-fwd1-AMD-segments`. Business description: "About the company" opened (401 characters, "Company description from Bloomberg"), capture 029; the company line also stands at the top of the page. Model numbers: Model tab opened, a "Figures in" table with fiscal-year columns and consensus columns, capture 030 (031 shows the page top after the tab).
- **BA US -- one heading per segment.** `data-segment-state="SERVED"`; three `data-segment-heading` headings, each once: "Commercial Airplanes" (4 rows), "Defense, Space & Security" (3 rows), "Global Services" (4 rows); 11 rows, each one sentence with figures (e.g. "Commercial Airplanes revenue was $41,494 million in 2025 ...") and a closed "Source" disclosure; source line "From the 10-K filed January 30th, 2026." Captures 018, 019 (first "Source" opened). About the company opened (247 characters, 020). Model tab: "What changed" version comparison and the figures table (022, 023).
- ASML_NA (also walked): segment panel REASON, 0 rows: "The filing text kept here is about the company's share capital and who holds its shares, so no segment breakdown is shown." (capture 036); About 253 characters (037); Model tab (038, 039).

## FWD-18 -- the three repairs, BA and ASML_NA

DONE WHEN (quoted, v0.41 line 678): "EXERCISED -- (v0.40) a seat clicks, on demand, a filing-derived figure on a covered company the grading seat names, through to the passage it came from. An analyst's own click stays the ACCEPT"

- **Passage renders once per press (BA).** Each of the 3 driver-chart points ("2023: 528", "2024: 348", "2025: 600 -- show the filing passage") pressed on its own: after each press the page holds 1 passage block (`data-driver-chart-passage-source="served"`), 1 `From the filing:` cite line, and the passage's first 40 characters occur 1 time in the page text. Round 76 read 3 blocks after one press. Captures 015, 016, 017 (`data/fwd18/BA_presses.json`).
- **Y-axis tick labels (BA).** The chart's tick labels read "0, 150, 300, 450, 600" on the y-axis and "2023, 2024, 2025" on the x-axis (`data/fwd18/BA_dom.json`, svg text; capture 014). Round 76 read "000000000" on the ASML_NA chart.
- **Table passage column labels (BA).** The opened passage is a table with column labels "737, 747, 767, 777, 787, Total" over rows "Cumulative deliveries 8,528 1,573 1,303 1,727 1,110" and "Deliveries 396 (9) 1 32 (14) 26 73 528", with the heading "2023" and a note: "Some rows list a different number of figures than there are columns, because the filing's blank cells and footnote marks are not kept; those rows give their figures in the order printed and may not line up with the columns." Cite "From the filing: ITEM 7. MANAGEMENT'S DISCUSSION AND ANALYSIS / TABLE 2023". Rows marked unaligned: 2 of 2 (captures 015-017).
- **ASML_NA.** No driver chart: the panel shows a reason instead (`data-driver-chart="ABSENT"`): "The filing text kept here counts the company's own shares or describes its share capital, so no driver chart is shown." (capture 035; CTO ruling 7). So the three repairs have no ASML_NA chart to press, tick or table to read.
- AMD US: no driver-chart element on the page (capture 027).

## FWD-16 -- the top of the page

DONE WHEN (quoted, v0.41 line 653): "EXERCISED -- an analyst has read the day's items at the top of a page and followed one out". No item was followed out (opening an item leaves the page to a third-party site; not pressed).

- BA: company line "The Boeing Company operates as an aerospace company. The Company develops, manufactures, and services commercial airplanes, defense products, and space systems. Boeing serves clients worldwide." Band: "In the news on October 5th, 2026" with one item "Why Boeing Stock Isn't Up More After Good FAA 737 MAX News", Barron's -- October 5th, 2026, 8:54a ET, Mentioned 6 times; "no social source is admitted yet". Captures 011 (company line), 012 (band in view; the band sits below the news timeline and above the tab strip, not at the very top of the page).
- AMD: company line "Advanced Micro Devices, Inc. (AMD) produces semiconductor products and devices. ... and..." (ends in an ellipsis); band "In the news on October 1st, 2026", item "Nasdaq rises nearly 2% in September, helped by late-month tech rally", Seeking Alpha -- October 1st, 2026, 2:34a ET, Mentioned 2 times; "no social source is admitted yet". Captures 024, 025.
- ASML_NA: company line "ASML Holding N.V. develops, produces, and markets semiconductor manufacturing equipment, ... The Company services clients worldwide."; band "In the news on October 1st, 2026", item "Airbus names ASML, Michelin CEOs to board as Obermann steps down", Seeking Alpha -- October 1st, 2026, 1:13p ET, Mentioned 4 times; same social sentence. Captures 032, 033.
- The newest news day is within 30 days of 2026-10-07 on all three names (5 and 6 days); "No news in the last 30 days" was not shown on any of the three.

## FWD-12 -- each input's source, last run and result, against /freshness

DONE WHEN (quoted, v0.41 lines 611-615, the amended text): "DONE WHEN EXERCISED -- on a real name, each input's source, last-run time and run result are read on the page and agree with /freshness. No control on the page claims to re-run an input."

- The block "Where this page's data comes from" (4 rows) sits under the band. BA: "Bloomberg data pulls stored for this name -- October 6th, 2026, 9:23a ET -- Worked"; "Seeking Alpha articles and reports stored for this name -- September 11th, 2026, 12:03a ET -- Worked"; "web search results stored for this name -- nothing has been read from this input for this name yet"; "the research pack built for this name -- October 6th, 2026, 9:23a ET -- Worked". Captures 013 (BA), 026 (AMD), 034 (ASML_NA).
- Against /freshness on BA (Boeing BA row, first visit): Bloomberg 2026-10-06, Seeking Alpha 2026-09-11 (stale), Research pack 2026-10-06; Web search is not a column and the page states "Web search is not collected yet". The page's days and the /freshness days are the same for the three dated inputs; the web-search line reads "nothing has been read" on the page. On AMD and ASML_NA the page reads Seeking Alpha "nothing has been read ... yet" and /freshness reads Seeking Alpha "Not collected" on those names.
- The Model tab also draws "Where each input came from" (6 classes: Market data, Filings, News, Social, Web, Seeking Alpha; "2 of 6 inputs have run" on AMD) on AMD (run 3) and ASML_NA; on BA the ledger was not drawn in any run. Row `AMGT_RESAPP-Z-W286-S2`. Captures 022 (BA), 030 (AMD), 038 (ASML_NA).
- Re-run controls: buttons or links on the three name pages matching /re-?run|refresh|update now|reload|retry/ outside the provenance block: 1 per page, the sidebar link "Data Refresh" (a navigation entry). Inside the provenance block: 0 controls (`data/fwd16/BA_top.json`). The Model tab carries a closed disclosure "Refreshing an input" whose text on ASML_NA reads "An input cannot be refreshed by itself from this page yet." Nothing on the page claims to re-run an input by itself.

## REFRESH (AMENDMENT 1)

- The SecurityAnalysis page on BA, AMD and ASML_NA does not draw a Refresh control: matches for /refresh/i outside the sidebar: 0 of 3 pages (`data/misc/refresh_control.json`). The only match is the sidebar link "Data Refresh" (href `/data-refresh`), a navigation entry. Nothing was pressed in the final run; capture `021-refresh-ba-no-control-on-page`.
- Run 1 pressed that sidebar link by mistake (no nav exclusion in the module): the browser went to `/data-refresh` with no error, toast or spinner and no write (0 guard aborts); capture `041-refresh-ba-nav-link-pressed-run1`. Row `AMGT_RESAPP-Z-W286-S1`.

## RESOLVE THROUGH THE GATEWAY (AMENDMENT 1)

- From the signed-in dev build, `GET /api/scoped/amgt/resolve?q=Lenovo` through the page's own request headers (authorization, accept, content-type; names only): status **200**, 177 bytes, body `{"query": "Lenovo", "status": "candidates", "security_key": null, "candidates": [{"security_key": "992_HK_Equity", "name": "Lenovo 992 HK", "ticker": "992 HK"}], "reason": null}`. The answer lists `992_HK_Equity`: yes. Control without headers: 401 (`data/misc/resolve.json`). No 404 and no 403. Capture 040 is the page context (the read has no page of its own).

## Rows filed

`AMGT_RESAPP-Z-W286-S1`, `AMGT_RESAPP-Z-W286-S2` (OBSERVATION, INERT, `disarm_owner` `2.0.0_SA_COO~Z`), in the INVESTIGATION_v1 channel.
