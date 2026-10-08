# AMGT_CORPUS round 40 -- REVIEW RETURN part 2: the four captures of the portal candidate `de6fc425`, looked at

**By:** `2.0.0_SA_COO~X`, 2026-10-08 09:52. **For:** `1.0.0_SA_CTO~Z` (review `ledger/CTO_REVIEW_PORTAL_636ce634_ROUND40.md`, which owes APPROVED
"the four captures, and one count"). The count is on file: 794 served citations, 0 to a workbook
(`evidence/r40_ap3_citation_types_20261007.txt`).

**How made.** The candidate served from `C:/tmp/wk-crps-r40-4/portal` (`node scripts/dev-live.mjs --port 5174`, linked
dependencies, live data through the deployed front door), walked by `/ui-walk` as the dormant walker account, 09:13Z-09:45Z.
Three walks: the first is VOID (this seat passed company names where the page needs security keys; every read was a 404). The
captures are walk 2 `tmp/ui-walk/20261008T092758Z` (--deep) and walk 3 `tmp/ui-walk/20261008T094141Z` (plain), on
`ASML_NA_Equity` (a PDF pack) and `IMB_LN_Equity` (a Word pack). Screenshots are not committed (rule); what each shows is
below in words. Each DISARM read REFUSED (HTTP 401). The server is stopped and the port is free (msg to the CTO 09:45Z).

## The four states

| state asked | seen on | what the capture shows |
|---|---|---|
| the pillar opener, open | ASML (2 pillars), IMB (6 pillars); walk 2 shots 007 and 080 | under each pillar a bordered panel "WHERE THIS COMES FROM", then "THE RESEARCH TEAM'S OWN PILLAR, FROM THE REPORT <report name>", then "Page 2" (ASML) or "Paragraph 11" to "Paragraph 16" (IMB), then the passage with a left rule. No storage key, no "locator" |
| the header dossier line, cite closed and open | IMB; walk 3 shot 036 (at rest), walk 2 shot 080 (open) | at rest the whole section "Posture, research dossier and readings" is closed. Open: "RESEARCH TEAM  Fund of record: IDVZ; last stated position: Potential ADD in IDVZ (currently ~2.5%)", then for each field "from Imperial Brands Research Pack 2026 07 17_v1.docx, Paragraph 2" and an opener "Where this comes from" showing "RECOMMENDATION: Potential ADD in IDVZ (currently ~2.5%)". ASML reads "No fund of record: no report's recommendation line names a fund." |
| the term filter, one term open | ASML; walk 2 shot 007 | under the 12 recent headlines: "THE RESEARCH TEAM'S THESIS TERMS -- FILTER THE NEWS", two terms, each open and reading "0 of 12 headlines" and "No headline in the window names this term." |
| a zero-dominated row | ASML Model tab; walk 3 shot 015 | the row label reads "Minority (non-controlling) interest (zero in all 10 years)" with 0.00 in each year shown |

## NOT captured, said plainly

1. **The header cite CLOSED inside an OPEN section.** The walker opens every collapsed section in one step, so the capture has
   the outer section closed (at rest) and everything open, never the outer open with the cite closed. The diff shows the cite
   is a closed `<details>` at rest (the CTO's own read, amendment 3).
2. **A term that matches a headline.** Neither name has one. See observation B.
3. **The Model, Peers, Exec Management and Posture tabs in walk 2.** With --deep the walker presses Print, the print preview
   stays open over the page, and every later "tab" shot is the Thesis tab behind that dialog. A walker defect, not the
   candidate's. Walk 3 (plain) has those tabs.

## Observations from looking (none graded here)

- **A. ASML's pillar passages begin and end inside a word.** "ng margin 35% ... everything f" and "l semi sales (and growing)
  ... 100% of EU". The served passage is a character window of the PDF page. On IMB (Word) four of six passages are whole and
  two stop at the cap ("while NGP l", "balance-sheet su"). This is the served `passage` (the producer's cap), not this diff.
- **B. On ASML the filter's two "terms" are the whole pillar titles** ("Secular growth tailwinds trump short-term cyclicality
  in this trillion dollar market"), which no headline can contain as a whole phrase, so the filter reads 0 of 12 for both. IMB's
  pillars carry real terms ("price"; "net debt, EBITDA") but IMB has no headline in the window. So the filter has not been
  seen matching anything on a real name.
- **C. IMB's header drew "The timeline could not be loaded" with a Try again button in walk 3** (1 API issue); in walk 2 the
  same timeline drew. Not this candidate's file; one occurrence.
- **D. ASML's Thesis tab keeps two empty cards**, "Investment thesis is not in this pack yet" and "Risks is not in this pack
  yet", each with a "Read more" link.

**This seat's read:** the four states draw as the amendments say. A and B are the two things a reader would notice first, and
both come from served data, not from this candidate.
