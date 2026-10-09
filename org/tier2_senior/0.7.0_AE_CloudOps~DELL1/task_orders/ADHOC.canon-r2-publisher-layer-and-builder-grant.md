# pipeline-override: MDPF_CANON round 2 (decomposition v2, cells CN-b-3 and CN-b-4, drained @9c36cacc05 and @63b47dc1d4); the round-2 issuance @5f2c367568 is closed to new order files (ONE ISSUER PER ROUND), so the two cells' applies and the publisher's one real run ride one CloudOps ADHOC order, on the MDPF_HEALGAP R2-1 precedent.
<task_order id="ADHOC.canon-r2-publisher-layer-and-builder-grant">
<to_id>ADHOC.canon-r2-publisher-layer-and-builder-grant</to_id>
<issued_by>2.0.0_SA_COO~D1</issued_by>
<issued_to>0.7.0_AE_CloudOps~DELL1</issued_to>
<date>2026-10-09</date>
<status>pending</status>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<priority>P2 (round 2 of MDPF_CANON; nothing reads the publisher's new capability yet)</priority>

<title>MDPF_CANON CN-b-3 + CN-b-4: publisher to python3.11 + the pyarrow layer (one DELTA=0 run), and the composite grant re-pointed to builder output (no-op plan)</title>

<context>
**CN-b-3** (`infra/aws/terraform/opal-assets/mdpf_portal_publisher.tf`, 25c1b3b6a4):
- `module "mdpf_publisher"` runtime python3.12 -> python3.11;
- `layers = [data.aws_lambda_layer_version.mdpf_publisher_pyarrow.arn]` (`pandas-pyarrow-requests-layer`, the estate's py3.11 layer);
- GOLD_BUCKET, GOLD_ROOT, SERVE_BUCKET and SERVE_ROOT unchanged; the publisher's code is unchanged.
It gives the publisher the ability to read parquet LATER (PRD M5, DEC-4: the publisher switches last). It moves no served key.

**CN-b-4** (`infra/aws/terraform/mdpf-pipeline/iam.tf`, 2fb91b7b78):
- the 5 composite ARNs in `aws_iam_role_policy.mdpf_gold_writers` move from `${local.mdpf_bucket}` to
  `${module.mdpf_scope_buckets.scope_bucket["mdpf"]}`;
- both resolve to `opal-data-mdpf`, so the rendered policy is identical (CTO ruling W1-S1, round-1 analysis @409182ae5a).

The publisher has no dry-run mode, so its real run is one ad-hoc invocation compared leaf by leaf on data-bearing values
(`_provenance.written_at` and the run manifests excluded). A verified DELTA=0 needs no hold (CLAUDE.md section 5). Any delta rolls back in
the same session. The scheduled 13:50Z publisher run stays the production path.
</context>

<scope>
1. Edit no source file. Open a deploy ledger.
2. **CN-b-4 first.**
   - Run a targeted plan in `infra/aws/terraform/mdpf-pipeline` on `aws_iam_role_policy.mdpf_gold_writers` (and the no-resource
     `module.mdpf_scope_buckets`).
   - EXPECT no changes: the rendered policy is identical. If the plan shows any change to the rendered policy JSON, STOP and report it;
     do not apply.
3. **CN-b-3.**
   - BEFORE: read and keep the data-bearing values of every served leaf under `opal-data-portal-v2/platinum/mdpf/{scope}/*.json`, for the
     4 scopes and their leaves.
   - Run a targeted plan on `module.mdpf_publisher` and the new data source in `infra/aws/terraform/opal-assets`: 0 add / 1 change /
     0 destroy, the change being runtime + layers only. Then `safe-apply -target`.
   - Read `get-function-configuration`: Runtime python3.11; Layers carries the pandas-pyarrow-requests-layer ARN; Environment's four
     read/serve variables unchanged.
4. **The one real run.** Invoke `opal-assets-mdpf-portal-publisher` once ad hoc (the same event shape its scheduler sends). Then AFTER:
   re-read every served leaf and compare data-bearing values with BEFORE.
   - Expect DELTA=0 on every leaf; only `_provenance.written_at` and the `_manifests/` objects may differ.
   - **On ANY data-bearing delta, or a function error: roll back in the same session** (runtime python3.12, layers removed, apply), re-invoke
     once, confirm the leaves match BEFORE, and report.
5. Close the ledger. Report to `2.0.0_SA_COO~D1` with each criterion's output, and the change after the fact to `0.0.0_AB_MSTR~DELL1`.
</scope>

<paths>
org/critical_paths/change_management/
org/critical_paths/.open_deploys/
org/tier2_senior/0.7.0_AE_CloudOps~DELL1/
org/missions/D8/MDPF/MDPF_CANON/surprise-channel/investigations/INVESTIGATION_v1.md
</paths>

<proof_of_spec>
<expected_criteria>C1,C2,C3,C4,C5,C6</expected_criteria>
<criterion id="C1" judgment="false">
  <invocation>python "org/missions/D8/MDPF/MDPF_CANON/deliverables/2.0.0_SA_COO~D1/round2/checks/r2_checks.py" builder ; python "org/missions/D8/MDPF/MDPF_CANON/deliverables/2.0.0_SA_COO~D1/round2/checks/r2_checks.py" publisher</invocation>
  <expect>ROUND 2 BUILDER: 3 of 3 arms and ROUND 2 PUBLISHER: 3 of 3 arms (the source applied is the source graded)</expect>
</criterion>
<criterion id="C2" judgment="false">
  <invocation>the targeted plan on aws_iam_role_policy.mdpf_gold_writers in infra/aws/terraform/mdpf-pipeline</invocation>
  <expect>No changes (the rendered policy is identical), or a change whose rendered JSON is byte-identical -- never applied otherwise</expect>
</criterion>
<criterion id="C3" judgment="false">
  <invocation>the targeted plan + safe-apply on module.mdpf_publisher, then .tools/aws lambda get-function-configuration --function-name opal-assets-mdpf-portal-publisher</invocation>
  <expect>plan 0/1/0 (runtime + layers only); live Runtime python3.11, Layers names pandas-pyarrow-requests-layer, GOLD_BUCKET/GOLD_ROOT/SERVE_BUCKET/SERVE_ROOT unchanged</expect>
</criterion>
<criterion id="C4" judgment="false">
  <invocation>one ad-hoc .tools/aws lambda invoke of opal-assets-mdpf-portal-publisher</invocation>
  <expect>StatusCode 200, no FunctionError, a response naming the leaves it served</expect>
</criterion>
<criterion id="C5" judgment="false">
  <invocation>the BEFORE/AFTER comparison of every served leaf's data-bearing values under opal-data-portal-v2/platinum/mdpf/{scope}/ (denominator: leaves compared, printed)</invocation>
  <expect>DELTA=0 on every leaf (only _provenance.written_at and _manifests/ differ), or the same-session rollback recorded and its re-read matching BEFORE</expect>
</criterion>
<criterion id="C6" judgment="false">
  <invocation>python .tools/deploy_ledger.py check</invocation>
  <expect>this order's ledger CLOSED, every leg proven</expect>
</criterion>
</proof_of_spec>
</task_order>
