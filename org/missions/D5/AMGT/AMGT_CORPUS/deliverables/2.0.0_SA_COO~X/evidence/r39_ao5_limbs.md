# AMGT_CORPUS round 39 CRPS-ao-5 -- the six FWD limbs (2.0.0_SA_COO~X, 2026-10-06 ~21:0xZ)

Each limb the CVO named in `ADJUDICATION_v44.md` is driven, read, or shown to have no control. Source read on the candidate portal
tree (`wk-AMGT_CORPUS-2-portal`, paths under `portal/src/pages/SecurityAnalysis/`); served reads on CLOUD `85547630d1`.

| FWD | limb | result | evidence |
|---|---|---|---|
| 10 | a pillar "openable to the report and the passage it came from" | **NO CONTROL EXISTS.** A pillar is a plain `<li data-dossier-pillar>` carrying `data-dossier-report-key` and `data-dossier-locator` as attributes only; its visible text is the pillar, `Terms: ...` and `Source: <file name>`. No button, link or handler. The three `[data-thesis-card]` buttons open the machine draft's filing passages, not the team's pillars. | `tabs/ThesisTab.tsx:154-168`; `components/ThesisCards.tsx:465-471` |
| 11 | "a name whose pack carries none reads ABSENT with its reason"; roster unchanged | **A WALK IS OWED** (one name). 48 of 95 served dossiers carry no management passage (47 cited, 1 name has no dossier, 96 registered); e.g. `1299_HK_Equity`, reason as served: "no MANAGEMENT section in class A missing or class B missing". The absent branch renders `<p data-dossier-management data-dossier-reason>`. The roster count is `tr[data-exec-officer]` (ASML read 7 at round 38). | `tabs/ExecManagementTab.tsx:382-399`, `:128`, `:284`; served read over `_read_dossier_document`, this file's date |
| 12 | the rows are the SharePoint model template's, in its order and labels | **NOT COMPARABLE IN THE REPOSITORY.** The page's rows are constants (`FINANCIAL_SUMMARY_ROWS`, `MARGIN_HISTORY_ROWS`, `V3_LINE_ROWS`); the template itself is not in the repo (0 matches for the template in `lib/research` or `modelSheet.ts`; a workbook name appears only in a comment). The comparison needs the team's workbook as its comparand. | `modelSheet.ts:6-10`, `:96-169` |
| 15 | "both render cited on the header posture line and the Posture tab" | **NO CONTROL EXISTS on the header.** The header lines (`PostureHeaderLine`, `DossierPositionLine`, inside the closed "Posture, research dossier and readings" details) print "Fund of record: ...; last stated position: ..." with no citation element. The Posture tab does cite (`data-dossier-report-key` + "Source: ...", `li[data-posture-cite]`). | `components/SecurityOverlay.tsx:194-283`, `:475-479`; `tabs/PostureTab.tsx:318`, `:619-627` |
| 16 | "the docx path ... still recovers what it recovered before" | **READ: UNCHANGED on the cases.** `dossier.py --case-census` (read-only, rc 0): 95 names, 285 slots, body 102, absent 183, ordering violated 0 -- identical line for line to the 2026-09-29 read (`r12_after_case_census.txt` @`4f52b3f69d`): 0 of 95 names changed, 0 lost a recovered case. Limit: the census covers the three cases, not the pillars or the management passage. | `r39_ao5_case_census_20261006.txt` beside this file |
| 18 | "the feed filters to them for at least one name" | **NO CONTROL EXISTS.** Pillar terms are a plain `<p>` ("Terms: a, b"); word-cloud terms are `<span data-term>` with no handler; the feed (`[data-header-feed]`) has no filter input or state. | `tabs/ThesisTab.tsx:163-165`; `components/TimelineWordCloud.tsx:94-102`; `components/HeaderBrief.tsx:106-151` |

Instrument note: on `/security-analysis` the walker ignores `--press` and `--hover` (they run only on a plain route,
`walk.mjs:1617-1643`); it opens every closed `<details>` per tab and `--deep` presses up to 10 buttons per tab. So a walk can
show a rendered state, never prove a control that is not there; the three NO CONTROL results rest on the source read.

Found beside the limbs (for the CVO, not this cell's): two cited management values read "Management/Board 80" (`8306_JP_Equity`,
`8316_JP_Equity`), which looks like a heading and a score, not a passage. And the served absent reason "no MANAGEMENT section in
class A missing or class B missing" is not a PM's words.
