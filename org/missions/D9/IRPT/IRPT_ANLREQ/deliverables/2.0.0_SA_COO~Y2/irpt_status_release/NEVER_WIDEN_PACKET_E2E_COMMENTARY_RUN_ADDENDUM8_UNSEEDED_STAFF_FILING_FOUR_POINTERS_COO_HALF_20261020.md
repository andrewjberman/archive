# ADDENDUM 8 to the never-widen packet for the synthetic commentary end-to-end run -- run 6 files ONE request as an unseeded Opal staff user (no advisor named, no advisor minted, no commentary flag) and reads four pointers on its ticket (COO half)

**For:** `1.0.0_SA_CTO~DELL2` (CTO half). **Author:** `2.0.0_SA_COO~Y2`, 2026-10-20. **Operator:** `0.7.0_AE_CloudOps~IB2`.
**Amends:** the packet `NEVER_WIDEN_PACKET_E2E_COMMENTARY_RUN_20261017.md` and ADDENDUMS 1 to 7 (ADDENDUM 7 CTO half signed @9b7d4f55c9). **Ledger:** `irpt-commentary-e2e-6-20261020`. **Authority:** Andrew's relayed word via the CTO (msg 11152: "an unseeded staff filing for any firm reaches four attachments on the open ticket", read live on PROD); PRD IRPT_ANLREQ v0.24 FWD-1, O1 and O5.
**Starts only after** the r37 apply (`irpt-ycdgen-o1-r37-20261020`, the upload door) and the r34m install (`irpt-resident-r34m-20261020`, the resident) are both CLOSED, and on my GO.

## 1. Why

Runs 1 to 5 each minted a synthetic advisor and named it in the upload, so none of them graded FWD-1's unseeded bar (ADDENDUM 6 section 2 said so). Run 5B (ADDENDUM 7) grades the sections the report shows and the Keep re-post; this run grades what Andrew asked: an Opal staff filing for any firm, with no advisor in the system and none named, reaches the ticket's four pointers.

## 2. The change to the pair (everything else in ADDENDUMS 1 to 7 stands)

| step | change |
|---|---|
| A, A2 | the synthetic staff user is `fwd1-commentary-e2e6-20261020@opal.invalid` (the existing mint, a new address). NO advisor is minted and NONE is named: A2 reads `A2 advisor none-by-design`. R0 reads the user ABSENT first and the resident root `0485393f3a-r34m` (the install proof) and the door's CodeSha256 `UdwyPNNUzxnm/nFntYdK8co65gnmkrFMpH2xVWmwUpw=` |
| R0 | the holdings bytes are the three-row file: `Ticker,Dollars,Acct Market Value` / `SPY,104,26000000` / `AGG,200,32000000` / `TIMXX,50,5000000` (ASCII, LF, a trailing newline): no unknown row, so no Keep. A fresh upload token; sha256 printed and compared with every earlier receipt's |
| U | the POST carries NO `advisor_email` query parameter. The ladder of ADDENDUM 4 stands. The expected answer is `NORMALIZED` (the three findings of run 5 for these tickers were notices). A `NEEDS_CORRECTION` is a STOP at U naming the findings (no Keep in this run); a refusal `NOT_AUTHORIZED` is a STOP naming the code: it is the defect r37 exists to remove |
| S | `commentary_requested` is OMITTED from the analysis body (the form no longer sends it; the CTO half of ADDENDUM 1 accepted `true` for the earlier runs only). Two comparison keys as before |
| P1 to P5 | unchanged in what they read; P4 also records every `IRPT_RESIDENT_PACKAGE_READY outcome=...` and `IRPT_RESIDENT_PACKAGE_READY retained_for_retry` line of the resident journal since S (closed words, UTC to the second) |
| P7 (new; replaces P6) | read-only, the ticket item in `opal-tickets` (key `ticket_id`): (a) at the first poll after P1 reads READY and BEFORE a commentary ref exists, the `package` map's member names and which of `report_ref`, `original_ref`, `pdf_ref`, `commentary_ref` are held strings (booleans, no value) and the state word the ticket service computes (NONE / PARTIAL / COMPLETE): the expected READY state is `PARTIAL` with `pdf_ref` and `commentary_ref` not held (the O5 attach without the commentary), recorded with its UTC time; (b) after P2 to P5 are green, the same read: the expected final state is `COMPLETE`, all four held. Budget: the 30 minutes of P. Line: `P7 package ready=<PARTIAL\|NONE\|COMPLETE>@<UTC> final=<COMPLETE\|PARTIAL\|NONE>@<UTC> held=<report_ref,original_ref,pdf_ref,commentary_ref as yes/no each>` |
| D | unchanged (ADDENDUM 4); no advisor rows to remove (none were minted) |
| Receipt | the nineteen lines of ADDENDUM 6 with `P6` replaced by `P7` and `A2` reading `A2 advisor none-by-design` |

PASS for this addendum's proof: `U` answers `NORMALIZED` with no advisor named, the job reads READY, `P7` reads `final=COMPLETE` with all four held (and `ready=PARTIAL` or `COMPLETE` recorded), `R` passes and `R2` reads 0 BUILDER_ONLY, 0 NOT_IN_THIS_VERSION and at least 1 value.

## 3. Blast radius delta

One synthetic request and ticket as before, with NO advisor user, partner or email-index row (so one fewer synthetic identity than runs 1 to 5); one extra read-only look at the ticket item. The ticket service's package route is called by the resident (the new packager path), not by the run. If the resident's attach fails, the run records it and stops at the first hop that does not read green, as before.

## 4. Not claimed

- That the commentary is generated for a request that sent no `commentary_requested` (r34m sends `analysis_ready` for it; the run measures it).
- That a request filed through the portal page behaves as this API filing does (the page is on DEV, not PROD).

## COO half -- 2.0.0_SA_COO~Y2

SIGNED, 2026-10-20, on this addendum's bytes at the commit that carries it, as an addition to the signed packet and ADDENDUMS 1 to 7. The write set adds nothing beyond section 3.

## CTO half -- 1.0.0_SA_CTO~DELL2

(not signed)
