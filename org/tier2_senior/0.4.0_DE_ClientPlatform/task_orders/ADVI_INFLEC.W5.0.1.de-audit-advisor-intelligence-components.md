<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-21-inflec-w5.0.1-component-audit</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-04-21</date>
    <status>staged</status>
    <project_code>ADVI_INFLEC</project_code>
  </metadata>

  <objective>
    Enumerate every component under `portal/src/pages/AdvisorIntelligence/` and tag each as `SHARED` (renders any firm's data), `49F-SPECIFIC` (encodes 49F-only logic — Schwab overlay, BD-custodian conditionals, role-name hardcodes), or `AMBIGUOUS` (needs architect review). Deliver a component inventory as a markdown table. This is the reconnaissance pass before the refactor — no code changes in this TO.
  </objective>

  <context>
    ADVI_INFLEC PRD v1.2 §7.3. Adding Inflection as the second partner exposes that components built for 49F mix shared rendering logic with 49F-specific conditionals. Before Inflection overrides can land in `_partners/inflection/`, DE must inventory exactly where the 49F-assumptions live so the refactor (W5.0.4) is scoped, not exploratory.

    Per CTO PRD §7.3 principle: "If a component renders data whose shape is the same across partners, it belongs in `_shared/`. If a component encodes a partner-specific decision (e.g., 'if firm has Schwab custodian, show this panel'), that conditional lives in `_partners/{firm}/` and is injected by the partner-router."

    Known 49F-ism hotspots from CTO compiler runs (PRD §8.1 direct-grep row):
    - `portal/src/api/endpoints/advisor-intelligence.ts`: 10 hardcoded `'49financial'` default-fallbacks (W5.3 scope, but likely propagates into components that don't pass firmId down)
    - `portal/src/contexts/AuthContext.tsx`: 3 dev-mode `'49financial'` hardcodes (W5.4 scope)
    - `portal/src/pages/PageSurfaceControl.demo.tsx`: 1 hardcode (demo file; low priority)

    **Parallelizable with W1-W4** — no Inflection data or infrastructure required. Purely codebase analysis.
  </context>

  <compiler_tools_mandate>
    Phase 1 (before writing):
    <run>comp-transform schema-check AdvisorIntelligence</run>
    <expect>Current MISSING/UNUSED/NOTE inventory on the page. Baseline before refactor. Save output to session log.</expect>

    <run>find portal/src/pages/AdvisorIntelligence -type f -name "*.tsx" -o -name "*.ts" | wc -l</run>
    <expect>Known file count. Not an acceptance criterion; just for scope estimation.</expect>

    <run>grep -rn "49financial\|'49fin\|BD\b\|schwab\|Schwab" portal/src/pages/AdvisorIntelligence/</run>
    <expect>Every 49F-specific reference. Flag each in the inventory table as potential 49F-specific logic.</expect>

    <run>grep -rn "firmId\|allowedFirmIds" portal/src/pages/AdvisorIntelligence/ | head -40</run>
    <expect>Current firmId propagation points. Components that DON'T reference firmId but render firm-dependent data are candidates for `SHARED` tagging.</expect>

    Phase 2 (during implementation):
    (N/A — this is an audit TO, no code modification.)

    Phase 3 (after audit written):
    <run>comp-transform fields AdvisorIntelligence</run>
    <expect>Fields rendered per component. Cross-check against the inventory table — every component in the inventory should appear in comp-transform fields output (or be a container that composes others).</expect>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    shared_resource: `portal/src/pages/AdvisorIntelligence/` (read-only in this TO).
    also_in_to: W5.0.2 (proposed structure — consumes this inventory). W5.0.3 CTO review. W5.0.4 execution.
    last_write_owner: — (no writes in this TO except the new inventory markdown).
    required_action: "No agent should refactor AdvisorIntelligence/ during this audit. If DE has parallel cleanup work on the tree, pause until this inventory is locked so categories don't shift under the audit."
  </cross_domain_coordination>

  <acceptance_criteria>
    1. Inventory table committed at `org/tier2_senior/0.4.0_DE_ClientPlatform/deliverables/advi_inflec_component_inventory.md` (or equivalent artifact location the DE standardizes on). Table columns: `File`, `Component`, `Category (SHARED | 49F-SPECIFIC | AMBIGUOUS)`, `Evidence (grep hit, conditional description, hardcoded constant)`, `Proposed target folder (_shared | _partners/49financial | _partners/inflection | AMBIGUOUS — CTO review)`.
    2. Every `.tsx` and `.ts` file under `portal/src/pages/AdvisorIntelligence/` has a row.
    3. For each `49F-SPECIFIC` row, the exact evidence (file:line or grep-hit) is cited — not "feels 49F-specific".
    4. `AMBIGUOUS` rows have a specific question for CTO (e.g., "renders custodian breakdown but hardcodes BD — is this a SHARED primitive that takes a `custodianType` prop, or a 49F-specific overlay?").
    5. Count summary at the top: `N components total; S shared; F 49F-specific; A ambiguous`.
    6. Session log at `org/tier2_senior/0.4.0_DE_ClientPlatform/logs/2026-04-{NN}/advi_inflec_w5_0_1_component_audit.md` with compiler runs + grep output + inventory methodology note.
  </acceptance_criteria>

  <scope>
    <files>
      <file action="create">org/tier2_senior/0.4.0_DE_ClientPlatform/deliverables/advi_inflec_component_inventory.md</file>
      <file action="reference">portal/src/pages/AdvisorIntelligence/**</file>
      <file action="reference">docs/architecture/ADVI_INFLEC.md §7.3</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">Audit is read-only on AdvisorIntelligence/. No refactor in this TO.</requirement>
    <requirement id="2">Evidence required for every `49F-SPECIFIC` tag — grep hit or file:line citation. Opinion without evidence is rejected.</requirement>
    <requirement id="3">AMBIGUOUS rows pose a specific question for CTO, not "needs review".</requirement>
    <requirement id="4">Count summary at top of file.</requirement>
    <requirement id="5">No emojis. ASCII only.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="document">Component inventory markdown table.</deliverable>
    <deliverable type="document">Session log.</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT refactor components in this TO.</rule>
    <rule>Do NOT tag 49F-SPECIFIC without evidence.</rule>
    <rule>Do NOT skip AMBIGUOUS rows — surface them for CTO review in W5.0.3.</rule>
  </do_not>
</task_order>
