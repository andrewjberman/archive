# Task Order (ad-hoc, no PRD): SES sender lint -- enforce CLAUDE.md Rule 23 (opalinvest.dev only)

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-07-07-ses-sender-lint</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps~B</issued_to>
    <date>2026-07-07</date>
    <status>pending</status>
    <dispatch_state>DISPATCHED 2026-07-07T17:05Z -- re-routed to ~B (idle, all Wave-1 work closed) since base 0.7.0 is busy on DNS/decommission work. CTO-ratified rule (commit 888c4b381), from today's partner-etl-ops-alerts P1 (an unauthenticated andrew@opalinvest.com sender triggered an EOP quarantine).</dispatch_state>
    <gate_note>Deterministic, cheap check -- no architecture decision needed.</gate_note>
  </metadata>

  <objective>Add a commit/deploy-time lint over ses.send_email/send_raw_email Source= literals and Lambda EMAIL_FROM/SES_SENDER env values, flagging any non-opalinvest.dev sender. Institutionalizes CLAUDE.md Rule 23 before the pattern drifts back (the andrew@opalinvest.com unauthenticated-sender class that caused today's silent EOP quarantine).</objective>

  <requirements>
    <requirement id="1">Scan for ses.send_email/send_raw_email Source= literals across the repo (fold into an existing gate script, e.g. commit-gate.sh, or a standalone comp-* check -- your call on the cheapest integration point).</requirement>
    <requirement id="2">Scan Lambda EMAIL_FROM/SES_SENDER env values (TF or deployed config) for non-opalinvest.dev senders.</requirement>
    <requirement id="3">Flag (WARN or BLOCK, your call given no live incident currently) any non-opalinvest.dev sender found.</requirement>
  </requirements>

  <acceptance_criteria>
    <criterion>Lint runs deterministically (commit-time or deploy-time, whichever fits the chosen integration point) and correctly flags a planted non-opalinvest.dev sender fixture.</criterion>
    <criterion>Lint passes clean on the current estate (today's fix already uses noreply@opalinvest.dev).</criterion>
  </acceptance_criteria>

  <references>
    <ref type="rule">CLAUDE.md Rule 23</ref>
    <ref type="finding">3.0.0_SA_CVO partner-etl-ops-alerts P1 investigation, 2026-07-07</ref>
  </references>
</task_order>
```
