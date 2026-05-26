<task_order>
<metadata>
  <to_id>ADHC_COMPIL_V5.002</to_id>
  <project>ADHC_COMPIL_V5</project>
  <title>Fix 2: comp-pipescript io Lambda-side coverage extension (~5-8h; sequential post-TO-001)</title>
  <assigned_to>0.7.0_AE_CloudOps</assigned_to>
  <issued_by>2.0.0_SA_COO</issued_by>
  <issued_date>2026-05-26</issued_date>
  <status>pending</status>
  <priority>HIGH (CVO Wave 2; LD-0097 §A north-star operationalization)</priority>
  <references>
    <ref type="prd">docs/architecture/ADHC_COMPIL_V5.md v0.1 commit `701103ccf` (1.0.0_SA_CTO; PRD §6 TO-002).</ref>
    <ref type="predecessor">TO-001 SHIPPED `6ffc457d5` 2026-05-26 ~16:15Z (~30min wall; ~6-10x faster than PRD est; AC1-AC6 MET; EC2 services 1→8; cloudfront:CreateInvalidation MATCHED on bd-exporter + inf-gold-layer roles).</ref>
    <ref type="empirical_anchor">DS 0.1.0 YALP_MKTOVR.001 brief §11 Level-1 mapping (market-overview-tiered-generator + yang-ingest-dynamodb + others) is the ground-truth oracle for AC2 (Fix 2 reproducibility).</ref>
  </references>
  <dependencies>
    <dependency>TO-001 SHIPPED ✓ — TO-001 parse-pattern reference benefits this TO per CVO Wave 2 sequencing.</dependency>
  </dependencies>
</metadata>

<scope>
Per PRD v0.1 §6 TO-002:

Extend `comp-pipescript io <script>` graph schema to index Lambda-source pipeline scripts under `infra/aws/lambda/**/lambda_function.py` (alongside existing `data/*/scripts/gold/**` BD-gold corpus). Same IO-column-gap + portal-consumer detection semantics; same `comp-build` rebuild path.

**Net-new graph node-class:** `lambda_pipeline_script` per PRD §3.5. Queryable via existing `comp-trace` + `comp-blast` traversal.

**Empirical anchor for AC2:** DS 0.1.0 YALP_MKTOVR.001 brief at `docs/briefs/yalp_mktovr_market_overview_field_comparison_2026-05-22.md` §11 Level-1 mapping table. Post-extension, `comp-pipescript io infra/aws/lambda/v2_portal/01_market_overview/market-overview-tiered-generator/lambda_function.py` should reproduce that brief's column-gap + portal-consumer enumeration.
</scope>

<acceptance_criteria>
- AC1: `comp-pipescript io infra/aws/lambda/v2_portal/01_market_overview/market-overview-tiered-generator/lambda_function.py` post-extension returns COLUMN GAPS + PORTAL CONSUMERS + S3-DYNAMIC reads.
- AC2: DS 0.1.0 YALP_MKTOVR.001 brief §11 Level-1 mapping table reproducible from `comp-pipescript io` on market-overview-tiered-generator + yang-ingest-dynamodb + others (ground-truth oracle per CVO brief §3 Fix 2 acceptance candidate).
- AC3: BD-gold scope NOT regressed (regression-test sample: `comp-pipescript io data/black_diamond/scripts/gold/<sample>.py`).
- AC4: `comp-build` runs clean (no parser errors on Lambda-source files).
- AC5: New `lambda_pipeline_script` node-class queryable via existing `comp-trace` + `comp-blast` traversal.
- AC6: comp-tools.yaml V5.002 note appended per CLAUDE.md "Compiler Tools" canonical surface.
</acceptance_criteria>

<compiler_tools_mandate>
**Phase 1 (before write):** `comp-build` baseline; capture pre-extension graph state for AC3 regression-test.

**Phase 2 (during impl):** Per PRD §5 (parser extension + graph node-class addition + traversal extension). Reuse TO-001 parse-pattern reference per CVO Wave 2.

**Phase 3 (after commit):** `comp-build` post-extension; AC2 reproducibility test against YALP_MKTOVR.001 brief; regression-test sample on BD-gold script (AC3).
</compiler_tools_mandate>

<cross_domain_coordination>
- **TO-VAL composite regression** (sequential post-Fix 1+2+3) — last in chain; folds 7+ Sub-class Y fires + AE 0.6.1 IAM additions + DS 0.1.0 YALP_MKTOVR Level-1 mapping (this TO's empirical anchor) as worked-example acceptance evidence; updates comp-tools.yaml + CLAUDE.md "Compiler Tools" section.
- **TO-003 Fix 3 comp-registry sync** (CTO direct, deferred next session per capacity) — parallel-compatible with TO-002; no AE 0.7 coordination needed.
- **AE 0.6.1 follow-on candidate (C2 v1.3 scope-filter)** — non-blocking; queued after ADHC_COMPIL_V5 chain.
</cross_domain_coordination>

<expected_evidence>
- Commit hash for comp-pipescript Lambda-side extension + new graph node-class
- `comp-pipescript io market-overview-tiered-generator` post-extension output (showing COLUMN GAPS + PORTAL CONSUMERS)
- AC2 YALP_MKTOVR.001 brief §11 reproducibility evidence
- BD-gold regression-test pass
- comp-tools.yaml V5.002 note
- Session log with archetype IMPLEMENT
</expected_evidence>

<notes>
**Sequential per CVO Wave 2:** benefits from TO-001 parse-pattern reference. Your TO-001 fast-lane ~30min suggests this TO may also compress significantly below 5-8h estimate if reuse holds clean.

**Empirical pull-validation continues:** Fix 1 + Fix 2 + (deferred Fix 3) close the 3-fire convergence at concrete fix-scope. LD-0097 §A north-star operationalization in flight.

**4th compiler-tool R&D candidate** (DE 0.4 tool-gap finding: comp-graph multi-"index" component-name collision) banked for ADHC_COMPIL_V5 v0.2 OR separate v6 — CTO + CVO disposition pending; not blocking this TO.

**Pre-existing mdpf-daily-trigger gap surfaced by TO-001 AC4** (Lambda role missing s3:GetObject + s3:PutObject for aws s3 cp invocation at lambda_function.py:76) — flagging for separate AE-side fix-TO consideration on mdpf-pipeline lane. ~30min effort; non-blocking on this TO.

Architectural questions / PRD scope → ws CTO (1.0.0_SA_CTO). Dispatch / RAVC2 / blockers → me.
</notes>
</task_order>
