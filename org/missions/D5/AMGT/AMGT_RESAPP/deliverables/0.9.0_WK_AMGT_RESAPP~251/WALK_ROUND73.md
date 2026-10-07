# WALK_ROUND73 -- AMGT-aw-8, worker 0.9.0_WK_AMGT_RESAPP~251

Records what was seen; no verdict on any judgment read. Role: the walker account is role admin, so role-gated differences are NOT covered.

## Build, instrument, safety

- Build walked: local dev build `http://localhost:5174`, started by this worker with `bun run dev:live --port 5174` from `C:/tmp/r73-251/portal` (port 5174 was not listening before: curl read 000), stopped at the end. Portal `fb939c4a` (DEV + aw-4 page + its App.tsx hookup). Backend: deployed `opal-amgt-scoped-api` after aw-7 (code `satkY3HX`).
- Walker slot: `ui_walker_account.py status` read disarmed before every run (`disabled armed=no, SSM ABSENT`); no other holder appeared. Four runs, each armed and disarmed by the walker itself; every run printed `DISARM ... -> HTTP 401 ... REFUSED`. Final status: `status=disabled armed=no armedBy=none; SSM ABSENT`.
- Instrument: `instrument/walk_aw8.mjs` is a copy of `.claude/skills/ui-walk/walk.mjs` with ONE change: when `AW8_MODULE` is set it imports that module after sign-in and hands it the page, `shot`, `settle`, `waitForLoaded`, `clickLabel`; stock routes are skipped. `UI_WALK_ROOT=C:/tmp/r73-251`. The walker's own `secret` call, network guard (GET/HEAD/OPTIONS plus the admitted sign-in POSTs) and disarm `finally` are unchanged: 0 guard aborts in every run. The modules are `aw8_stage2.mjs` (the walk), `aw8_stage3.mjs` (print GET), `aw8_stage4.mjs` (About-the-company). Every data read is a GET with the page's own bearer from `localStorage`, as `requestPrintPack` makes it.
- One local response edit, named: the FWD-31 "without the passage" control re-renders the same tab with the live `/thesis` answer fetched and `dossier_fields.management` deleted IN THE BROWSER ONLY (`page.route`, then removed). No write reaches the store. It is a control, not served data.
- Positive control on every capture: the record carries `location.pathname` and the five tab labels read from the DOM (`data/captures.json`, `data/CAPTURE_INDEX.tsv`): 81 of 81 captures carry the route; 77 of 77 tab-bearing captures carry all five labels `Thesis, Exec Management, Peers, Model, Posture` (the 4 `/freshness` captures have no tabs). The labels are also visible in each screenshot.
- Walk stamps (gitignored under `tmp/ui-walk/`, never committed):
  - `20261006T050158Z` -- the walk: 81 screenshots (FWD-18 8, FWD-31 6, FWD-1 60, FWD-5 3, FWD-7 4), 93 `/thesis` bodies, `/freshness` body. 0 guard aborts; the 2 API issues are the BP and NG 404s.
  - `20261006T050953Z` -- the print GETs: 3 PDFs (BA 104,415 bytes, ASML_NA 112,849, BABA 95,790; 200, `application/pdf`) rendered to 70 PNG pages (24 + 26 + 20) in `print-pages/`.
  - `20261006T051201Z` -- FWD-1 "About the company" opened: 12 screenshots.
  - `20261006T044620Z` and `20261006T045214Z` -- two earlier runs of the same modules: the first stopped on a file name with `*`; the second recorded no tab labels in the control and left the print bodies at 0 bytes (Playwright `response.body()` of a blob fetch). Superseded by the stamps above; not relied on.
- The order cites PRD lines `:487`, `:521-525`, `:539-542`, `:660-661`, `:857-868`; at the bytes the DONE WHENs sit at lines 493, 531, 549, 670 and 869 of `prd/AMGT_RESAPP_PRD.md`. Text quoted below is read at those lines.
- Cold/warm: the live `/freshness` answered in 10,170 ms from the page (2,850,172 bytes) and 11,958 ms to the first table row.

## FWD-18 -- a driver-chart figure clicked through to its passage (BA, ASML_NA)

DONE WHEN (quoted, v0.40): "EXERCISED -- (v0.40) a seat clicks, on demand, a filing-derived figure on a covered company the grading seat names, through to the passage it came from. An analyst's own click stays the ACCEPT"

