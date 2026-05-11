<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFTGT.TO-10</id>
    <project>ADVI_INFTGT</project>
    <title>[P1] IWM catchall rendering — relabel `inflection_wealth_management` as "Unassigned" with tooltip</title>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-11</issued_date>
    <status>active</status>
    <priority>P1 — parity gap (parties read as 4th advisor)</priority>
    <authorized_by>Andrew GO on ADVI_INFTGT 2026-05-11; COO Q3 default "Unassigned" — Andrew can override post-demo prep</authorized_by>
  </metadata>

  <context>
    `inflection_wealth_management` advisor_key is the IWM catchall data artifact (per memory `project_inflection_iwm_catchall_bucket.md`). Currently renders as a 4th advisor row in AdvisorsTab. Partners read this as a named advisor when it's actually the residual bucket for accounts not yet attributed to a named advisor.

    PRD §4.8 + §6.TO-10 disposition: relabel as "Unassigned" with info tooltip that names it as the residual bucket. Keep visible so partner sees that residual accounts exist; don't read as 4th advisor.

    COO Q3 default: "Unassigned" copy. Andrew may override during demo prep.
  </context>

  <scope>
    <step>Phase 1 — Compiler runs:
      `comp-transform schema-check AdvisorsTab --feature unassigned_bucket`
      `comp-transform ternary-audit AdvisorsTab`
    </step>

    <step>Phase 2 — Identify render sites:
      `grep -rn "inflection_wealth_management" portal/src/`
      `grep -rn "Inflection Wealth Management" portal/src/`
      Locate all display-name renders for the advisor_key.
    </step>

    <step>Phase 3 — Implementation:
      In AdvisorsTab.tsx + any other render site, when advisor_key === 'inflection_wealth_management':
      - Render display name as "Unassigned"
      - Add tooltip/info-icon: "Residual bucket for accounts not yet attributed to a named advisor."
      - Style consistent with other rows (don't visually separate)
      - Keep row in advisor list so AUA sums are reconciled visually
    </step>

    <step>Phase 4 — Visual verify:
      `bun install && bun run dev --port 5175`
      Confirm: AdvisorsTab shows 3 named advisors (Peter Lee, Patrick Scanlan, Joe Brandenburg) + 1 "Unassigned" row.
      Tooltip displays on hover.
      No layout breakage.
    </step>

    <step>Portal commit on submodule DEV + push.</step>

    <step>RAVC2 to COO with screenshot before/after.</step>
  </scope>

  <acceptance_criteria>
    1. `inflection_wealth_management` rows render as "Unassigned" with tooltip.
    2. Partner sees 3 named advisors + 1 "Unassigned" row (not 4 advisor names).
    3. Tooltip describes residual-bucket meaning.
    4. No layout breakage.
    5. Portal submodule commit on DEV.
    6. RAVC2 with before/after screenshots.
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      `comp-transform schema-check AdvisorsTab --feature unassigned_bucket`
      `comp-transform ternary-audit AdvisorsTab`
    </phase>
    <phase id="3" when="after commit">
      Visual diff against canonical four-row list
    </phase>
  </compiler_tools_mandate>

  <notes>
    Andrew may want to change copy ("Unassigned" vs "Unattributed" vs "Firm Residual" vs hide entirely). The "Unassigned" default is the PRD/CTO recommendation. If Andrew flags during demo prep, swap copy via single replace_all.

    Effort: ~1h. Small, self-contained.
  </notes>
</task_order>
