# WALK_ROUND71 -- AMGT-au-5, worker 0.9.0_WK_AMGT_RESAPP~235 (re-seated; Z-W235-S1 resolved by the re-seat)

Reads and records only; no verdict on any judgment criterion. Role: the walker account is role admin, so role-gated differences
are NOT covered by anything below.

- Build walked: local dev build on http://localhost:5174 (started by this worker; `bun run dev:live --port 5174`), portal ref e6ab82ad,
  against the deployed `opal-amgt-scoped-api` (CodeSha256 `GS//XHnVd4+bBIg1VU++r1fp9v495pi6jKFat9KbEYE=`, read 2026-10-05).
- Names walked: BA ("BA US"), AMD ("AMD US"), ASML_NA ("ASML NA"), each picked by typing the ticker into "Search any ticker".
- Walk stamp folders (gitignored, never committed): `tmp/ui-walk/20261005T161750Z/` (stock engine, 96 shots) and
  `tmp/ui-walk/20261005T163146Z/` (the same walk with the `--au5` additions of `walk_au5.mjs`, 108 shots, `au5-reads.json`, three
  `print-from-page-*.pdf`), and `tmp/ui-walk/20261005T165304Z/` (a short walk with `--pick-bar AMD_US_Equity`, the FWD-15 row click, 10 shots;
  two earlier short walks, `20261005T164501Z` and `20261005T164947Z`, fell back to typing the ticker because the price bars had not
  drawn yet, and are void for FWD-15). Four armed walks were made in all; every one disarmed. The stock capture names are the same in both; the screenshots I read were from 161750Z for the
  numbered stock shots and from 163146Z for every `au5-*` shot. Every walk armed and disarmed the walker itself
  (`DISARM ... REFUSED`: "LOGIN WITH THE WALK PASSWORD AFTER DISARM: HTTP 401 -> REFUSED"), 0 guard aborts, 0 API issues.
- `walk_au5.mjs` (this folder) is a copy of `.claude/skills/ui-walk/walk.mjs` with three additions: `--au5` (hover the header figure
  cards; press the page's own "Print" button, which is a GET; read each tab's own data attributes), `--pick-bar <security_key>` (click that
  ranked-list row) and a `PICK` log line. The engine has no step for
  those acts. "Export as a document" names a DO_NOT_CLICK word and was NEVER pressed. Row `Z-W235-S4`.
- Positive control carried in every capture set: the location is `/security-analysis` and the five tab labels (THESIS, EXEC
  MANAGEMENT, PEERS, MODEL, POSTURE) are in the shot. (`au5-reads.json` `tab_label_present` reads false because my selector
  looked for `role=tab`; the tabs are not `role=tab` -- a defect of my read, not a finding about the page.)

Capture counts in `20261005T163146Z/shots/` (108 files): lead list 3; per name overlay 1, timeline 1; header hover 3 each (9);
Print modal 1 each (3); Thesis 8/2/8 (BA/AMD/ASML); Exec Management 1/2/1; Peers 2 each; Model 18 each; Posture 2/1/2.

## FWD-1 -- "EXERCISED -- an analyst has actually done it, not merely could" (PRD :481)
ACCEPT: "An analyst opens a company the firm already covers and the model numbers, the business description and the segment
breakdown are already on screen."
- Saw (BA, AMD, ASML): the overlay shows PRICE / MARKET CAP / ENTERPRISE VALUE / NET DEBT / BETA / AVERAGE VOLUME, "ABOUT THE
  COMPANY" description (BA, ASML read; "Company description from Bloomberg"), recent news, a news timeline; the Model tab shows a
  FINANCIAL SUMMARY by fiscal year. I did NOT find a segment breakdown on the page, and the deployed rich export for BA has no segment
  breakdown either (one incidental word). Row `Z-W235-S5`.
- The pack was reached and downloaded: pressing "Print" took 16.2 s (BA), 20.8 s (AMD), 19.3 s (ASML) to a "PRINT PREVIEW -- <name>"
  modal showing the PDF (21 of 21 pages for BA); the page's own blob was saved (`print-from-page-*.pdf`, 178,896 / 191,098 /
  195,657 bytes, `%PDF-`), byte-identical (sha256) to the same route invoked directly (see FWD-5).
- Captures: `004-BA-US-overlay.png`, `037-AMD-US-overlay.png`, `064-ASML-NA-overlay.png`, `au5-BA-US-print-modal-viewport.png`,
  `au5-AMD-US-print-modal-viewport.png`, `au5-ASML-NA-print-modal-viewport.png`. 12 captures + 3 PDFs.

