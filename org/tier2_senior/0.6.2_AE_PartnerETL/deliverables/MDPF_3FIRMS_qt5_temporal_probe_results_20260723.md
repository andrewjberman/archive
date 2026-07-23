# qt5 Temporal Probe — Execution Results (paired: CRO design @040036Z/040505Z, 0.6.2 mechanics)

**Agent:** 0.6.2_AE_PartnerETL~A · **Date:** 2026-07-23 04:0x-04:16Z · **Authorization:** Andrew-direct
acceleration ("get it done now", egress granted, COO 035548Z) · **Verdict authority:** 4.0.0_SA_CRO
(campaign carrier; adjudication in flight). **Zero template persists** — inline selection proven honored,
production 226334 never touched server-side. Raw exports retained:
`s3://opal-data-cot/code/bronze/probe_results/qt5_window_{0515,0615,0707,0708,0710,0714}.xlsx`
(runs 252861-252871; scripts `b6_qt5_bisect.py` / `b6_qt5_retained.py` staged at `code/bronze/`).

## The window matrix (the load-bearing table)

| as-of window | rows | distinct accts | Opal-assigned | churn controls present | note |
|---|---|---|---|---|---|
| 2026-05-15 | 113 | 83 | 14 rows / 4 Opal names | 0/8 | pre-migration; 3 non-Opal names dominate |
| 2026-06-15 | 1,393 | 780 | 11 Opal names | 2/8 (Sat-50, Sat-40) | mid-migration |
| 2026-07-07 | 1,494 | 857 | 14 Opal names | 8/8 | pre-freeze |
| 2026-07-08 | 1,499 | 859 | 293 accts | 8/8 (stable) | "frozen" date — POPULATED NOW |
| 2026-07-10 | 1,507 | 867 | 293 | 8/8 | "frozen" date — POPULATED NOW |
| 2026-07-14 | 1,502 | 862 | 293 | 8/8 | "frozen" date — POPULATED NOW |
| today (07-23) | 0 | 0 | — | — | R0 baseline; snapshot not yet materialized |

Supporting: R1 inline-deselect of CRO's 12 candidate dims -> columns 56->47 (**inline selection HONORED
by v1/run**) and STILL 0 rows today (the 12-dim hypothesis for the emptiness is ELIMINATED).

## Findings (Rule-22 labels)

1. **SOURCE-CONFIRMED: the surface returns DIFFERENTIAL DATED BOOKS per window** — rosters 83->780->857->
   859->867->862->0, controls 0/8->2/8->8/8 in migration order, Opal set 4->11->14. No single stamped
   state produces this. ~~(Formal TEMPORAL verdict = CRO's ruling; ... the parsimony read is re-save-stamp
   dates + retroactive names.)~~
   **VERDICT RULED (CRO 042709Z, his authority): CURRENT-STAMPED ASSIGNMENT — NOT temporal.** The
   differential windows prove temporal EXISTENCE + VALUE (real onboarding growth, real PIT holdings) —
   but CRO's direct transition test (the test my summary did not run) shows EVERY matched account
   carrying its EXACT today-assignment in every window it appears (0 window-assigned->today-unassigned,
   0 reverse, and the only 5 both-assigned-different are one non-Opal label reclass) — the definition of
   current-stamped assignment. **My re-save-stamp parsimony hypothesis is FALSIFIED** by his
   createdAt-stability test: createdAt stable 22/22 across the 07-21/07-22 partitions (real birth dates);
   the nightly movement my B6 liveness work measured was `updatedAt`, a DIFFERENT field. The 05-15
   Opal-name presence was the current-stamp artifact; CRO's window-integrity IGNORED flag was correct.
   **Consequence: qt5 offers NO temporal assignment — the interpolated backfill's assignment leg STANDS;
   qt5 IS a real dated VALUE/existence source (value-leg refinement to ~05-15).** The recovery sweep
   remains valid as value/existence recovery (recent-dates assignment ~= correct at ~zero 2-week churn),
   and the recovered qt5 assignment must NEVER be used as deep PIT assignment history.
2. **SOURCE-CONFIRMED: the ~07-09 qt5 "freeze" is vendor LATE MATERIALIZATION, and the frozen dates are
   RECOVERABLE NOW** — the daily chain's 0-row rejects were true at the time (SSM verbatim, runs
   244438/247780) and the same as-of dates return full exports today on the same call shape.
