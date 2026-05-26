<task_order>
<metadata>
  <to_id>MDPF_OWNTS.002</to_id>
  <project>MDPF_OWNTS</project>
  <title>AE chain wire: add Stage 4 OWNTS to mdpf-daily-dispatch.sh + per-stage CloudWatch alarm + RUNBOOK update</title>
  <assigned_to>0.7.0_AE_CloudOps</assigned_to>
  <issued_by>2.0.0_SA_COO</issued_by>
  <issued_date>2026-05-26</issued_date>
  <status>in_review — chain-wire SHIPPED commit `1a320180e` 2026-05-26T~22:25Z; AC1-AC4 MET; AC5 live-fire deferred to next 15:00 UTC EventBridge tick (or expedited via SSM ad-hoc per ws COO direction); RAVC2-Request to ws COO this cycle</status>
  <dispatch_held>false</dispatch_held>
  <priority>HIGH (Andrew sovereign chain; ws CTO PRD canonical; sequential after MDPF_OWNTS.001)</priority>
  <references>
    <ref type="prd">docs/architecture/MDPF_OWNTS.md v0.1 (commit `8a125c682`)</ref>
    <ref type="prd_section">§6 TO decomposition (MDPF_OWNTS.002); §9 sequencing; §8.2 AC7 RUNBOOK update</ref>
    <ref type="depends_on">MDPF_OWNTS.001 (DS author) — RAVC2-ACCEPT required before this dispatch fires; scripts must be S3-deployed before chain wires Stage 4 to dispatch them</ref>
    <ref type="existing_chain">mdpf-pipeline-v1.0.2 + mdpf-daily-dispatch.sh + RUNBOOK_AE_mdpf_daily_chain.md</ref>
  </references>
  <dependencies>
    <dependency>**HARD GATE:** MDPF_OWNTS.001 RAVC2-ACCEPTED + DS-side scripts S3-deployed + comp-pipescript deployed MATCH verified</dependency>
  </dependencies>
</metadata>

<scope>
**Wire the new Stage 4 OWNTS into the existing MDPF daily chain** per PRD v0.1 §3.1 Option A architecture (CTO-selected v1).

**Substrate (3 deliverables):**

1. **Modify `infra/aws/ec2/.../mdpf-daily-dispatch.sh`**
   - Add Stage 4 (post-aggregate stage 3) invoking `build_mdpf_etf_ownership_timeseries.py`
   - Fail-loud on script rc != 0 (mirror Stage 1-3 pattern)
   - Telemetry into existing chain manifest (chain run-id + stage start/end timestamps + stage-rc)
   - Sequential ordering: Stage 4 fires AFTER stage 3 aggregate-AUA emits the augmented platinum with ownership_pct field

2. **Add CloudWatch alarm for Stage 4 failures**
   - Mirror Stage 1-3 alarm pattern (per-stage failure alarm with appropriate SNS topic routing)
   - Threshold: any Stage 4 rc != 0 in the daily chain = alarm fires
   - Update Terraform module covering MDPF chain alarms

3. **Update `RUNBOOK_AE_mdpf_daily_chain.md`**
   - Add Stage 4 section (script + S3 outputs + alarm + recovery procedure)
   - Update chain DAG diagram if present
   - Stage 4 recovery procedure: re-run via SSM if Stage 4 fails after Stage 1-3 pass (no need to re-run upstream stages)

**Per CLAUDE.md Rule 7:** Terraform is the only mechanism for infrastructure changes (alarm + any IAM modifications if needed).

**Per CLAUDE.md Rule 8:** `EC2_MANIFEST.json` checked — if the runner role/instance is unchanged, no manifest update needed. If alarm wiring needs IAM additions, Terraform owns.

**Per CLAUDE.md Rule 9:** Terraform manages EC2 infrastructure; code deployment (the chain script update) is a separate step via `safe-ec2-deploy.sh`.

**Per CLAUDE.md Rule 11:** `./infra/aws/ec2/verify-ec2.sh` MUST run before starting work (verify no drift between local source and deployed code).

**Per CLAUDE.md Rule 18 (NEW):** `terraform apply` MUST go through `.tools/safe-apply.sh` (HALTGT checkpoint).
</scope>

<acceptance_criteria>
- AC1: `mdpf-daily-dispatch.sh` Stage 4 added + fail-loud on rc != 0 + telemetry into chain manifest.
- AC2: CloudWatch alarm for Stage 4 failures wired via Terraform; terraform plan 0-diff after apply.
- AC3: `RUNBOOK_AE_mdpf_daily_chain.md` updated with Stage 4 + recovery procedure (PRD §8.2 AC7).
- AC4: `safe-ec2-deploy.sh` used for deploy (no direct code-on-instance edits per CLAUDE.md Rule 12).
- AC5: First chain fire post-deploy verified Stage 4 fires + emits new artifacts cleanly OR scheduled for next chain run.

**Pass requires all 5 ACs MET.**
</acceptance_criteria>

<compiler_tools_mandate>
- `comp-pipescript deployed` on `build_mdpf_etf_ownership_timeseries.py` (verify runner has the DS-deployed code MATCH before wiring chain)
- `comp-iam service` if any new IAM permissions needed (e.g., S3 write to new prefix — though PRD §3.1 says `inf-gold-runner-ec2-role` already covers it; verify)
- `comp-iam gaps` if `iam.tf` is modified
</compiler_tools_mandate>

<cross_domain_coordination>
- **MDPF_OWNTS.001 (DS) HARD GATE** — your TO does NOT fire until DS RAVC2-ACCEPTED + S3-deployed scripts verified.
- **MDPF_OWNTS.003 (DS RAVC) gates on this RAVC2-ACCEPT** — DS validates end-to-end live-run after your chain wiring lands.
- **CTO ratifies this TO** per PRD §6 (infra change touching MDPF chain) — RAVC2 routes to ws COO; ws COO CC's CTO for ratify.
</cross_domain_coordination>

<deliverable_disposition>
**Submit RAVC2-Request to ws COO** at completion citing:
- Commit hashes (chain script + Terraform alarm + RUNBOOK)
- terraform plan 0-diff confirmation post-apply
- safe-ec2-deploy.sh deploy receipt
- AC1-AC5 evidence inline

**Target wall-time ETA:** ~1d per PRD §6.

**Post-RAVC2-ACCEPT:** MDPF_OWNTS.003 GO-dispatch to DS 0.4.0 for end-to-end RAVC consolidation.

**Live-fire gate:** the next mdpf-daily-dispatch chain run after your deploy MUST emit augmented aggregate-AUA platinum + new etf_ownership_timeseries artifact + alarm coverage active. Live-fire verification gates MDPF_OWNTS.003 dispatch + project close.
</deliverable_disposition>

<notes>
- Sequential single-threaded with .001; no parallel work option. Your spawn timing is "right after .001 RAVC2-ACCEPTed" + spawn-with-direction substrate from CTO PRD + .001 RAVC2 ratification chain.
- AE 0.7 not currently LIVE per broker scan; will spawn via MSTR /allocation SPAWN-NEEDED at .001 RAVC2-ACCEPT time (carry-forward dispatch).
</notes>
</task_order>
