PORTAL_REF: e6fb269c83
# WALK_ROUND83 -- AMGT-hh-5, worker 0.9.0_WK_AMGT_RESAPP~333

Records what was seen; no verdict on any act. The walker account is role admin, userType Dev: role-gated differences are NOT covered.

## Build, instrument, safety

- Build walked: local dev build `http://localhost:5174`, started by this worker with `bun run dev:live --port 5174` from `C:/tmp/r83-333/portal`
  (portal ref `e6fb269c83`, `git -C portal rev-parse --short=10 HEAD`; clean working copy; no bun install). Listener count before the start: 0; after the stop: 0.
- Start-of-task contention (row `AMGT_RESAPP-D1-W333-S1`, BLOCKING, committed `f931b9fe75`): at 09:57Z-09:58Z the walker read `armed=yes` by
  `DESKTOP-HK1UU7N:22288:c2a1066b` and another seat's walk and dev server held port 5174. I stopped and filed the row. At about 10:01Z the walker read
  `status=disabled armed=no armedBy=none` and port 5174 read 0 listeners, so I started this walk then. The row stays as filed.
- PRD quote at `prd_version` v0.41 (`org/missions/D5/AMGT/AMGT_RESAPP/prd/AMGT_RESAPP_PRD.md`).
- Stored-text read, run first (`round81_prep/checks/r81_store.py`): AC1 `R81 STORE AC1 SERVED: YES` (silver row accession 000162828026011378, items
  `Item 4.B. Business Overview`, `Item 3.D. Risk Factors`, `Item 5. Operating and Financial Review and Prospects`; heading `ITEM 4.B. BUSINESS OVERVIEW` opens 400 chars of prose);
  AC2 `--where deployed`: `status 200, served locations 23, Item 4.B locations 6, refusal sentence x0`, `R81 STORE AC2 SERVED: YES`.
- One arm/walk/disarm pass: stamp `20261009T100516Z` (gitignored `tmp/ui-walk/`), holder `DESKTOP-HK1UU7N:30376:05c91aec`, armed 10:05:20Z, disarmed 10:06:10Z, printed
  `LOGIN WITH THE WALK PASSWORD AFTER DISARM: HTTP 401 ... REFUSED` and `OK: DISARMED`. `status` read `armed=no armedBy=none` before and after (`SSM PRESENT`: the skill does not delete the parameter).
- Instrument: `instrument/walk_ay6.mjs` and `signin_detect.mjs` copied from round 80 (`~317`; `WALK_PY` points at Python 3.12); `instrument/hh5_walk.mjs` is this walk's module, extended from round 79's `cc8_walk.mjs` (FWD-18 on ASML NA only).
  GET only; the guard is unchanged: 0 guard aborts, 0 API issues, 2 console errors (not read further), walk void: no. Third-party document requests aborted in the browser context.
- Captures COPIED to `captures/`: 8 PNG (`001`-`008`, same names as in the stamp). `data/` holds `captures.json`, `fwd18/`, `api/`, `walk_stdout.log`.
- Positive control (`data/captures.json`): 8 of 8 captures carry route `/security-analysis/ASML_NA_Equity`, 8 of 8 carry all five tab labels (Thesis, Exec Management, Peers, Model, Posture), 0 capture errors,
  8 of 8 PNG over 120 KB. Byte-identical pairs: 001 = 003 (both the page top), 004 = 005 = 006 (the open Investment-thesis window, before and after the press).
- What the page draws against what the SERVER sends is read from the dev build's own signed-in API client: `GET /api/scoped/amgt/security/ASML_NA_Equity/thesis` from inside the page with the headers the page sent; status 200,
  1,104,355 bytes. The full body stays in the gitignored stamp; `data/api/thesis_ASML_locations.json` holds the `location` list and counts.

## FWD-18

DONE WHEN (quoted, v0.41 lines 678-681): "EXERCISED -- (v0.40) a seat clicks, on demand, a filing-derived figure on a covered company the grading seat names, through to the passage it came from. An analyst's own click stays the ACCEPT".

### ASML NA (`ASML_NA_Equity`), Thesis tab