## FWD-3 -- "EXERCISED -- a figure has actually been challenged and answered from the page" (PRD :498)
ACCEPT: "Someone asks where a figure came from, on what basis, and as of when. The analyst answers by pointing at the screen."
- Saw: hovering each header figure card opens a tooltip: BA "Price value USD 193.56 as of October 5th, 2026, 9:33a ET source Bloomberg";
  AMD "... USD 633.91 as of October 5th, 2026, 9:32a ET source Bloomberg"; ASML "... EUR 1653.00 as of October 5th, 2026, 9:32a ET
  source Bloomberg". Market cap, EV, net debt, beta, volume answer the same three questions (value, as-of, source). The card also
  prints "as of October 5th, 2026" and the strip below prints "Source: Bloomberg." Positive control: the same shot carries the card
  and the header strip.
- Captures: `au5-{BA-US,AMD-US,ASML-NA}-hover-{1,2,3}-viewport.png` (9) + the three overlay shots.

## FWD-6 -- "EXERCISED -- someone has actually compared two versions" (PRD :526)
ACCEPT: "An analyst returns to a company researched before and can say what moved, naming the earlier version that shows it.
Refreshing adds a version; it does not overwrite the old one."
- Saw (Model tab, all three names): a WHAT CHANGED block with an "Earlier version" and a "Later version" select. BA: October 2nd,
  2026 11:49a ET -> October 5th, 2026 9:33a ET, "354 added", "37 changed", rows Figure / Before, October 2nd, 2026 / After,
  October 5th, 2026 / Change / Change %, each with a "Full figures" opener. AMD: October 1st 3:09a ET -> October 5th 9:32a ET.
  ASML: September 30th 4:39a ET -> October 5th 9:32a ET. The engine also selected, per name, up to eight options in each of the two selects (the
  select-0 / select-1 shots).
- Captures: `017-BA-US-Model.png`, `018-BA-US-Model-expanded.png`, `019`..`034` (BA, 16), `045`..`062` (AMD, 18), `077`..`094` (ASML, 18).
  54 captures.

## FWD-10 -- "EXERCISED -- a check has actually refused something and the refusal was seen on the page" (PRD :560)
ACCEPT: "A figure that failed or skipped its check looks different from one that passed, and the analyst can tell which. A failure
shows as a marked value -- never as a blank, a zero, or a row that quietly disappeared."
- Saw: the Model tab carried 0 refused rows on all three names (`[data-model-refused]` 0; no "REFUSED" word), so the model-line
  refusal arm was NOT exercised on these names. Refusals seen on the page elsewhere: BA Posture, expanded, shows warning-marked
  lines "Citation not resolved -- a filing passage the research pack cites, which no drafted sentence on this name's thesis
  quotes, so this page does not carry its text" (four on BA's Posture reasons 3, 5 and 6) and the footer "17 of the 21 citations can be
  shown on this page; 21 of 21 were checked against their filings"; BA and ASML Thesis show the driver-chart point links answering
  "The filing passage for this point is not shown on this page." (row `Z-W235-S3`); AMD Exec Management says why it is empty.
  Positive control: the passing lines (served citations with a filing locator) sit in the same shots.
- Captures: `036-BA-US-Posture-expanded.png`, `096-ASML-NA-Posture-expanded.png`, `006`..`013` (BA Thesis), `066`..`073` (ASML Thesis),
  `063-AMD-US-Posture.png`. 19 captures.

## FWD-15 -- "EXERCISED -- a PM has actually opened the page, read the ranked list, and clicked through to a name it surfaced" (PRD :614)
ACCEPT: "Adam or Lauren opens the page cold, sees a short ranked list of names that are moving in price or spiking in discussion,
and follows one into its full page."
- Saw: the page opens on "What is moving" with Chatter / Price faces; Price shows GAINERS (Advanced Micro Devices +38.7%, SYNOPSYS
  +17.8%, CADENCE +14.6%, ASML Holding +14.3% ...) and LOSERS (Netflix -18.9% ...), "Show all 94 names", "Ranked from Bloomberg prices
  (94 names); requested for October 5th, 2026. This list is from October 2nd, 2026, the newest available." A click on the ranked list's first row (AMD,
  `li[data-price-bar="AMD_US_Equity"]`, `walk_au5.mjs` logged `PICK AMD US ROW-CLICK on the ranked list`) opened the full page
  "Advanced Micro Devices Inc / AMD US", Information Technology -- US, with its header figures. The stock engine's three-name walk
  selected each name by typing its ticker, not by a row click (row `Z-W235-S4`).