- Route `/security-analysis/<key>`, Thesis tab. Captures: `fwd18-BA_US_Equity-thesis-before-click`, `-point1-opened`, `-point2-opened`, `-point3-opened`, and the same four for `ASML_NA_Equity` (8 shots).
- BA US: chart "Commercial Airplanes (BCA) aircraft deliveries -- from the filing, not the model", 3 points; links "2023: 528 -- SHOW THE FILING PASSAGE", "2024: 348 ...", "2025: 600 ...". Each click set `aria-expanded=true` and the line under it read: "The filing passage for this point is not shown on this page." (3 of 3).
- ASML NA: 3 links ("2023: 393421721 ...", "2024: 393283720 ...", "2025: 385417665 ..."), all citing passage P0086. Same sentence on each open (3 of 3; the second click closed the shared passage, was pressed again, and read the same sentence).
- The served `/thesis` body for both carries `thesis_driver_chart.points[].passage_text` (BA 168, 92, 93 characters; ASML 101) and `passage_cite`; the page showed none of it. Row `AMGT_RESAPP-Z-W251-S1`. Per-click record: `data/fwd18/*.json`.

## FWD-31 -- the team's MANAGEMENT passage beside the filing roster (BABA, SAP_GY; control BA; census name)

DONE WHEN (quoted, v0.40, abridged only at the clause breaks): "for a name whose pack carries a MANAGEMENT passage, the Exec Management tab renders that passage LABELLED AS THE TEAM'S and cited to its report, positioned BESIDE the filing roster rather than in place of it; the roster's own rows are BYTE-UNCHANGED against the same tab captured without the passage; and a name whose pack carries none renders the roster alone with the passage slot ABSENT WITH ITS REASON. The rendered state carries a POSITIVE CONTROL in the same capture -- the location is the application route and the tab's own label is present"

- BABA US (`fwd31-BABA_US_Equity-exec-with-passage`): route `/security-analysis/BABA_US_Equity`; tab labels present with EXEC MANAGEMENT selected. Heading "THE RESEARCH TEAM ON MANAGEMENT", the passage (592 characters, begins "Management/Board 80 Eddie Wu ..."), line "Source: Alibaba BABA Research Pack 2026 03 09_v1"; below it the roster, "7 OFFICER(S) FROM ITEM 6. DIRECTORS, SENIOR MANAGEMENT AND EMPLOYEES, THE 20-F FILED MAY 20TH, 2026", 7 officer rows. Position: passage box y 635-751, first officer row y 809, same column (x 111, width 1266): passage above the roster in the one panel, roster present.
- Without (`fwd31-BABA_US_Equity-exec-without-passage-local-control`, the local response edit): slot reads "The research team on management: no management passage is stated in the research team's pack." and the same 7 roster rows. Compared in the browser: 7 of 7 `tr[data-exec-officer]` outerHTML strings equal, hash of all rows equal (`56ae1cad796870c6`).
- SAP GY (`...SAP_GY_Equity-exec-with-passage` and `-without-...`): passage 1,832 characters, "Source: SAP Research Pack 2026 06 12_v1", 6 officer rows; without: same slot sentence; 6 of 6 rows equal (hash `72ca80256e87ab6a`).
- BA US (`fwd31-BA_US_Equity-exec-with-passage`), the absent arm: no passage on file; slot reads "The research team on management: no management section, because neither a research pack nor an earnings update is on file for this name." and the roster alone, 12 officer rows.
- Census name Tokyo Electron 8035 JP (`fwd31-8035_JP_Equity-exec-with-passage`): passage SERVED (1,637 characters, "Source: TEL research pack 5_7_2026"), 0 officer rows; the roster area reads "No officer list has been published for this name yet." with the served reason (no company filing stored; Bloomberg officer list needs a new Bloomberg request).
- The Exec Management panel subtitle on BABA reads "Officers from the filing, with tenure against the pool". Record: `data/fwd31/fwd31.json`.

## The 44-name census

`FWD31_CENSUS.md` (this folder): last line `CENSUS 42 names, 42 with a reason`. Not 44: today's population is the 95 covered names (93 readable; BP/_LN_Equity and NG/_LN_Equity answer 404 on `/thesis`), 46 with a passage, 4 of those with a roster, 42 with none. Classes: 22 no company filing stored; 19 no filing could be matched; 1 filing found with an empty officer section. Row `AMGT_RESAPP-Z-W251-S4`.

## FWD-1 -- the segment breakdown on the 12 names that serve it

DONE WHEN (quoted, v0.40): "EXERCISED -- (v0.40) a seat opens, on demand, a covered company the grading seat names, and the model numbers, the business description and the segment breakdown are on screen with no spreadsheet or data terminal opened. An analyst's own use stays the ACCEPT"

