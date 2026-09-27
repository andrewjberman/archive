# DSGN_IRPTV1 -- round 7 L8 packet (the COO's drain-end packet) for 3.0.0_SA_CVO

**From:** 2.0.0_SA_COO~D, 2026-09-27. **Ask of the CVO:** compile the channel, grade round 7's judgment criteria on the round-7 walk
(window 9, `w9-round7-walk-20260927.md`), adjudicate the 20 ARMED rows below on their evidence, and send the one L10 slug
to 1.0.0_SA_CTO. Round 7 is `<risk>LOCAL</risk>` throughout (local portal DEV only). **Final (2026-09-27 ~06:5xZ): every round-7 issuance order is terminal and the window-9 walk has landed; the one open order, IV-e-50, is a round-less direct act, parked below.**

## Orders (round 7 issuance @f56587bf9e over PRD v0.15, decomp v7; direct acts round-less)

| order | cell | state | portal (local DEV) |
|---|---|---|---|
| IV-e-37 | C28 search (+UIR-04) | complete | d6e6eda3, merged 6bbf4141 |
| IV-e-38 | C29 header rows | complete | 9516cab4, merged 6bbf4141 |
| IV-e-39 | C30 picker + refusal | complete | fea63064, merged c3d422a3 |
| IV-e-40 | C26 per-account YTD (FWD-20) | complete | 277a51e6, merged 05c97d2d |
| IV-e-41 | C27 every account in every view (FWD-21) | complete | e6d26016, merged da25ae69 |
| IV-e-42 | C31 the drill and its bases | complete | 62834bbd, merged da25ae69 (+5816e61b lint) |
| IV-e-43 | C32 one colour, one meaning | complete | e6e64d14, merged ad06e37f |
| IV-e-44 | C33 the securities map (FWD-22) | complete | 80763061, merged 6757223a |
| IV-e-45 | batch (UIR-17/20/27/28/29/35/38/40/45) + amendment 1 | complete | 1fdbe11b, merged ad06e37f (+0a83fbc4 lint) |
| IV-e-35 | S7 residual (direct act) | superseded (CTO 101651) | merged 9c0cff2f (31 -> 16 failing) |
| IV-e-36 | Export preview account scope (direct act) | complete | a5f073c2, merged fe7beb7a |
| IV-e-46 / 49 / 51 | AI-TAGS: composition admits structured + commodities; commodities = PALETTE.green900 (CTO 101649 / 101681) | complete | d9593607, ace4f08d, 888215a7, c506381e; merged 79977369 (+bc9aa02c DEFAULT_LAYOUT, lint) |
| IV-e-47 | UIR-07 Global merge (direct act, CTO 101590) | complete (issuer flip, W25-S5) | b5915df3, merged 6bbf4141 |
| IV-e-48 | C34 new asset classes on the IR page (direct act) | complete | cc1d3419, merged 66bcfbe0 (+a28c0172 lint) |
| IV-e-52 | UIR-27 / UIR-29 in full (CTO 101768, direct act) | complete (issuer close: AC2's one failure pre-existing) | 5e6befb7, merged 200d257a |
| IV-e-50 | harness: deterministic suite, only Q rows fail (CTO 101651) + amendment 1 | **pending, PARKED** (direct act, round-less; its fixes merged; AC1's instance INVALID, controls.determinism UNSTABLE; AC2 FAIL, 5 of 7 not Q rows; the gate refuses a terminal flip; un-parks on the CTO's W29-S8/S10 ruling) | 464b7a37, 34a80a16, merged 3f76cdb2 |

**Drain checks at local DEV 3f76cdb2 (round 7 complete):** tsc 0 errors; lint 0 errors; suite 907 pass / 27 skip / 8 fail. IV-e-50 fixed 9 of
the 17 at 200d257a, added none. The 8 left: IVE26-AC3 (flaky, W29-S9), F45-AC9 and F57-AC2 (product paths, W29-S8), F25-AC2 x2,
F25-AC3, the smoke-map fixture set and the source-bounds scan. A second 3-run sample differed from the first (W29-S10): the suite is not
deterministic on this machine. Local DEV contains origin DEV c3dd9ca9 (with PROD a0314f22, the C25 release)
plus round 7, pull-merged at 9c45800b; nothing of round 7 is on origin.

## Judgment criteria (for the CVO's L9)

IVE37-AC2 .. IVE45-AC2, IVE47-AC2 and IVE48-AC2: "each row above, read on the running page at 1440 px". The artifact is the window-9 walk
of local DEV 200d257a (asked of 2.0.0_SA_COO~P, read-only, window-5 shape); its record is `w9-round7-walk-20260927.md` @a32823e232 (below). IVE48-AC2 needs
~M's structured / commodities values written first (not yet).

## The 20 ARMED rows (`comp-surprise --project DSGN_IRPTV1 --armed --json`, 20 of 144 rows, 0 malformed), with the disposition at this seat

| row | disposition |
|---|---|
| S7, W21-S1, W21-S2, W23-S1 | CTO 101449 / 101651: IV-e-35 merged as a strict improvement; the "only Q rows fail" + determinism bar moved to IV-e-50 (running) |
| W22-S1, W22-S2, W22-S3 | IV-e-34 amendment 2 re-scoped the three sibling tests; complete |
| W22-S5 | the "79 of 869" pre-existing set; every drain since diffs the failing set (no new failure outside the named ones) |
| W22-S6 | IV-e-36 (Export preview follows the one focused account), merged fe7beb7a |
| W25-S5 | issuer flip of IV-e-47 @26f1fa6165 (the slot predated the order) |
| W29-S1 | IV-e-45 amendment 1 (IVE45-AC3 PASS) |
| W30-S1 | DEFAULT_LAYOUT admits the two classes, drain repair bc9aa02c (CTO 101649) |
| W29-S2, W29-S3 | CTO 101768 (a) -> IV-e-52, complete |
| W29-S6, W29-S7 | IV-e-50 amendment 1 @095401b6be: both fixed (UIR-29d/e re-goldened; F30-AC4 re-scoped), merged 3f76cdb2 |
| **W29-S8** | BLOCKING, disarm_owner 1.0.0_SA_CTO: F45-AC9 (scripts/dev-live.mjs) and F57-AC2 (contracts/adapt.ts) need a product-path cell |
| **W29-S9** | disarm_owner a cell granting iv-e-26.wire-regen.test.ts: IVE26-AC3 is flaky (failed 1 of 3 runs) |
| **W29-S10** | BLOCKING, disarm_owner 1.0.0_SA_CTO: two independent 3-run samples gave different stable failing sets (15 vs 7); the "only Q rows fail" bar cannot be graded deterministically here |
| S19 | disarmed: 34 walk screenshots untracked @cfed2c067b, `*.shots/` ignored @01d82f1550 (closing evidence S21); history purge is Andrew's call |

## What the signed-in windows showed (records committed; HARs in place, gitignored)

- C25: `c25-devwalk-20260926.md`, `c25-rewalk-20260926.md` -> CVO PASS on the narrow payload, promoted: PROD a0314f22 = portal-v2.1.189.
- Window 7 (`window7-k10-k11-20260927.md`): the page cannot show an Analysis job from another session (no request-list route);
  the Performance window ends on the holdings as-of (CTO 101758 / R10: keep, plus an exception label in round 8).
- Window 8 (`w8-20260927.har`): Inflection ****4944 7.98% and Cottonwood ****0441 -1.18% on the face after one reopen each.
- **Window 9 (the round-7 walk, the judgment artifact):** `w9-round7-walk-20260927.md` @a32823e232, local DEV 200d257a, 05:39Z-05:47Z;
  HAR `w9-round7-20260927.har` sha256 62fea7a8.. (746 entries, 0 /export, 0 /analysis, 0 /__mockcot/); the record's row table is the evidence
  per UIR row. Its screenshots are local only (untracked @cfed2c067b, row S19/S21); the CVO reads them on this device on request.
- **Window 10 (K7/K8, P's never-widen pair):** K7 reopened a 49F report (8.05%); K8's Export preview refused client-side at
  `export/resolveBundle.ts:255` (MissingPayloadError on the report's own revision, P 101833); 0 export POSTs, nothing written, principal
  deleted 06:32:17Z (@16f05ab61c). HAR `w10-20260927.har` sha256 488da2d7.. (451 entries). Row S20; root cause row S22 (P 101835): the preview's
  Performance GET drops `selected_tenant` (resolveBundle.ts:292-300), so the internal viewer gets UNAVAILABLE.

## Round-8 candidates (for the CTO's analysis)

1. **One shared Performance read per account:** the tab and IV-e-40's chooser YTD read fire together; on a one-use plan the chooser's
   read won the call and the panel showed the twin's refusal until a reopen (window 8, both firms).
2. **The chooser's YTD label ignores PARTIAL:** "value pending" stays while a PARTIAL answer carries the figure.
3. **The exception label** (CTO R10 @54323a0fb5): a section whose own source cannot reach the header date says so on its face.
4. **Analysis job status visible in the page** across sessions (window 7 K10; FE-s-13: no request-list route).
5. **Cottonwood ****0441:** the cumulative series starts 2026-07-21 while the header says answered 2026-01-02; HOW MUCH reads -$40,348.28.
6. **The Export preview cannot resolve the report the tab shows** (window 10, row S20): the thread's export hop is broken on DEV. Cause (S22):
   thread `selectedTenant` from the export target through the preview into resolveBundle's request. P
   re-cuts window 10 as window 11 on the fix's pin. Thread-breaking, so first in the recut.
7. **UIR-25:** the account-level pie slices share one colour (window 9).
8. **UIR-41:** the map's model chips repeat once per sleeve (window 9).
9. **UIR-04 / 13 / 30:** the firm is shown by its tenant key (`cottonwood`, `49financial`), not a display name (window 9).
10. **The chooser shows YTD in place of the account value (UIR-15),** and one account reads -100.00% YTD (window 9).
11. **The S7 bar (IV-e-50's residual):** W29-S8's two product-path failures and W29-S10's run-to-run instability need a CTO ruling:
    a product cell, a wider Q allowance, or another disposition.
12. **Parked, not a cell:** UIR-50's structured / commodities values await 2.0.0_SA_COO~M's write (both portal readers, IV-e-46 and
   IV-e-48, are merged on local DEV; neither is on PROD).
