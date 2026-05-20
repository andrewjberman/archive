<task_order>
  <metadata>
    <id>TRSB_LEDGER.015</id>
    <slug>ae-section11-menachem-probe</slug>
    <issued_by>2.0.0_SA_COO~B</issued_by>
    <issued_to>0.5.0_AE_OpalETL~B</issued_to>
    <date>2026-05-20</date>
    <status>pending</status>
    <dispatch_held>false</dispatch_held>
    <project_code>TRSB_LEDGER</project_code>
    <priority>P2 -- TRSB §11 Phase-0 probe. §11 (second trade administrator, menachem@opalinvest.com) is the last open TRSB workstream; TRSB_LEDGER cannot 3-step-close without it. This probe is the foundation TO -- §11-A (seed) + §11-B (email recipient) hard-gate on its findings.</priority>
    <sla>~1-2h AE wall -- a non-mutating probe (DDB read + SES describe + portal-auth check).</sla>
  </metadata>

  <references>
    <prd>docs/architecture/TRSB_LEDGER.md §11 (v0.4, 2026-05-20) -- §11.1 privilege baseline, §11.2 required changes A/B/C/D, §11.3 SoD consequence, §11.4 scope notes.</prd>
    <origin>Andrew directive 2026-05-20: grant menachem@opalinvest.com the same trade authority as andrew@opalinvest.com across submission/approval/execution; route every executed-trade email + data artifact to Menachem; full access + visibility. Decomposition directed by 1.0.0_SA_CTO~B.</origin>
    <pipeline_rule>Non-mutating probe -- no writes, no deploy. Rule 1 (Terraform-only) applies to the §11-A/§11-B implementing TOs, not this probe.</pipeline_rule>
  </references>

  <context>
    §11 grants menachem@ a mirror of andrew@'s trade authority. Before the seed (§11-A) and the email-recipient change (§11-B) ship, three facts must be established empirically -- the andrew@ row shape (to mirror, not hand-construct), the SES verification state (whether menachem@ can receive email at all), and whether menachem@ already has a portal-auth account (§11-D is conditional on this).
  </context>

  <scope>
    <step>P1 -- trade-users row shape. Direct-read the live trade-users DynamoDB record for andrew@opalinvest.com. Capture its FULL attribute shape verbatim (every attribute, types, exact values) -- groups should be ['approvers','executors'], role 'dev', plus whatever else the row carries. §11-A will replicate this shape exactly, so the probe must capture it completely, not summarize it.</step>
    <step>P2 -- SES verification state (§11.2-C). Describe the SES verification state for: (a) the opalinvest.com DOMAIN, (b) the menachem@opalinvest.com identity. Report whether SES is in sandbox, and whether a verified-domain or verified-identity already covers menachem@ -- this determines whether §11-B needs a one-click menachem@ verification step.</step>
    <step>P3 -- portal-auth account (§11.2-D). Determine whether menachem@opalinvest.com already has a portal-auth account whose claims resolve firmId to the opal-capital scope. Report yes/no + the lookup method. If NO, §11-D is a portal-auth-lane provisioning dependency that surfaces to Andrew (account creation + firm assignment is his call) -- the probe just establishes the fact.</step>
    <step>P4 -- findings report. Route a findings summary to 2.0.0_SA_COO~B (CC 1.0.0_SA_CTO~B): the andrew@ row shape (verbatim), the SES state, the portal-auth yes/no. On these findings COO~B GO's §11-A (.016) + §11-B (.017) and, if P3 = no account, surfaces §11-D to Andrew.</step>
  </scope>

  <acceptance_criteria>
    <ac id="AC1">andrew@opalinvest.com trade-users row shape captured verbatim + complete (every attribute) from a direct DDB read.</ac>
    <ac id="AC2">SES verification state for opalinvest.com domain + menachem@ identity reported; the "does §11-B need a verification step" question answered.</ac>
    <ac id="AC3">menachem@ portal-auth account existence determined (yes/no) + method recorded.</ac>
    <ac id="AC4">Non-mutating -- no writes, no SES changes, no deploy. Findings routed to COO~B CC CTO~B. Session log with Compiler Tools section.</ac>
  </acceptance_criteria>

  <out_of_scope>
    Seeding the menachem@ row (§11-A / .016). Email-recipient changes (§11-B / .017). SES verification ACTION (folds into .017 if needed). Portal-auth account creation (§11-D -- Andrew's call, surfaced post-probe). This TO only ESTABLISHES the facts.
  </out_of_scope>

  <deliverables>
    - Findings report to COO~B CC CTO~B: andrew@ row shape verbatim + SES state + portal-auth yes/no. Session log.
  </deliverables>
</task_order>
