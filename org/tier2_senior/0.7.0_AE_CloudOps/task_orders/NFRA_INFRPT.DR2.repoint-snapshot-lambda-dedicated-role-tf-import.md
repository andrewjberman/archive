<to_id>NFRA_INFRPT.DR2</to_id>
<project>NFRA_INFRPT</project>
<title>Repoint infrastructure-daily-snapshot to the dedicated role + import the orphan Lambda+EventBridge into TF -- unwinds the DR temp over-grant + fixes the console-orphan drift</title>
<assigned_to>0.7.0_AE_CloudOps</assigned_to>
<co_assignees>none (CloudOps IAM + TF-import; the ~B NFRA_INFRPT lane)</co_assignees>
<issued_by>2.0.0_SA_COO (NFRA_INFRPT 2026-06-16; CTO architectural ruling 201006Z -- the clean end-state for the DR fix)</issued_by>
<issued_date>2026-06-16</issued_date>
<status>staged</status>
<priority>BINDING near-term (CTO 201006Z) -- NOT open-ended. Unwinds the TIME-BOXED least-privilege EXCEPTION the DR fast-fix added (EC2 image/snapshot lifecycle Resource=* on the SHARED opal-portal-lambda-role, which widens that portal-serving role's blast radius). GATE: ~B's DR (NFRA_INFRPT.DR) must FIRST verify a REAL restore point lands (close-gate = DR producing restore points, NOT TF-applied) -- do NOT repoint onto an unverified base. GOes on ~B's DR restore-point RAVC2.</priority>

<references>
  <ref type="dr-ravc1">~B NFRA_INFRPT.DR RAVC1 (200309Z): root-cause = infra-snapshot Lambda NEVER produced a restore point (~4mo); 3 bugs (missing bucket / wrong shared role / unused dedicated role); Lambda+EventBridge are console orphans (not in TF). Minimal fix f6c905fdb.</ref>
  <ref type="cto-ruling">CTO 201006Z: concur temp over-grant for DR-urgency; YES the orphan-import repoint = clean end-state; verify-restore-point-FIRST; DR2 binding.</ref>
</references>

<scope>
The clean end-state CTO ruled (three wins: unwinds the over-grant / fixes the console-orphan DRIFT / wires the code into CI-zip->S3 per Rule-12):
1. **Orphan-import** the infrastructure-daily-snapshot Lambda + its EventBridge trigger into Terraform (they are console orphans — source-tracked + in source-map, NOT in TF). The code artifact goes through the CI-zip->S3 path (Rule-12; this is the careful CI-artifact change, NOT a fast-track move).
2. **Repoint** the Lambda's execution role from the shared `opal-portal-lambda-role` to the EXISTING dedicated `infrastructure-snapshot-role` (already has the verified-complete correct perms).
3. **REMOVE** the temporary DR-fix grant from the shared portal role (the EC2 image/snapshot Resource=* + InfraSnapshotIO added in NFRA_INFRPT.DR) -> least-privilege restored, the time-boxed exception unwound.
4. **Verify 0-loss to DR:** a real restore point must still land post-repoint (the repoint must not break the just-restored DR).
5. **EBS step REMOVE-or-FIX + land the COMPLETE manifest (folded in from DR's 2nd bug; Rule-1-coupled to THIS import).** The handler's re-raise-on-any-component-error is made NON-FATAL regardless (try/except + continue) so the COMPLETE manifest (manifest.json + restore.sh + the 7 component JSONs) lands -- the AMIs-only DR close deferred this. The `snapshot_ebs_volumes` (~L206) step = **SCOPED FIX, LOCKED** (coverage answered 2026-06-16: 0 standalone/detached vols [CTO literal condition clean] BUT step-2 covers 16 vols on 16 NON-critical instances the 9 AMIs don't capture -- dead SmartX EC2 / OPLMCP gw / ~14 agent EC2s -- so REMOVE would drop that coverage): **(1) SKIP volumes whose instance was AMI'd in step 1** (kills the SnapshotCreationPerVolumeRateExceeded double-snapshot bug + cost waste) + **(2) snapshot the REMAINING volumes (the 16 non-critical-instance + any future detached) NON-FATALLY** (try/except continue). Eliminates the double-snapshot WHILE preserving full volume DR coverage + lands the complete manifest. (Strictly better than remove [coverage drop] or naive-fix [keeps double-snapshot].) The DR close logs those 16 vols as a known DR2-pending coverage item. Rule-1-coupled to this import (no console hotfix — the Lambda enters TF + CI-zip->S3 here), which is why it rides DR2 not DR.

NOTE: this is NFRA_INFRPT eating its own dogfood — the console-orphan drift fixed here is the exact class the report's DRIFT (P1/E) section is built to catch. Note the linkage.
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before change">
    <step>
      <run>comp-iam service infrastructure-daily-snapshot + comp-blast opal-portal-lambda-role</run>
      <expect>Confirm the dedicated infrastructure-snapshot-role has the complete correct perms (the Lambda's needs). comp-blast the SHARED portal role: enumerate every OTHER Lambda using it -> confirm removing the EC2-snapshot/InfraSnapshotIO grant breaks NONE of them (the grant was DR-only; portal Lambdas never needed it).</expect>
      <if_mismatch>If any other consumer of the shared role actually uses the EC2-snapshot grant, STOP — the removal would break it; surface before unwinding.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before apply">
    <step>
      <run>comp-iam gaps + safe-apply targeted plan</run>
      <expect>Post-repoint: the Lambda on the dedicated role (no gap); the shared portal role NO LONGER carries the EC2-snapshot/InfraSnapshotIO grant; the orphan Lambda+EventBridge now in TF state (0 console-orphan drift). Terraform-only (Rule 1).</expect>
      <if_mismatch>Resolve before apply. HALTGT checkpoint.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after apply">
    <step>
      <run>Controlled-invoke (or next 2AM) + verify a REAL restore point lands post-repoint + comp-manifest-check (orphan now tracked)</run>
      <expect>DR STILL produces a restore point on the dedicated role (0-loss to the DR restored by NFRA_INFRPT.DR — artifact lands, fresh mtime, NOT rc=0). comp-manifest-check shows the Lambda+EventBridge no longer console-orphans (in TF + source-map aligned). The shared-role over-grant is gone.</expect>
      <if_mismatch>If no restore point post-repoint -> the repoint broke DR; roll back to the (working) DR-fix state + re-diagnose. DR producing restore points is the close-gate, NOT TF-applied.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
- GATED on NFRA_INFRPT.DR verifying a real restore point first (CTO binding sequencing) — do NOT repoint onto an unverified base; the repoint must be 0-loss to the restored DR.
- This fixes a console-orphan DRIFT — the SAME class the report's P1/E DRIFT section catches (dogfood). When P1 lands, the DRIFT section should no longer flag this Lambda (it's now in TF).
- The reaper (flag B) is folded into P2 (cost), paired with the 30-day-rollback retention — separate from DR2.
</cross_domain_coordination>

<acceptance_criteria>
- The infrastructure-daily-snapshot Lambda runs on the dedicated infrastructure-snapshot-role (NOT the shared portal role).
- The temporary EC2-snapshot/InfraSnapshotIO grant is REMOVED from opal-portal-lambda-role (least-privilege restored; the time-boxed exception closed).
- The Lambda + EventBridge trigger are in Terraform (console-orphan drift fixed; comp-manifest-check clean; code via CI-zip->S3 per Rule-12).
- Post-repoint DR is 0-loss: a real restore point lands (artifact verified, not rc=0).
- Session-log Compiler Tools section reproduces every <run> with observed output + pass/fail.
</acceptance_criteria>

<data_reprocess_scope><no_reprocess_needed>Infra/IAM + TF-import change to the DR backup Lambda; no data-pipeline re-emit. Verification = a real restore point landing post-repoint.</no_reprocess_needed></data_reprocess_scope>
