<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-04-09-49push-032-pii</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform~B</issued_to>
    <date>2026-04-09</date>
    <status>pending -- blocked on DS .027 (pseudonymized platinum data)</status>
    <project_code>ADVI_49PUSH</project_code>
    <wave>7</wave>
    <phase>PII compliance</phase>
    <mcp_identity>Register with MCP as "0.4.0_DE_ClientPlatform" before starting.</mcp_identity>
  </metadata>

  <objective>
    Enforce server-side pseudonymization of all client (relationship) names in the
    Distribution tab advisor drilldown views. Client identity data is partitioned
    exclusively to the Books tab. The Distribution tab must never render a cleartext
    client name under any condition, regardless of user role, tier, or firmId.
  </objective>

  <design_decision>
    Approved by Andrew (CTO) 2026-04-09:

    "It's probably better to just hash it by default server side for this window.
    Doesn't matter what your roles are, you shouldn't see anything here.
    If you want to see client data, we keep it solely partitioned to the books tab."

    Architectural rule:
      DISTRIBUTION TAB: all client names always pseudonymized. No role exceptions. No
      admin bypass. No future flag to enable cleartext. The Distribution tab is an
      aggregate/analytics surface -- individual client identity has no place here.

      BOOKS TAB: client names may be rendered with appropriate auth gating (existing
      Lambda /books/relationship/{id} path handles this separately).

    Implementation model:
      Pseudonymization is applied at the DATA layer by DS (D_04), not at the serve layer.
      D_04 writes platinum Distribution files with pseudonymized names baked in.
      There is no server-side conditional: the file always contains hashed names.
      DE reads whatever name is in the platinum file -- no client-side name handling needed.
  </design_decision>

  <ds_requirements label="DS must implement -- part of .027 issue_4">
    DS .027 issue_4 is responsible for the data side of this fix. Specifically:

    1. In D_04, when building any Distribution-serving platinum file that contains
       client/relationship names (e.g. platinum/advisors/{id}/nna_clients.json,
       any advisor client list for ADV-AUA or ADV-NNA drilldowns):
       Apply the existing pseudonymizer to relationship names before writing.
       Use the same pseudonymizer already in use for Books tab platinum files.
       The pseudonymized name goes in the display_name field.
       The relationship_id remains unobfuscated (needed for internal joins).
       Raw relationship_name must NOT appear in any Distribution platinum file.

    2. Verify: grep platinum/advisors/ after D_04 runs. No file under any Distribution
       path should contain a field that maps to a raw client name. Only hashed/pseudonymized
       display names and relationship_ids.

    3. This rule extends to any future Distribution platinum files -- pseudonymization at
       write time is the invariant, not a runtime option.
  </ds_requirements>

  <de_requirements label="DE implementation">
    After DS .027 ships with pseudonymized platinum data:

    1. Remove all TODO / placeholder [Client N] markers added by .030 and .031.
       Replace with the actual display_name field from the platinum data.
       Since display_name is already pseudonymized by DS, no additional DE hashing needed.

    2. Do NOT add any client name de-anonymization logic, role-based name reveal,
       or "show real names for admins" toggle anywhere in the Distribution tab.
       If anyone requests this in the future, the answer is: use the Books tab.

    3. Add a code comment at the point where display_name is rendered in the advisor
       drilldown:
         // display_name is pseudonymized server-side (DS D_04).
         // Real client names are exclusively available via the Books tab.
         // Do not add de-anonymization here regardless of user role.

    4. Run comp-pii audit after shipping:
         comp-pii scan DistributionTab
       Confirm: zero cleartext relationship names detected in rendered fields.
       Confirm: relationship_id fields are present but not rendered to the UI.
  </de_requirements>

  <scope>
    Surfaces this covers:
      - Distribution tab ADV-AUA: advisor → client relationships by AUA (from .030)
      - Distribution tab ADV-NNA: advisor → client relationships by NNA (from .031)
      - Any future Distribution tab view that surfaces individual client entries

    Surfaces explicitly OUT of scope:
      - Books tab client views (separate auth model, handled by Lambda gateway)
      - Advisor names (not PII in this context -- advisors are employees, not clients)
      - State/city geographic labels (not PII)
  </scope>

  <acceptance_criteria>
    1. All client display names in Distribution advisor drilldowns are pseudonymized
    2. No cleartext relationship names exist in any Distribution platinum file (verified by DS)
    3. No role-based name reveal logic exists anywhere in DistributionTab.tsx
    4. Code comment present at the display_name render site
    5. comp-pii scan DistributionTab passes: zero cleartext name fields rendered
    6. Books tab client name behavior unchanged (no regression)
    7. relationship_id fields used only for internal lookups, never rendered to UI
  </acceptance_criteria>


  <compiler_tools>
    comp-pii audit
      -- The primary verification tool for this entire TO. Run after all fixes are
         deployed. Sweeps all ADVI components for cleartext relationship names,
         flags [CLEARTEXT] vs [HASHED] fields, and confirms Distribution tab paths
         are clean. This is the pass/fail gate for acceptance criterion #5.

    comp-pii scan DistributionTab
      -- More targeted than comp-pii audit. Run during development (not just at the end)
         to catch regressions as each advisor drilldown panel is wired up.

    comp-pii fields
      -- Shows the full list of PII target fields the pseudonymizer is configured to
         handle. Confirms display_name is in the target list before relying on it.
  </compiler_tools>

</task_order>
