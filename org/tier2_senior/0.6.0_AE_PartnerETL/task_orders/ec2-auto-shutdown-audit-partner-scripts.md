# EC2 Auto-Shutdown Audit — Partner ETL Run Scripts

<task_order>
  <issuer>2.0.0_SA_COO</issuer>
  <issued>2026-04-02</issued>
  <agent>0.6.0_AE_PartnerETL</agent>
  <status>complete</status>
    <!-- CLOSED 2026-05-12 by 2.0.0_SA_COO per Andrew directive: bulk-close pending/unaddressed pre-May 2026 TOs. Inherits closure from parent project state or supersession. Re-author as new TO if work still required. -->
  <priority>normal</priority>
  <source>CTO directive (ad-hoc operational hygiene, no PRD)</source>
</task_order>

## Context

GLDRST.015 deployed a watchdog-shutdown systemd service for bd-gold-layer-runner.
CTO wants the same shutdown-on-completion discipline verified across ALL EC2 run
scripts in your ownership scope. The goal is to ensure no EC2 instance stays
running (and billing) after its job finishes.

## Scope

Audit every run script you own or execute on EC2, specifically:

1. **bd-gold-layer-runner** — `run_gold_layer.sh`, `ssm-run-gold.sh`
   - Watchdog already deployed (GLDRST.015). Confirm the script itself calls
     `sudo shutdown` or relies on the watchdog. Document which path applies.

2. **Silver build scripts** — any scripts you run on bd-exporter, bd-allocations,
   or bd-transactions instances for silver layer rebuilds (e.g., RPS silver build,
   merge-daily-incremental.py).
   - Does the SSM document or wrapper script shut down the instance on completion?
   - If triggered by EventBridge (bd-allocations at 21:48 UTC, bd-transactions at
     21:40 UTC), these are persistent instances — document whether they SHOULD
     shut down or stay running for the next scheduled trigger.

3. **Gold detail generator** — `bd-gold-detail-generator` (ephemeral, user-data baked).
   - Does user-data.sh include a shutdown command at the end?

## Deliverable

A markdown file in your `logs/2026-04-02/` folder with a table:

| Script / SSM Document | Instance | Shuts Down on Completion? | Mechanism | Gap? |
|---|---|---|---|---|

For each gap found (script completes but instance stays running without watchdog
or shutdown command), note it in the Gap column. Do NOT remediate yet — just audit.
Remediation will be a follow-up TO if gaps are found.

## Acceptance Criteria

- [ ] Every run script in your ownership scope is listed
- [ ] Each entry documents the shutdown mechanism (or lack thereof)
- [ ] Gaps clearly identified with instance name and estimated billing impact
