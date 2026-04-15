<task_order>
  <metadata>
    <id>0.4.0_DE_ClientPlatform-2026-04-14-advi-fntend-b1-fe</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-04-14</date>
    <status>complete</status><!-- Shipped portal DEV 82c6b73 2026-04-15T00:05Z. /frontend-dev pending DT; DS B1 fee-split canonical stream pending. -->
    <project_code>ADVI_FNTEND</project_code>
    <wave>C</wave>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_FRONTEND_CORRECTNESS.md (Bundle 1)</ref>
  </references>

  <objective>
    Wire `feeView` through Summary counts + RoleDonut + Lifetime Activity on AdvisorPublicProfile.
    Remove "fee filter not applied" footnote at `AdvisorBookView:1105`.
  </objective>

  <acceptance_criteria>
    **Tightened 2026-04-14 per Andrew + CTO directive — explicit Role Decomposition wiring:**
    1a. RoleDonut reads `entry.role_breakdown[role].{fee_paying|no_fee}.{aua, nna}` indexed by `feeView` state. Toggling Fees Only (fee_paying) vs. All (fee_paying + no_fee summed or parent) changes each segment's **numeric value, arc size, and tooltip content** — not just a visual re-render.
    1b. Summary Clients / New Clients / Account counts read the matching `fee_breakdown.{fee_paying|no_fee}.{client_count, new_clients, account_count}` per feeView.
    1c. When Fees Only is checked, every displayed AUA/NNA/count figure across Summary + RoleDonut + Lifetime Activity reflects the `fee_paying` bucket exclusively. Unchecking expands to the parent (fee_paying + no_fee).
    2. No static values when toggling — every displayed figure is state-driven.
    3. "Fee filter not applied" footnote at `AdvisorBookView:1105` removed.
    4. Skill `frontend-dev` (or direct `.tools/frontend-dev.py --constitution portal/.frontend-dev/testing/<name>.json`) closed-loop pass.
    5. MCP COMPLETE to COO.
  </acceptance_criteria>

  <compiler_tools_mandate>
    Phase 1: `comp-transform schema-check --feature feeView` on AdvisorPublicProfile + RoleDonut + LifetimeActivity; **`comp-transform ternary-audit RoleDonut`** (added 2026-04-14 per CTO directive — W6 OFC lesson: every `role ===` / `feeView ===` chain must have both branches covered).
    Phase 2: `comp-transform ternary-audit` on all affected components (feeView routing).
    Phase 3: Skill `frontend-dev` (or direct `.tools/frontend-dev.py --constitution portal/.frontend-dev/testing/<name>.json`).
  </compiler_tools_mandate>

  <dependencies>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_FNTEND.B1 DS" status="staged"/>
  </dependencies>

  <cross_domain_coordination>
    AdvisorBookView.tsx + types.ts touched by B1, B4, B5. Sequential commits; no parallel FE commits to these files.
  </cross_domain_coordination>

  <frontend_dev_note>
    If no constitution exists at `portal/.frontend-dev/testing/` for the target component + scenario, author one first per the schema in that directory's README.md. Do not hand-roll Playwright scripts in repo root — the smoke-test.py/.mjs pattern is deprecated.
  </frontend_dev_note>
</task_order>
