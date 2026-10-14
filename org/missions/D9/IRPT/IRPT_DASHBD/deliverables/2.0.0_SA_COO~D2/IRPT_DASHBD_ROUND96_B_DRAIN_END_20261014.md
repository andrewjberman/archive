# IRPT_DASHBD round 96, workstream B -- drain-end (issuer 2.0.0_SA_COO~D2, 2026-10-14 ~01:0xZ)

**Two cells, both LOCAL:** `DB-b-181` (~147, the classifier rule and the count; drained @66e73a39e5) and `DB-b-180` (~146, the local render of the real sample, re-seated after the round-97 shape fix; drained @89f747e70f). Both orders `complete`; round-close `verdict=MAY-CLOSE` (`round-close-check --project IRPT_DASHBD --round 96`: orders=2, judgment=0). No served byte moved, no deploy, no push; counts and hashes only in the repo, no client data.

## DB-b-181 (FDRXX to CASH, cell A) -- see the pair

The rule (a canonical row typed Cash by `sub_asset_class` takes the cash class; no ticker list) is committed at `e340e07f4e`, 37 tests pass across the four classifier test files, a mutant fails. The count (365 Cash-typed canonical rows, 348 already cash, 17 move, FDRXX among them; at least 20 served positions move) and the consumers are in the never-widen packet `NEVER_WIDEN_PACKET_FDRXX_CASH_CLASSIFIER.md` (sha256 `cfc1dd8d...`), SIGNED on both halves (CTO half @d3b576bb67). The apply is round 98's `DB-b-183`.

## DB-b-180 (the real 49 Financial sample rendered)

`DB96-1-AC1` PASS, re-run by this seat after the drain. The outputs are in the private folder `C:/dev/_irpt_private_evidence_20261009/fwd21_sample/` and nowhere in the repo: the tab HTML, the export HTML and the export PDF. This seat read them:

- **PDF:** 18 page objects (this seat's own count of `/Type /Page`), 255,131 bytes; the export document numbers 12 sheets, so 6 sheets break across two pages (worker row W146-S4).
- **Export HTML, opened in a browser:** the eight sections in the baseline's order (Cover, Portfolio Overview, Summary of Portfolio Accounts, Holdings Overview, Taxable Realized Gain/Loss Summary Year To Date, Account Overview, Gain/Loss Review by Account Last 12 Months, Disclosure page); no horizontal overflow; the cover and the Summary page read in full.
- **What is filled and what is absent:** 44 of 117 members filled, 73 absent, each absent cell saying why in words ("Not available yet: ..."), none blank or zero. Ending values per account and household are filled; beginning value, contributions, withdrawals, net gain and income read absent for the 12-month window because gold `account_activity_daily` holds four trading days (the activity-history backfill is IRPT_BCKEND's, queued).
- **Display defects for Andrew's read, not fixed here:** (1) the absent reason is printed in full in every cell, so tables run long and narrow (the household row repeats it five times); (2) the page footer reads "As of Not available yet: ..." because the as-of date is absent; (3) the four chart slots print their absent words and draw nothing (worker row W146-S5); (4) the cover's household name and account list are absent by contract (no name source). The PDF pages were not rasterised (no rasteriser on this box), so a clipping verdict on the PDF is NOT ESTABLISHED; the HTML at sheet width shows none.

## Open

- Andrew's read of the sample; the served FilledReport (platinum object and route) waits on it (CTO msg 7349). Nothing here mounts the report.
- Round 98: `DB-b-183` (the apply, AE applier) and `DB-b-184` (the IR holdings class read) issued @5860c35e98. Ledger leg L7 held to the 2026-10-14T11:41Z fire.
- Push state: LOCAL on box/dell2.

-- 2.0.0_SA_COO~D2
