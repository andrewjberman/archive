<task_order>
<metadata>
  <to_id>ADHC_COMPIL_V5.001</to_id>
  <project>ADHC_COMPIL_V5</project>
  <title>Fix 1: comp-iam service EC2-role coverage extension (~3-5h)</title>
  <assigned_to>0.7.0_AE_CloudOps</assigned_to>
  <consult>0.6.1_AE_PartnerETL</consult>
  <issued_by>2.0.0_SA_COO</issued_by>
  <issued_date>2026-05-26</issued_date>
  <status>complete</status>
  <shipped>2026-05-26T~16:15Z; commit `6ffc457d5`; AC1+AC2+AC3+AC4+AC5+AC6 all MET; EC2 services 1->8 (bd-allocations + bd-assets + bd-fees + bd-price-runner + bd-transactions on bd-exporter-ec2-role + demo-transform-runner + moltbot + preserved bd-gold-runner); underscore↔dash normalization in cmd_service; cloudfront:CreateInvalidation verified MATCHED on bd-exporter-ec2-role (AC1) + inf-gold-layer-ec2-role (AC2); Lambda baseline preserved (AC3 via bd-portal-publisher); 2 pre-existing gaps surfaced (AC4); py_compile clean (AC5); comp-tools.yaml V5.001 note (AC6). ~30min wall TO start -> RAVC2 ready (PRD est ~3-5h; ~6-10x faster).</shipped>
  <priority>HIGH (3-fire convergence empirical anchor + LD-0097 §A north-star operationalization)</priority>
  <references>
    <ref type="prd">docs/architecture/ADHC_COMPIL_V5.md v0.1 commit `701103ccf` 2026-05-26 (1.0.0_SA_CTO; PRD chartered per Andrew direct → CVO brief `92b198aac` → CTO charter). Full §3 dispositions + §5 compiler mandate + §6 TO-001 block.</ref>
    <ref type="empirical_anchor">AE 0.6.1 surfaced today (cycle ADHC_CDNCOHT.001-INTERIM) — `comp-iam service` Lambda-only blocked EC2-role IAM audit; manual terraform grep + role-to-EC2 cross-ref workaround used to land `cloudfront:CreateInvalidation` on bd_exporter + inf_gold_layer roles (commits `b00e2733e` INF + `053bba6f7` BD).</ref>
    <ref type="sister_fixes">TO-002 Fix 2 comp-pipescript Lambda-side extension (AE 0.7 lane; sequential Wave 2) + TO-003 Fix 3 comp-registry sync (CTO direct; parallel-compatible).</ref>
  </references>
  <dependencies>
    <dependency>AE 0.7 critical-path: LEDGEH + CDNCOHT TO-VAL SHIPPED `526074077` ✓ (just-ratified). Lane clear for ADHC_COMPIL_V5 sequence.</dependency>
    <dependency>AE 0.6.1 co-consult availability — KEEP-EPHEMERAL standby; ~30min-1h handoff window for empirical-context transfer (today's manual IAM additions pattern reference).</dependency>
  </dependencies>
</metadata>

<scope>
Per PRD v0.1 §6 TO-001:

Extend `comp-iam service <name>` to accept **EC2 instance roles** alongside existing Lambda execution roles. Parse `aws_iam_role_policy` + `aws_iam_role_policy_attachment` blocks from `infra/aws/terraform/{pipeline}/iam.tf` for EC2 roles (bd_exporter, inf_gold_layer, bd-gold-runner, demo-transform-runner, future). Surface `Action` set per role; cross-check against discovered boto3 calls in `data/*/scripts/**` + `infra/aws/ec2/**`. Output table matches Lambda-side format (MATCHED / MISSING / EXTRA).

**Co-consult with AE 0.6.1** at start (~30min): empirical context handoff from today's manual EC2-IAM additions (bd_exporter + inf_gold_layer roles, `cloudfront:CreateInvalidation` Sid block pattern) — pattern reference for parser implementation. AE 0.6.1's terraform-grep + role-to-EC2 cross-ref workaround pre-this-extension is the worked-example AC anchor.
</scope>

<acceptance_criteria>
- AC1: `comp-iam service bd_exporter` post-extension returns full IAM action set including `cloudfront:CreateInvalidation` MATCHED (added today via `053bba6f7`).
- AC2: `comp-iam service inf_gold_layer` post-extension returns full IAM action set including `cloudfront:CreateInvalidation` MATCHED (added today via `b00e2733e`).
- AC3: Lambda-services parsing path NOT regressed (regression-test sample: `comp-iam service shared-advisor-router-response` returns expected baseline; sister CDNCOHT TO-001 ship `0a9c90b16` reference).
- AC4: `comp-iam gaps` post-extension covers EC2 roles alongside Lambda roles (cross-product gap detection).
- AC5: `comp-build` runs clean (no parser errors on EC2-role-bearing TF files).
- AC6: Documented role-coverage table appended to `org/modules/graph/comp-tools.yaml` per CLAUDE.md "Compiler Tools" canonical surface (consumed by TO-VAL composite update).
</acceptance_criteria>

<compiler_tools_mandate>
**Phase 1 (before write):** `comp-build` baseline run — confirm pre-extension graph state; capture before-snapshot for AC5 regression-test.

**Phase 2 (during impl):** Per implementation steps in PRD §5 (parser extension + cross-product gap detection + regression-test pattern). No new external compiler tools needed; this TO IS the compiler-tool extension.

**Phase 3 (after commit):** `comp-build` post-extension; `comp-iam gaps` exercise; regression-test sample on `shared-advisor-router-response` (Lambda-side baseline).
</compiler_tools_mandate>

<cross_domain_coordination>
- **TO-002 Fix 2 sequential post-this-ship per CVO Wave 2** — `comp-pipescript io` Lambda-side extension benefits from your TO-001 parse-pattern reference. I dispatch TO-002 GO when this TO RAVC2-Accepted.
- **TO-003 Fix 3 (CTO direct, deferred next session per CTO capacity)** — parallel-compatible with TO-001; runs in CTO's own lane; no AE 0.7 coordination.
- **TO-VAL composite regression** — last in chain; folds 5 historical Sub-class Y fires (now 7+ today) + AE 0.6.1 IAM additions (this TO's AC anchor) + DS 0.1.0 YALP_MKTOVR Level-1 mapping (Fix 2 anchor) as worked-example acceptance evidence; updates comp-tools.yaml + CLAUDE.md "Compiler Tools" section.
- **AE 0.6.1 co-consult** — empirical context handoff at start (~30min); AE 0.6.1's manual IAM patterns from today are the worked-example reference; no rework on AE 0.6.1 side.
</cross_domain_coordination>

<expected_evidence>
- Commit hash for comp-* tool extension + parser code + regression-test scaffold
- `comp-iam service bd_exporter` post-extension output (showing cloudfront:CreateInvalidation MATCHED)
- `comp-iam service inf_gold_layer` post-extension output (same)
- Lambda-side regression-test pass evidence
- comp-tools.yaml update banked (or queued for TO-VAL composite update)
- Session log with archetype IMPLEMENT
</expected_evidence>

<notes>
**CVO PRE-EXECUTION pre-propagate gate expected** per inaugural pattern `d12028652` (YALP_MKTOVR). I'll route CVO when this TO drafts to gate dispatch; CVO can fire PRE-EXECUTION verdict before AE 0.7 starts (~30min CVO turn-around).

**3-fire convergence empirical density continues climbing today** — 7 Sub-class Y fires + 2 self-correction-upstream-of-verify-channel fires across 3 distinct projects in <3h wall = continuous empirical pull-validation of LD-0097 §A north-star (language/file-agnostic systems-wide graphing+traversal for AI agents). This TO's ship is the operational expression of that north-star at concrete fix-scope.

**Sequencing context (your queue):** TO-001 (this; ~3-5h) → TO-002 Fix 2 (~5-8h sequential) → TO-VAL (~1-2h sequential post-Fix 1+2+3). Total AE 0.7-lane effort ~9-15h after this dispatch; TRSB_LEDGER + AE 0.6.1 C2 v1.3 follow-on stay queued behind ADHC_COMPIL_V5 chain.

**AE 0.7 fast-lane potential:** today's record sub-tick fast-lane (~30min RAVC2-ACCEPT → next-TO ship for CDNCOHT TO-001 + ~6min wall for CDNCOHT.VAL) suggests TO-001 may compress significantly below 3-5h estimate if scope holds clean.

Architectural questions / PRD scope → ws CTO (1.0.0_SA_CTO). Dispatch / RAVC2 / blockers → me.
</notes>
</task_order>
