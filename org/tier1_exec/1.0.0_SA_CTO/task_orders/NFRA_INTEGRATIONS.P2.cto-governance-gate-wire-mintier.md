# Task Order: NFRA_INTEGRATIONS P2 -- GOVERNANCE (repeatable arch-gate + wire min_tier to the live SCTY guard)

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-07-02-nfra-integrations-p2-governance-gate</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>1.0.0_SA_CTO</issued_to>
    <date>2026-07-02</date>
    <status>complete</status>
    <completed>2026-07-06</completed>
    <completion_note>
      All 3 ACs met. AC1 (repeatable 3-axis arch-gate checklist SS8.1 G1-G8 + read-only
      + min_tier + audit) + AC3 (ownership model SS8 + fail-closed invariant SS6/SS8.1)
      codified in NFRA_INTEGRATIONS_STANDARD.md v1.2 (commit 8dca11976). AC2 -- the last
      open gate -- CLOSED on CVO's independent gate-3 CERT = PASS (3.0.0_SA_CVO
      20260702T221522Z): below-tier-deny LIVE-GROUNDED on the DEPLOYED gateway
      (i-07dccb1615503ac99) + SERVED audit lake -- readonly-cert-probe (tier read_only)
      DENIED min_tier 'standard' on ycharts_freshness @2026-07-01T22:32:50Z (credential
      never fetched = zero egress), and andrew@ (master_admin) PASS @22:32:52Z; ONE shared
      SCTY guard for _run() AND the integration path (base.py:106-115). CTO ACK'd the cert
      20260702T221836Z. Generalizes the YCharts self-cert into the STANDARD gate-3
      requirement. Grounded on deployed bytes + served audit, not self-report. Parent
      project NFRA_INTEGRATIONS stays ACTIVE (P1/P3 pillars ongoing). Closed on Monday-boot
      reconciliation -- flip lagged the 07-02 gate-3 verdict (session was un-logged).
    </completion_note>
    <thread_serial>NFRA_INTEGRATIONS-002</thread_serial>
    <prd_ref>docs/architecture/NFRA_INTEGRATIONS_PRD.md (Pillar 2, sec 3) + sec 6 gates 2-3-5</prd_ref>
  </metadata>

  <objective>
    Codify the REPEATABLE per-integration CTO arch-gate and CONFIRM/GENERALIZE the min_tier enforcement
    against the LIVE SCTY_MCPGUARD guard (shipped 2026-07-01) so the governance spine is reusable for
    N integrations, not re-derived per source. YCharts-enable (2026-07-01) already demonstrated min_tier
    enforcement on the deployed guard (below-tier-deny self-cert PASS) -- generalize that into the standard
    + get CVO's independent live-cert of the pattern.
  </objective>

  <scope>
    <files>
      <file action="modify">docs/architecture/NFRA_INTEGRATIONS_STANDARD.md (governance section: the 3-axis arch-gate checklist + tier-enforcement + ownership model)</file>
      <file action="verify">infra/aws/ec2/m365-mcp-gateway/app/integrations/ (run_integration_tool enforcing spec.min_tier against the deployed SCTY guard module)</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">READ FIRST: NFRA_INTEGRATIONS_PRD.md sec 3 + sec 6 gates 2/3/5; SCTY_MCPGUARD_PRD.md (the LIVE tier gate); the YCharts-enable served audit records (below-tier-deny + roster-200) that already exercised the wiring.</requirement>
    <requirement id="2">CODIFY THE 3-AXIS ARCH-GATE (repeatable checklist, PRD gate 2): every new integration is a gated change verified BEFORE enable on -- (a) NEW EGRESS (the hosts allowlist), (b) NEW TOOL SURFACE on the crown-jewel gateway, (c) SECRET + IAM (one scoped SM secret + a scoped GetSecretValue grant). Plus read-only-confirmed + min_tier-set + audit-wired. Enabling is an arch-gated DEPLOY (env + IAM), NEVER a runtime flip.</requirement>
    <requirement id="3">TIER ENFORCEMENT WIRED (PRD gate 3): confirm run_integration_tool() enforces spec.min_tier against the LIVE deployed SCTY guard -- ONE shared guard module for _run() AND the integration path. YCharts already runs under min_tier=standard on the deployed bytes; generalize the wiring as the standard's requirement (not YCharts-specific). CVO independently live-verifies a below-tier caller is DENIED on the running gateway.</requirement>
    <requirement id="4">OWNERSHIP MODEL codified (PRD sec 3): gateway owner-of-record (CloudOps/AE) owns box + deploy; the integration AUTHOR builds under the framework (build-pen); CTO arch-gates; CVO live-certs read-only + audit + tier behavior on the running gateway.</requirement>
    <requirement id="5">FAIL-CLOSED proven (PRD gate 5): an un-enabled integration adds zero live tools -- state it as a standing governance invariant CVO verifies on the running gateway.</requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">The 3-axis arch-gate (egress/tool-surface/secret+IAM) + read-only + min_tier + audit is codified as a REPEATABLE checklist in STANDARD.md -- runnable for the next integration without re-derivation (PRD gate 2).</criterion>
    <criterion id="2">run_integration_tool() min_tier enforcement against the LIVE guard is confirmed + generalized in the standard; CVO independently live-certs a below-tier caller denied on the running gateway (PRD gate 3).</criterion>
    <criterion id="3">Ownership model + fail-closed-enablement invariant codified (PRD sec 3 + gate 5).</criterion>
  </acceptance_criteria>

  <compiler_tools_mandate>
    comp-which for search/inspection; comp-iam for the gateway role's scoped GetSecretValue grants (note: comp-iam default modes parse TF=DESIRED; ground a FRESH grant on live aws iam get-role-policy). Verify the min_tier enforcement + fail-closed on the DEPLOYED gateway bytes (SSM/box-verify), not source -- the YCharts self-cert used exactly this method.
  </compiler_tools_mandate>

  <cross_domain_coordination>
    SEQUENCING (0.5.0_AE flag): P2 is SCTY-adjacent -- it CONSUMES the SCTY_MCPGUARD certified guard and pairs with SCTY_PREMCP (egress perimeter). Sequence P2 with/after the SCTY_MCPGUARD + SCTY_PREMCP decomposition since all touch the SAME guard module -- that is where hands cross-schedule (0.5.0/CTO own those). SCTY_MCPGUARD is live-cert PASS (CVO 4/4) -- confirm its state before wiring. Coordinate CVO for the independent tier-deny live-cert; AE (0.7.0/0.5.0) for any gateway-code wiring.
  </cross_domain_coordination>

  <constraints>
    <constraint>Read-only by default; mutating = separate escalation. Enabling is an arch-gated deploy, never a flip.</constraint>
    <constraint>ONE shared guard module for _run() and the integration path -- do NOT fork a second tier gate.</constraint>
    <constraint>Ground tier/fail-closed claims on the DEPLOYED/running gateway (Rule 22 + verify-served); a causal/behavioral claim needs source+graph grounding to be actionable. No emojis/non-ASCII on AWS. safe-commit --author under your serial.</constraint>
  </constraints>

  <deliverables>
    <deliverable type="commit">CLOUD commit: STANDARD.md governance section (3-axis gate + tier-enforcement + ownership + fail-closed invariant)</deliverable>
    <deliverable type="ravc">RAVC to COO: the repeatable checklist + CVO's independent tier-deny live-cert verdict</deliverable>
    <deliverable type="log">Session log with Compiler Tools section</deliverable>
  </deliverables>
</task_order>
```
