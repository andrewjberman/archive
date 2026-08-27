# Task Order: NFRA_INTEGRATIONS P3 -- STORAGE (net-new schema: code-location / dependency-models / firm-separation / egress)

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-07-02-nfra-integrations-p3-storage-schema</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.5.0_AE_OpalETL</issued_to>
    <date>2026-07-02</date>
    <status>complete -- SPRING-CLEAN 2026-08-25: project NFRA_INTEGRATIONS is complete; this TO was last touched 2026-07-02, predating the project close 2026-07-08. Closed as a record act, not a work verdict. Prior status: active</status>
    <thread_serial>NFRA_INTEGRATIONS-003</thread_serial>
    <prd_ref>docs/architecture/NFRA_INTEGRATIONS_PRD.md (Pillar 3, sec 4) + sec 6 gate 4</prd_ref>
    <seed>docs/briefs/nfra-integrations-pillar3-storage-draft-20260701.md (your draft this session)</seed>
  </metadata>

  <objective>
    Author the NET-NEW canonical STORAGE / dependency / bucket / egress schema for gateway integrations
    (PRD Pillar 3) -- the gap this pillar closes (it is CONVENTION today, not canonical). Your draft
    (nfra-integrations-pillar3-storage-draft-20260701.md) is the seed; the canonical home is PRD sec 4 /
    STANDARD.md sec pointed at line 129. Fold to STANDARD.md on CTO RAVC. This pillar is INDEPENDENT of
    the SCTY sequencing (storage/bucket/firm-separation, does not touch the guard) -- run it in PARALLEL
    with your MDPF flip hold (doc/schema work, non-blocking on the flip).
  </objective>

  <scope>
    <files>
      <file action="finalize">docs/briefs/nfra-integrations-pillar3-storage-draft-20260701.md -&gt; fold into docs/architecture/NFRA_INTEGRATIONS_STANDARD.md (storage section, on CTO RAVC)</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">READ FIRST: NFRA_INTEGRATIONS_PRD.md sec 4 + sec 6 gate 4; CLAUDE.md rule 13 (firm-separation bucket convention); LAMBDA_DEPLOYMENT_PROTOCOL (the layer/layer-map model); Third-Party Data Standard sec 3 (credentials).</requirement>
    <requirement id="2">CODE LOCATION + NAMESPACE: app/integrations/&lt;id&gt;/ (spec + integration + client); every tool namespaced by tool_prefix (e.g. ycharts_) -- collision-free on the shared MCP surface.</requirement>
    <requirement id="3">DEPENDENCIES -- TWO models documented + WHEN-EACH: the gateway-EC2 uses in-package + the gateway VENV (a new heavy dep = a gateway-venv + deploy concern); DISTINCT from the pipeline-Lambda LAYER / layer-map model. An integration on the gateway is venv-deps; a data-pipeline Lambda is layer-deps -- explicitly do-not-cross the models.</requirement>
    <requirement id="4">CREDENTIALS: one SM secret per integration (&lt;source&gt;/credentials); IAM GetSecretValue scoped to that EXACT ARN on the gateway role.</requirement>
    <requirement id="5">DATA / FIRM-SEPARATION INVARIANT (hard, PRD gate 4): if an integration PERSISTS pulled data, it follows the per-firm bucket (opal-data-{firm}) + medallion convention and MUST NOT cross firm buckets (rule 13 + IAM-enforced). YCharts is read-only-passthrough (persists nothing); kuzu/nessie/iceberg read-only in-estate; a FUTURE persisting integration binds to this rule -- specify where its artifacts land + the naming.</requirement>
    <requirement id="6">EGRESS: the hosts allowlist per integration IS the network-egress governance basis (pairs with the P2 arch-gate axis-a + the SCTY_PREMCP SSRF-egress-deny posture).</requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">The storage schema (code-location/tool_prefix, the two dependency models + when-each, one-SM-secret-per-integration, egress-allowlist) is canonical in STANDARD.md sec 4 -- an integration author can locate + provision without re-deriving convention.</criterion>
    <criterion id="2">The FIRM-SEPARATION invariant on persisted integration data is stated as a HARD rule (PRD gate 4): a persisting integration cannot write cross-firm; where artifacts land + naming specified; ties to rule 13 + IAM enforcement.</criterion>
    <criterion id="3">Folded to STANDARD.md on CTO RAVC (draft -&gt; canonical), draft brief retired/pointed.</criterion>
  </acceptance_criteria>

  <compiler_tools_mandate>
    comp-which for search; for the firm-separation invariant, ground the bucket/IAM reality via comp-iam / the rule-13 PIPELINE_MAP -- confirm the per-firm separation is IAM-enforced, not just documented. Do not cross bd/cot/inf trees in any example.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    DATA_PLATFORM / rule 13 (the firm-separation bucket convention this pillar canonicalizes for integration data). SCTY_PREMCP (the egress/SSRF perimeter the hosts-allowlist pairs with). CTO folds the draft to STANDARD.md on RAVC. INDEPENDENT of P2/SCTY sequencing -- no cross-scheduled hands (does not touch the guard). Parallel-safe with your MDPF flip hold.
  </cross_domain_coordination>

  <constraints>
    <constraint>Firm-separation is a HARD invariant (rule 13, IAM-enforced) -- never a soft convention in this schema. Read-only by default.</constraint>
    <constraint>Do not cross the two dependency models (gateway-venv vs pipeline-Lambda-layer). One SM secret per integration, scoped IAM.</constraint>
    <constraint>Non-blocking on the MDPF flip -- if the flip GO fires, the flip takes priority; P3 is doc/schema and resumes after. No emojis/non-ASCII. safe-commit --author under your serial.</constraint>
  </constraints>

  <deliverables>
    <deliverable type="commit">CLOUD commit: P3 storage schema folded into STANDARD.md sec 4 (on CTO RAVC); draft brief retired/pointed</deliverable>
    <deliverable type="ravc">RAVC to COO (CC CTO for the fold): the canonical storage/dependency/firm-separation/egress schema</deliverable>
    <deliverable type="log">Session log with Compiler Tools section</deliverable>
  </deliverables>
</task_order>
```
