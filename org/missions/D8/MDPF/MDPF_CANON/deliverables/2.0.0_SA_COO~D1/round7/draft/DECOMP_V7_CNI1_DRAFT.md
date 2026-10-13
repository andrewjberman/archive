# DRAFT -- NOT APPENDED. The v7 decomposition row for CN-i-1 (FWD-9), to be appended to `decompositions/MDPF_CANON_DECOMP.md` at the round-7 issuance, after
# the CTO's round-6 analysis. Written by a fork of 2.0.0_SA_COO~D1, 2026-10-13 ~19:5xZ.

| cell | serves (cell_refs) | candidate | owned files | depends on | actor |
|---|---|---|---|---|---|
| `CN-i-1` the AUA Trend (Global) groups its custom models into ONE 'Custom Models' series and names its two additive bands 'ETF Strategies' and 'ALT Strategies', all three in the Total Assets colours through one exported palette; no new served key, no served-object change (LOCAL: a portal DEV candidate; client-facing at the PROD push) | FWD-9 | portal / AUA Trend | `portal/src/components/CategoryViewTree.tsx` (export two symbols), `portal/src/lib/trendGrouping.ts` (new, pure), `portal/src/pages/ModelPortfolios.tsx` | none for the code; its data arm reads the folded global object, so the fold's first scheduled fire (2026-10-14 13:30Z) is read first | ~18 (worker-light) |

**Fan-out:** 1 of 1 chains, cap 8 beside CN-h-1 (no shared file: CN-h-1 owns `dim_mdpf_aggregate_aua_timeseries.py` and tests, this owns portal files); 2 of 2
independent chains if both are issued in one round. `portal_ref:` the portal `DEV` HEAD at the cut.

**What it is not (measured, carried to the CTO as the issuer's forks):** (1) the Client Supervised / Unsupervised chips (the portal serves no dated
category-views; 21 dated objects exist only in the gold tree), (2) the whole ETF Strategies group as a stacked series (the carve-out members sit inside
`non_model_aua`; drawing them double counts, and removing them is client arithmetic), (3) the ALT colour (Total Assets green400 against the 2026-10-01
vermilion pin). The cell cuts what a FIELD READ can carry today: Custom Models, and the two additive bands relabelled and recoloured.

**Close (carried to the CTO):** FWD-9 reads MET for the custom-model grouping when the rendered Global trend, from the folded object, shows one 'Custom
Models' series in the Total Assets Custom colour, the five canonical series unchanged, no 'Other Models' entry, the two bands named and coloured, and a
tooltip whose rows add to the Total on a sampled date; and PARTIAL (named) for the Client chips until a served history route or an as-of-only ruling.

**Checks:** `deliverables/2.0.0_SA_COO~D1/round7/checks/` (drafts at `round7/draft/checks/`). At base: `r7_cn_i_1.py module` 0/1 (the module is absent),
`page` 0/5, `data` 3/3 (a control: it grades the rule on the real served objects, 486 valued dates, 11 custom members, membership inside the served
Custom node). A scratch reference patch reads 6/6 and 5/5; three mutants (null coalesced to 0; a hex literal beside a group label; not Global-gated)
turn M2, P5 and P4 red (`r7_cn_i_1.py selftest` prints `ROUND 7 SELFTEST: OK`).
