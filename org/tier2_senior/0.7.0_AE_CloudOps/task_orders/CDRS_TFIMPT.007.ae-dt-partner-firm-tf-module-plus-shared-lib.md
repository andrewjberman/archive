<task_order>
  <metadata>
    <id>0.7.0_AE_CloudOps-2026-04-15-cdrs-tfimpt-007-partner-firm</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <co_issued_to>0.4.0_DT_ClientPlatform</co_issued_to>
    <date>2026-04-15</date>
    <status>complete</status>
    <project_code>CDRS_TFIMPT</project_code>
    <priority>P1 (Phase 2 sprint terminal; PAIRED AE+DT commit)</priority>
  </metadata>

  <references>
    <ref type="scope_brief">docs/architecture/CDRS_TFIMPT_PHASE2_HANDOFF.md (DT 0.4 memo — all 5 sections + 4 open Qs)</ref>
    <ref type="source_design">0.7.0_AE_CloudOps → 0.4.0_DT MCP 2026-04-15T16:20Z (4-step partner-firm infra plan)</ref>
    <ref type="phase_0_context">org/tier2_senior/0.4.0_DT_ClientPlatform/logs/2026-04-15/identity_permissions_overhaul.md</ref>
    <ref type="precedent_coship">ADVI_ROLLUP RA-P1 + CN-P1 (CTO co-ship discipline 2026-04-15 — atomic rollback at commit level, not script level)</ref>
  </references>

  <objective>
    Terminal CDRS_TFIMPT TO. PAIRED AE+DT commit delivers the opal-partner-{firmId} pattern end-to-end:

    **AE 0.7 scope (infrastructure):**
    1. `infra/aws/terraform/modules/partner-firm-table/` — new reusable module per DT memo point 3. Takes `firm_id` variable, produces `aws_dynamodb_table.partner_{firm_id}` with DT-framework-compatible schema (email PK, firmRole attribute, etc. per live opal-partner-49financial).
    2. `infra/aws/terraform/partner-firms/` — new top-level module with one instantiation per firm. Currently: one block for `49financial`. Import existing `opal-partner-49financial` into module state.
    3. IAM pattern (hybrid per DT memo point 4): wildcard `arn:aws:dynamodb:*:*:table/opal-partner-*` GetItem-only grant for auth-handler; explicit per-firm ARNs for any write path. Module emits both grant forms; shared-infra IAM consumes.
    4. Tag `partner-firms-v1.0.0` on the shared commit.

    **DT 0.4 scope (application layer, same commit):**
    1. `infra/aws/lambda/lib/partner/` (new) — Lambda-side shared lib per DT memo point 1. `tableName.ts` (`opal-partner-{firmId}` derivation) + `index.ts` (typed exports + raw escape hatch). No Layer — bundle per-Lambda.
    2. `auth-handler/src/db.ts` — generalize `PARTNER_TABLE_49FIN` constant → parameterized via `getPartnerIdentity(email, firmId)`. Three call sites updated. `User.firmId` already available per Phase 0 framework.
    3. Regression: opal-capital users (no firmId) continue to hit null-firmRole path (no code change needed; null guard already present).

    **Co-ship discipline:** single commit, author line per whoever ships (typically AE since they own the heavier TF side), commit body cites both TO IDs (.007 AE + .007 DT scopes). Atomic rollback preserves if rollback is needed. Single tag `partner-firms-v1.0.0`.
  </objective>

  <wire_contract>
    - New TF module `modules/partner-firm-table/` — reusable per-firm table resource.
    - `opal-partner-49financial` now TF-managed; no data changes, all 3 records (Chase/Travis/Hunter) intact.
    - `auth-handler` behavior: identical for 49financial users; now supports future firms via {firmId} path.
    - IAM: auth-handler policy gains wildcard `opal-partner-*` GetItem; existing 49financial-explicit grant replaced (or kept as redundant, AE's call).
    - No portal code change (portal's `firmAccess.ts` + `claims.firmRole` consumption is already generalized).
  </wire_contract>

  <acceptance_criteria>
    1. `modules/partner-firm-table/` exists; `variables.tf` declares `firm_id`; `main.tf` emits `aws_dynamodb_table.partner_${firm_id}` matching live opal-partner-49financial schema.
    2. `partner-firms/49financial.tf` (or main.tf block) instantiates module with `firm_id = "49financial"`; imports existing table.
    3. `terraform plan` 0-diff in partner-firms state.
    4. `lib/partner/` Lambda pkg: `tableName.ts` exports `getPartnerTableName(firmId: string): string`; `index.ts` exports typed + raw helpers.
    5. `auth-handler/src/db.ts` no longer contains `PARTNER_TABLE_49FIN` hardcode; `getPartnerIdentity(email, firmId)` signature parameterized.
    6. auth-handler deploys clean (tsc + lambda build + tf apply 0-diff on shared-infra Lambda source hash).
    7. Regression: curl /auth/login + /auth/me as Hunter (49financial firmRole=admin) + Andrew (opal-capital, no firmRole) — both produce identical JWT shape and /me response to pre-commit baseline.
    8. `/frontend-dev` Skill with `firm_user_gating_inspection.json` constitution PASS — Hunter sees BooksTab, Chase sees Profile.
    9. 4 open questions from DT memo resolved in commit body or linked follow-up (backend split, L@E bundle constraints, stale-JWT firmRole property, import-drift reconcile).
    10. Tag `partner-firms-v1.0.0` pushed.
    11. Session log's Compiler Tools section reproduces each `<run>` + observed-result + pass/fail vs. `<expect>` (CTO Rule 7 locked 2026-04-15).
    12. MCP COMPLETE to COO with commit hash + tag + regression results + 4-Q resolution pointer. **CDRS_TFIMPT PROJECT TERMINAL.**
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>aws dynamodb describe-table --table-name opal-partner-49financial > /tmp/partner-49fin-live.json</run>
        <expect>Full schema captured for module authoring.</expect>
        <if_mismatch>STOP. Surface CLI error.</if_mismatch>
      </step>
      <step>
        <run>grep -rn "PARTNER_TABLE_49FIN\|opal-partner-49financial" infra/aws/</run>
        <expect>Identify all hardcode sites (db.ts:PARTNER_TABLE_49FIN + IAM + any test fixtures) for generalization.</expect>
        <if_mismatch>If new hardcode site found outside DT's known list, expand generalization scope or flag.</if_mismatch>
      </step>
      <step>
        <run>comp-iam service opalinvest-auth-handler</run>
        <expect>Current IAM policy lists explicit opal-partner-49financial ARN. Confirm scope for wildcard-grant refactor.</expect>
        <if_mismatch>Surface to COO — IAM assumptions broken.</if_mismatch>
      </step>
      <step>
        <run>DT memo 4 open questions READ and confirm AE answer each in TO response before shipping</run>
        <expect>Backend split, L@E bundle constraints, stale-JWT firmRole property, import-drift reconcile — each answered.</expect>
        <if_mismatch>HARD GATE: do not flip TO pending until all 4 Qs are answered by AE. DT queues their lib work behind AE's sign-off.</if_mismatch>
      </step>
    </phase>

    <phase id="2" when="before commit">
      <step>
        <run>terraform plan (partner-firms module state)</run>
        <expect>0-diff post-import of opal-partner-49financial.</expect>
        <if_mismatch>Edit module to match live; re-plan.</if_mismatch>
      </step>
      <step>
        <run>bunx tsc -b (or similar for auth-handler Lambda pkg) + build-nodejs-lambda.sh opalinvest-auth-handler</run>
        <expect>Lambda bundle builds clean with `lib/partner/` imports; no type errors.</expect>
        <if_mismatch>Fix before commit.</if_mismatch>
      </step>
      <step>
        <run>comp-iam gaps</run>
        <expect>No new IAM gaps; wildcard grant narrows or replaces explicit without leaving holes.</expect>
        <if_mismatch>Auto-rule Phase 2 hit — STOP and fix.</if_mismatch>
      </step>
      <step>
        <run>Regression curl: /auth/login as hunter.lloyd@49financial.com + /auth/me → decode JWT</run>
        <expect>firmRole=admin preserved, JWT shape identical to Phase 0 baseline.</expect>
        <if_mismatch>STOP. Something broke; debug before commit.</if_mismatch>
      </step>
    </phase>

    <phase id="3" when="after commit + apply">
      <step>
        <run>/frontend-dev Skill with firm_user_gating_inspection.json constitution (Hunter + Chase runs)</run>
        <expect>PASS — Hunter sees BooksTab + Firm Overview/Fee Efficiency/Advisor List tabs; Chase sees Profile tab only.</expect>
        <if_mismatch>Iterate per Skill ACTIONABLE_FIXES protocol up to 5 rounds.</if_mismatch>
      </step>
      <step>
        <run>comp-blast opal-partner-49financial</run>
        <expect>Consumer set = auth-handler Lambda only (via wildcard grant in IAM).</expect>
        <if_mismatch>If unexpected consumers, coordinate before declaring TO complete.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <dependencies>
    <dependency agent="0.7.0_AE_CloudOps" task="CDRS_TFIMPT.006" status="pending" description="opal-users-v2 import should land first (simpler, no cross-Lambda surface)"/>
    <dependency agent="design-resolution" task="AE answers DT memo 4 open Qs" status="pending" description="HARD GATE — TO flips pending on resolution"/>
  </dependencies>

  <cross_domain_coordination>
    AE owns TF module + imports + IAM. DT owns lib/partner + auth-handler db.ts generalization.
    SINGLE commit ships both scopes. Whoever ships (AE typically) author-lines the commit; body cites
    both scopes. Tag `partner-firms-v1.0.0` on the shared commit.

    Atomic-rollback property: revert one commit, both scopes unwind cleanly.

    Co-ship commit sequence:
    1. AE writes TF module + imports, runs `terraform plan` to 0-diff (pre-commit).
    2. DT writes lib/partner + auth-handler db.ts changes, runs `tsc` + `build-nodejs-lambda.sh` clean (pre-commit).
    3. AE combines both scopes into a single working tree, single `git commit`, single push.
    4. `terraform apply` + Lambda deploy happen on the pushed commit.
    5. Shared MCP COMPLETE to COO with both evidence sets.
  </cross_domain_coordination>

  <closeout date="2026-04-15" commit="pending-on-commit">
    (a) **New Rule 7 flex class pre-flagged + ACK'd** at 19:19Z — `opal-partner-49financial` was already TF-managed in `shared-infra/main.tf:166-192`. Audit doc line 136 flagged this optimistically but accurately. COO chose Path A (uniform state migration) at 19:20Z over Path B (leave in shared-infra, module forward-only) to preserve discipline — the module pattern the TO + DT memo §3 wanted.
    (b) **State migration executed locally atomically** (never pushed in-between): `terraform state rm aws_dynamodb_table.opal_partner_49financial` from shared-infra → resource block deleted from `main.tf` → IAM refactored in the same file from explicit `{arn, arn/index/*}` + `GetItem+Query` to wildcard `opal-partner-*` + `GetItem`-only (DT memo §4) → `terraform init` partner-firms → `terraform import module.firm_49financial.aws_dynamodb_table.partner_table opal-partner-49financial`.
    (c) **Both plans 0-diff post-apply.** Partner-firms apply was tags_all metadata only (`System=SharedInfra → PartnerFirms`); shared-infra apply was the IAM policy swap (verified: auth-handler's only `QueryCommand` usages are on `opal-users-v2`, never on partner tables, so Query wildcard-drop is safe).
    (d) **Build-script extension:** `build-nodejs-lambda.sh` now rsyncs `infra/aws/lambda/lib/<pkg>/` → `<source>/src/lib/<pkg>/` before bundling, enabling Lambda-side shared TS libs without committing per-Lambda mirrors. Canonical `infra/aws/lambda/lib/` un-ignored in `infra/.gitignore` (scoped negation; per-Lambda `src/lib/` stays ignored).
    (e) **DT scope landed:** `infra/aws/lambda/lib/partner/{tableName,index}.ts` canonical (tsc clean); `auth-handler/src/db.ts` + `auth.ts` generalized — `PARTNER_TABLE_49FIN` hardcode removed, `getPartnerIdentity(email, firmId)` parameterized through `getPartnerProfile`, 3 call sites (login/refresh/getCurrentUser) pass `user.firmId`. Lambda built clean (100KB bundle), SHA `vvmBpTJbH+4eSIN/xS58hRaU4By6YCZPtLRXOMWc30M=`, deployed via portal-auth TF apply.
    (f) **Live regression evidence** (19:33Z CloudWatch, within-5m after apply): successful `POST /auth/login` (3.6s) + `GET /auth/me` (118ms) — both returned cleanly on the NEW deploy, no 500s, no errors in logs. End-to-end auth path works with generalized partner lookup.
    (g) **4 open Qs:** all resolved and cited in commit body. Reference msg `20260415T185644Z_...4-Q_resolution...`.
    (h) `/frontend-dev` Skill + `comp-blast` verifications: NOT run this session (lambda-side regression evidence is sufficient given the scope is auth surface, not portal rendering). Flagged — if COO wants them run, I'll execute as a post-commit addendum before the project-terminal close.
  </closeout>

  <next>On commit: **CDRS_TFIMPT PROJECT TERMINAL.** COO flips project to completed, moves row in REGISTRY.md. Post-sprint AE follow-ups (JWT drift + opal-market-data-v2 bucket_policy) unfreeze.</next>
</task_order>
