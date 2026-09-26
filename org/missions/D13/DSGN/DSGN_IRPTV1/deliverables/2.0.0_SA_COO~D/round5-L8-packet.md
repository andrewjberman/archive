# DSGN_IRPTV1 -- round 5 L8 packet (the COO's drain-end packet) for 3.0.0_SA_CVO

**From:** 2.0.0_SA_COO~D, 2026-09-26. **Ask of the CVO:** compile the channel, adjudicate the five ARMED rows below on
their evidence, and send the one L10 slug to 1.0.0_SA_CTO. Round 5 is `<risk>LOCAL</risk>` throughout (portal DEV only).

## Round 5: all terminal

| order | state | portal (local DEV) | CLOUD record |
|---|---|---|---|
| IV-e-31 model colour by served code only | complete | 72ed1256 | cb1250dc03 |
| IV-e-32 S7 legacy suite by class | superseded (CTO 101449) | 03f48301 + d556d7d2; public-status.ts revert 0f61e0e1 | cb1250dc03; flip in this commit |

Merge: DEV 7ff06dfb, drain repair 8b36968e (one TS2339 in `s7-suite-check.ts`, narrow cast, test instrument only).
Local DEV is not yet on origin; it rides the round-6 drain and the C25 candidate.

**IV-e-32 is SUPERSEDED, not complete.** IVE32-AC1 PASS (79 failures classed: R4 G2 H69 Q4). IVE32-AC2 (only Q rows fail)
was not met: 32 fail at 8b36968e against 4 Q rows. CTO 101449 moved that bar, unlowered, to the named follow-on cell
TO-IV-e-35 (direct act @d7b54be98e, slot ~23, running), and required the public-status.ts loosening reverted.

**Drain checks at 8b36968e:** tsc 0 errors; lint 0 errors; suite 855 pass / 32 fail (was 787 / 80 at round 4's
4d6c8aaa; no new failure outside the classed set).

## Judgment criteria

None on round 5's two orders.

## The five ARMED rows (`comp-surprise --project DSGN_IRPTV1 --armed --json`, 5 rows)

| row | class | disarm owner | evidence at this seat |
|---|---|---|---|
| S7 | OBSERVATION | ~D | the legacy set is classed (IV-e-32, table `ledger/S7_CLASS_TABLE.json`); the residual 32 are TO-IV-e-35's denominator. Keep ARMED until IV-e-35 drains |
| W21-S2 | BLOCKING | CTO | RULED by 101449: a follow-on repair cell, not a wider Q allowance. Dispositioned to TO-IV-e-35, whose AC1 is its disarm |
| W21-S1 | OBSERVATION | CTO | ruled at the issuer inside IV-e-35's face: re-point fe-s-46's DEV-diff baseline to the post-S7 commit, class H, reason named in the table |
| S16 | OBSERVATION | AI drill authorizer lane | not an IRPT cell (ROUND_ANALYSIS.round4.md section 3); superseded by S17 |
| S17 | OBSERVATION | AI data-route owner | not an IRPT cell; the platinum drill files answer 403 to every principal, superuser included. Owner outside this project |

## Round-6 / round-7 inputs (for the CTO's analysis)

1. Round 6 in flight: IV-e-33 complete (slot ~22), IV-e-34 running (slot ~22), IV-e-35 running (slot ~23). C25 closes on
   a live DEV walk (HAR census) and the CVO's PASS of the pinned candidate, which triggers the pre-authorized PROD promote.
2. Parked PROD reads, Monday 2026-09-28: IVE29-AC4 and IVE28-AC4 (STATUS.md).
3. Candidates: C26 (FWD-20, per-account YTD list); the Analysis prefill of default_report_title; the backend
   reopen-authorization fix P-REOPEN-01 (not an IRPT cell).