- The 12 names (`/thesis` `segment_breakdown.rows` non-empty): ASML_NA 5 rows, BABA 11, BA 11, COST 10, HAL 12, HD 10, INTU 9, KMB 9, NU 10, PBR 8, SAP_GY 11, VLO 10 (116 rows).
- Each opened at `/security-analysis/<key>`; all five tabs read and shot (60 captures `fwd1-<key>-<Tab>`), then "About the company" opened on each (12 captures `fwd1-<key>-about-the-company-open`, stamp `...051201Z`).
- Seen: model figures on the Model tab on 12 of 12 (13k-16k characters of page text); the business description under "ABOUT THE COMPANY" (closed on load, 247-438 characters once opened) on 12 of 12; the header cards, news, timeline.
- Not seen: a segment breakdown. No tab and no opened disclosure draws the served rows as a breakdown. Of the 116 served row sentences, 1 (COST) is found whole on a page, as a drafted-thesis sentence; segment labels recur only as ordinary words in other text (BABA Thesis page: 3 of 9 labels). Positive control: the same reader finds those BABA words; the portal source holds 0 references to `segment_breakdown`. Row `AMGT_RESAPP-Z-W251-S2`. Records: `data/fwd1/fwd1.json`, `data/fwd1/fwd1_about.json`.

## FWD-5 -- the rendered BA print pages

DONE WHEN (quoted, v0.38 text in the PRD): "EXERCISED -- (v0.38) a seat prints the pack on demand for three covered names, and each reads as a document: Opal Brand form, every figure traceable to its page field, no raw code, no dashboard chrome (a JUDGMENT read at L9). Adam's actual forward stays the ACCEPT"

- The Print button was pressed in the browser on BA US, ASML NA and BABA US (captures `fwd5-<key>-print-modal`: the page's PRINT PREVIEW dialog showing page 1 of "of 24" for BA, the PDF viewer drawn in the dialog). The same GET (`/api/scoped/amgt/security/<key>/print`) was then read for the bytes and rendered page by page: BA 24 pages, ASML_NA 26, BABA 20 (`print-pages/<key>-pNN.png`, 70 PNGs).
- Seen on BA page 1: title "BOEING CO/THE [BA US Equity] Research Note", heading "Model figures", sub-heading "Header", then one line per field in a monospace face, each ending "- as of 2026-10-06 - Bloomberg", long lines wrapped with a hanging indent; units in words ("USD 152,984.0 million"). Page 12 is the same listing form, e.g. "Revenue/Sh: USD 105.93 per share - as of 2026-10-06 - Bloomberg".
- Measured on the three PDFs (`data/fwd5/print_metrics.json`; pattern counters each fire once on a planted string): upper-case underscore code tokens 0 of 3; figures with 5 or more decimals 0 of 3; Python repr marks 0 of 3; widest text right edge 535.5 pt on a 612 pt page in 3 of 3 (no line past the page edge).
- Not read here (judgment): whether it reads as an Opal Brand document or carries dashboard chrome. The pages are plain black text with no logo or colour.

## FWD-7 -- the /freshness page on the dev build

DONE WHEN (quoted, v0.39 in the PRD): "EXERCISED -- (v0.39) a seat opens the one place on demand, sees every covered company with its last-refreshed date, and finds a stale one without opening any folders. Adam's own use stays the ACCEPT"

- Route `/freshness` (nav "Freshness"), aw-4's page. Table first row at 11,958 ms. Captures `fwd7-freshness-default`, `-sort-Stalest first`, `-sort-Freshest first`, `-sort-Company name`.
- Seen: 95 rows, columns Company, Last refreshed, Bloomberg, Seeking Alpha, Web search, Research pack, Stale; every Last refreshed 2026-10-04; the Research pack column now reads a date (it read NEVER before aw-3). Summary line: "95 of 95 covered companies have an input that is stale (older than 7 trading days, or never read)." Each row's Stale cell names its inputs, e.g. "Alibaba BABA ... Seeking Alpha last read 2026-09-11 / Web search has never been read", "Adobe ADBE US ... Seeking Alpha has never been read / Web search has never been read". Three sort buttons (Stalest first pressed by default, Freshest first, Company name); on all three sorts the first five rows read the same (Adobe ADBE US, AIA Group, Air Liquide AI FP, Alibaba BABA, Alphabet GOOGL US), since every row ties on date and flag.
- A stale name is found without opening a folder, but the flag does not separate one name from the rest: 95 of 95 rows carry a flag.
- In the capture the card is a dark navy ground with dark-blue text and navy-bordered sort buttons; the text reads only faintly. The DOM text reads in full. Row `AMGT_RESAPP-Z-W251-S3`.

## Rows filed

`AMGT_RESAPP-Z-W251-S1` (FWD-18 passage not shown), `-S2` (FWD-1 no segment breakdown on the page), `-S3` (FWD-7 page look, 95 of 95 flagged, 12 s), `-S4` (census 42 not 44; slash-key 404). All OBSERVATION, INERT, `disarm_owner` `2.0.0_SA_COO~Z`.
