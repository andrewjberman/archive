# Task Order: NFRA_INFRPT P2 -- cost-depth section + security triage + snapshot-reaper (STAGED+undriven since ~06-17 -- owner-gap, UNBLOCKED)

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-07-07-nfra-infrpt-p2</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-07-07</date>
    <status>complete</status>
    <dispatch_state>DISPATCHED 2026-07-07 (post-reboot Wave-1), completed same session by 0.7.0_AE_CloudOps.</dispatch_state>
    <gate_note>COO-RESOLVABLE: assign an active lane (the owner-gap is the true blocker, not a dependency). Validate-on-scheduled-nightly.</gate_note>
    <evidence>
      Req 1 (cost-depth $ attribution) + req 3 (false-clean-safe, status=watch not ok on failed probes) shipped as one increment in opal-infrastructure-monitor Lambda, shared-infra-v1.36.0, ledger infrpt-p2-cost-depth-security-trend CLOSED.
      Req 2 (snapshot-reaper) shipped as reap_old_snapshots() in infrastructure-daily-snapshot step 8b, shared-infra-v1.33.0, ledger infrpt-p2-snapshot-reaper CLOSED -- verification rides the scheduled 07:00 UTC run (no ad-hoc gold-run per CLAUDE.md).
      Also folded in (COO-directed, same session): TF-import of 2 undeclared IaC-drift resources (opal-data-portal-v2 S3 + opal-portal-market-data DynamoDB), shared-infra-v1.35.0, ledger infrpt-p2-tf-import-drift CLOSED.
      Req 4 (CVO verifies on the emitted artifact, not rc=0) intentionally rides the natural next scheduled runs (07:00 UTC reaper, 13:00 UTC monitor report) -- both already past for 2026-07-07, so first live verification window is 2026-07-08. This is by design (no-ad-hoc-validation discipline), not an unresolved gap. CVO CC'd separately with the verify-ask by 0.7.0_AE_CloudOps.
      Adjacent finding (not fixed, out of scope): base opal-infrastructure-monitor inline IAM policy on opal-portal-lambda-role is itself undeclared in TF -- noted in pipeline_inventory.xml core doc for a future pass.
      Session log + core doc (pipeline_inventory.xml) update: 0.7.0_AE_CloudOps, 2026-07-07.
    </evidence>
  </metadata>

  <objective>Cost-depth (per-pipeline $ attribution off the 6 live CE tags + trend/forecast + biggest-movers + EC2 right-size flags) + security triage (trend/top-N-new/Claude briefing) + snapshot-reaper (daily AMI/EBS cleanup + 30d retention). STAGED but undriven since the ~B lane stood down 06-16 + 0.7.0_AE was consumed by PREMCP.</objective>

  <requirements>
    <requirement id="1">per-pipeline $ attribution grounded on the 6 live CE keys</requirement>
    <requirement id="2">snapshot-reaper verified on a SCHEDULED run (no ad-hoc), retention honored</requirement>
    <requirement id="3">false-clean hard-criterion: no section reports 'clean' it hasn't probed</requirement>
    <requirement id="4">CVO verifies on the emitted 13:00 UTC artifact, not rc=0</requirement>
  </requirements>
</task_order>
```
