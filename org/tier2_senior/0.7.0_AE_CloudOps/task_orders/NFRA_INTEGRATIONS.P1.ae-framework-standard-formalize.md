# Task Order: NFRA_INTEGRATIONS P1 -- IMPLEMENTATION (formalize the framework standard)

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-07-02-nfra-integrations-p1-framework-formalize</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-07-02</date>
    <status>complete -- SPRING-CLEAN 2026-08-25: project NFRA_INTEGRATIONS is complete; this TO was last touched 2026-07-02, predating the project close 2026-07-08. Closed as a record act, not a work verdict. Prior status: active</status>
    <thread_serial>NFRA_INTEGRATIONS-001</thread_serial>
    <prd_ref>docs/architecture/NFRA_INTEGRATIONS_PRD.md (Pillar 1, sec 2) + docs/architecture/NFRA_INTEGRATIONS_STANDARD.md (v1, already exists)</prd_ref>
  </metadata>

  <objective>
    Formalize the gateway-local INTEGRATION_FRAMEWORK.md (0.7.0 v1) into the canonical standard.
    KEY GROUNDING (0.5.0_AE, CTO-ruled doc-layering 2026-07-01): NFRA_INTEGRATIONS_STANDARD.md v1
    ALREADY EXISTS and is canonical -- so this TO is NOT re-authoring the contract. Scope it to what
    REMAINS: (a) confirm framework-standard-code FIDELITY, (b) MANDATE the 5-step add-process as the
    required checklist, (c) reduce the gateway-tree INTEGRATION_FRAMEWORK.md to a POINTER to the STANDARD.
  </objective>

  <scope>
    <files>
      <file action="verify">docs/architecture/NFRA_INTEGRATIONS_STANDARD.md (canonical contract -- confirm fidelity, do NOT rewrite)</file>
      <file action="modify">infra/aws/ec2/m365-mcp-gateway/INTEGRATION_FRAMEWORK.md (reduce to a pointer to the STANDARD)</file>
      <file action="verify">infra/aws/ec2/m365-mcp-gateway/app/integrations/ (the built code the standard must stay faithful to: base.py IntegrationSpec, registry.py, run_integration_tool)</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">READ FIRST: NFRA_INTEGRATIONS_PRD.md sec 2 + sec 6 gate 1; NFRA_INTEGRATIONS_STANDARD.md (full); app/integrations/base.py + registry.py.</requirement>
    <requirement id="2">FIDELITY CHECK (PRD gate 1): confirm the STANDARD matches the BUILT framework -- IntegrationSpec schema (id/display_name/description/auth_kind/tool_prefix/secret_id/read_only/min_tier/hosts), the 3 AuthKinds (DELEGATED_USER/SHARED_SECRET/NONE), registry.register_factory, the audited run_integration_tool() fail-closed-on-missing-credential path, and fail-closed enablement (ENABLED_INTEGRATIONS default-empty; server.py registers only enabled). Source-confirmed vs app/integrations/, NOT self-report. Any drift STANDARD-vs-code = fix the STANDARD (code is ground truth) and note it.</requirement>
    <requirement id="3">MANDATE THE 5-STEP ADD-PROCESS as the required checklist (PRD sec 2): (1) author app/integrations/&lt;id&gt;/ + read-only tools via run_integration_tool(); (2) register the factory; (3) provision the SM secret (Third-Party Data Standard sec 3, HAR-&gt;C6); (4) grant scoped secretsmanager:GetSecretValue via Terraform; (5) add id to ENABLED_INTEGRATIONS + deploy -- CTO ARCH-GATE FIRST. Make this the referenced gate for any future integration (cite it from the STANDARD so it is not merely prose).</requirement>
    <requirement id="4">POINTER: reduce infra/aws/ec2/m365-mcp-gateway/INTEGRATION_FRAMEWORK.md to a short pointer to docs/architecture/NFRA_INTEGRATIONS_STANDARD.md (code-adjacency only; the canonical contract lives in docs/architecture).</requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">Framework-standard fidelity confirmed source-vs-code (PRD gate 1): STANDARD.md matches app/integrations/ on IntegrationSpec + registry + run_integration_tool + fail-closed enablement + 3 AuthKinds. Any drift fixed in STANDARD.md with a cited line.</criterion>
    <criterion id="2">The 5-step add-process is MANDATED + citable as the required pre-integration checklist (referenced from STANDARD.md), not just documented prose.</criterion>
    <criterion id="3">INTEGRATION_FRAMEWORK.md (gateway tree) is a pointer to the STANDARD; no divergent duplicate contract remains.</criterion>
  </acceptance_criteria>

  <compiler_tools_mandate>
    Use comp-which for any search/inspection. Verify the DEPLOYED gateway behavior (not source) where the standard makes a runtime claim -- e.g. fail-closed enablement (an un-enabled integration adds zero live tools) is a running-gateway fact, confirm on the box, not from source alone. YCharts-enable (2026-07-01) already exercised the enable path -- cite its served audit records if useful.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    NFRA_OPLMCP (the gateway host). CTO arch-gates the standard promotion (PRD standing-role). CVO live-certs fail-closed on the running gateway (P2/gate 5). Coordinate with P2 (0.5.0/CTO) since both reference run_integration_tool + the guard hook; and P3 (0.5.0) owns the storage/dependency section this standard points to.
  </cross_domain_coordination>

  <constraints>
    <constraint>Read-only by default (a mutating integration is a separate explicit escalation). Fail-closed enablement -- enabling is an arch-gated DEPLOY, never a runtime flip.</constraint>
    <constraint>Do NOT re-author NFRA_INTEGRATIONS_STANDARD.md -- it is canonical v1. This is fidelity + checklist-mandate + pointer only.</constraint>
    <constraint>No emojis/non-ASCII in anything that runs on AWS or in the gateway. Commit via .tools/safe-commit.sh --author under your serial.</constraint>
  </constraints>

  <deliverables>
    <deliverable type="commit">CLOUD commit: fidelity-fixes (if any) + 5-step-mandate wiring in STANDARD.md + INTEGRATION_FRAMEWORK.md reduced to pointer</deliverable>
    <deliverable type="ravc">RAVC to COO (CC CTO): fidelity verdict (source-vs-code), the mandated-checklist reference, pointer done</deliverable>
    <deliverable type="log">Session log with Compiler Tools section</deliverable>
  </deliverables>
</task_order>
```
