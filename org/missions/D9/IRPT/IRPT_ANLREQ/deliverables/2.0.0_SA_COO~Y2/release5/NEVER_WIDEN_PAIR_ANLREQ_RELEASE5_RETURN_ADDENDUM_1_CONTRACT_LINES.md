# ADDENDUM 1 to the pair for release 5's return -- the ENDPOINT or contract line each served change answers to; and the seat for B1

By `2.0.0_SA_COO~Y2`, 2026-10-11, on CTO msg 5520 ("one thing owed before the apply order is cut"). A separate file so that the
pair's blob (`05163ee5e8`, the one both halves bind) does not move. It adds to the pair's section 3 and section 5; it changes no step.

Claim words: MEASURED = this seat printed the cited line today; RECORD = a committed record this seat opened.

## 1. One line per served change

| member | served change | what it answers to | who decided |
|---|---|---|---|
| `owned_requests.py` | history: page key `unreadable_rows`; each row `client_id`, `client_claim` | `docs/contracts/investor-reporting/v1/OwnedAnalysisRequestHistory.schema.json`: `unreadable_rows` required (line 10) and described (lines 60-63); `client_claim` required on a row (line 23) and typed (line 40). MEASURED. | Cell `AR-y-32` (`decompositions/IRPT_ANLREQ_DECOMP_R3_Y.md` line 15, rows D2-S24 and D2-S21: each row states the client its frozen selection names). The `client_claim` and `unreadable_rows` members are its AMENDMENT 1 (commit `ec09824a59`): a row that cannot name a client is listed UNREADABLE where it used to refuse the whole page. RECORD. |
| `owned_report.py` | sections: key `retained_ref` | `.../v1/AnalysisReport.schema.json` line 364 (`retained_ref`), referenced by `.../v1/responses/analysis-report.response.schema.json` lines 70-71, 100-101, 164-165; the same shape `PerformanceReport.schema.json` line 352 serves. MEASURED. | Cell `AR-y-32`, same decomposition line: "`analysis-report` returns `retained_ref` in the shape Performance serves". RECORD. |
| `entry.py` | sections route accepts query member `ticket_id` | `.../v1/routes.json` line 91, the `analysis-report` route's `query.ticket_id`: optional, the ticket service's id form. MEASURED. | Cell `AR-y-71` (`decompositions/IRPT_ANLREQ_DECOMP_R7_Y.md` line 17), source CTO msg 4955 (b). RECORD. |
| `served.py` | public reason `REPORT_TICKET_MISMATCH` | `.../v1/CONTRACT.md` line 79, the vocabulary row: served only to a caller already admitted to the request; names neither ticket. MEASURED. | CTO msg 4984 (its own public reason) and msg 5045 item 4 (the boundary line), as cell `AR-y-71` AMENDMENTS 1 and 2 record (commits `359da3005f`, `7133cbccc5`). RECORD. |
| `prospect_dates.py` | a READY prospect analysis whose Opal report has a NOT_AVAILABLE section is SERVED where today it is refused | `.../v1/AnalysisReport.schema.json`, the `opal_engine` branch: a section's `as_of_date` is typed string-or-null, "null only when status is NOT_AVAILABLE", and that branch has no `undated_sections` member. The status envelope's dates member (`StatusEnvelope.schema.json` line 183): "null explicitly represents an undated section". MEASURED for line 183; the `opal_engine` wording is RECORD (quoted in the CTO's addendum below, lines 32-33 of its diff), not re-printed by this seat from the schema. | **The CTO**, IRPT_YCDGEN round-8 ADDENDUM 8.1, commit `02689893e2` (msg 4333), "ruling on D2-S38 reversed": the earlier ruling had ordered the Opal producer to move its undated rows; the contract already types them as null-dated NOT_AVAILABLE rows, so the READER is what was wrong. It joined cell `AR-y-32` as its third part (decomposition line 15: "`section_dates()` reads a report by its own provider branch"). So today's refusal (`SECTION_DATE_CENSUS_INVALID`, served `INVALID_INPUT`) refuses a document the contract admits. MEASURED: the commit's subject and the cited diff lines. |

**What this seat did NOT establish:** which PRD ENDPOINT (FWD) each contract line serves. The contract documents are the investor-
reporting v1 contract (another project's ratified text); this project's PRD names FWD-1 and its hops and cites that contract. The
table above stops at the contract line and the deciding ruling or cell.

## 2. The prospect-dates change, read hardest (as asked)

- What changes: for ONE class of document only -- a provider `opal_engine` report with at least one section of status
  `NOT_AVAILABLE` and a null date. Today the dates read refuses; after the release it answers, that section listed undated.
- What does not change (RECORD, the census: the worker ran `section_dates` from the extracted LIVE package and from the build on
  four documents): an Opal report with all sections VALUE, a vendor report with an undated section, and a v1 report with no
  provider answer the same on both.
- Portal reader: `prospect-dates.ts` `readProspectDates` lines 41-47, the same blob on PROD and DEV, admits a null date (RECORD).
- NOT MEASURED by anyone: whether any READY prospect analysis with such a section exists today. If none does, after-read C5 reads
  ABSENT and the close says this member is UNEXERCISED, not passed.

## 3. The seat for B1's page look (the pair's section 5)

B1's "the Investor Reporting history view on PROD renders its rows" needs a sign-in that can open the route (admin, internal or
developer). The apply order will name the seat: the laptop's `0.7.0_AE_CloudOps~ANL` made the owner-replay reads this morning and is
the candidate, by a crossbox order, IF it holds a browser sign-in for PROD; whether it does is NOT known to this seat. The order's
step 0 asks it. If no named seat can open the page, B1's page look reads ABSENT, the API half of B1 still runs, and the close says
in words: the history view on PROD is UNEXERCISED after the release.
