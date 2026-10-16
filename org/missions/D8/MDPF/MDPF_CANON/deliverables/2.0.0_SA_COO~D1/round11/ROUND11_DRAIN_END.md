# MDPF_CANON round 11 -- drain-end packet (2.0.0_SA_COO~D1), 2026-10-16 ~16:0xZ

To `3.0.0_SA_CVO` (L8/L9). **STATUS: INTERIM.** Gradable NOW: CN-s-4 AC3 and CN-s-3 AC2 (section 3, on the issuer's real run). Not yet gradable and NOT asked: nothing on CN-s-1 (a WORLD cell with no judgment criterion; its outcome is the CTO's exercised read after a never-widen pair, a CloudOps deploy and a scheduled fire, no earlier than 2026-10-17 13:30Z). A FINAL revision follows when CN-s-1's fire is read. Input: the CTO's round-10 analysis `ledger/ROUND_ANALYSIS.round10.md` (msg 6731), PRD v2.23 @1fb9ac96ab, decomposition v11 and its AMENDMENT 1. Issuance `e96996c705`: 2 of 2 chains, cap 8.

## 1. Orders, merges and evidence (MEASURED by the issuer at the merged tree)

| order | worker | merge | mechanical result | judgment owed |
|---|---|---|---|---|
| CN-s-1 Muni becomes the registered custom model "Opal Municipal Bonds" (WORLD) | ~32 | `66ae82d62d` | `r11_cn_s_1.py` pure 6 of 6, seams 4 of 4; pytest 28 passed (27 + 1); the two crosswalk copies byte-identical; drain: py_compile ok, ruff clean, 77 passed across the touched suites; instance VALID | none |
| CN-s-4 the Variant 2 Models band is never carried on or after the boundary (LOCAL, client-facing at landing) | ~31 | `532a25c852` | pure 6 of 6, real 5 of 5 (base 4 of 6 and 3 of 5: 9 of 9 carried dates red); portal `af2ae947` (one line) | AC3 |
| CN-s-5 the demo session on Variant 1 | ~31 | `532a25c852` | built to its criteria (wiring 10 of 10), then SUPERSEDED by the CTO's ruling (XA-20261016T143752Z-6cad; msg 6762: (C) final, (B) struck): not cherry-picked into any landing candidate | none (superseded) |
| CN-s-3 the Cottonwood AUM Trend upgrade (LOCAL, client-facing at landing) | ~31 | `532a25c852` | pure 7 of 7 (90 of 90 rows partition; the oracle at 5 period ends; 12 of 12 absent-leg dates carried); portal `34a15de1` | AC2 |

Drain, on the landing candidate (portal DEV `39dab87f3b` + `1e39adc9` CN-s-4 + `978da061` CN-s-3; CN-s-3's commit conflicted with CN-s-5's context and was resolved by text): `bun run typecheck` rc 0 with a negative control (a scratch type error reads TS2322, rc 2); `r11_cn_s_4.py pure` 6 of 6 and `real` 5 of 5, `r11_cn_s_3.py pure` 7 of 7 on it. No worker filed a row; the `surprises` arrays are empty.

## 2. WORLD acts

None yet. CN-s-1's deploy is a CloudOps ADHOC order (the gold package AND the daily-emitter package: the crosswalk is vendored verbatim into the emitter), after a signed never-widen pair (COO half drafted after the build; CTO half), no earlier than the window before the 2026-10-17 13:30Z fire. Measured preconditions (read-only, flags and counts): the identity flag (the sole account carrying `Opal_Muni_Income` is one of three Happyland-named accounts) is TRUE; the account holds a value on 9 dates only (2026-10-07 .. 10-15), so at most those 9 dates move; baselines of the two lambdas are in `round11/draft/CN_S_1_DEPLOY_BASELINE_20261016.md`.

## 3. The real run (the issuer looked at the pages)

`round11/real_run/REAL_RUN_20261016.md` and two screenshots, rendered from a vite build of the candidate above with the served 2026-10-15 objects as fixtures: `cn_s_3_cottonwood_trend_20261016.png` (a Cottonwood session: the window starts 2026-06-09, Other AUM filled from the first date, the interpolated window and the carried legend) and `cn_s_4_demo_global_variant2_20261016.png` (a demo-tenant session on Global: Variant 2, no band beside the stack across the 9 carried dates). Said in the record: the monthly bar of 2026-08-31 and the internal Global view were not seen; there is no base picture for CN-s-4 (the base defect is measured by arms R2 and R3).

## 4. The demo tenant, and what it does not get

Per the CTO's final ruling the demo stays on Variant 2: before 2026-05-15 it differs from the internal global view, because the per-model lines there are single-firm values (all 1,865 pre-05-15 per-model points rest on exactly one firm; measured, `round11/CN_S_5_RULING_READ_20261016.md` @ac7b8e71ef). Cell (B) is struck.

## 5. Rows and what is the CVO's

`MDPF_CANON-D1-S29` (ARMED): its remedy is CN-s-4 (the band repair) on PROD; with the demo staying on Variant 2 it disarms on CN-s-4's PROD read. The landing of CN-s-4 and CN-s-3 is client-facing and waits on Andrew's word. The judgment criteria are CN-s-4 AC3 and CN-s-3 AC2.
