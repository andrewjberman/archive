<to_id>NFRA_INFRPT.DR</to_id>
<project>NFRA_INFRPT</project>
<title>FAST-TRACK operational fix: diagnose + fix infrastructure-daily-snapshot (2AM DR backup) failing 3/3</title>
<assigned_to>0.7.0_AE_CloudOps</assigned_to>
<co_assignees>none (CloudOps operational fix; execution lane = allocation-TBD, see priority)</co_assignees>
<issued_by>2.0.0_SA_COO (NFRA_INFRPT 2026-06-16; the report's one legitimate signal, surfaced by CVO 6d5954360)</issued_by>
<issued_date>2026-06-16</issued_date>
<status>pending</status>
<priority>HIGHEST in NFRA_INFRPT — this is an ACTIVE operational failure, not report content. `infrastructure-daily-snapshot` (the 2AM DR backup, 30-day rollback) is failing 3/3 = ~3 days with no fresh DR restore point. Fix BEFORE/ALONGSIDE the report-content TOs. Gate: AE capacity (execution lane allocation-TBD).</priority>

<references>
  <ref type="finding">docs/briefs/infra-report-revamp-proposal-20260616.md §1 + evidence appendix: infrastructure-daily-snapshot (2AM, 30-day rollback) failing 3/3 — the report flagged it but couldn't explain it (triage dead).</ref>
</references>

<scope>
Diagnose WHY the `infrastructure-daily-snapshot` Lambda (the DR backup) is failing 3/3, and fix it.
- Pull the Lambda's CloudWatch logs for the 3 recent failures -> root-cause (IAM denial? a renamed/deleted source resource? a timeout/memory? a downstream dependency that moved — same class as the SmartX dead-EC2-path drift?).
- Fix the root cause (Terraform for any IAM/config; code via the normal deploy cycle if the Lambda logic is stale). NOT a console hotfix.
- Verify the NEXT scheduled 2AM run (or a controlled invoke) SUCCEEDS + writes a fresh restore point. A backup Lambda is exactly the "positive-signal-only can't detect a frozen producer" class — verify the ARTIFACT (the snapshot) lands, not just rc=0.
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before change">
    <step>
      <run>comp-iam service infrastructure-daily-snapshot (+ pull the 3 CloudWatch failure logs)</run>
      <expect>Root-cause identified from the actual failure logs (NOT guessed). If IAM: the denied action surfaces. If a moved/renamed source: the missing resource surfaces.</expect>
      <if_mismatch>If the failure is a dependency that moved (drift), note it — it is the same stale-architecture class the report itself suffers; fold the learning into P1 DRIFT.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before deploy">
    <step>
      <run>comp-iam gaps (if iam.tf changed)</run>
      <expect>The fix closes the gap; no new gap introduced. Deploy = Terraform (Rule 1) / normal code cycle.</expect>
      <if_mismatch>Resolve before apply.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after deploy">
    <step>
      <run>Verify the next 2AM run (or controlled invoke) + the ARTIFACT it produces (the snapshot object lands fresh)</run>
      <expect>Run SUCCEEDS + a fresh DR restore point is written (mtime current). 0/3 -> passing. Verify the snapshot ARTIFACT exists, not just exit 0.</expect>
      <if_mismatch>Still failing -> re-diagnose. A DR backup that reports success but writes nothing is the false-clean class.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
- Distinct from the report-revamp TOs (P0-P3): this FIXES the failing backup; P1's AUTOMATION-HEALTH section will REPORT on DR-snapshot health going forward (it must distinguish "0 failures because healthy" from "blind"). The fix + the monitoring are complementary.
- If the root cause is a moved/renamed dependency (drift), feed it to P1 DRIFT as a real motivating example.
</cross_domain_coordination>

<acceptance_criteria>
- Root cause of the 3/3 failure identified from the actual CloudWatch logs (documented).
- Fix deployed via Terraform / normal cycle (no console hotfix).
- Next scheduled run (or controlled invoke) SUCCEEDS + writes a fresh DR restore point (artifact verified, not just rc=0).
- Session-log Compiler Tools section reproduces every <run> with observed output + pass/fail.
</acceptance_criteria>

<data_reprocess_scope><no_reprocess_needed>Operational fix to the backup Lambda; no data-pipeline re-emit. The verification is the next successful backup run.</no_reprocess_needed></data_reprocess_scope>
