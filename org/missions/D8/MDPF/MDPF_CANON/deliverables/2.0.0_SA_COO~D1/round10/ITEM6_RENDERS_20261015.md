# Round 10, enrichment item 6: the two issuer renders (2.0.0_SA_COO~D1 fork, 2026-10-15 ~15:3xZ)

Grade inputs for the CVO: (A) `MDPF_CANON.TO-CN-l-2` AC3 (the Other Models card), (B) the non-internal Global Trend (Variant 2) that CN-p-2 AC4 named as a limit. Nothing ships; nothing was committed or pushed; no AWS write. Screenshots stay under the session scratchpad (`.../scratchpad/i6/`, client data, never committed or pasted). Words only here.

## Method

- Portal worktree `C:/dev/ajb_workspace/portal` on DEV `e0b033253b` (clean; only the pre-existing untracked `.runtmp/`), plain `bun run dev --port 5174 --strictPort` (no live front door), killed by PID afterwards; port 5174 read free.
- Instrument: `portal/scripts/ui-smoke.mjs` (headless Edge, stubbed `/auth/refresh` session, `--fixtures` URL-substring answers). `FIXTURES-MATCH: matched 4 of 4` on every run.
- Data: the four served Global objects read from `s3://opal-data-portal-v2/platinum/mdpf/global/` (aum-metrics, aggregate-aua-timeseries (670,289 B, frontier 2026-10-14, 497 dates), account-distribution, category-views); read-only `s3 cp` to the scratchpad.
- Identity: `--firm demo` = `firmId=demo userType=Advisor role=user`. The page's own rule (`ModelPortfolios.tsx:386-411`) makes this a NON-internal session that views the Global scope (`MDPF_GLOBAL_VIEW_FIRMS`), so it exercises `isInternal()` false and Variant 2 on the Global object. Other firm ids would resolve to their own per-firm scope, not Global.

## (A) CN-l-2 AC3: the Other Models card (3 states, same session, Snapshot view, legend row "Other Models" pressed)

Planted by fixture only (the served aum-metrics edited in the scratchpad copy): S1 the real object (Other Models row 68.9M, 211 accounts, no `as_of`); S2 the same row stamped `as_of 2026-10-10` (carried; page as-of 2026-10-14); S3 the Other Models row removed (no pool within four days: row ABSENT).

- **S1 pool present:** the donut centre reads "Other Models" and "$68.9M", nothing beneath. No extra line. Legend lists Other Models between Ultra Long-Term and Other AUA.
- **S2 carried:** centre reads "Other Models", "$68.9M", and under it in small muted type on the band "as of 2026-10-10" (11 px, 60% white on the dark band; readable at screenshot size).
- **S3 no pool:** the legend has no Other Models row, the donut has no Other Models segment, and the click target does not exist (`CLICK-FAIL: Other Models ... Timeout`, control list printed without it). Centre reads "Total AUA $2.16B" unchanged.
- Observed, not a defect of the cell: with the row absent the 68.9M is not lost; the gray "Other AUA" residual segment grows (Other AUA = Total minus SmartX model AUM, the card footnote). Total stays $2.16B in all three.
- Denominators: 3 states x 1 session x 1 page width (1440 px); one scope (Global). Not shown: a firm scope, a narrower viewport, the Trend view of the card.

## (B) Global Trend, Variant 2 (non-internal `demo` session, real 2026-10-14 object, Trend view)

- Header copy: "Since-inception AUA growth from November 1, 2024 to October 14, 2026." Then "Per-model detail begins May 15, 2026; earlier model assets are in the Total and are not broken out", and "models held at one firm are in the total and not broken out".
- Legend: the five models, Custom Models, Models (the band), Client Supervised, ETF Strategies, ALT Strategies, and the dashed "Carried forward (last known value)" key. No Cottonwood/Inflection composition footnote (that is the internal Variant 1 text).
- Quarterly bars: nine bars Dec 31 2024 to Oct 14 2026. The six bars before 2026-05-15 are one lavender "Models" band over Client Supervised; the three after are the five model colours plus Custom Models, Client Supervised, ETF Strategies and ALT Strategies. The stitch is absent: no single-firm model line is drawn before 2026-05-15 (data check: 0 single-firm cells on those 383 rows, as `CN_P_2_REAL_DATA_VARIANTS_20261015.md`).
- Daily chart: full history from 2024-11 to 2026-10-14; one Models band before 2026-05-15 and the model stack after.
- Control run (default internal Dev admin, same fixtures, NO per-firm fixtures): header reads the Variant 1 composition footnote ("Inflection's models enter the Total on May 15, 2026; Cottonwood enters on May 28, 2026 (estimated until July 20, 2026)"), no Models band in the legend, and the page draws only from May 2026 because the stitch's per-firm objects were not supplied. This control proves the two modes differ by claim; it is NOT a Variant 1 render (Andrew smoked Variant 1 on 5174 earlier, record `9fbada016d`).
- **DEFECT FOUND in Variant 2 (not fixed):** the daily chart shows four tall spikes at 2026-05-30/31, 06-06/07, 06-13/14 and 06-19/20/21 (the y-axis runs to $3.2B while the Total there is about $1.77B). Cause measured on the page's own module output (`round9` measure file, v2 rows): on the 9 carried dates after per-model detail begins, the row carries BOTH the five model lines AND a `modelsBand` of 1,349M (the 2026-05-14 value, carried), so the stack counts the models twice. Count: 9 of 497 rows in Variant 2 (exactly `carried_dates`), 0 of 497 in Variant 1. The earlier variants record counted the band only on the 383 pre-detail rows and did not test carried dates after 2026-05-15. Owner: the issuer for round 11 (module `portal/src/lib/trendGrouping.ts`, `buildGlobalTrendRows` Variant 2 carry); client-facing (a non-internal session sees it), so a PROD push waits on Andrew's word.
- Denominators: 1 non-internal identity (`demo`), 1 scope (Global), 1 width, 1 object vintage (2026-10-14). 497 rows read from the module for the defect count.

## What these renders CANNOT show

- A real partner or demo login (no MFA-free partner login exists): the claim is stubbed, so `AuthContext` parsing and the live edge/authorizer path are not exercised; only the page's `isInternal()` branch is.
- Real Other Models behaviour on a carried day: the stamp and the removed row are planted copies of the served object; the producer's own stamping (CN-l-1) is graded elsewhere.
- Variant 1 on this build (control lacked the per-firm stitch objects); a firm scope; mobile width.
