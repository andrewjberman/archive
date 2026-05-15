<task_order>
  <metadata>
    <id>ETFS_NETAST.001</id>
    <slug>ae-opal-data-etfs-bucket-tf-adoption</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-05-15</date>
    <status>complete</status>
    <dispatch_held>false</dispatch_held>
    <project_code>ETFS_NETAST</project_code>
    <priority>P2 -- brings an unmanaged `aws s3 mb` bucket (opal-data-etfs, 296 objects) under Terraform (CLAUDE.md Rule 9). Andrew-directed. Not blocking; sequence around your in-flight ADVI_INFETL.RUNDATE-DISPATCH (deliverable (ii) stays the fast-priority).</priority>
    <sla>~1-1.5h wall -- import-to-0-diff; the brief is turnkey.</sla>
  </metadata>

  <references>
    <brief>docs/briefs/ae-brief-opal-data-etfs-bucket.md (commit da4931c85, pushed CLOUD) -- TURNKEY: the exact s3.tf resource block, the 3 `terraform import` commands, the full commit-plan-apply-tag-push sequence, the IAM note. This brief is the authoritative implementation guide -- do not re-derive.</brief>
    <probe_code>etf_netassets_watch/ (commit da4931c85) -- the ETF net-assets daily probe (etf_probe.py / backfill.py / run_daily.cmd). Context only; this TO does NOT touch the probe code.</probe_code>
    <directive>Andrew direct 2026-05-15 -- the ETF net-assets probe (TrueShares DIVZ/IDVZ) is needed and the opal-data-etfs bucket is to be brought under shared-infra Terraform management. Relayed COO via DS~C.</directive>
  </references>

  <context>
    An ETF net-assets daily probe was built this session at Andrew's direction; it writes silver-tier daily parquet to a new S3 bucket `opal-data-etfs` (us-east-1), created ad-hoc via `aws s3 mb` and currently holding 296 objects. The bucket is unmanaged -- not in Terraform -- the CLAUDE.md Rule 9 drift class. Andrew directed it be adopted into shared-infra Terraform. The bucket already exists and holds data: this is an IMPORT-to-0-diff, NOT a fresh apply.
  </context>

  <objective>
    `opal-data-etfs` is a Terraform-managed resource in `infra/aws/terraform/shared-infra/s3.tf`, imported to a clean 0-diff plan, with no disruption to the 296 existing objects.
  </objective>

  <scope>
    <item>Add the `opal-data-etfs` S3 resource block to infra/aws/terraform/shared-infra/s3.tf -- use the exact block in the brief. Per the brief / the s3.tf header note: pipeline data buckets normally live in pipeline modules, but opal-data-etfs has no pipeline module, so shared-infra is the pragmatic home per Andrew's directive -- the brief flags this; proceed with shared-infra.</item>
    <item>Run the `terraform import` commands from the brief (bucket + any sub-resources the brief specifies) -- `export MSYS_NO_PATHCONV=1` first per the CLAUDE.md Git note.</item>
    <item>`terraform plan` MUST reach 0-diff. The bucket and its 296 objects pre-exist; a non-0-diff plan means the resource block does not match reality -- reconcile the block, NEVER apply a destructive diff.</item>
    <item>Commit -> terraform apply -> verify 0-diff -> git tag shared-infra-v1.11.x -> push --follow-tags. Full sequence is in the brief. The brief says v1.11.0 -- VERIFY the correct next tag first (`git tag -l "shared-infra-v*" | sort -V | tail -5`) per the MEMORY pipeline-tag rule; do not assume.</item>
    <item>IAM: the brief notes NONE needed (the probe runs on local creds, not a Lambda/EC2 role). Confirm -- if that holds, no iam.tf change.</item>
    <item>Bucket, not a Lambda -- no lambda-source-map.json entry; EC2_MANIFEST.json N/A.</item>
  </scope>

  <acceptance_criteria>
    <ac id="AC1">opal-data-etfs is a resource in shared-infra/s3.tf; `terraform plan` is 0-diff (clean import -- no destroy/recreate of the bucket or its objects).</ac>
    <ac id="AC2">Committed -> terraform apply -> 0-diff verified -> git tag shared-infra-v1.11.x (correct next tag confirmed against existing tags) -> pushed --follow-tags.</ac>
    <ac id="AC3">The 296 pre-existing objects in opal-data-etfs are intact post-adoption (S3 object count unchanged).</ac>
    <ac id="AC4">No IAM change unless the scope confirm finds one genuinely needed; if iam.tf changes, `comp-iam gaps` before commit.</ac>
    <ac id="AC5">No emoji in any Terraform, commit, or log output.</ac>
  </acceptance_criteria>

  <compiler_tools_mandate>If iam.tf is touched (scope says it should NOT be): `comp-iam gaps` before commit. Otherwise the standard Terraform deploy gate -- plan 0-diff before apply, `record-terraform-deploy.sh` -- is the control. No comp-pipescript (no pipeline script in scope).</compiler_tools_mandate>

  <cross_domain_coordination>
    Sequence around your in-flight ADVI_INFETL.RUNDATE-DISPATCH -- that TO's deliverable (ii) stays the fast-priority; this bucket adoption is P2 and follows (ii). No file contention: RUNDATE-DISPATCH touches the catalog/dispatch, this touches infra/aws/terraform/shared-infra/s3.tf.
    .owned-paths.yaml: DS~C flagged that etf_netassets_watch/** has no path rule (DS~C's probe commit da4931c85 used an audited author-override). That is a CTO-owned governance-file fix -- COO has routed it to CTO separately; NOT in this TO's scope. This TO touches infra/aws/terraform/shared-infra/ (AE-owned path) -- no override needed.
  </cross_domain_coordination>

  <deliverables>
    <item>opal-data-etfs imported into shared-infra/s3.tf, 0-diff, tagged + pushed --follow-tags.</item>
    <item>Session log + RAVC2 to COO + CC DS~C (probe owner) + CC CTO.</item>
  </deliverables>

  <ravc>AE 0.7.0 RAVC2 to COO + CC DS~C + CC CTO on AC1-5 PASS.</ravc>

  <notes>
    The brief (da4931c85) is turnkey -- the exact s3.tf block + import commands + sequence are in it; do not re-derive. The only judgment points: confirm the correct next shared-infra tag (do not assume v1.11.0 -- verify against existing tags), and confirm the no-IAM-needed note holds. If `terraform plan` does not reach 0-diff after the import, STOP -- a non-0-diff means the resource block does not match the live bucket; reconcile the block, never apply a diff that would destroy/recreate the bucket or its 296 objects.
  </notes>
</task_order>
