PORTAL_REF: 9b06f6edcb
# WALK_ROUND84 -- AMGT-ii-4, worker 0.9.0_WK_AMGT_RESAPP~337

Records what was seen; no verdict on any act. The walker account is role admin, userType Dev: role-gated differences are NOT covered.

## Build, instrument, safety

- Build walked: local dev build `http://localhost:5174`, started by this worker with `bun run dev:live --port 5174` from `C:/tmp/r84-337/portal`
  (portal ref `9b06f6edcb`, `git -C portal rev-parse --short=10 HEAD`; no bun install). Listener count before the start: 0; after the stop: 0 (only TIME_WAIT sockets remained).
- PRD quote at `prd_version` v0.41 (`org/missions/D5/AMGT/AMGT_RESAPP/prd/AMGT_RESAPP_PRD.md`).
- Start of task: `ui_walker_account.py status` read `status=disabled armed=no armedBy=none` and port 5174 had 0 listeners, so no contention and no wait.
- Stored-text read, run first (`round84_prep/checks/r84_store.py --key NU_US_Equity --crit AC2`, exit 0): `status 200, served locations 39, business locations 4, sentences 53, English-marked 52 (98%)`;
  PASS T1 (route answers 200), PASS T2 (a served passage is cited to the business item), PASS T3 (98% English, floor 80%); `R84 STORE AC2 NU_US_Equity: YES`.
  (Row `AMGT_RESAPP-D1-W337-S1`: the checker's "4 business locations" is 3 Item 4.B locations plus one Item 3.D heading that contains "our business".)
- One arm/walk/disarm pass: stamp `20261009T104741Z` (gitignored `tmp/ui-walk/`), holder `DESKTOP-HK1UU7N:13356:f649bd4b`, armed 10:47:45Z, disarmed 10:48:53Z, printed
  `LOGIN WITH THE WALK PASSWORD AFTER DISARM: HTTP 401 {"error":"Invalid email or password"} -> REFUSED` and `OK: DISARMED at 2026-10-09T10:48:53.484036Z`
  (`DISARM: row status=disabled; SSM PRESENT`: the skill does not delete the parameter).
- Instrument: `instrument/walk_ay6.mjs` and `signin_detect.mjs` copied from round 83 (`~333`); `instrument/ii4_walk.mjs` is `hh5_walk.mjs` with ASML_NA_Equity replaced by NU_US_Equity (FWD-18 on NU only).
  Run: `UI_WALK_ROOT=C:/tmp/r84-337 WALK_PY=<python 3.12> AX6_MODULE=<ii4_walk.mjs> node walk_ay6.mjs --base http://localhost:5174 --max-minutes 8`.
  GET only; the guard is unchanged: 0 guard aborts, 0 API issues, 2 console errors (not read further), walk void: no. Third-party document requests blocked: 0 (`data/blocked_third_party.json` is `[]`).
- Captures COPIED to `captures/`: 8 PNG (`001`-`008`, same names as in the stamp). `data/` holds `captures.json`, `fwd18/`, `api/`, `walk_stdout.log`, `guard.tsv`, `summary.md`, `findings.json`.
- Positive control (`data/captures.json`): 8 of 8 captures carry route `/security-analysis/NU_US_Equity`, 8 of 8 carry all five tab labels (Thesis, Exec Management, Peers, Model, Posture), 0 capture errors,
  8 of 8 PNG over 120 KB (150,282 to 401,805 bytes). Byte-identical pairs: 001 = 003 (the page top), 004 = 005 = 006 (the open Investment-thesis window, before and after the press).
- What the page draws against what the SERVER sends is read from the dev build's own signed-in API client: `GET /api/scoped/amgt/security/NU_US_Equity/thesis` from inside the page with the headers the page sent
  (names: accept, authorization, content-type); status 200, 746,991 bytes. The full body stays in the gitignored stamp; `data/api/thesis_NU_US_Equity.json` holds the reads of the relevant keys
  and `data/api/thesis_NU_locations.json` holds the `location` list and counts.

## FWD-18

DONE WHEN (quoted, v0.41 lines 678-681): "EXERCISED -- (v0.40) a seat clicks, on demand, a filing-derived figure on a covered company the grading seat names, through to the passage it came from. An analyst's own click stays the ACCEPT".

### NU (`NU_US_Equity`, "NU Holdings LTD", NU US), Thesis tab

1. **The company description, as the page draws it** (capture 001; `data/fwd18/NU_top.json`): under the name band, one paragraph ending in an ellipsis, quoted: "NU Holdings Ltd. of the Cayman Islands operates as a holding company. The Company, through its subsidiaries, provides loans and digital banking services, as well as issues, administrates, processes, and transfers payments to post-paid credit cards and equity investments in other entities. NU..."
   (The walk module's `[data-top-band-description]` selector read empty on this name; the text above is from the page body text in the same file.)
   The page has no "About the company" disclosure (`data/fwd18/NU_about.json` `absent: true`). Under the Thesis heading it prints "the 20-F filed April 8th, 2026 -- read from the research pool", then "The research team's thesis pillars: the research team's pack is not on file for this security.", then "THE RESEARCH TEAM'S NOTES" with "Why we own it": "Why we own Nu is the largest digital bank in Latin America, operating under the Nubank brand across Brazil, Mexico and Colombia. They have 139mn customers with 118mn in Brazil ...".
   Inside the Investment-thesis window (captures 004-006) the page says, quoted: "No company description is on file yet." then the heading "FILED DETAIL (DOES NOT DESCRIBE THE BUSINESS)".
   API client: `dossier_sections` carries `company_description` with status `absent`, text null, reason "The research update of 2026-Q2 has no \"Company description\" section." (and `why_we_own` `served`); the walk did not open the Posture disclosure.
2. **The place where a driver chart would be** (capture 002; `data/fwd18/NU_chart_place.json`): a sentence in a bordered panel, no chart (0 svg, 0 buttons, `data-driver-chart="ABSENT"`), quoted: "The series for the thesis driver, "Total revenue", is not in the model data yet." and "No chart is drawn until its numbers are there; none is worked out from the drafted text. The research data team adds the series."
   The share-capital refusal sentence ("shares or describes its share capital") appears 0 times in the served body. API client: `thesis_driver_chart.status` `ABSENT`, `driver_series` "Total revenue", `driver_unit` "US$ millions", `points_count` 0, `block_series_probed` 75; its reason: the driver's series is not one of the model block's 75 fiscal series by exact mnemonic or definition, the interface carries its segments as cited prose with no numeric table, and the filing's own verified points do not clear the second branch's bar.
   Directly above that panel the page draws "BUSINESS SEGMENTS -- FROM THE FILING" (12 rows in the DOM; "Other" first: "No single segment can be named from the stored filing text for this finding."), then sentences each with a "Source" disclosure (first: "Total revenue reached US$15,774.8 million in 2025, up US$4,257.8 million or 37.0% from US$11,517.1 million in 2024."). API client: `segment_table.status` `none` ("No Bloomberg segment table has been stored for this name yet."); the DOM panel's state reads `SERVED` from `segment_breakdown` rows.
3. **The three cards and their windows** (captures 003, 004, 007, 008; `data/fwd18/NU_card_windows.json`): Investment thesis ("Gross profit rose 26.1% to US$6,625.0 million while gross margin fell to 42.0% from 45.6%.", 9 points), Risks ("The business depends on a well-regarded brand, and failure to maintain it would harm results.", 9 points), Recommendation ("The research team's Base case is not in this pack"; "This is a machine's draft from the company's filing, not the research team's recommendation."; the first sentence "The company expects 2026 to be \"an inflection year ...\"", 10 passages).
   Windows draw 20, 9 and 10 passage blocks (39), each with a citation line "NU US'S 20-F, FILED APRIL 8TH, 2026 -- <ITEM> > PARAGRAPH <n>"; the saved dialog text is cut at 9,000 characters, so the saved text carries 6, 6 and 2 of those lines.
4. **Served citations' `location` values** (API client, `data/api/thesis_NU_locations.json`): 39 locations, all under `drafted_sections`: ITEM 5. OPERATING AND FINANCIAL REVIEW AND PROSPECTS 23, ITEM 3.D. RISK FACTORS 13, ITEM 4.B. BUSINESS OVERVIEW 3 (paragraphs 153, 107, 109). The page's passage blocks (20 + 9 + 10 = 39) equal the API's 39.
   Refusal sentence ("shares or describes its share capital"): 0 times.
5. **THE ONE FIGURE PRESS** (captures 005 before, 006 after; `data/fwd18/NU_figure_press.json`): the figure "15,774.8" in the Investment-thesis window's first machine sentence, "Total revenue reached US$15,774.8 million in 2025, up US$4,257.8 million or 37.0% from US$11,517.1 million in 2024." (cursor over it `auto`; `host_is_interactive` true is the walker's `closest()` test on the sentence's paragraph; the page's inventory of pressable things in the Thesis panel, `NU_thesis_panel_pressables.json`, holds `summary` disclosures ("Where this comes from", "What is not on file", "Source"), the three card buttons and none on a figure; the window's only button is Close).
   Nothing changed: dialogs 1 before and after, dialog text length 22,549 before and after, passages 20 before and after, tooltips/menus 7 before and after, open `details` 0, `aria-expanded=true` 0, pages 1 before and after, URL `/security-analysis/NU_US_Equity` before and after; dialog text before and after identical, and the two screenshots are byte-identical.
   The passage each sentence rests on is already printed under it in the window (the figure's own passage: "ITEM 5. OPERATING AND FINANCIAL REVIEW AND PROSPECTS > PARAGRAPH 250").
