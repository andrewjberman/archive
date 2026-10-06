# WALK_ROUND76 -- AMGT-az-6, worker 0.9.0_WK_AMGT_RESAPP~266

Records what was seen; no verdict on any judgment read. Role: the walker account is role admin, so role-gated differences are NOT covered.

## Build, instrument, safety

- Build walked: local dev build `http://localhost:5174`, started by this worker with `bun run dev:live --port 5174` from `C:/tmp/r76-266/portal` (port 5174 read 000 before). Portal ref `6b4e89a8` (origin/DEV head carrying 1d6d2573 and 6de76f0509): this is the page as deployed to DEV, NOT a local merge (r75 walked a local merge). Backend: deployed `opal-amgt-scoped-api`, CodeSha256 `OVpDhfwD` (named by the GO).
- GO from the issuer: walk BA, AMD and ASML_NA; FWD-16's top band is not on this portal ref, so that act was skipped.
- Walker slot: `ui_walker_account.py status` read `status=disabled armed=no armedBy=none; SSM ABSENT` before the run; no other holder appeared. One run, holder `Opal_Bloomberg:21744:96b5d50b`, armed 21:31:38Z, disarmed 21:33:22Z, `LOGIN WITH THE WALK PASSWORD AFTER DISARM: HTTP 401 ... REFUSED`. Final status read in the AC2 output of the proof.
- Instrument (`instrument/`): `walk_ay6.mjs` (the stock walker plus one hook that imports `AX6_MODULE` after sign-in, copied from the r75 instrument), `signin_detect.mjs`, and this round's module `az6_walk.mjs`. Walker `secret`, network guard and the disarm `finally` unchanged: 0 guard aborts, 0 API issues, 0 findings, 2 console errors (the sign-in page's 401s before login). Third-party document requests are aborted in the browser context (`data/blocked_third_party.json`).
- Walk stamp (gitignored, never committed): `tmp/ui-walk/20261006T213136Z` -- 21 screenshots, copied to `captures/` (21 PNG) with the run's `data/` beside this file.
- Positive control on every capture (`data/captures.json`): 21 of 21 carry the route; 5 of 5 `/freshness` captures read `/freshness` (no tabs there); 16 of 16 `/security-analysis/<key>` captures carry all five tab labels `Thesis, Exec Management, Peers, Model, Posture`; 0 capture errors.
- PRD quotes at prd_version v0.40: DONE WHENs at lines 549 (FWD-7), 678 (FWD-18), 493 (FWD-1).

## FWD-7 -- the /freshness page, first visit

DONE WHEN (quoted): "EXERCISED -- (v0.39) a seat opens the one place on demand, sees every covered company with its last-refreshed date, and finds a stale one without opening any folders. Adam's own use stays the ACCEPT"

- Captures `001-fwd7-freshness-first`, `002..004` (sort Stalest first, Freshest first, Company name), `005-fwd7-freshness-second`.
- FIRST VISIT: the first page the fresh walker context opened after sign-in (sign-in landed on `/market`). First paint (navigation start to the first `tbody tr`): **4,116 ms** (DOMContentLoaded 223 ms; the `/api/scoped/amgt/freshness` read started at 954 ms and took 2,665 ms, 1,073,156 bytes encoded, 2,889,557 decoded). Second visit in the same session: 1,591 ms (read 643 ms). r75 read 2,043 ms cold; r74 9,135 ms; r73 11,958 ms.
- Seen: 95 rows; columns Company, Last refreshed, Bloomberg, Seeking Alpha, Web search, Research pack, Stale; summary "95 of 95 covered companies have an input that is stale (older than 7 trading days, or never read)." and "Web search is not collected yet."; footer "Data as of October 6th, 2026, 5:00p ET." Last refreshed is 2026-10-06 on 95 of 95 rows (one distinct value); Seeking Alpha "Never" on 92 and 2026-09-11 on 3 (Alibaba BABA, Boeing BA, Costco COST); Web search "Not collected" on 95; 95 of 95 rows carry `data-stale=true`; the Stale column reads "Seeking Alpha has never been read" (92) or "Seeking Alpha last read 2026-09-11" (3). Three sort buttons, Stalest first pressed by default. No folder is opened to see any row.
- Can a stale name be singled out? Every name is flagged and every Last refreshed is one date, so by flag or by that date the page does not single one out; the three names that differ read a different Seeking Alpha date and Stale text. Row `AMGT_RESAPP-Z-W266-S1`.

