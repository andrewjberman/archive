# Task Order (ad-hoc, no PRD): SES sender lint -- enforce CLAUDE.md Rule 23 (opalinvest.dev only)

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-07-07-ses-sender-lint</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps~B</issued_to>
    <date>2026-07-07</date>
    <status>complete</status>
    <dispatch_state>DISPATCHED 2026-07-07T17:05Z -- re-routed to ~B (idle, all Wave-1 work closed) since base 0.7.0 is busy on DNS/decommission work. CTO-ratified rule (commit 888c4b381), from today's partner-etl-ops-alerts P1 (an unauthenticated andrew@opalinvest.com sender triggered an EOP quarantine). CLOSED 2026-07-07T17:30Z.</dispatch_state>
    <gate_note>Deterministic, cheap check -- no architecture decision needed.</gate_note>
  </metadata>

  <objective>Add a commit/deploy-time lint over ses.send_email/send_raw_email Source= literals and Lambda EMAIL_FROM/SES_SENDER env values, flagging any non-opalinvest.dev sender. Institutionalizes CLAUDE.md Rule 23 before the pattern drifts back (the andrew@opalinvest.com unauthenticated-sender class that caused today's silent EOP quarantine).</objective>

  <requirements>
    <requirement id="1" status="met">Scan for ses.send_email/send_raw_email Source= literals. Folded into commit-gate.sh (org/modules/graph/ses_sender_lint_cli.py, wired into .tools/commit_gate_runner.py) -- the cheapest integration point since that runner already exists post-ADHC_COMMITGATE.</requirement>
    <requirement id="2" status="met">Scan Lambda EMAIL_FROM/SES_SENDER env values. Two surfaces: Python os.environ.get(NAME, 'default@domain') sender-shaped bindings, AND a new .tf handling branch in commit_gate_runner.py (Terraform wasn't scanned by any check before this TO) for literal EMAIL_FROM/SES_SENDER Lambda env values.</requirement>
    <requirement id="3" status="met">BLOCK, not WARN (my call): the check is cheap + fully deterministic (a hardcoded string literal has zero false-positive surface) and the failure mode is a SILENT nondeterministic delivery quarantine -- exactly today's incident. No reason to let a second one through on a WARN.</requirement>
  </requirements>

  <closure_evidence>
    Found + fixed 4 LIVE estate violators during Phase-1 discovery (not just a test fixture):
    all 4 trade-pipeline Lambdas (trade-dashboard-api, trade-parquet-batch-export,
    trade-submission-handler, trade-workflow-handler) shared an identical copy-pasted
    EMAIL_FROM default of trades@opalcapital.com. Live-grounded (Rule 22a APPLIED check):
    2/4 had the correct value set live via Terraform (no incident); 2/4 had NO EMAIL_FROM env
    var declared in Terraform at all AND dead-code-unused in source (confirmed via
    get-function-configuration + source grep) -- a latent landmine, not a live incident. Fixed
    all 4 defaults to trades@opalinvest.dev. Self-test 9/9, planted-fixture BLOCK exercised for
    both .py and .tf, full estate re-scan returns 0 findings post-fix. Commits: 16c691566
    (lint + fixes), c4d1f8300 (session log:
    org/tier2_senior/0.7.0_AE_CloudOps/logs/2026-07-07/ses_sender_lint_rule23_enforcement.md).
  </closure_evidence>

  <references>
    <ref type="rule">CLAUDE.md Rule 23</ref>
    <ref type="finding">3.0.0_SA_CVO partner-etl-ops-alerts P1 investigation, 2026-07-07</ref>
  </references>
</task_order>
```
