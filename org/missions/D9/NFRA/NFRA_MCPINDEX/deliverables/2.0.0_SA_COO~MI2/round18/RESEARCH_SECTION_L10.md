# NFRA_MCPINDEX round 18 -- workstream RESEARCH -- section for the one L10 slug

**By** `2.0.0_SA_COO~MI2`, 2026-10-16 ~09:3xZ. **For** `2.0.0_SA_COO~MI`, who sends the single round-18 slug (msg 34807) and cites this file by path and hash. Seated by `0.0.0_AB_MSTR~Z` on Andrew-direct ~18:4xZ 2026-10-15; finish line (PRD v0.17 @532d1e68bb, CONTRACT C-GROUP): every in-scope row carries C-GROUP and a live `read_tool`, by 2026-10-16 ~22:00Z.

## 1. The finish-line condition, measured

`C30_CATALOG=C:/tmp/mi-final/DATA_CATALOG.final.yaml` (md5 9519ebce3a1b92cee07a5507d1912dd3, emitted by `2.0.0_SA_COO~MI` on HEAD 76eb302faf with my landing 58660556d3, deployed commit 3d5c9c8bf1, N=127 tools) through `bash org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/2.0.0_SA_COO~MI2/round18/checks/c30.DRAIN.sh`: **RESULT PASS**, 9 of 9 checks. Denominator: 144 research-set rows (78 harvest, 5 portal_datasets, 61 silver), 136 rows outside the set. Counted from the same file with the check's own `in_set`: **144 of 144 research-set rows carry a `read_tool`; 0 null**; 0 carry `nl_tags_basis: inferred`; the 34 excluded entities are not rows. The tools are live: OG-ap-23 deployed at 3d5c9c8bf1, `CODE_SERVED.json` served 27 of 27 added tools, ledger closed 09:21:54Z (msg 34882).

**Re-graded on the v2 catalog (2026-10-16 ~11:2xZ).** `2.0.0_SA_COO~MI` re-measured depth and freshness (the r15 catalog failed `r13.AC3` on one stale claim, `2c9cabebe5`) and placed catalog v2 (blob 4c27b28171, md5 983464f80adc45ac51f1f3eebbdf2001; `58ae2c5417`; CTO half `b8b3d0bd30`: a freshness-only diff). `c30.DRAIN.sh` on the tracked `DATA_CATALOG.yaml` at HEAD, which is that blob: **RESULT PASS**, the same 144 research-set rows, **read_tool null 0** (280 rows in all, 188 with a `read_tool`). The first final catalog above (md5 9519ebce...) is superseded by v2 for the live release; the live host holds `0cb4a87bcb` (blob cf7616c08e) until the v2 apply under the MX-r-15 ledger.

## 2. The orders (all complete and merged; each re-graded by the issuer on the merged tree)

| order | what | merge / commit | grade at close |
|---|---|---|---|
| MX-c-30 | the two advisor-intelligence rows out; `--scope-exclusions` | 5dad340056 | c30.AC1 and AC2 (AC1 pinned the old 214 and is superseded by c38.AC1) |
| MX-c-34 .. -37 | curated tags for the 37 `inferred` RESEARCH rows (32 harvest, 5 portal), four `--group-map` files | abaefd2c81, d59c86de1a, 31ddf6afe8, f5fa108fae; flips 23b89ba47f | ct.h1/h2/h3/p1 PASS; drain: 0 inferred |
| MX-c-31 | the generator's `--read-links`; the deployed link wins over a contract proposal (amended 4982e4190c) | 023d944a80 | c31.AC1, AC2 (34 of 34 with the future list), AC3 (21 tests) |
| MX-c-38 | `--entity-exclusions` and the row removals | fa3ca5c401 | c38.AC1 (entities 34, fresh rows 180), AC2 (8 tests) |
| landing | 67 row files take their links on the census of the live release (28 RESEARCH, 39 ASSETS); `read-links applied: 65 of 65` | 58660556d3 | c40.landed PASS |

Workers: `0.9.0_WK_NFRA_MCPINDEX~50, ~52..~57` (haiku, one worktree each). Fan-out: 5 of 5 chains, cap 8 (first issuance dfabd4baff); 1 of 1 (c21cb3ce28); 1 of 1 (93cac2e41b). Direct acts (LOCAL, under the size floor): the exclusions of the CTO-ratified rows 7d7e8b2b94, 437cdc9ecf, 623dc1f9ae; link and tool-list data edda93dcca, 2b1d542901.

## 3. Rows ruled out of the finish line (34), each with its reason class

`entity_exclusions.json` (reason classes) and `research_no_tool_dispositions.md` (full reasons) in this folder. CTO rulings: @32a4dd88dd (29 of 32 ratified, 3 amended), msg 34673 / @131991960e (harvest_articles, market_updates, semantic_news_trending_daily), msg 34700 / @d97ea3ae82 (ai_classified_securities, provenance_input), msg 34712 / @e4a5d0d18c (model_portfolios_views, harvest_security_metrics). `benchmark_returns` is recorded `held_at_andrew` and reopens on his word. Reopen conditions: the table holds items again; the producer is back inside the frontier; the AMGT_HARVST tool ships (harvest_security_metrics, link it then). Open owed items outside the line, owner NFRA_OPLGTW (`2.0.0_SA_COO~O`): the DynamoDB etf-classifications table (needs a census and a grant; CTO @d97ea3ae82 section 2).

## 4. Surprise rows

13 worker rows of ~50, ~52..~57 are disposed by one seat row, `NFRA_MCPINDEX-Z-S125` @83761c1376 (DISMISSED_WITH_REASON, adjudicates all 13; includes the two BLOCKING rows Z-W53-S2 and Z-W55-S2, disarmed by the issuer's status flips). `comp-surprise --project NFRA_MCPINDEX` read none of my workers' rows open after it. One finding for the CTO's round analysis, the issuer's own drafting: an order's step-2 command and step-0 control must be dry-run in a SPARSE worktree at the cut, not only at the base (the 8-versus-12 planted arms in three faces; MX-c-31 step 2 without `--read-links`; MX-c-38 step 2 pinned 214; a step-0 pytest control that cannot pass on a sparse cone; a status flip outside the worker's `<paths>`).

## 5. What this section does not claim

It does not grade the ASSETS workstream, TO-MX-c-23 or TO-MX-r-15 (the other issuer's). Measured for the round: `python .tools/round-close-check.py --project NFRA_MCPINDEX --round 18` at 09:3xZ reads `orders=11`, 9 complete, 2 not complete and outside the verdict (TO-MX-c-23, TO-MX-r-15), `proof_ok=9 proof_bad=0`, **verdict=MAY-CLOSE**; at 05:2xZ it read REFUSED on a PROOF-BAD TO-MX-c-23. The quality of the curated words is a sample of 16 tag sets read by the issuer (plain words, none states a fact the row does not carry); the CTO reads it at the Z-C-S61 close. No judgment criterion is declared in any RESEARCH order, so no round-close grade by the CVO is owed on them.

## 6. Push state (measured 09:3xZ)

`git ls-remote origin box/sitez` reads 365b8c133a; it contains 83761c1376 and 623dc1f9ae (earlier commits of this section) and does NOT yet contain 58660556d3 (the landing): LOCAL until the box's scheduled `box-sync` pushes it.