3. **The daily-chain defect is OUR-side and small: it asks once for same-day and NEVER RETRIES.** Repair
   spec (WS-1 lane, CTO to schedule): (a) catch-up sweep re-attempting REJECTed as-of dates (the sec-8.1
   auto-pickup class, one page of code in the daily runner); (b) consider D-1 as-of for the daily pull if
   same-day materialization stays lagged. Applies to qt4 plausibly — verify with one qt4 explicit-window
   run before assuming.
4. **RECOVERY SWEEP AVAILABLE, GATED:** 07-09..07-22 explicit-window re-runs -> sanctioned forwardfill
   landing -> normal silver conversion. A LANDING operation — moves on CTO's word only. Box window closes
   ~06:00Z; next window tomorrow same time if the word comes later.

## Provenance

Mechanics reused from production `cot_bronze_ingest` (`_request`/`poll_status`/`download_export`; run-body
normalization :405-415 — the class whose omission produced the earlier instrument-side 500). GUID->name
join from the 07-22 `rebalancer_models` roster (60 strategies). Sequential single-session vendor use;
CRO held zero concurrent calls (his 040505Z).

## RECOVERY SWEEP EXECUTED (CTO GO 041852Z + Andrew-direct "run it now" via COO 042006Z; completed ~04:30Z)

Two passes (pass one SSM 02110d7a; resume 62d87d31 after a bearer-TTL 401 -- an owned instrument gap,
patched with production's re-mint-once-on-401 discipline). **FULL RECOVERY, both tables, 10/10 possible
trading dates each, sanctioned forwardfill path, weekends honest-empty, zero forced landings:**

| date | allocations rows | unrealized rows |
|---|---|---|
| 07-09 | 1,499 | 161,398 |
| 07-10 | 1,507 | 161,474 |
| 07-13 | 1,501 | 161,507 |
| 07-14 | 1,502 | 77,796 |
| 07-15 | 1,503 | 67,077 |
| 07-16 | 1,503 | 67,082 |
| 07-17 | 1,508 | 67,012 |
| 07-20 | 1,516 | 67,108 |
| 07-21 | 1,521 | 67,206 |
| 07-22 | 158 (PARTIAL-FLAGGED) | 412 (PARTIAL-FLAGGED) |

**PROVENANCE (CTO in-flight amendment 042804Z, verbatim): value: real late-materialized vendor data /
assignment: current-stamped (accurate-window, not point-in-time). Nothing landed reads as PIT assignment
recovered; the daily honest-rejects history stays un-edited.**

Open items out of the sweep: (a) 07-22 both tables ~10-100x undersized vs neighbors = likely
mid-materialization partials -- disposition at CTO (rec: delete + re-run next window) BEFORE the next
02:00Z conversion; (b) qt4 count-regime shifts inside the span (161K -> 77.8K -> 67K) observed, not
adjudicated -- DS lens next; (c) the qt4-vs-qt5 two-mode hypothesis REFUTED for the freeze (one vendor
late-materialization mechanism covers both; the 500 was instrument-side); (d) the daily-chain never-retry
fix = the designed morning-batch item (CTO).

## 07-22 DISPOSITION EXECUTED (CTO 044012Z leg 1; attempt ~04:45Z)

Deletion REJECTED by CTO (versioned same-key re-land supersedes; nothing to human-confirm). Gated
re-land attempted THIS window (SSM 91c6c89e, gate = >=50% of the 07-21 neighbor): allocations 158 rows
(gate >=760) and unrealized 412 (gate >=33,603) -- **STILL PARTIAL, LANDED NOTHING** (absent >
false-drop; the partials remain unconverted bronze-only, DS's conversion hold keeps 07-22 honestly
absent). **NEXT ATTEMPT: the next box window (~02:00Z 07-24), same gated script
(`code/bronze/qt_0722_reland.py`, staged) -- owner me if live, else the morning-batch never-retry fix
(CTO's designed item) structurally covers this exact case.** The 07-21 materialization pattern (full by
D+1's window) says tomorrow's attempt should pass the gate.
**LIFT PROTOCOL (DS 044447Z, quarantine deployed @88d165366, ETag 513d9095...):** the 07-22 pair is
conversion-quarantined (sweep-skip LOUD + hand-run/--force refusal, exercised). After the gated re-land
passes (next box window): ping 0.4.0_DS with the verification -> DS removes the two FORWARDFILL_QUARANTINE
entries + deploys same-hour -> conversion follows on the next sweep. Race harmless in both orders. The
raw partials sit untouched (no deletion, CTO-rejected) for diagnosis.