- Captures: `20261005T163146Z/shots/001`, `002-lead-Trending-Chatter.png` (57 bubbles), `003-lead-Trending-Price.png` (20 bars);
  `20261005T165304Z/shots/004-ranked-list-before-click-AMD-US.png`, `005-AMD-US-overlay.png` (after the click). 5 captures.

## FWD-17 -- "EXERCISED -- an analyst has used the profile to answer a question about a management team" (PRD :636)
ACCEPT: "One tab lists the company's senior executives, each with their role, a profile link and how long they have held the role,
and states how the team's average tenure compares with the average across every company the page covers."
- Saw: BA Exec Management lists 12 officers with role, role start, tenure (years), a Profile button on 4 of 12, "confirmed from the
  filing", and "Average tenure: this name 2.58 years over 12 of 12 officer(s) carry a role start; the pool 4.09 years over 40
  officer(s) at 7 company(ies)." CEO public profile reads "no public profile is on file yet." ASML: 7 officers from the Bloomberg
  fallback with role start and tenure "not stated", pool line "not stated"; the tab says the filing roster did not resolve. AMD: no
  officer list, with its reasons in words. Served roster == page roster for all three (BA 12 of 12, ASML 7 of 7, AMD 0 of 0; read
  from the deployed thesis route).
- Captures: `014-BA-US-Exec-Management.png`, `041`/`042` (AMD), `074-ASML-NA-Exec-Management.png`. 4 captures.

## FWD-18 -- "EXERCISED -- an analyst has clicked a filing-derived figure through to the passage it came from" (PRD :651)
ACCEPT: "The Thesis tab says, in the company's own words and with each sentence linked to the passage in the filing it came from..."
- Saw: BA Thesis, "Read more" on RISKS opens a dialog "Risks -- What each line rests on": each MACHINE-marked sentence is followed by the
  filing text and its cite ("BA US'S 10-K, FILED JANUARY 30TH, 2026 -- ITEM 1A. RISK FACTORS > PARAGRAPH 8"). That click-through worked.
  The three driver-chart point links on BA ("2023: 528 -- SHOW THE FILING PASSAGE", 2024, 2025) and the three on ASML each answered "The
  filing passage for this point is not shown on this page." (0 of 6 showed a passage; row `Z-W235-S3`). ASML Thesis shows the team's
  pillars with "Source: ASML research pack 5_5_2026"; its INVESTMENT THESIS and RISKS cards read "is not in this pack yet". AMD Thesis:
  "no research pack for this security" and "No drafted prose for this name yet."
- Captures: `008`..`013` (BA), `068`..`073` (ASML), `039`/`040` (AMD), `011` carries the passage dialog. 16 captures.

## FWD-19 -- "EXERCISED -- a PM has read a posture and acted on it, or declined it, on the page" (PRD :664)
ACCEPT: "The last tab, and a line in the header, say whether this company looks like a better or a worse pick than the most similar
name on the other side ... marked as a machine's view for a person to accept or reject; it is never an instruction."
- Saw: BA Posture: header line "Posture (as of September 15th, 2026): HOLD -- neither BA US nor Deere & Company looks clearly the better
  pick on this evidence -- a machine's view for a person to accept or reject, never an instruction"; the tab lists 6 numbered REASONs
  with CITES (21 cites read), the comparable named (Deere & Company). AMD: "No call on this name yet as of October 5th, 2026 ...
  no posture has been drafted for this name yet; the research team adds one" (status ABSENT, with its reason). ASML: verdict `absent`
  with the comparable-null reason in the data attribute. I saw NO control to accept or decline a posture on the page (nothing was
  acted on); the page says the person does that.
- Captures: `035`, `036` (BA), `063` (AMD), `095`, `096` (ASML). 5 captures.

