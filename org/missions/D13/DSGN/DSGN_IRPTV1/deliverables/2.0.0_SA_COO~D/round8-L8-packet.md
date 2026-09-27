# DSGN_IRPTV1 -- round 8 L8 packet (the COO's drain-end packet) for 3.0.0_SA_CVO

**From:** 2.0.0_SA_COO~D, 2026-09-27. **Ask of the CVO:** compile the channel, grade round 8's judgment criteria on the round-8 walk
(record to follow in this packet's addendum), adjudicate the 12 ARMED rows below on their evidence, and send the one L10 slug to
1.0.0_SA_CTO. Round 8 is `<risk>LOCAL</risk>` throughout (local portal DEV only). **Final (2026-09-27 ~21:1xZ):** every round-8 order is terminal and the round-8 walk has landed: `w18-round8-walk-20260927.md`
(window 18, local DEV 3b98939b, byte-proof clean).

## Orders (round 8 issuance @83576f9dd9 over PRD v0.16/v0.17, decomp v8 + addenda 1-3; direct acts round-less)

| order | item | state | portal (local DEV) |
|---|---|---|---|
| IV-e-54 | E10a product-path residuals (W29-S8) | complete -- both fixed at the test pin (17 declared routes; dev-live measured) | 9c71f9a4, merged 3e54ec31 |
| IV-e-55 | E10b pinned runner (W29-S10, W29-S9) | complete -- 3 identical pinned runs, failing set a subset of Q; JUnit attribution bug + iv-e-26 EOL fixed | b67fdb22, 851f3830, merged c66f980c |
| IV-e-56 | E1 firm display names + UIW-0927-03 | complete -- token-free title case (naming gate, W35-S1) | e88b2c45, merged 089c3cbb |
| IV-e-57 | E2 search covers page + UIR-06, UIR-20 | complete -- Analysis Export closed outright (W35-S2) | e7746057, merged e8a00b23 |
| IV-e-58 | E3 picker value + YTD | complete | f49e120c, merged 1f149d69 |
| IV-e-59 | E4 account colours | complete | 419079c1 |
| IV-e-60 | E5 breadcrumb, one-slice pie | complete (its UIR-33 arm re-asserted old strings; carried into IV-e-61 amendment 2) | f04c0c1e |
| IV-e-61 | E6 map chips + UIW-0927-07 + UIR-33/36/47 wording | complete; chain V merged 8a99369e + drain re-golden 71896c93 (W38-S1) | bc0c0b9f |
| IV-e-62 | E9 request history + UIW-0927-02 | complete | 4f0ae52d, merged ab107147 |
| IV-e-63 | E7 dates, sources, R10 label + UIW-0927-01/06 | complete ("Series starts" clause scoped out, W40-S1) | aa1a47f8, merged 3b98939b |
| IV-e-53 | E11 preview carries selectedTenant (S20/S22) | complete (direct act) | 97c08b21, merged cad4d979 |
| IV-e-64 | submit/receipt/download carry selectedTenant (S23) | complete (direct act) | 512e3ba1, merged 55bbdd71 |
| IV-e-65 | export names the report by RPT- id (S24) | complete (direct act) | 5e3a9a99, merged 21ec94d8 |
| IV-e-66 | analysis item/status/report reads carry selectedTenant (S25) | complete (direct act) + census re-golden a5107226 (W36-S2) | 11fbff18, merged c8906a62 |
| IV-e-50 | round-7 harness | superseded by IV-e-55 (CTO 101845) | -- |

**Drain checks at local DEV 3b98939b (round 8 complete):** tsc 0 errors; lint 0 errors; suite 923 pass / 27 skip / 5 fail. The 5 are
F25-AC2 x2, F25-AC3, the smoke-map fixture set and the source-bounds scan; IV-e-55 measured them as the same set on three pinned runs, a
subset of the Q rows. Nothing of round 8 is on origin.

## Judgment criteria (for the CVO's L9)

IVE56-AC2, IVE57-AC2, IVE58-AC2, IVE59-AC2, IVE60-AC2, IVE61-AC2, IVE62-AC2 and IVE63-AC2: each UIR / UIW row read on the running page
at 1440 px. The artifact is the round-8 walk, `w18-round8-walk-20260927.md` (window 18, local DEV 3b98939b). 4.0.0_SA_CRO's own
/ui-walk re-grade of the same build (docs/briefs/irpt-ui-cleanup-brief-20260927.md @97cb8bf734) is a second reading: 8 MET, 1 met
page-side, 8 NOT MET (UIR-17/30/32/34/37/40/45/49). E8's coverage rows
(UIR-17, UIR-18/19, UIR-22) are walked in the same window; UIR-50 grades when 2.0.0_SA_COO~M's values land.

## The 12 ARMED rows (`comp-surprise --project DSGN_IRPTV1 --armed --json`, 12 of 192 rows, 0 malformed), with the disposition at this seat

| row | disposition |
|---|---|
| S7, W21-S2, W23-S1, W29-S9, W29-S10 | IV-e-55 PASS: three identical pinned runs, failing set a subset of Q (CTO 101845: these close on its pass) |
| W29-S8 | IV-e-54 PASS: F45-AC9 and F57-AC2 green (both were stale test pins against the ratified contract) |
| W34-S1 | carried to round 9: fe-s-45/residuals fails intermittently under the pinned runner (dev-server timing, not order) |
| W35-S1 | resolved in IV-e-56: display names are a token-free title case, so no firm literal meets the naming gate |
| W35-S2 | carried to round 9: Analysis Export is closed outright until AnalysisTab threads an answer-bearing signal up to index.tsx |
| W36-S2 | re-goldened at the drain (a5107226): the fe-s-54 census counts 4 production getJobStatus sites (2 in OwnedRequestHistory) |
| W38-S1 | re-goldened at the drain (71896c93): iv-e-42 (UIR-33/47 wording) and iv-e-44 (grouped tile colour vs the Other class) |
| S19 | disarm owner 0.0.0_AB_MSTR (push the untrack @cfed2c067b); the history purge is Andrew's call |

## What the signed-in windows showed (records in the channel; HARs in place, gitignored; no media committed)

- **Windows 12, 14, 16, 17 (K8 export):** the page's export hop is now correct end to end on the portal side -- tenant on the preview
  (W12), on the submit (W14), the report named by its RPT- id and revision (W16). W16 hit the backend owner check (ReportDenied,
  OBJECT_NOT_COVERED); W17 (owner rule 3EST/hewG) passed the authorizer and failed at the narrative packet build after 60 s, behind a
  gateway 503 at 29.3 s. Both are backend; 2.0.0_SA_COO~P owns the fix and a new K8 window.
- **Window 15 K10 (Analysis):** the owner history lists the READY job; the per-row status and item reads dropped the tenant (S25),
  fixed by IV-e-66. The report was not reached in that window.
- **Byte-proof on every window:** start and end HEAD equal to the signed pin, 0 tracked changes, 0 /__mockcot/ requests.

## Round-9 candidates (for the CTO's analysis)

0. **The page must read the async export's queued acknowledgement (S26, window 18):** the served export now accepts (QUEUED,
   exr_d9ee2b18 in 3.1 s); the page reads no receipt from it and stops. Thread-breaking; first in the recut.
1. **Export, backend:** the narrative packet build fails validation (asserts_causation) and the submit outlives the 29 s gateway limit
   (2.0.0_SA_COO~P's; a K8 window follows the fix).
2. **Analysis Export signal (W35-S2):** AnalysisTab should tell the page when its report is answer-bearing, so Export opens there again.
3. **Prospect jobs without a client:** the owner history mounts only with a client chosen, so a prospect Overview is invisible until one is.
4. **"Series starts" label (W40-S1):** the series-start exception needs a comparison that does not fire on the clean case.
5. **fe-s-45 timing flake (W34-S1).**
6. **Carried from the CRO walk (CTO 101880):** UIR-40 (one band), UIW-0927-04 (picker entry carries the refusal sentence),
   UIW-0927-05 (Report details speaks client language).
7. **PRD v0.18 UI CLEANUP FINDINGS UIC-01..23** (CTO @5d44d0fa62, from CRO 102100): 20 are DSGN_IRPTV1's; the CTO asks they ride round 9.
   Also from window 18: the Performance header's ISO dates (UIR-45) and the system-code source line (UIC-14).
8. **Not DSGN cells:** UIR-26 and UIR-48 (2.0.0_SA_COO~M), UIR-50's values (~M).
