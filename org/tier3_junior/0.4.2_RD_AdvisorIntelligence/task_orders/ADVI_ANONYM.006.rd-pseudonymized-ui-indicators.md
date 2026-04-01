<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-01-ADVI_ANONYM-006-rd-ui-indicators</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <date>2026-04-01</date>
    <status>complete</status>
    <!-- Completed 2026-04-01. Portal DEV commit 2ebf55b. 4 surfaces: DistributionTab drill header, ClientsTab L2+L4 column headers, ClientDetailPage header. TSC clean. Export disable N/A (button doesn't exist yet). -->
    <priority>high</priority>
    <type>feature</type>
    <project>ADVI_ANONYM</project>
  </metadata>

  <objective>
    Add pseudonymization indicators to four UI surfaces. When advisor/user tier is viewing
    hashed client data, the UI should clearly indicate that names and IDs are pseudonymized.
    Internal/admin users see no indicators (they see cleartext names from the API).
  </objective>

  <references>
    <ref type="prd">docs/architecture/ADVI_ANONYM_PRD.md -- Phase 2: Frontend Graduated UI</ref>
    <ref type="de_to">ADVI_ANONYM.005.de-authcontext-canseecleartext.md (canSeeCleartext helper -- must be committed first)</ref>
    <ref type="file_1">portal/src/components/DistributionTab.tsx</ref>
    <ref type="file_2">portal/src/components/ClientsTab.tsx</ref>
    <ref type="file_3">portal/src/pages/ClientDetailPage.tsx</ref>
  </references>

  <pre_verified_facts>
    1. P1 is fully deployed. advisor/user tier receives hashed client names from the API
       in the format "Client a7f3b2c1", "Acct ef9b0465", "id 3a2f1b8c". These are
       real API responses -- not placeholder text.
    2. DE (ADVI_ANONYM.005) has added canSeeCleartext() to AuthContext. Use
       `const { canSeeCleartext } = useAuthContext()` to gate all indicator logic.
    3. Export disabled for advisor/user on client-level data is a P2 requirement.
  </pre_verified_facts>

  <requirements>

    <requirement id="1">
      READ all three files completely before editing:
      - portal/src/components/DistributionTab.tsx
      - portal/src/components/ClientsTab.tsx (note lines 1518 and 1559)
      - portal/src/pages/ClientDetailPage.tsx (note line 90)

      Understand the existing component structure before making any changes.
    </requirement>

    <requirement id="2">
      DISTRIBUTION TAB -- DistributionTab.tsx

      When the ADV drill-down is showing client-level data (hashed "Client a7f3b2c1" labels)
      and `!canSeeCleartext()`:

      a) Add a subtle "(pseudonymized)" text indicator in the drill header or near the
         chart legend. Use muted/secondary text style -- this should inform, not dominate.

      b) Disable the CSV/clipboard export button for client-level drill data.
         The export must not be disabled for firm-level or architect-level segments --
         only when the active drill is showing per-relationship client data.

      Condition both changes strictly on `!canSeeCleartext()`. Internal/admin users
      must not see the indicator or experience disabled export.
    </requirement>

    <requirement id="3">
      CLIENTS TAB -- ClientsTab.tsx line 1518 (L2 advisor client table)

      The `client_name` column in the L2 advisor client table shows hashed names
      for advisor/user. Add a "(pseudonymized)" indicator in the column header
      when `!canSeeCleartext()`. A small badge or parenthetical text is sufficient.
    </requirement>

    <requirement id="4">
      CLIENTS TAB -- ClientsTab.tsx line 1559 (L4 account table)

      The `account_id` column in the L4 account drill table shows hashed IDs
      (format: "Acct ef9b0465") for advisor/user. Add a "(pseudonymized)" indicator
      in the column header when `!canSeeCleartext()`.
    </requirement>

    <requirement id="5">
      CLIENT DETAIL PAGE -- ClientDetailPage.tsx line 90 (page header clientLabel)

      The page header renders `clientLabel` which for advisor/user is a hashed name
      ("Client a7f3b2c1"). Add a "(pseudonymized)" indicator near the header label
      when `!canSeeCleartext()`. Inline text or a small badge. Do not change
      the layout or size of the header itself.
    </requirement>

    <requirement id="6">
      Commit all changes on portal DEV branch with author attribution:
      ```
      git commit --author="0.4.2_RD_AdvisorIntelligence <0.4.2_RD_AdvisorIntelligence@opal.agent>" \
          -m "feat(ADVI_ANONYM P2): pseudonymized UI indicators on 4 surfaces"
      ```
      Do NOT merge to PROD. DT handles DEV -> PROD after this commit.
    </requirement>

    <requirement id="7">
      Verify TypeScript compiles: `bunx tsc -b` (from portal/ directory, bun at
      /c/Users/AndrewBerman/.bun/bin/bun).

      Write session log:
      org/tier3_junior/0.4.2_RD_AdvisorIntelligence/logs/2026-04-01/advi_anonym_p2_ui_indicators.md

      Message COO (2.0.0_SA_COO) when committed, with DEV commit hash.
    </requirement>

  </requirements>

  <acceptance_criteria>
    <criterion id="1">advisor/user sees "(pseudonymized)" indicator on: DistributionTab drill header, ClientsTab L2 client_name column header, ClientsTab L4 account_id column header, ClientDetailPage header.</criterion>
    <criterion id="2">internal/admin sees NO indicators on any surface.</criterion>
    <criterion id="3">CSV/clipboard export disabled for advisor/user on client-level DistributionTab drill data only.</criterion>
    <criterion id="4">Export NOT disabled for firm-level or architect-level segments.</criterion>
    <criterion id="5">bunx tsc -b passes in portal/.</criterion>
    <criterion id="6">All changes gated on canSeeCleartext() from AuthContext (no hardcoded tier/role checks in RD components).</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>PREREQUISITE: DE ADVI_ANONYM.005 (canSeeCleartext helper) must be committed to portal DEV before this work begins. Do not hardcode tier/role logic -- use canSeeCleartext().</constraint>
    <constraint>Indicators must be subtle -- informational text, not warnings or alerts. This is not an error state.</constraint>
    <constraint>Do not change data, layout, or functionality beyond what is specified. No additional columns, no component restructuring.</constraint>
    <constraint>Commit to portal DEV branch. Do NOT merge to PROD.</constraint>
    <constraint>No emojis per CLAUDE.md.</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DE_ClientPlatform" task="ADVI_ANONYM.005.de-authcontext-canseecleartext" status="pending">
      canSeeCleartext() helper must be exported from AuthContext before RD can use it.
      Wait for DE commit notification before starting.
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="code-commit">UI indicators on 4 surfaces in portal DEV branch</deliverable>
    <deliverable type="message">COO notification with DEV commit hash</deliverable>
  </deliverables>
</task_order>