1. **The company description, as the page draws it** (capture 001; `data/fwd18/ASML_top.json`): under the name band, one line, quoted: "ASML Holding N.V. develops, produces, and markets semiconductor manufacturing equipment, specifically machines for the production of chips through lithography. The Company services clients worldwide."
   The page has no "About the company" disclosure (`data/fwd18/ASML_about.json` `absent: true`). Under the Thesis heading it prints "the 20-F filed February 25th, 2026 -- read from the research pool", then "THE RESEARCH TEAM'S THESIS PILLARS" (first: "Secular growth tailwinds trump short-term cyclicality in this trillion dollar market", source line "ASML research pack 5_5_2026").
   Inside the Investment-thesis window (captures 004-006) the page says, quoted: "No company description is on file yet." then the heading "FILED DETAIL (DOES NOT DESCRIBE THE BUSINESS)".
   API client: `dossier_sections` carries `company_description` with status `served` and 1,535 characters of text (and `why_we_own`, `positives`, `negatives`, `special_items`, all `served`); the walk did not open the Posture disclosure, so where that text is drawn, if anywhere, is not read here.
2. **The place where a driver chart would be** (capture 002; `data/fwd18/ASML_chart_place.json`): a sentence in a bordered white panel, no chart (0 svg, 0 buttons, `data-driver-chart="ABSENT"`), quoted: "The series for the thesis driver, "EUV system revenue recognition (EXE and NXE units recognized in sales)", is not in the model data yet." and "No chart is drawn until its numbers are there; none is worked out from the drafted text. The research data team adds the series."
   The share-capital refusal sentence appears 0 times on the page and 0 times in the served body. API client: `thesis_driver_chart.status` `ABSENT`, `driver_series` "EUV system revenue recognition (EXE and NXE units recognized in sales)", `driver_unit` "units per year".
   Directly above that panel the page draws "BUSINESS SEGMENTS -- FROM THE FILING" (12 rows; "Other" first: "No single segment can be named from the stored filing text for this finding."), then sentences each with a "Source" disclosure, ending "From the 20-F filed February 25th, 2026." API client: `segment_table.status` `served`, 12 rows.
3. **The three cards and their windows** (captures 003, 004, 007, 008; `data/fwd18/ASML_card_windows.json`): Investment thesis ("In April 2025 ASML demonstrated the first ever 1,000-watt light source for EUV lithography, built on 25 years of...", 5 points), Risks ("Counterparty credit risk is concentrated: the three largest customers accounted for EUR 1,294.2 million or 35.4% of...", 3 points), Recommendation (the research team's base case, then a machine draft sentence, 8 points).
   Windows draw 11, 3 and 9 passage blocks, each with a citation line "ASML NA'S 20-F, FILED FEBRUARY 25TH, 2026 -- <ITEM> > PARAGRAPH <n>" (23 lines).
4. **Served citations' `location` values** (API client, `data/api/thesis_ASML_locations.json`): 23 locations, all under `drafted_sections`: ITEM 5. OPERATING AND FINANCIAL REVIEW AND PROSPECTS 12 (paragraphs 31, 32, 38 x2, 75, 77, 78, 82, 90, 91, 94, 95), ITEM 3.D. RISK FACTORS 5 (paragraph 32, 53, 61, 98, and "Counterparty credit risk / paragraph 140"), ITEM 4.B. BUSINESS OVERVIEW 6 (paragraphs 68, 127, 128, 140, 180, 187).
   Refusal sentence ("shares or describes its share capital"): 0 times. The page's 23 citation lines read the same 11 + 3 + 9 as the API's per-card locations: Investment thesis window 5 of the 6 Item 4.B lines (127, 128, 140, 187, 180); Recommendation window 1 (paragraph 68); Risks window 0.
5. **THE ONE FIGURE PRESS** (captures 005 before, 006 after; `data/fwd18/ASML_figure_press.json`): the figure "2.9" in the Investment-thesis window's first sentence, "In Logic, net sales increased by EUR 2.9 billion, primarily driven by leading-edge foundry growth in support of strong AI demand." (cursor over it `auto`; the page's inventory of pressable things in the Thesis panel, `ASML_thesis_panel_pressables.json`, holds `summary` disclosures ("Where this comes from", "About these figures", "Source"), the three card buttons and none on a figure; the window's only button is Close).
   Nothing changed: dialogs 1 before and after, dialog text length 7,286 before and after, passages 11 before and after, tooltips/menus 6 before and after, open `details` 0, `aria-expanded=true` 0, pages 1 before and after, URL `/security-analysis/ASML_NA_Equity` before and after; the two screenshots are byte-identical.
   The passage each sentence rests on is already printed under it in the window (the figure's own passage: "ITEM 5. OPERATING AND FINANCIAL REVIEW AND PROSPECTS > PARAGRAPH 31").
