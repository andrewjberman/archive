# MDPF_CANON round 11 -- rectangle DRAFT (not issued) -- 2.0.0_SA_COO~D1

**archetype:** COORDINATE
**Status:** DRAFT, written 2026-10-15 ~17:1x ET ahead of the issuance. Nothing is cut. Round 10 is not closed (CN-r-1 AC4 reads the 2026-10-16 13:30Z fire), so the decomposition (`decompositions/MDPF_CANON_DECOMP.md` v10) stays frozen and this file is the only carrier. The issuance happens when the CTO's round-10 analysis arrives (obligation 1), or earlier if the CTO says round 11 may be cut over the open AC4 (CTO msg 6131 says "after round 10 drains").

## Source

PRD v2.23 @1fb9ac96ab (ADMITTED: ratified-text SIGNED by 3.0.0_SA_CVO @eb00bfa63b, brief half auto). CTO msgs 6131, 6135. CRO spec `org/tier1_exec/4.0.0_SA_CRO/deliverables/MDPF_CANON_COTTONWOOD_AUM_TREND_UPGRADE_SPEC_20261015.md` @21caa664be (BASE ONLY). Andrew's records: Muni (`ANDREW_DIRECT_20261015_152xZ_*`, `ANDREW_DIRECT_20261015_184xZ_*`), demo tenant (`ANDREW_DIRECT_20261015_162xZ_*`).

## Cells (proposed; one behaviour each)

| cell | serves | what | files (read at HEAD before the cut) | risk | actor |
|---|---|---|---|---|---|
| CN-s-1 Muni to Custom | FWD-9 head (g) | IDENTITY CHECK FIRST: the `Opal_Muni_Income` account equals the Happyland Ventures account, printed as a match flag, no name; no match -> stop and report. Then Muni leaves `income_non_model_residual` and enters `by_model` / `model_aua` as "Opal Municipal Bonds" at Cottonwood; Global moves through the sums (about $64M, Other -> Custom). Only Muni: the 2026-09-21 auto-classify rule stands for every other Opal-named model. | `data/assets/scripts/gold/build_cottonwood_mdpf_slice.py` (the routing near `income_non_model_residual`, `custom_residual_detail`) and its tests | WORLD (a gold-package deploy; moves served bytes at two firms) | worker + CloudOps deploy under a never-widen pair |
| CN-s-2 Cottonwood carried model legs | FWD-9 head (f) | the 12 absent model-leg dates (2026-07-28/29/30, 08-04, 08-12, 08-31, 09-01..09-04, 09-08, 09-09) are emitted `carried` (last measured leg, total stays measured) | same producer file; depends on CN-s-1 (same file, one chain) | WORLD, a served change under a pair | same chain as CN-s-1 |
| CN-s-3 Cottonwood Trend per the spec | FWD-9 head (f) | window starts at the first measured total (2026-06-09); Other AUM = `partner_custody_total` - `model_aua` on every total-bearing row; the interpolated marking kept; the carried dates marked; NO 2026-04-22 extension. Oracle: the spec's month-end table (6 rows) | `portal/src/pages/ModelPortfolios.tsx` and the Trend lib it reads (CN-s-4 may share the page) | SERVED (a page on DEV) | worker; DEV only |
| CN-s-4 demo = Variant 1, Variant 2 repair | FWD-9 head (a) | `trendModeFor`: a demo-tenant session draws Variant 1 (same code as the internal session). In the same function: `buildGlobalTrendRows` never carries `MODELS_BAND_LABEL` on or after `per_model_detail_begins` (one condition in the roll-forward loop at `trendGrouping.ts` ~L242-249; the Models band is set only when `mode === 'variant2' && pre`). Test on the real object: 0 of 497 rows draw both the band and the model stack; no drawn group above the Total. If the edge gate refuses a demo session the pre-05-15 read, the cell REPORTS it and never widens the gate. | `portal/src/lib/trendGrouping.ts`, its tests, the call site of `trendModeFor` | SERVED | worker; DEV only; disarms D1-S29 on DEV |

## Issuer decisions to take at the cut (not decided here)

1. CN-s-3 and CN-s-4 may both edit `ModelPortfolios.tsx`: one chain, or disjoint `<paths>` (read the page at HEAD first).
2. CN-s-2: producer emission (the Global precedent, `carried_dates`) versus read-side roll-forward. The PRD allows either; a producer emission is a never-widen pair, a read-side roll costs none. Recommendation: producer, to match Global and let the portal read the field.
3. DEPLOY ORDER: round 10's gold change fires 2026-10-16 13:30Z; one gold change per fire, so CN-s-1/s-2 cannot deploy before the 2026-10-17 13:30Z fire, and only after the 10-16 readback passes.
4. Never-widen pair for CN-s-1/s-2: count the writers of each moved leaf, both Cottonwood and Global objects, the Muni identity flag as the precondition, a rollback per key, the prior VersionId.
5. The portal PROD promote is client-facing and waits on Andrew; the cells end at DEV.

## Checks to dry-run at the base before the cut

Per `/dispatch` Step 2: each cell's criteria run against the base commit and must read red where the cell is not built (controls green). The month-end oracle (spec table) is the CN-s-3 arm; "0 of 497" is the CN-s-4 arm. Not yet written.