## FWD-18 -- a driver-chart point to its filing passage

DONE WHEN (quoted): "EXERCISED -- (v0.40) a seat clicks, on demand, a filing-derived figure on a covered company the grading seat names, through to the passage it came from. An analyst's own click stays the ACCEPT"

- BA (captures 006, 007): `[data-driver-chart]` SERVED, source filing, caption "Commercial Airplanes (BCA) aircraft deliveries -- from the filing, not the model"; 3 points (2023: 528, 2024: 348, 2025: 600). Clicked "2023: 528 -- show the filing passage": passage opened in place (`data-driver-chart-passage-source=served`) reading "2023 / Cumulative deliveries 8,528 1,573 1,303 1,727 1,110 / Deliveries 396 (9) 1 / 32 (14) / 26 / 73 528 / * Intercompany deliveries identified by parentheses / Loss From Operations", cite "From the filing: ITEM 7. MANAGEMENT'S DISCUSSION AND ANALYSIS / TABLE 2023". It is flat text (0 table elements); the row labels are inline with the numbers and only "2023" stands above them -- no column labels for the five numbers.
- AMD (capture 012): no `[data-driver-chart]` on the page; no point to click.
- ASML_NA (captures 016, 017): driver chart SERVED, caption "Issued ordinary shares outstanding (nominal EUR0.09), reflecting the buyback authorization -- from the filing, not the model"; 3 points (2023: 393421721, 2024: 393283720, 2025: 385417665); the chart's y-axis tick labels read "000000000" on the capture. Clicked the first link: lines "2023", "2024", "2025", "Issued ordinary shares with nominal value of EUR0.09", "393,421,721", "393,283,720", "385,417,665", cite "From the filing: TABLE / period 2023". Year column labels and the row label are present as separate lines (0 table elements); the passage block shows three times on the page after the one click, each citing "period 2023".
- Row `AMGT_RESAPP-Z-W266-S3`.

## FWD-1 -- model numbers, business description, segment breakdown

DONE WHEN (quoted): "EXERCISED -- (v0.40) a seat opens, on demand, a covered company the grading seat names, and the model numbers, the business description and the segment breakdown are on screen with no spreadsheet or data terminal opened. An analyst's own use stays the ACCEPT"

- Segment breakdown (captures 008, 009, 013, 018, 019):
  - BA: SERVED, one heading "BUSINESS SEGMENTS -- FROM THE FILING" over the whole block; 11 rows, each a segment label, one sentence and a closed "Source" disclosure; source "From the 10-K filed January 30th, 2026." Labels: Commercial Airplanes (4 rows), Defense, Space & Security (3), Global Services (4) -- three segments, the label repeated on each row and the rows interleaved (not one heading per segment). First "Source" pressed (capture 009).
  - AMD: state REASON, 0 rows; the panel reads "No filing analysis is stored for this name yet, so no segment breakdown is shown. A segment table with figures needs a separate segment data pull."
  - ASML_NA: SERVED, 5 rows labelled Authorized share capital, Other, Treasury shares, Major holders, Board holdings; source "From the 20-F filed February 25th, 2026." First "Source" pressed (capture 019).
- Business description: "About the company" opened on 3 of 3 (captures 010, 014, 020): text of 247 (BA), 401 (AMD), 253 (ASML_NA) characters, e.g. BA "The Boeing Company operates as an aerospace company. The Company develops, manufactures, and services commercial airplanes, defense products, ...".
- Model numbers: Model tab pressed on 3 of 3 (captures 011, 015, 021): the tab reads "Reported figures and Bloomberg consensus estimates, from the model block", a "What changed" version comparison and a "Figures in USD" table (BA capture shows fiscal-year columns 2016-2025 and consensus 2026E-2028E).
- Row `AMGT_RESAPP-Z-W266-S2`.

## FWD-16

Not walked: the GO states the top band is not on this portal ref.

## Rows filed

`AMGT_RESAPP-Z-W266-S1`, `-S2`, `-S3` (OBSERVATION, INERT, `disarm_owner` `2.0.0_SA_COO~Z`), in the INVESTIGATION_v1 channel.
