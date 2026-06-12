<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-06-12-page-inventory-full-reaudit</id>
    <issued_by>2.0.0_SA_COO (authoring delegated to 0.4.2_RD per COO GO 20260612T211436Z)</issued_by>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <date>2026-06-12</date>
    <status>complete</status>
    <project_code>ad-hoc (doc-accuracy; registry pointer routed by COO per GO)</project_code>
  </metadata>

  <objective>
    Full re-audit of page_inventory.xml against the live post-ORPHAN-AI portal tree. The current
    inventory's file paths and counts are April 2026 vintage — they predate the ADVI_INFLEC 9423f71e
    _shared/_partners refactor — so every path is wrong-shaped, several live files (_partners/*,
    AdvisorBookAccountModal, ClientListPanel, charts/, lib/, types/, hooks/) have no entry, and the
    api_calls section trails the platinum endpoint migration. The 2026-06-12 surgical update fixed
    the deletion-affected entries only.
  </objective>

  <context>
    Trigger: D5 ORPHAN-AI cleanup (Andrew-approved 27-file deletion, portal DEV ab1c11b0; RD comment
    fixes 61e1677f; surgical inventory update ws ed28053b8). COO GO 20260612T211436Z authorized RD to
    author + execute this follow-on. The inventory is the authoritative live state of the page read by
    DE/Tier-1; the April drift already produced one wrong claim ("ClientDetail still active") that the
    orphan census had to falsify. Audit baseline: portal DEV HEAD at execution time (record the hash
    in the metadata audit_scope).
  </context>

  <compiler_tools_mandate>
    Phase 1 — before writing:
      <run>git -C portal ls-files src/pages/AdvisorIntelligence/</run>
      <expect>Complete live file enumeration at the audited HEAD; no ClientDetail/, no deleted v1-era components</expect>
      <if_mismatch>If deleted files reappear, STOP — tree is not on the post-deletion HEAD; pull origin/DEV first</if_mismatch>
      <run>comp-transform schema-check AdvisorIntelligence (+ spot-check DistributionTab, ClientsTab, PartnerAnalytics)</run>
      <expect>Field/type surface to describe in entries; no MISSING fields on live components</expect>
      <if_mismatch>A MISSING field on a live component is a real defect, not an inventory item — flag DE before documenting around it</if_mismatch>
    Phase 2 — before commit:
      <run>python -c "import xml.etree.ElementTree as ET; ET.parse('org/tier3_junior/0.4.2_RD_AdvisorIntelligence/deliverables/page_inventory.xml')"</run>
      <expect>Parses clean (exit 0)</expect>
      <if_mismatch>Fix malformed XML before commit — downstream readers parse this file</if_mismatch>
    Phase 3 — after commit:
      <run>cross-check: every &lt;file path&gt; in the XML exists in the Phase-1 ls-files output, and every ls-files entry has an XML entry</run>
      <expect>0 phantom entries, 0 missing entries; counts in audit_summary match</expect>
      <if_mismatch>Reconcile and amend in a follow-up commit; log the miss in the session log</if_mismatch>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <none/> <!-- single-file deliverable in RD's own deliverables/ dir; portal tree read-only for this TO -->
  </cross_domain_coordination>

  <acceptance_criteria>
    1. Every file under portal/src/pages/AdvisorIntelligence/ at the audited HEAD (git ls-files) has an
       inventory entry with its REAL _shared/_partners path; zero entries reference nonexistent paths.
    2. api_calls section matches src/api/endpoints/advisor-intelligence.ts ground truth: every useQuery
       consumer named per function; UNUSED/legacy functions explicitly marked (incl. the 4 D5-orphaned ones).
    3. page_structure + lifecycle sections describe the live tab/drill architecture (L4 = AdvisorBookAccountModal
       in accountDetailSlot; L2 = ClientListPanel; _partners tenant-override layer documented).
    4. audit_summary counts (tsx/ts/api/tabs) computed from the enumeration, not carried forward.
    5. XML parses clean (Phase 2 check exits 0).
    6. Session log with Compiler Tools table; metadata audit_scope records the audited portal HEAD hash.
  </acceptance_criteria>

  <scope>
    <files>
      <file action="modify">org/tier3_junior/0.4.2_RD_AdvisorIntelligence/deliverables/page_inventory.xml</file>
      <file action="reference">portal/src/pages/AdvisorIntelligence/** (read-only)</file>
      <file action="reference">portal/src/api/endpoints/advisor-intelligence.ts (read-only)</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">Re-enumerate from git ls-files, not from the prior XML (the prior XML is the drift source).</requirement>
    <requirement id="2">Carry forward prior entry prose only after verifying it against the current file header/comments.</requirement>
    <requirement id="3">Document the _partners/ tenant-override layer (49financial, inflection: layout.ts, index.tsx, overrides/) — currently absent from the inventory entirely.</requirement>
    <requirement id="4">Keep the 2026-06-12 D5 ORPHAN-AI update note in metadata as audit history.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="commit">page_inventory.xml full re-audit commit (RD author line, safe-commit.sh)</deliverable>
    <deliverable type="document">Session log with Compiler Tools section</deliverable>
  </deliverables>

  <do_not>
    <rule>Do not modify any portal file under this TO — read-only audit; code fixes found en route are flagged to DE, not fixed inline.</rule>
    <rule>Do not trust prior-XML claims without verifying against the live file (the "ClientDetail still active" lesson).</rule>
  </do_not>
</task_order>
