# AMGT_CORPUS round 45 -- CRPS-au-7: the IMB LN Thesis-tab walk (FWD-10's missing read)

**Issuer:** `2.0.0_SA_COO~C1` (dell1), 2026-10-11 12:12Z-12:14Z. **Instrument:** `/ui-walk` (`.claude/skills/ui-walk/walk.mjs`), signed in as the
dormant walker account on the local `dev:live` build, `--route /security-analysis --security "IMB LN" --security-press
"details[data-pillar-open] summary"`. A walk is a development instrument and grades nothing; the CVO grades FWD-10 on this read.
Screenshots and `findings.json` stay local under `tmp/ui-walk/20261011T121206Z/` (gitignored; client data and page content are never
committed or pasted), so this record states what was read in words.

**The account.** Armed 12:12:07Z (`HOLDER DESKTOP-HK1UU7N:16068:dbf1ec13`), disarmed 12:14:00Z: the row reads `status=disabled`, and a login
with the walk password after the disarm printed `HTTP 401 ... REFUSED`. `ui_walker_account.py status` read afterwards: `status=disabled armed=no armedBy=none`.
dell1's right to arm was read first: `simulate-principal-policy` for `cloudops-dell1-agent-user` on `dynamodb:UpdateItem`, `dynamodb:PutItem`,
`ssm:PutParameter`, `ssm:GetParameter` read `allowed` on all four.

**The build under the walk.** Port 5174 was already served by another seat's `scripts/dev-live.mjs --port 5174` (pid 28592, started
08:03 local); this seat did not start it. It serves a `modelSheet.ts` carrying `teamSheet` and a `ThesisTab.tsx` carrying
`data-pillar-open`, and the shared portal working copy is `DEV` `8ed372cb` (equal to `origin/DEV` at the walk). The exact bundle's commit
is not read from the running process; the two feature markers are.

## What was read on IMB LN's Thesis tab (screenshots 005 and 007)

| DONE WHEN clause (PRD:326-329) | read |
|---|---|
| the pack's pillars render as a bold lead plus a paragraph | 6 pillars under "The research team's thesis pillars", each a lead line then its paragraph (Cash-return machine; Buyback compounding on a shrinking share count; Pricing power reliably outruns volume decline; Deliberately capital-light "fast follower" NGP strategy; Clean balance sheet for a Tobacco company; Litigation overhang resolved). Whether the lead is BOLD is not read from a screenshot; the component's `ap2` harness is the instrument for that. |
| each is openable to the report and the passage it came from | 6 of 6 pillars carry a "Where this comes from" opener |
| one pillar opened to its passage (the cut's own bar) | the walker's press opened the first: it names the report (Imperial Brands Research Pack 2026 07 17_v1), the locator (Paragraph 11) and the passage text, which equals the pillar's own sentence |
| each marked as the team's rather than generated | the section is headed "The research team's thesis pillars"; the opened pillar reads "The research team's own pillar, from the report ..." and every pillar carries a "Source: Imperial Brands Research Pack 2026 07 17_v1" line |

Five of the six openers were NOT pressed; the clause "each openable" is read from their presence, not from five more presses.

## Also read on the same walk (not FWD-10, recorded because it bears on row D1-S3)

IMB LN is `own_new` with 138 team-sheet rows (workbook `Imperial Brands FactSet Based ONE PAGER 2026 07 17_v1.xlsx`, sheet
`Model NEW VERSION`). The walker's `raw-code` check read the Model tab's text, including the collapsed "All figures" fold, and flagged
exactly the labels the sheet-builder read named: `Ticker:`, `FG_COMPANY_NAME`, `FG_FACTSET_SECTOR`, `Location:`, `Currency:`,
`FF_FISCAL_DATE`, `Financial Summary`, `Tobocco Volume`. So the HEADING and CONTROL rows the CTO's ADDENDUM 1 (@161ccad473) classifies
reach the real page DOM on a live name; the round-46 reader cell is what removes them. That is a corroboration of D1-S3 in a browser, not a new row.

Other walker findings, none FWD-10: control not found `Earlier month`; 4 truncated labels; no timeline day bar and no timeline event
element on IMB LN; two date formats (2026-09-22 and September 22nd, 2026); 57 text elements clipped sideways on the Model tab. Zero guard
aborts, 0 API issues, 12 console errors (not read here).
