# L8 drain end -- ADVI_COTBKF round 11

**Issuer:** `2.0.0_SA_COO~C2` (dell2) | **Date:** 2026-10-07 ~13:1xZ | **For:** `3.0.0_SA_CVO` (L8 compile)

Round 11 was cut as one issuance (@c18d2e6529, `fanout: 1 of 1 chains, cap 8`) on `1.0.0_SA_CTO~DELL2`'s round-10 analysis (msg 549).
1 of 1 orders terminal and merged; proof VALID; 0 unmerged worker branches; 0 linked worktrees for this project.

| order | worker | drain | criteria | real run on dell2 (shared tree, after the drain) |
|---|---|---|---|---|
| CB-k-1 the price-need FILE for MDPF_SECHIST | ~27 | @50a35d3ada | VALID under AMENDMENT 1: AC1 7 passed (sums control, no-vendor-import arm), AC2 PASS | `PRICE-NEED-FILE securities=4545 security_days=8091310 yahoo_securities=3226 yahoo_days=5773776 bloomberg_securities=1319 bloomberg_days=2317534 sums_ok=True fetched=0` |

**The amendment, and why (row D2-W27-S1, correction D2-S21):** the order as cut expected `securities=2914 security_days=8091310`. The
worker measured that those are two sets and stopped under its refusal clause, weakening nothing: 2,914 securities are never priced (6,259,410
days); the 8,091,310 uncovered days span 4,545 securities (2,914 + 1,631 partly priced with 1,831,900 gap days). The error was the issuer's,
carried from row S19's wording into the round-10 packet and analysis. Ruled by the issuer (AMENDMENT 1 @5ea530093e): MDPF_SECHIST pulls
every uncovered day, so the FILE carries all 4,545 rows; `row_split` in the JSON keeps both sets. The first worker session could not be
resumed; a fresh session of slot ~27 finished on the same branch.

**The FILE:** `deliverables/0.9.0_WK_ADVI_COTBKF~27/PRICE_NEED_FOR_SECHIST.csv` (4,545 rows: id, asset class, source, first and last date
needed, days) and `.json` (totals per source, the census line it reconciles to, `row_split`). No price fetched. It goes to
`1.0.0_SA_CTO~DELL2` for forwarding to dell1; the pull is MDPF_SECHIST's, under Andrew's per-use word.

## Rows

| row | class | standing |
|---|---|---|
| D2-W27-S1 | BLOCKING | INERT -- AC2 as first cut could not be met; resolved by AMENDMENT 1 (AC2 PASS) |
| D2-S21 | OBSERVATION | INERT -- corrects S19's wording: 2,914 and 8,091,310 are different sets |

ARMED: 0.
