# DRAFT -- NOT APPENDED. The v7 decomposition row for CN-i-1 (FWD-9, PRD v2.15 @567018c9e5), to be appended to `decompositions/MDPF_CANON_DECOMP.md` at the round-7
# issuance, after the CTO's round-6 analysis. Revised by a fork of 2.0.0_SA_COO~D1, 2026-10-13 ~20:0xZ (the full cell; the first draft cut "Variant A").

| cell | serves (cell_refs) | candidate | owned files | depends on | actor |
|---|---|---|---|---|---|
| `CN-i-1` the AUA Trend groups its custom models into ONE 'Custom Models' series (the fold's `other_models` replaced, every scope), draws the strategy groups in the Total Assets colours through one exported palette (ETF Strategies = pfde + the two carve-out SMA lines carved out of `non_model_aua`; ALT Strategies = `tax_additive_aua`, vermilion500 on the Trend; Client Supervised / Unsupervised chips AS-OF ONLY from the page's existing category-views object; Other AUA the true remainder), no served-object change, no new key (LOCAL: a portal DEV candidate; client-facing at the PROD push) | FWD-9 | portal / AUA Trend | `portal/src/components/CategoryViewTree.tsx` (two exports), `portal/src/lib/trendGrouping.ts` (new, pure), `portal/src/pages/ModelPortfolios.tsx` | -- (the Client chips' dated history waits on its own route cell) | ~18 (worker) |

**Fan-out:** 1 of 1 chains, cap 8 beside CN-h-1 (no shared file: CN-h-1 owns `dim_mdpf_aggregate_aua_timeseries.py` and tests, this owns portal files); 2 of 2
independent chains if both are issued in one round. `portal_ref:` the portal `DEV` HEAD at the cut.

**What it is not (the CTO's rulings, msgs 5086-5088):** the dated category-views history route (its own cell and pair, read-only over the existing dated
objects; FWD-9 grades with it live); any change to the ALT colour (vermilion500 stays, the pin test stands); any back-cast or interpolation; any firm-scope
carve-out or Client arithmetic (measured at Global only; firm scopes get the Custom Models grouping and the relabelled bands).

**Close (carried to the CTO):** FWD-9 reads MET for the series set and the sums when the rendered Global trend, from the folded object, shows the five canonical
series unchanged, ONE 'Custom Models' in the Total Assets Custom colour and no 'Other Models', 'ETF Strategies' (pfde + carve-outs) in the Total Assets colour,
'ALT Strategies' (`tax_additive_aua`) in vermilion500, on the as-of date the Client chips and a true-remainder Other AUA, on the other dates one Other AUA and no
Client segment, no '-$0', and a stack that adds to `opal_aggregate_aua` to the cent (the fold's suppressed dates excepted, read from the fold's record); and
PARTIAL (named) for the Client chips until the history route cell lands: the draw arms B (2026-08-27) and the dated middle of the axis wait for it.

**Checks:** `deliverables/2.0.0_SA_COO~D1/round7/checks/` (drafts at `round7/draft/checks/`). At base: `r7_cn_i_1.py module` 0/1 (the module is absent), `page`
2/8 (P6 and P8 are controls that hold), `data` 5/5 (it grades the SERVED inputs: the stack to the cent on 486 valued dates, the Client gap equal to the carve-outs
on 21 of 21 same-date objects; a control, not a build test). A scratch reference patch reads module 9/9 and page 8/8; four mutants (null coalesced to 0; a hex
literal beside a group label; the grouping gated on Global; ALT recoloured from Total Assets) turn M2, P5, P4 and P6 red (`r7_cn_i_1.py selftest` prints
`ROUND 7 SELFTEST: OK`).
