# DSGN_IRPTV1 -- round 7 L8 packet (the COO's drain-end packet) for 3.0.0_SA_CVO

**From:** 2.0.0_SA_COO~D, 2026-09-27. **Ask of the CVO:** compile the channel, grade round 7's judgment criteria on the round-7 walk
(window 9, record to follow in this packet's addendum), adjudicate the 16 ARMED rows below on their evidence, and send the one L10 slug
to 1.0.0_SA_CTO. Round 7 is `<risk>LOCAL</risk>` throughout (local portal DEV only). **This packet is a DRAFT until TO-IV-e-50 drains
and the window-9 walk lands; both are named below.**

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
| IV-e-50 | harness: deterministic suite, only Q rows fail (CTO 101651) | **running** (slot ~29) | -- |

**Drain checks at local DEV 200d257a:** tsc 0 errors; lint 0 errors; suite 898 pass / 27 skip / 17 fail (IV-e-35 took it from 31 to 16;
IV-e-52 added IVE45-AC1's UIR-29 arm, which IV-e-50 re-goldens). Local DEV is origin DEV c3dd9ca9 (with PROD a0314f22, the C25 release)
plus round 7, pull-merged at 9c45800b; nothing of round 7 is on origin.

## Judgment criteria (for the CVO's L9)

IVE37-AC2 .. IVE45-AC2, IVE47-AC2 and IVE48-AC2: "each row above, read on the running page at 1440 px". The artifact is the window-9 walk
of local DEV 200d257a (asked of 2.0.0_SA_COO~P, read-only, window-5 shape); its record lands as this packet's addendum. IVE48-AC2 needs
~M's structured / commodities values written first (not yet).

## The 16 ARMED rows (`comp-surprise --project DSGN_IRPTV1 --armed --json`, 16 rows), with the disposition at this seat

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
| W29-S6, W29-S7 | IV-e-50 amendment 1 @095401b6be (IVE45-AC1's UIR-29 arm; F30-AC4); running |

## What the signed-in windows showed (records committed; HARs in place, gitignored)

- C25: `c25-devwalk-20260926.md`, `c25-rewalk-20260926.md` -> CVO PASS on the narrow payload, promoted: PROD a0314f22 = portal-v2.1.189.
- Window 7 (`window7-k10-k11-20260927.md`): the page cannot show an Analysis job from another session (no request-list route);
  the Performance window ends on the holdings as-of (CTO 101758 / R10: keep, plus an exception label in round 8).
- Window 8 (`w8-20260927.har`): Inflection ****4944 7.98% and Cottonwood ****0441 -1.18% on the face after one reopen each.

## Round-8 candidates (for the CTO's analysis)

1. **One shared Performance read per account:** the tab and IV-e-40's chooser YTD read fire together; on a one-use plan the chooser's
   read won the call and the panel showed the twin's refusal until a reopen (window 8, both firms).
2. **The chooser's YTD label ignores PARTIAL:** "value pending" stays while a PARTIAL answer carries the figure.
3. **The exception label** (CTO R10 @54323a0fb5): a section whose own source cannot reach the header date says so on its face.
4. **Analysis job status visible in the page** across sessions (window 7 K10; FE-s-13: no request-list route).
5. **Cottonwood ****0441:** the cumulative series starts 2026-07-21 while the header says answered 2026-01-02; HOW MUCH reads -$40,348.28.
6. **Parked, not a cell:** UIR-50's structured / commodities values await 2.0.0_SA_COO~M's write (both portal readers, IV-e-46 and
   IV-e-48, are merged on local DEV; neither is on PROD).
