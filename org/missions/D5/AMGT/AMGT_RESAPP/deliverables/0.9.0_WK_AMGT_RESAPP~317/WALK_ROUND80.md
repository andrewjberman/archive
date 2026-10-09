PORTAL_REF: 8d2a08a92b5e857af63f56f87d1e99225f1b08c6
# WALK_ROUND80 -- AMGT-dd-3, worker 0.9.0_WK_AMGT_RESAPP~317

Records what was seen; no verdict on any act. The walker account is role admin, userType Dev: role-gated differences are NOT covered.

## Build, instrument, safety

- Build walked: local dev build `http://localhost:5174`, started by this worker with `bun run dev:live --port 5174` from `C:/tmp/r80-317/portal`
  (port 5174 read 0 listeners before the start; the walker read `armed=no armedBy=none` before each arm). Portal ref `8d2a08a92b5e` (`git -C portal rev-parse HEAD`
  = `8d2a08a92b5e857af63f56f87d1e99225f1b08c6`, origin DEV, one commit on `84e13d0f`). No bun install. Live function per the GO.
- PRD quotes at `prd_version` v0.41 (`org/missions/D5/AMGT/AMGT_RESAPP/prd/AMGT_RESAPP_PRD.md`).
- Two arm/walk/disarm passes (stamps in the gitignored `tmp/ui-walk/`; walker `status` read `status=disabled role=admin ... armed=no armedBy=none` before and after each):
  | pass | stamp | holder | module | ran |
  |---|---|---|---|---|
  | 1 the walk | `20261009T020341Z` | `DESKTOP-HK1UU7N:9420:4992ff38` | `instrument/dd3_walk.mjs` | armed 02:03:45Z; FWD-7 then FWD-1; 16 PNG |
  | 2 the AMD segment panel's own table, read as the DOM draws it | `20261009T020743Z` | `DESKTOP-HK1UU7N:18376:d3f60920` | `instrument/dd3_amd_seg.mjs` | armed 02:07:46Z; 1 PNG |
  Pass 2 exists because pass 1's selector `[data-segment-breakdown]` reads the "Business segments -- from the filing" panel (a reason), and the page also draws a "Revenue by segment" table above it (capture 014 shows both) that pass 1's DOM read missed.