## FWD-31 -- Exec Management team passage beside the roster (PRD :844-854)
DONE WHEN (quoted): "for a name whose pack carries a MANAGEMENT passage, the Exec Management tab renders that passage LABELLED AS THE
TEAM'S and cited to its report, positioned BESIDE the filing roster rather than in place of it; the roster's own rows are
BYTE-UNCHANGED against the same tab captured without the passage; and a name whose pack carries none renders the roster alone
with the passage slot ABSENT WITH ITS REASON. The rendered state carries a POSITIVE CONTROL in the same capture -- the location is
the application route and the tab's own label is present -- so a zero on the absence clauses cannot be a blind read".
- PASSAGE arm, ASML: heading "THE RESEARCH TEAM ON MANAGEMENT", the passage text, "Source: ASML research pack 5_5_2026"; data:
  `data-dossier-management="SERVED"`, report key `.../ASML research pack 5_5_2026.pdf`, locator 3. It sits above the roster table in
  the same panel (passage box y=635, 256 high; table below it); the roster's 7 rows follow. NOTE: ASML's roster is the Bloomberg
  fallback ("the filing roster did not resolve"), not a filing roster.
- ABSENT-with-reason arm, BA and AMD: "The research team on management: no management section, because neither a research pack nor an
  earnings update is on file for this name." (`data-dossier-management="ABSENT"`, reason "no MANAGEMENT section in class A missing or
  class B missing"); BA's roster of 12 renders alone beneath it; AMD's panel adds "No officer list has been published for this name
  yet:No officer list could be shown..." (the page prints "yet:No" with no space).
- BYTE-UNCHANGED arm: NOT exercised as written. The same tab cannot be captured with and without the passage for one name from the UI.
  Substitute read (not the clause): the page roster rows equal the deployed served `management.officers` (BA 12 of 12, ASML 7 of 7
  names found in page rows), and the passage is a separate served key (`dossier_fields.management`). Row `Z-W235-S4`.
- Positive control: every capture shows the location `/security-analysis` and the tab label EXEC MANAGEMENT.
- Captures: `014` (BA), `041`, `042` (AMD), `074` (ASML) + `au5-reads.json` rows. 4 captures.

## FWD-5 (v0.38, PRD :515-519) -- the print on demand, three names
DONE WHEN (quoted): "(v0.38) a seat prints the pack on demand for three covered names, and each reads as a document: Opal Brand form,
every figure traceable to its page field, no raw code, no dashboard chrome (a JUDGMENT read at L9). Adam's actual forward stays the ACCEPT".
- Files: `print/BA_US_Equity.pdf` (21 pages, 178,896 bytes), `print/AMD_US_Equity.pdf` (23 pages, 191,098), `print/ASML_NA_Equity.pdf` (24 pages,
  195,657), each from `GET /api/scoped/amgt/security/<key>/print` (default `format=pdf`) on the deployed function, and byte-identical
  to the file the page's Print button obtained (sha256 equal for all three).
- What I saw (no verdict): page 1 of each begins "BOEING CO/THE [BA US Equity] Research Note / MODEL BLOCK (from the landed record,
  provenance per the figure rule) / Header" followed by lines such as `BOEING CO/THE TEXT (string field) - NAME (Bloomberg-maintained
  legal/short name of the issuer.) - as of 20` and `193.56 PRICE (local trading currency, per share/unit) - PX_LAST (Last ...`,
  monospace, clipped at the right page edge, and a Python list repr (`[{'announcement_date': '2026-07-28', ...`). Raw field codes: 109
  (BA), 108 (AMD), 107 (ASML) distinct UPPER_CASE_WITH_UNDERSCORE tokens across the pages (e.g. CNTRY_OF_DOMICILE, GICS_SECTOR_NAME,
  PX_LAST). Row `Z-W235-S2`. Judgment criterion: graded at L9, not here.

## FWD-8 (v0.38, PRD :540-543) -- the identity read
`fwd8_identity.py` reads, on the deployed function, for each of the covered names (`covered_security_keys()`, fresh from S3), the
page's subject (overlay: `security_key`, `identity.security_key`, `display_name`) against the comparison block's subject (peers route and
the overlay's own `peers` copy: `security_key`, `identity.security_key`, `subject.security_key`, `subject.display_name`), counts an absent
arm RIGHT only when it carries words, and prints `FWD8 WRONG n of N`.
- Run (stdout, exit 0): `FWD8 population: 95 covered names`, `FWD8 peer-block basis absent-with-words: 38 of 95 (the rest derived/analyst)`,
  `FWD8 WRONG 0 of 95`.
- Negative control (`fwd8_control.out`): the same check on BA with the peers answer's subject swapped to AMD's key and name reads
  `WRONG` with both mismatches named; unplanted BA reads `RIGHT`.
