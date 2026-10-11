# NFRA_MCPINDEX round 9 -- the issuer's drain-end packet for L8/L9 (2.0.0_SA_COO~MI, 2026-10-11 ~15:0xZ)

Addressed to `3.0.0_SA_CVO~Z`.
- **Source:** `ledger/ROUND_ANALYSIS.round8.md` @d2eb6c471b, items E1-E3. Issuance @c7f0978131: 5 cells, fanout 3 of 3
  chains. The decomposition's round-9 section was amended at the cut.
- **State:** 5 of 5 orders are COMPLETE and drained. `round-close-check.py --round 9` reads 5 complete, proof_ok 5,
  MAY-CLOSE.
- **This round has NO judgment criterion; every check is mechanical.** No oracle has yet judged whether the two GAP
  verdicts are plausible. Section 3 asks for that read.

## 1. Orders -- graded on box/sitez (issuer re-run after each drain)

| order | analysis item | status | mechanical (issuer re-grade) |
|---|---|---|---|
| MX-o-1 trade-rec census/reader | E1 | complete, drained @bac72d2e3a | o1.AC1 PASS: 8 candidates, each with its denominator; verdict **GAP**, owner `unowned`. AC2/AC3 PASS by branch (no reader); proof VALID |
| MX-o-2 billing census/reader | E1 | complete, drained @92dc842a98 | o2.AC1 PASS: 6 candidates; verdict **GAP**, owner `ADVI_BILLING` (no object carries a paid status). AC2/AC3 PASS by branch; proof VALID |
| MX-x-6 batch repair | E3 | complete, drained @ea11910486 | x6.AC1 2 of 2 named tests (the emitter refuses a foreign census dir; the worker's revert control failed only that test). x6.AC2 SELF-TEST PASS: baselines full 41, sparse 99; proof VALID |
| MX-c-7 catalog writer | E1 + E2 | complete, drained @fbeb5b628b | c7.AC1 6 of 6 present, 29 of 29 kept; AC2 10 of 10 first-try; AC3 5 of 5 (FWD-18 3 of 14, C3 3 of 3, folds 0, E-13 guidance 5 of 5); proof VALID. Drain suite via `suite_delta`: 41 failed / 711 passed, so new 0 against the baseline |
| MX-r-10 release | E1 + E2 | complete @522c85edf8; ledger `nfra-mcpindex-r9-ops-readers-release` CLOSED 4/4 @87bf2c8723 | live `c3af8687e4` on `6aadf7db37`, 2 files. Label read back before L1 closed. r10.AC1 PASS; r10.AC2 PASS (routes 4 of 4, fwd18 3 3, guide E-13 5) after the issuer's counter fix A3 @3e6a138a1a (row Z-S99). Halves: COO @a6e212dfe8, CTO + G-A @b51c82abe6 |

## 2. The one real run of the outcome, 2026-10-11 ~14:5xZ, through this seat's opalgateway session (served host `c3af8687e4`)

- "how did the growth model do against its benchmark last quarter": need **E-13** first, SERVED, tool
  `mdpf_get_model_benchmarks`. The match now carries E-13's `note`: "When the asked model is not one of the five served
  models (UST, ST, INT, LT, ULT), the answer lists those five and asks which one, and never gives a figure for the
  unnamed model." Ruling 2a is live.
- "trade reconciliation": need **E-30** first, GAP, owner `unowned`, tool null, with the census reason in its note.
  The operations lead is told plainly that nothing serves this; no fixture value is ever served.
- "S&P YTD": need **E-19** first (PARTIAL, YCharts, live error stated). This route now comes from catalog example
  text; the word folds are retired.

## 3. What L9 is asked to judge (no criterion holds it; this is the plausibility read)

- **FWD-19 is NOT done:** both readers are GAP. Read the two censuses for search quality:
  - `deliverables/0.9.0_WK_NFRA_MCPINDEX~30/census_trade_rec.json` (8 candidates; the nearest is Orion, one status from
    one system, with null order IDs on 1,520,347 rows);
  - `deliverables/0.9.0_WK_NFRA_MCPINDEX~31/census_billing.json` (6 candidates; no paid status anywhere).
  Is GAP the right verdict, and is each owner right?
- **FWD-18:** 3 of 14, read from the SERVED catalog (C2, W5, W6), with C3 carried by E-4/E-5/E-9 (GAP). This is a
  re-grade of round 8's Z-C-S44 NOT_REALIZED.
- **FWD-11 J1:** still HELD at Andrew (Alyssa's own run). The live answer path above is its precondition, and it holds.

## 4. Rows this round, and the issuer's rulings

| row | in-file | ruled by |
|---|---|---|
| Z-W30-S1, Z-W31-S1 (census `served` means "serves the shape") | OBSERVATION/INERT | Z-S98 @88719444bc: CONFIRMED |
| Z-W32-S1 (suite baseline 41/99, not 34-38; sparse needs `--continue-on-collection-errors`) | OBSERVATION/ARMED | Z-S98: DISARMED |
| Z-S96 (MX-f-1's YAML broke the bd-pipeline plan, IAMROLES Z-S29) | OBSERVATION/INERT | ruled here; written in `2.0.0_SA_COO~ZI`'s w-2 A6-r6 @59d56f3848 |
| Z-S99 (r10.AC2 counter dead, the issuer's defect) | BLOCKING/ARMED | Z-S100 @a8f5f3fa2a: DISARMED; fixed by A3 |

## 5. Carried to the round-9 L10 slug (enrichment candidates)

1. **FWD-19's two GAPs need producers, not readers:**
   - trade rec (`unowned`): a per-trade Opal status joined to a custodian status. Andrew-class: who owns it.
   - billing (`ADVI_BILLING`): AUM per period, fee rate and a paid status. A cross-project ask.
2. **The battery lesson (Z-S100):** a check excused from the base dry-run still needs its PASS arm exercised once on a
   planted input before the cut.
3. **The deploy wrapper's sparse-tree imports** (`deploy-to-ec2.sh:94` lib/opal_naming; `commit_gate_runner.py:96`)
   recurred on both MCPINDEX releases. They belong to `2.0.0_SA_COO~O`'s wrapper fix (ruling 2c), and were told to it.
4. **Round 7** stays open on MX-s-19 (s19.PRE 2026-10-13 after 03:00Z).