- **Disarm did not complete as the skill describes** (row `AMGT_RESAPP-D1-W317-S1`): after each pass the account row reads `status=disabled armed=no armedBy=none`, but the disarm's `ssm:DeleteParameter` is denied to this box's agent user, so `SSM PRESENT` stays and the login-refused proof did not print. Rows `AMGT_RESAPP-D1-W317-S2` (the order's `R1` id form is refused by the row gate; `D1` is the registered coordinate: `-S3`): the walker's own `python` call was pointed at Python 3.12 through `WALK_PY` in my copy of `walk_ay6.mjs`.
- Instrument: `walk_ay6.mjs` (round 79's, one line changed, S2) and `signin_detect.mjs`; `dd3_walk.mjs` is extended from round 79's `cc8_walk.mjs` (FWD-7 and AMD sections, the segment DOM read widened). GET only; guard unchanged: 0 guard aborts, 0 API issues, 2 console errors (the sign-in page's) in each pass, walk void: no. Third-party document requests aborted in the browser context.
- Captures COPIED to `captures/`: 17 PNG (`001`-`016` from pass 1, `017` from pass 2), file names as in the stamps. `data/` holds pass 1's data (`captures.json`, `fwd7/`, `fwd1/`, `api/`, logs); `data/pass2/` holds pass 2's.
- Positive control (`data/captures.json`): 16 of 16 pass-1 captures carry a route and 0 capture errors; 12 of 12 `/freshness` captures read `/freshness`; 4 of 4 AMD captures read `/security-analysis/AMD_US_Equity` with all five tab labels (`Thesis, Exec Management, Peers, Model, Posture`); 17 of 17 PNG files are over 5 KB (107-221 KB). Four `/freshness` captures (001, 003, 010, 012) are byte-identical: Lenovo 992 HK and Alibaba BABA stand inside the first screen (the page lists the stalest first), so the row scroll moved nothing; the screen holds both rows (capture 010 read).
- What the page draws against what the SERVER sends is read from the dev build's own signed-in API client: `GET /api/scoped/amgt/security/AMD_US_Equity/thesis` and `GET /api/scoped/amgt/freshness?view=page` from inside the page with the headers the page itself sent (names: `accept, authorization, content-type`); both status 200.

## FWD-1

DONE WHEN (quoted, v0.41 lines 493-496): "EXERCISED -- (v0.40) a seat opens, on demand, a covered company the grading seat names, and the model numbers, the business description and the segment breakdown are on screen with no spreadsheet or data terminal opened. An analyst's own use stays the ACCEPT".

### AMD US (`AMD_US_Equity`)

- **Model numbers**, header figures as drawn (capture 013): Price USD 645.86, Market cap USD 1.05T (as of October 8th, 2026), Enterprise value USD 1.05T, Net debt USD -6.71B, Beta 1.55, Average volume 20.41M, Short interest 2.5%. The Model tab (capture 016; `data/fwd1/AMD_model_tab.json`) draws two tables: a version comparison ("Figure | Before, October 7th, 2026 | After, October 8th, 2026 | Change | Change, % | Detail", 9 rows, first row the consensus price/earnings ratio for fiscal year 2026, 86.8x to 86.3x) and "Consensus (Bloomberg) | Financial Summary" with 65 rows.
- **Business description** (captures 013, 015): the company line at the top ends in an ellipsis ("... as well as provides assembling, testing, and..."); "About the company" opened, quoted "Advanced Micro Devices, Inc. (AMD) produces semiconductor products and devices. The Company offers products such as microprocessors, embedded microprocessors, chipsets, graphics, video and multimedia products and supplies it to third-party foundries, as well as provides assembling, testing, and packaging services. AMD serves customers worldwide." with "Company description from Bloomberg".
- **Where the segment breakdown is** (captures 014, 017; `data/pass2/AMD_revenue_by_segment_dom.json`): **the page draws a table** under the heading "REVENUE BY SEGMENT" (wrapper `data-segment-table="served"`, table `data-segment-table-revenue`), columns `Segment | Fiscal year 2025 | Period 2 | Period 3 | Period 4 | Period 5`, six rows with first values:
  | row as drawn | Fiscal year 2025 |
  |---|---|
  | Data Center | 16,635 |
  | Client & Gaming | 14,550 |
  | Client (indented) | 10,640 |
  | Gaming (indented) | 3,910 |
  | Embedded | 3,454 |
  | All Other | (empty) |
  Beneath it a second table, "OPERATING INCOME BY SEGMENT" (`data-segment-table-operating`), six rows (Data Center 3,603; Client & Gaming 2,855; Embedded 1,243; All Other -4,007; Client and Gaming empty in column 1). Then four note lines, quoted: "Figures are in millions of USD, the units and currency of the reported revenue these columns add up to."; "A column is named with a fiscal year where its top-level rows add up to the company's reported revenue for that year. The other columns keep Bloomberg's own period numbers."; "Period 2, Period 3, Period 4, Period 5: The rows of this column do not add up to the company's reported revenue for any year we hold, so the year is not stated."; "Source: Bloomberg product segments, pulled October 7th, 2026".
- **The same page, further down**, the panel "BUSINESS SEGMENTS -- FROM THE FILING" (`data-segment-state="REASON"`, 0 rows, 0 tables, `data/fwd1/AMD_segments_dom.json`) still reads, quoted: "No filing analysis is stored for this name yet, so no segment breakdown is shown. A segment table with figures needs a separate segment data pull." Both are on screen in capture 014.
- **API client, `segment_table`** (`data/pass2/AMD_segment_table_full_api.json`): `status` "served"; `rows` 6 (Data Center level 1 first value 16635; Client & Gaming 1 14550; Client 2 10640; Gaming 2 3910; Embedded 1 3454; All Other 1 null); first row name "Data Center", first value 16635; `periods[0].label` "Fiscal year 2025" (then Period 2 to Period 5); `currency` "USD"; `units` "millions"; `operating_income_rows` 6. The served `segment_breakdown.reason` is the same sentence the filing panel draws.
- Page against server: the page's revenue table draws the 6 rows, first value 16,635 and the "Fiscal year 2025" first column the server sends; the filing panel draws the served reason.

## FWD-7

DONE WHEN (quoted, v0.41 lines 549-551): "EXERCISED -- (v0.39) a seat opens the one place on demand, sees every covered company with its last-refreshed date, and finds a stale one without opening any folders. Adam's own use stays the ACCEPT".

- First visit: `/freshness` was the first page opened after the sign-in landing on `/market` (`data/fwd7/dom_first.json`, `landed_before_visit` `/market`). 95 rows; columns Company, Oldest input, Bloomberg, Seeking Alpha, Built analysis, Stale. Summary: "1 of 95 covered companies have an input older than 7 trading days." Page end: "End of Freshness. Data as of October 8th, 2026, 5:00p ET." Captures 001 (first visit top), 012 (second visit top).
- **First-paint time** (navigation start to first table row; `data/fwd7/dom_first.json`, `dom_second.json`): first visit **3,702 ms** (DOMContentLoaded 243 ms); second visit in the same session **1,792 ms** (DOMContentLoaded 326 ms).
- **Rows the page flags stale: 1 of 95**, "Lenovo 992 HK" (`data-stale="true"`; Stale cell "Seeking Alpha last read 2026-09-22"; Oldest input 2026-09-22; capture 010). The API client's `stale` reads true for the same row and no other among the ten read.
- **Ten Seeking Alpha cells** (page cell exactly as drawn, with its `data-state` attribute; then the API client's `seeking_alpha.state` and `.sentence`; captures 002-011 one per row in this order; `data/fwd7/ten_rows.json`). The page draws the API sentence on the row for 10 of 10 (`page_draws_api_sentence` true):
  | # | row | page draws | page `data-state` | API `state` | API `sentence` |
  |---|---|---|---|---|---|
  | 1 | Boeing BA | Seeking Alpha last read 2026-10-07. | read | read | Seeking Alpha last read 2026-10-07. |
  | 2 | Alibaba BABA | Seeking Alpha last read 2026-10-06. | read | read | Seeking Alpha last read 2026-10-06. |
  | 3 | Costco COST | Seeking Alpha last read 2026-10-07. | read | read | Seeking Alpha last read 2026-10-07. |
  | 4 | AIA Group | No Seeking Alpha collection record is held for this company yet. | no_record | no_record | No Seeking Alpha collection record is held for this company yet. |
  | 5 | ServiceNow NOW US | No Seeking Alpha collection record is held for this company yet. | no_record | no_record | No Seeking Alpha collection record is held for this company yet. |
  | 6 | Zurich Insurance ZURN SW | No Seeking Alpha collection record is held for this company yet. | no_record | no_record | No Seeking Alpha collection record is held for this company yet. |
  | 7 | Hon Hai 2317 TT | Seeking Alpha was checked on 2026-10-05 and no article is held for this company. | checked | checked | Seeking Alpha was checked on 2026-10-05 and no article is held for this company. |
  | 8 | Monster MNST | Seeking Alpha was checked on 2026-10-08 and no article is held for this company. | checked | checked | Seeking Alpha was checked on 2026-10-08 and no article is held for this company. |
  | 9 | Lenovo 992 HK | Seeking Alpha last read 2026-09-22. | stale | read | Seeking Alpha last read 2026-09-22. |
  | 10 | KDDI | Seeking Alpha was checked on 2026-10-05 and no article is held for this company. | checked | checked | Seeking Alpha was checked on 2026-10-05 and no article is held for this company. |
  Six of the ten read without a date as a last-read date (rows 4-8 and 10: three `no_record`, three `checked`); the `checked` rows carry the check date inside the sentence. The `no_record` and `checked` rows draw different sentences.

## Not walked

Nothing named by the order was left unwalked. Not walked outside the order: the non-Dev negative arm, any role-gated view, the Thesis/Exec Management/Peers/Posture tabs of AMD.

## Cleanup

Walker `status` after pass 2: `status=disabled ... armed=no armedBy=none; SSM PRESENT` (see S1). Dev server stopped by this worker (its own process tree by pid); listeners on port 5174 read 0 afterwards.
