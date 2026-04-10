<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-10-advi-role-composition-nna-tagged</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <date>2026-04-10</date>
    <status>staged</status>
    <project_code>ad-hoc</project_code>
    <related_to>Grouped with rd-advi-nna-frontend-migration.md (shared RD ClientPlatform NNA workstream). Wraps the already-shipped D_00c gold script fix in commit 4f821b99.</related_to>
  </metadata>

  <objective>
    Light-touch RD task wrapping the already-shipped D_00c role_breakdown NNA tagged equal-split fix (commit `4f821b99`, S3 etag `959dd3a4316815bbd98236ea5e08a7a7`, uploaded 2026-04-10T22:44:30Z). **No required frontend code changes for correctness** — RoleDonut already reads `breakdown[role].nna` directly and the gold fix makes those values reconcile automatically after the next bd-gold-trigger cycle. This TO exists to (a) document the activation, (b) run two optional polish items RD may choose to pick up, (c) verify the post-activation invariants in the browser.

    Closes Andrew's 2026-04-10 Chase Bertrand QTD observation: Summary Flows NNA = +$1.20M vs Role Composition center total = -$16.9K. Root cause was role_breakdown using stale C_08 advisor_fee_detail (fee-paying-only) while Summary used tagged canonical. DS fix: equal-split tagged canonical NNA across overlapping roles, mirroring the existing `_weighted_aua` rule. Full RCA in `org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-04-10/d00c_role_breakdown_nna_tagged_equal_split.md`.
  </objective>

  <context>
    **Authoritative brief:** `docs/briefs/rd-brief-role-composition-nna-tagged-split.md` — READ IN FULL. The brief is short (~130 lines) and already captures the "no code change required" design with the two optional polish items.

    **What DS already shipped:**
    - D_00c.portal_leaderboard.py — `role_breakdown[r].nna / inflows / outflows` now reads from `gold/canonical/nna/*.parquet` (same path as `entry.nna`) and equal-splits across overlapping roles.
    - Sub-buckets (`role_breakdown[r].fee_paying.nna`, `role_breakdown[r].no_fee.nna`) also equal-split.
    - Gold commit 4f821b99 on CLOUD, S3 etag 959dd3a4316815bbd98236ea5e08a7a7.
    - AUA treatment unchanged (already was equal-split). `aua_growth_pct`, `clients`, `accounts`, `implied_revenue` also unchanged.

    **What activation looks like:**
    - No portal deploy needed. No schema change. The JSON field set is byte-for-byte identical; the values change.
    - DS's staged script runs on the next `bd-gold-trigger` cycle (scheduled OR Andrew manual). `gold/artifacts/employee_leaderboard.json` is rewritten with the new reconciled values.
    - React Query `staleTime: 5 * 60 * 1000` on the leaderboard query means the next page load OR natural stale-refetch after the new file is in CloudFront picks it up.
    - Per memory `feedback_mcp_inbox_not_autonomous.md`, Andrew triggers the gold runner when ready; COO does not.

    **COO compiler audit (2026-04-10, logged in org/compiler-tools-log.md):**
    - `comp-transform fields AdvisorPublicProfile` — confirms component reads `entry.role_breakdown` and `entry.roles` at the top-level field tracker; the RoleDonut subcomponent reads `breakdown[role].nna` / `.inflows` / `.outflows` / `.aua` at a deeper level that the field-tracker doesn't index. Matches the brief's "no required FE changes" claim.
    - `grep` on `AdvisorPublicProfile.tsx` confirms the brief's code references:
      - Line 541: `RoleDonutProps` interface
      - Line 548: `RoleDonut` component
      - Line 552: `const activeRoles = ROLE_KEYS.filter(r => (breakdown[r]?.aua ?? 0) > 0)` — exact target for Polish 1
      - Line 565: `getMetricValue(role)` — reads `breakdown[role].nna` per the brief
      - Lines 581-583: donut absolute-value slices + signed center label (brief confirms this is correct, no change)
    - `comp-platinum reverse employee_leaderboard.json` — WARN: graph has no route/producer/consumer recorded for this platinum artifact (compiler coverage gap, same pattern as other platinum JSONs). Not blocking. Manual verification via grep confirms the RoleDonut consumer chain.
    - `comp-pipescript io D_00c` — PASS: D_00c reads CANONICAL_NNA_PREFIX + ADVISOR_FEE_DETAIL_PREFIX + ACCOUNT_TEAM + REL_ARCHITECT_LOOKUP, writes EMPLOYEE_LEADERBOARD. The DS fix is in-scope for D_00c's existing I/O surface; no new input was added.

    **Invariants that should hold after activation** (lift these verbatim into the session log as a checklist):
    - `entry.nna == sum(role_breakdown[r].nna for r in keys(role_breakdown))` within $0.01
    - `entry.inflows == sum(role_breakdown[r].inflows for r)` within $0.01
    - `entry.outflows == sum(role_breakdown[r].outflows for r)` within $0.01 (signed)
    - `entry.total_aua == sum(role_breakdown[r].aua for r)` (pre-existing, preserved)
    - `role_breakdown[r].nna == role_breakdown[r].fee_paying.nna + role_breakdown[r].no_fee.nna` within $0.01
    - `entry.fee_breakdown.fee_paying.nna == sum(role_breakdown[r].fee_paying.nna for r)` within $0.01
    - `entry.fee_breakdown.no_fee.nna == sum(role_breakdown[r].no_fee.nna for r)` within $0.01
  </context>

  <compiler_tools_mandate>
    Phase 1 (before starting):
    - Read the brief in full.
    - Read DS's RCA log: `org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-04-10/d00c_role_breakdown_nna_tagged_equal_split.md` (reference only — you are not modifying gold scripts).
    - `comp-transform fields AdvisorPublicProfile` — baseline. If you pick up any of the optional polish items, the field tracker output should match before and after (no new rendered fields introduced by either polish).
    - `comp-transform schema-check AdvisorPublicProfile` — baseline. Both polish items are either client-side predicate logic (Polish 1) or a string literal edit (Polish 2); neither should shift the schema.
    - Read `portal/src/pages/AdvisorIntelligence/AdvisorPublicProfile.tsx` lines 548-720 (the full `RoleDonut` function) to understand the current activeRoles filter and the PanelHeader helpText location for the tooltip.

    Phase 2 (if you pick up Polish 1 or Polish 2):
    - Polish 1 code change is strictly the `activeRoles` filter predicate at line 552. Use the exact replacement from the brief:
      ```ts
      const activeRoles = ROLE_KEYS.filter(r => {
        const rb = breakdown[r]
        if (!rb) return false
        const hasAua = (rb.aua ?? 0) > 0
        const hasFlow = Math.abs(rb.nna ?? 0) > 0 || Math.abs(rb.inflows ?? 0) > 0
        return hasAua || hasFlow
      })
      ```
    - Polish 2 is a one-line string edit on the `helpText=` prop of the Role Composition `PanelHeader` (brief says line 663, verify with grep first — line numbers shift with edits). Replace with the brief's updated text that mentions NNA/flows are also equal-split.
    - `bun run tsc -b` exit 0 after any edit.
    - `bun run eslint src/pages/AdvisorIntelligence/AdvisorPublicProfile.tsx` — 0 errors.

    Phase 3 (post-activation verification, AFTER Andrew triggers the gold runner):
    - Pull the raw `employee_leaderboard.json` from S3 after the new file is in CloudFront and inspect Chase Bertrand's entry directly. Verify the invariants in §context against the raw JSON.
    - Browser QA: load Chase Bertrand's AdvisorPublicProfile at QTD, Fees=All. Confirm:
      - Summary Flows NNA shows +$1.20M (or whatever the current value is after the gold run)
      - Role Composition donut center total matches Summary Flows NNA within rounding
      - Per-role slices sum to the center total
    - Second advisor spot-check: Alex Bright or any advisor with multi-role overlap. Verify the sum-across-roles reconciles.
    - `comp-transform fields AdvisorPublicProfile` — re-run. Output should match the Phase 1 baseline exactly if you only did the polish items (no new rendered fields).
    - Log results in the session log.

    Log every compiler tool run to `org/compiler-tools-log.md`.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    shared_resource: `gold/artifacts/employee_leaderboard.json` schema — DS owns the producer (D_00c); RD consumes via AdvisorPublicProfile + AdvisorsTab leaderboard. DS has already shipped; the schema field set is unchanged, values are corrected. No coordination needed at write time.
    shared_resource: `portal/src/pages/AdvisorIntelligence/AdvisorPublicProfile.tsx` — RD exclusive for this TO. Same file is also touched by ADVI_PROFIL.001/.002 (already landed) and ADVI_PROFIL.007 (admin my-profile toggle — SHIP decision per Andrew 2026-04-10, status flipped to pending). Polish edits here are in a different function (`RoleDonut`) from .007's BooksTab header insertion, so merge conflict risk is minimal.
    shared_resource: `portal/src/pages/AdvisorIntelligence/AdvisorsTab.tsx` — referenced by the brief for leaderboard NNA filtering context. This TO does NOT modify AdvisorsTab. The cursor-affordance cleanup bundled into `rd-advi-nna-frontend-migration.md` is the other AdvisorsTab touchpoint; do those edits on the same working tree if you pick up both TOs in the same session.
    last_write_owner: 0.4.2_RD_AdvisorIntelligence (if polish items picked). DS last-write on D_00c is already committed + deployed.
    required_action: "This TO can ship anytime after `rd-advi-nna-frontend-migration.md` lands (or in parallel if the two edits don't collide). If RD picks up both TOs in the same session, bundle the working tree changes into one handoff to DT. Per memory `feedback_no_direct_ds_messages.md`, RD does not direct-message DS with findings; route through Andrew."
  </cross_domain_coordination>

  <acceptance_criteria>
    **Required (all TOs):**

    1. **Brief read and activation understood.** Session log confirms RD has read the brief and understands there are no required code changes, only optional polish.

    2. **Post-activation browser verification.** After Andrew triggers the gold runner and the new `employee_leaderboard.json` lands in CloudFront, RD loads Chase Bertrand's AdvisorPublicProfile at QTD + Fees=All and verifies:
       - Role Composition donut center total matches Summary Flows NNA within rounding (the specific number will be whatever the gold run produces — the brief's +$1.20M reference was the 2026-04-10 observation and may drift).
       - Per-role slices sum to the center total within rounding.
       - No visual regression on other RoleDonut elements (colors, labels, per-role tiles, metric toggle).
    
    3. **One additional advisor spot-check.** Pick any advisor with multi-role overlap (DS's RCA log flags ~3.7% of accounts) and verify the same invariants. Alex Bright or Sam Owens are candidates if you want a named target.

    4. **Invariants verified against raw JSON.** Pull `employee_leaderboard.json` from S3 and verify at least 3 of the invariants from §context on Chase's entry (and one other advisor's entry). Log the actual deltas.

    5. **Compiler Tools section in session log.** Phase 1 baseline + Phase 3 re-run results, plus any additional runs triggered by polish edits. Append to `org/compiler-tools-log.md` per the standard format.

    **Optional (pick any or none):**

    6. **Polish 1 — `activeRoles` flow-aware filter.** If you choose to ship this, follow the brief's exact code snippet. Edge case fix for an advisor who churned out of a role mid-window: still shows up in the donut because flow activity is present even with zero current AUA. Very small real-world effect. OPTIONAL.

    7. **Polish 2 — Tooltip copy update.** If you choose to ship this, replace the Role Composition `helpText` (brief says line 663, verify with grep) with the brief's updated text that mentions NNA/flows are also equal-split. Trivial one-line edit. OPTIONAL.

    8. **If both polish items shipped, tsc + eslint clean.** `bun run tsc -b` exit 0, `bun run eslint src/pages/AdvisorIntelligence/AdvisorPublicProfile.tsx` 0 errors.

    9. **Hand off to DT for commit + push** (if any polish items shipped). Same pattern as ADVI_PROFIL.001/.005 — RD stages the working tree, DT commits under RD author attribution and pushes to portal DEV.

    10. **Session log format.** `org/tier2_senior/0.4.2_RD_AdvisorIntelligence/logs/2026-04-{NN}/advi_role_composition_nna_activation.md` with: activation verification results (Chase Bertrand + spot-check advisor), raw JSON invariant checks, which polish items were picked (if any), the DT handoff message SHA (if any), and compiler tools log.
  </acceptance_criteria>

  <scope>
    <files>
      <file action="verify">portal/src/pages/AdvisorIntelligence/AdvisorPublicProfile.tsx → RoleDonut component (lines 548-720)</file>
      <file action="modify" optional="true">portal/src/pages/AdvisorIntelligence/AdvisorPublicProfile.tsx line 552 (Polish 1 — activeRoles filter)</file>
      <file action="modify" optional="true">portal/src/pages/AdvisorIntelligence/AdvisorPublicProfile.tsx line ~663 (Polish 2 — tooltip copy)</file>
      <file action="reference">docs/briefs/rd-brief-role-composition-nna-tagged-split.md — authoritative brief</file>
      <file action="reference">org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-04-10/d00c_role_breakdown_nna_tagged_equal_split.md — DS RCA log</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">Read the brief in full before verifying. It is authoritative on the activation model and the two polish items.</requirement>
    <requirement id="2">Do NOT modify D_00c or any gold script. The DS fix is already shipped and deployed.</requirement>
    <requirement id="3">Do NOT assume the activation happens instantly. It requires Andrew (or a scheduled cycle) to trigger the gold runner, then up to 5 minutes for React Query staleTime to expire OR a page reload. Log the gold-run trigger time and the first successful browser verification time separately in the session log.</requirement>
    <requirement id="4">Do NOT ship Polish 1 without Polish 2 or vice versa as a sequencing rule — they are independent. Pick either, both, or neither.</requirement>
    <requirement id="5">If any polish is picked, bundle the handoff with the `rd-advi-nna-frontend-migration.md` working tree if both TOs are in flight simultaneously. Single DT commit pass is preferable to two.</requirement>
    <requirement id="6">Do NOT escalate a "totals don't reconcile" finding until AFTER the invariants-against-raw-JSON check. The DS RCA log documents a fee-bucket partition edge case (`fee_rate_history.is_billable` join); if the raw JSON doesn't reconcile, surface it with the specific advisor IDs + deltas so DS can diagnose.</requirement>
    <requirement id="7">Per memory `feedback_no_direct_ds_messages.md`, if a post-activation issue is found, RD surfaces it to Andrew — do NOT direct-message 0.4.0_DS. Andrew routes.</requirement>
    <requirement id="8">Log every compiler tool run to `org/compiler-tools-log.md`.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="verification">Browser QA of Chase Bertrand AdvisorPublicProfile at QTD + Fees=All after gold runner activation. Logged with timestamp + observed values.</deliverable>
    <deliverable type="verification">Raw JSON invariant check against `employee_leaderboard.json` for Chase + one other multi-role advisor. Logged with deltas.</deliverable>
    <deliverable type="code" optional="true">If polish items picked: modified `AdvisorPublicProfile.tsx` in portal DEV working tree, staged for DT commit+push under RD author.</deliverable>
    <deliverable type="document">Session log at `org/tier2_senior/0.4.2_RD_AdvisorIntelligence/logs/2026-04-{NN}/advi_role_composition_nna_activation.md` with verification results, polish decisions, compiler tools log, and DT handoff message SHA if any.</deliverable>
    <deliverable type="message" optional="true">Broker handoff to 0.4.0_DT_ClientPlatform if polish items were picked (same pattern as ADVI_PROFIL.001/.005).</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT modify D_00c or any gold script. DS has shipped.</rule>
    <rule>Do NOT ship either polish item as required — they are both OPTIONAL.</rule>
    <rule>Do NOT assume activation is instant. Log trigger time and verification time separately.</rule>
    <rule>Do NOT direct-message DS on findings. Route through Andrew per memory.</rule>
    <rule>Do NOT commit or push. Hand off to DT if polish items were picked.</rule>
    <rule>Do NOT escalate reconciliation issues without first checking the raw JSON + providing specific advisor IDs and deltas.</rule>
  </do_not>
</task_order>
