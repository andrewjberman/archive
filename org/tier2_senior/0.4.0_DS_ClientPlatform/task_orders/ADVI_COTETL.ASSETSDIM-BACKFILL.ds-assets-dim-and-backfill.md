<to_id>ADVI_COTETL.ASSETSDIM-BACKFILL</to_id>
<project>ADVI_COTETL</project>
<title>Daily cot assets_dim (port inf pattern) + full backfill from 04-22 (realized gap + feasibility-probed snapshot lookback) + probe-script fix</title>
<assigned_to>0.4.0_DS_ClientPlatform</assigned_to>
<issued_by>2.0.0_SA_COO (decompose of CVO scope cb62104b1; Andrew-direct "do all")</issued_by>
<issued_date>2026-06-22</issued_date>
<status>complete -- SPRING-CLEAN 2026-08-25: closed WITH its project ADVI_COTETL, which was closed the same day for having no directive attachment. Closed as a record act, not a work verdict; the work is recoverable by re-minting the project. Prior status: active</status>
<!-- GATED on AE's fresh-session signal (ADVI_COTETL.BACKFILL.ae-session) -- all live pulls/builds need the live session. NOT COT-launch-gating (parallel). DS-paced after the session lands. Full scope + findings: cb62104b1. -->

<context>
Andrew-direct ("do all"): a first-class daily cot assets_dim + a full backfill from the 04-22 onboarding ceiling. CVO grounded the reassuring finding: the null MV/Units on Andrew's manual Assets_Dim re-download = a BD-UI-context artifact (a raw re-download drops the date+activity context), NOT a data problem -- the PIPELINE silver/holdings has MV/Units POPULATED (1.7% null=cash) + is the $395.30M AUA source. Full scope: cb62104b1 sec 2-4.
</context>

<work_A_assets_dim>
Stand up a first-class daily cot `assets_dim` (per-account x per-asset positions: MV, Units, asset attributes) as a NAMED ETL table (not just the implicit holdings feed):
- Port inf's pattern: data/inf/manual_api/create_assets_dim_query.py + data/inf/scripts/silver/build_assets_dim.py -> cot, sourced from the existing Assets_Dim/holdings template 226355. ENSURE activityOptionId=1 (Ending MV) so MV/Units populate (the artifact-vs-pipeline-null lesson).
- OPTION (your call): also a deduped GOLD securities-master dim (one row per AssetID: ticker/cusip/name/asset-class/expense-ratio/cash-equiv) if a true asset-attribute DIM is wanted alongside the positions table -- include if cheap/clean this pass, else flag as a fast-follow (don't block Work-A core on it).
</work_A_assets_dim>

<work_B_backfill>
Full backfill from 04-22 (per cb62104b1 sec 3):
- transactions: HAVE (04-22->06-18) -- no action.
- realized: BACKFILL the GAP 05-04->05-31 (qt3, Custom + date-range; PIT-feasible -- 402 sell-side txns confirmed in-window, realized currently only 06-01->06-17).
- holdings/assets_dim, allocations (qt5), unrealized (qt4): FEASIBILITY-PROBE the historical snapshot lookback FIRST (Custom + past dates + activityOptionId=1), THEN backfill what works. Banked caveat: the holdings export pins to CurrentDay -> lookback may return current-day (Andrew: holdings worth-trying; alloc/unrealized likely current-state-only/not-PIT). NO SILENT CAPS -- document what is NOT lookback-feasible (so "backfilled" never overstates coverage).
- FIX the probe script data/cot/scripts/bronze/cot_backfill_date_probe.py BEFORE use: dateRangeType="DateRange"+ISO (400s) -> "Custom"+MM/DD/YYYY (the proven S3-template form).
</work_B_backfill>

<compiler_tools_mandate>
  <step><run>comp-which-first for every search/inspection; comp-pipescript io / comp-blast on the touched cot scripts</run><expect>estate-context + consumers before edit (Rule 21/22)</expect></step>
  <step><run>ds-commit-gate (py_compile + ds-precommit-check + ruff FA) per touched .py; from __future__ import annotations</run><expect>PASS; firm-sep cot (safe-deploy PIPELINE_MAP=cot; bd/49F zero-touch)</expect></step>
</compiler_tools_mandate>

<acceptance_criteria>
1. Daily cot assets_dim lands as a named table, MV/Units POPULATED (the pipeline value, not the UI-download null), reconciles to holdings/the $395.30M AUA. (+ the gold securities-master dim if built.)
2. realized backfilled 05-04->05-31 (PIT, sells confirmed); earliest-realized-date now ~05-04.
3. holdings/alloc/unrealized lookback feasibility-probed + backfilled-what-works; what's NOT feasible DOCUMENTED (no overstated coverage).
4. cot_backfill_date_probe.py fixed (Custom+MM/DD/YYYY) + proven.
5. Firm-separated (cot-tree only); ds-commit-gate PASS; served firm-AUA UNCHANGED at $395.30M (this is additive dim+backfill, must not move the certified number -- verify on the next nightly's served, no ad-hoc gold run for validation).
6. GATED: do not start live pulls until AE signals the fresh BD session. RAVC2 COO + CVO as each piece (assets_dim / realized / lookback-probe) lands; CVO verifies each.
</acceptance_criteria>

---
**RECONCILED-COMPLETE 2026-06-23** (COO /drive 132528Z): WORK A (A_05 assets_dim cbbbefb01 + 56-date backfill + nightly-chain 2ab5124dc) + WORK B (realized/txn/unrealized/allocations per-day backfill); CVO-verified 06-23. DONE.
