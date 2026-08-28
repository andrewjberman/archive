# TO D4_ETFPOS.TO-D4b — DIVZ+IDVZ holdings: PROVENANCE FIRST, then the delivery path (LAPTOP; UNGATED)

<task_order id="D4_ETFPOS.TO-D4b" project="ETFS_POSITIONING">
<issued_to>0.4.0_DS_ClientPlatform</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-19T19:55Z</issued>
<dated>startable NOW -- gates on nothing, independent of D1</dated>
<status>complete -- **MARKED 2026-08-28 ~18:5xZ by `2.0.0_SA_COO~Z` (issuer)** on Andrew-direct *"we need to either mark this completed or superseded depending on validity"*, against `1.0.0_SA_CTO~Z`'s verification. **COMPLETE, not superseded: this TO's OWN execution produced the result** -- it has a delivery commit `@afd2d831fe` AND the ONLY proof-of-spec instance in the whole `D4_ETFPOS` series (census: 55 hits over 27,852 files scanned, exactly one instance). ⭐ **ITS ONE FAILING CRITERION NOW PASSES, RE-MEASURED ON ITS OWN METHOD:** `D4b-4` demanded *"4/4 universe tickers present in silver/holdings for 3 consecutive days, denominators printed on both sides"* and measured **2 of 4** at filing (DIVZ+IDVZ absent). Re-measured at `s3://opal-data-etfs/silver/holdings/`: **2026-08-25 / -26 / -27, 187 rows each, 4 of 4 tickers [DIVZ, IDVZ, PFDE, PFOE], 3 of 3 consecutive days.** The gap it measured is the gap `TO-D4c` Phase A closed -- the remedy is named in live code at `etfs-netassets-daily/lambda_function.py` with Andrew's 2026-08-21T20:45Z egress grant quoted verbatim. ⚠ **COLUMN TRAP for the next reader: `fund_key` is LOWERCASE, `fund_ticker` is UPPER -- a ticker compare against `fund_key` returns a clean, confident 0 of 4.** ~~pending -- Terminal status left to COO~~</status>
<priority>P2 -- but the FIRST ACT is cheap and may DISSOLVE a sovereign ask, so it is worth doing early</priority>
<authority>D4_ETF_POSITIONING_VARIANT_PRD.md §4.1 + §6 item 2 at dispatch vintage @2ecc24d0c8, with Phase 1 REORDERED per CVO P1-2 @12f90b44d6. Placement: LAPTOP (CTO placement ruling FINAL 193804Z).</authority>
</task_order>

## DO NOT START WITH A SOURCE HUNT. START WITH PROVENANCE.
CVO measured that **the estate ALREADY HOLDS DIVZ+IDVZ holdings in the parquet's own shape**:
`research_transcripts/analysis/source_divz_holdings_20260731.csv` (2,790 B) and
`source_idvz_holdings_20260731.csv` (4,010 B) — header
`Date,Account,Stock Ticker,CUSIP,Security Name,Shares,Price,Market Value,Weightings,Net Assets`,
**the same eight fields as R7's schema, content-matched.**

**FIRST ACT = WHERE DID THESE COME FROM.** Provenance, not filepoint tracing.

**WHY THE ORDER IS THE POINT:** if the provenance turns out to be an existing entitlement, **the Q1
vendor-egress ask to Andrew is UNNECESSARY — and an unnecessary sovereign ask is not free.** The
egress word goes to Andrew **ONLY** if provenance shows a genuinely NEW vendor/feed is required.
Do not send that ask before this read.

⛔ **NO VENDOR EGRESS in the meantime.** Availability in the toolset is not authorization, and
neither is a plausible-looking need.

## SECOND ACT — the delivery-path half
Trace `etf_netassets_watch` (`comp-find` + `comp-pipescript io <script> --pipeline <tree>`, flag
REQUIRED).

## CROSS-PRD REPORTING RULE — THIS IS NOT A D4-LOCAL FINDING
**The provenance finding reports to BOTH D4 AND D5.** The same two CSVs are D5's materiality/weight
basis and are **currently UNOWNED** — two PRDs, one source, and until tonight neither knew the other
depended on it. **Whichever program lands the standing DIVZ/IDVZ feed DECLARES ITSELF THE OWNER and
the other CONSUMES — one source for one fact, never two homes.** State the ownership outcome
explicitly; leaving it implicit is how the second home gets built.

## Acceptance criteria
- **D4b-1 PROVENANCE ANSWERED** for both CSVs — where they came from, with evidence, and whether an
  existing entitlement covers a standing feed.
- **D4b-2 THE Q1 EGRESS QUESTION IS RESOLVED OR ESCALATED ON THAT BASIS** — resolved (no ask needed)
  or escalated with the specific new vendor/feed named. Not left open.
- **D4b-3 OWNERSHIP DECLARED** per the cross-PRD rule, reported to both D4 and D5 threads.
- **D4b-4 COVERAGE:** 4/4 universe tickers present in `silver/holdings` for 3 consecutive days,
  **denominators printed on both sides**.
- **D4b-5 proof instance VALID rc=0 positional: ids D4b-1..D4b-5.** MEASURED/RULED rows only.

<proof_of_spec>
  <expected_criteria>D4b-1,D4b-2,D4b-3,D4b-4,D4b-5</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/D4_ETFPOS.TO-D4b_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

## Reporting
COO at provenance-answered (fast — it gates a sovereign ask), cc CRO (D5's owner) and CTO.
Session log w/ Compiler Tools section = deliverable.
