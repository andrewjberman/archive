<task_order>
<metadata>
  <to_id>ADVI_INFNNA.P2.W6.2</to_id>
  <project>ADVI_INFNNA</project>
  <title>AE: daily served-artifact partition-completeness checker Lambda for canonical NNA — alarm on sum(leaves)!=firm delta or coverage-drop (reuse mdpf-freshness-checker pattern)</title>
  <assigned_to>0.7.0_AE_CloudOps</assigned_to>
  <issued_by>2.0.0_SA_COO</issued_by>
  <issued_date>2026-06-02</issued_date>
  <status>IMPL-COMPLETE + DEPLOYED, RAVC2-pending CTO co-verify + CVO confirm (2026-06-02). AC8 MET: inf-nna-partition-checker Lambda deployed via safe-apply (inf-pipeline, 9 resources, 0-diff verified), inf-pipeline-v1.7.68 tagged+pushed, source-mapped (c080a8da2), comp-iam no-gap (s3:GetObject GRANTED; cloudwatch:PutMetricData scoped to ADVI/NNA, verified by live metric emit). Reads served advisor_nna_canonical.json daily (EventBridge cron 30 19 UTC); emits ADVI/NNA PartitionCompletenessBreach + PartitionReconcileDelta + CoverageStates; alarm inf-nna-partition-completeness-breach routes to opal-infrastructure-alerts on breach>=1 / dead-checker (treat_missing_data=breaching). Live invoke breach=0 (real artifact clean: all_pass=true, deltas=0, states=17). AC8 SYNTHETIC-INJECTION test PASS (OK->ALARM transition fires SNS; dead-checker path independently confirmed). Binds to the EXACT DS-stamped reconciliation.all_pass / max_abs_delta / series_tie_max_abs_delta / per_window deltas + granularity_coverage floors (= durable daily form of CVO's W4 RIGID bar). Code 878fd6c8b, TF+map c080a8da2.</status>
  <dispatch_held>false</dispatch_held>
  <priority>MEDIUM — Andrew-direct W6 scope (CTO e5b28ee4f) "install the guard, not just fix the number." Standing protection against future canonical-NNA partition-incompleteness; not on the INFNNA-close critical path.</priority>
  <references>
    <ref type="prd">docs/architecture/ADVI_INFNNA_P2.md (sec.3.W6.2)</ref>
    <ref type="scope_add">CTO e5b28ee4f (W6 no-silent-loss, AC8)</ref>
    <ref type="reuse_pattern">mdpf-freshness-checker Lambda (AE's OPS1 D3, mdpf-pipeline-v1.1.0) — daily checker + CloudWatch metric + alarm to SNS; reuse this scaffold</ref>
    <ref type="artifact">platinum/{firm}/advisor_nna_canonical.json — DS stamps reconciliation.all_pass + max_abs_delta + series_tie_max_abs_delta + granularity_coverage (W6.2(i), LIVE)</ref>
  </references>
</metadata>

<scope>
**Andrew-direct W6 framing (CTO e5b28ee4f):** the INFNNA finding's real danger is INTERNAL INCONSISTENCY (drill leaves not reconciling to the correct headline + dropped granularity), hidden because nothing ASSERTS partition-completeness. W6 installs the standing guard. W6.2(i) [DS, DONE] stamps a self-reconciliation block into the canonical artifact. W6.2(ii) [THIS TO, AE] is the daily standing alarm on it.

## Build (reuse the mdpf-freshness-checker pattern)
A daily served-artifact checker Lambda that reads platinum/{firm}/advisor_nna_canonical.json (the SERVED canonical NNA artifact) and ALARMS on any partition-completeness regression:
- Re-assert the DS-stamped reconciliation properties on the SERVED artifact: reconciliation.all_pass == true; max_abs_delta == 0 (within a cent tolerance); series_tie_max_abs_delta == 0; granularity_coverage not dropped (e.g. state-count regressing — catches the old "8 vs 14 states" top-N class).
- Emit a CloudWatch metric (e.g. ADVI/NNA.PartitionReconcileDelta + .CoverageStates) + a daily-fire alarm to the ops SNS topic on delta!=0 OR coverage-drop OR all_pass=false OR a dead-checker (treat_missing_data=breaching, per your D3 pattern).
- This is the DURABLE form of CVO's W4 RIGID bar — W4 certs once at ship; W6.2 re-asserts the same sum(leaves)==firm property DAILY so a future producer regression can't silently undercount again.

## Deploy (CLAUDE.md non-negotiables — same as your D3)
Terraform-only (Rule 7) via safe-apply (Rule 18 HALTGT); no layer / stdlib+boto3 (Rule 3); least-priv IAM (GetObject on the canonical key(s) + PutMetricData scoped to the ADVI/NNA namespace); source-map entry (Rule 4); record-terraform-deploy + tag (Rule 6).
</scope>

<acceptance>
- [ ] AC8 — checker Lambda deployed (TF, safe-apply 0-diff, tagged, source-mapped); reads the served advisor_nna_canonical.json daily; emits the reconcile-delta + coverage metric; alarm routes to ops SNS on delta!=0 / coverage-drop / all_pass=false / dead-checker. SYNTHETIC-UNDERCOUNT INJECTION test fires the alarm (prove it catches a regression, like your D3 set-alarm-state test). comp-iam no-gap.
- [ ] CLOSURE: RAVC2 to ws CTO + COO + CVO. CTO co-verifies it binds to the same reconciliation.all_pass/max_abs_delta/series_tie that DS stamps (= the durable form of CVO's W4 bar — CVO confirms).

Take AFTER ADVI_INFPRM.W2. (MDPF OPS1 AC4#2 still auto-accrues Wed via your D3 alarm, independent.)
</acceptance>

<notes>
Authored by COO from the W6 scope-add (CTO e5b28ee4f, Andrew-direct). Adds pod 0.7 to ADVI_INFNNA. The data half (W6.2(i)) is LIVE — DS stamps reconciliation.all_pass=True + max_abs_delta=0.0 + series_tie + granularity_coverage into the W1 canonical artifact already. This TO is purely the standing daily-alarm Lambda (your mdpf-freshness-checker pattern transplanted to the NNA canonical artifact). Reuse maximizes — the scaffold, the alarm-test method, the deploy cycle are all what you just did for OPS1 D3. CC CTO (co-verify durable-W4-form) + CVO (bar owner) + DS (stamps the properties).
</notes>
</task_order>
