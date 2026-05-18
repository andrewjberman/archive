<task_order>
  <metadata>
    <id>MDPF_ASSETS.012</id>
    <slug>ae-opal-data-mdpf-feeder-bucket</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.5.0_AE_OpalETL</issued_to>
    <date>2026-05-18</date>
    <status>complete</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>DISPATCHED 2026-05-18 (COO) to AE 0.5.0 (the Opal shared-resources AE). GO -- P1, on the MDPF Phase-2 critical path: all four feeders (WS-B/C/D.2/E) land their convergent artifacts in this bucket. WS-B (MDPF_ASSETS.007) is built + verified but its AC4 S3-landing is blocked solely on this bucket not existing.</dispatch_unblock_condition>
    <project_code>MDPF_ASSETS</project_code>
    <priority>P1 -- MDPF Phase 2 critical path. WS-B is built and waiting; WS-C/WS-D.2/WS-E all land here; the WS-A aggregation script reads from here.</priority>
    <sla>0.5d wall -- a single new empty S3 bucket + Terraform, mirroring the opal-data-etfs precedent.</sla>
  </metadata>

  <references>
    <contract>docs/architecture/MDPF_ASSETS_WSA_CONTRACT.md (RATIFIED) §8 + CTO ruling vi: the convergent FEEDER intermediate parquet must NOT co-locate in the CloudFront-served opal-data-portal-v2 -- it is a pipeline intermediate, not a served artifact. Land it in a non-portal data bucket; CTO recommended a new opal-data-mdpf per the opal-data-etfs precedent. The platinum aggregate artifact stays in opal-data-portal-v2/platinum/mdpf/ (served) -- this TO does NOT touch that.</contract>
    <precedent>ETFS_NETAST.001 -- the opal-data-etfs bucket Terraform adoption into shared-infra. opal-data-etfs was created ad-hoc then import-adopted (it pre-existed with data). opal-data-mdpf is NET-NEW and EMPTY -- create it directly in Terraform (no import needed). Same shared-infra home, same region (us-east-1).</precedent>
    <deployment>infra/aws/TERRAFORM_PIPELINE_STRATEGY.md; docs/deployment/LAMBDA_DEPLOYMENT_PROTOCOL.md (the commit-before-apply + tag-after-deploy discipline). shared-infra state key shared-infra/tfstate; bucket resources live in infra/aws/terraform/shared-infra/s3.tf.</deployment>
  </references>

  <context>
    MDPF Phase 2's four feeders (WS-B 49F/SmartX, WS-C Inflection/Eclipse, WS-D.2 ETF, WS-E 49F non-model) each emit convergent-schema parquet that the MDPF aggregation gold script reads. Per the ratified contract §8 + CTO ruling vi, that feeder parquet must land in a non-portal data bucket -- a new opal-data-mdpf. WS-B is already built + verified (model_aua(49financial) = $1,360,250,355, -0.001% vs reference) and is writing/verifying its artifacts LOCALLY because the bucket does not exist; its AC4 (S3 landing) is blocked solely on this. WS-E builds next on the same lane and lands here too. This TO creates the bucket so the feeders can land and the aggregation can read.
  </context>

  <scope>
    <step>Create the opal-data-mdpf S3 bucket via Terraform in the shared-infra module (infra/aws/terraform/shared-infra/s3.tf) -- net-new and empty, so a direct Terraform-managed create, no ad-hoc-then-import. us-east-1. Versioning + encryption + public-access-block per the shared-infra bucket convention (mirror opal-data-etfs). This is a NON-portal data bucket -- do NOT put it behind CloudFront, do NOT add it to the portal-serving path.</step>
    <step>Confirm the prefix convention the feeders write to (contract §8): mdpf/feeds/{model_aua_positions, model_composition, non_model_aua, etf_net_assets}/{firm_id}/{date}.parquet. No need to pre-create prefixes (S3 prefixes are implicit) -- just confirm the bucket name + that the convention is recorded so the feeder lanes (DS) write a consistent path.</step>
    <step>IAM: ensure the principal(s) that run the MDPF feeders + the aggregation gold script can read/write opal-data-mdpf. At Phase 2 the feeders run ad-hoc (DS-run); confirm the working DS/AE credentials cover s3:GetObject/PutObject/ListBucket on opal-data-mdpf. Run comp-iam gaps if any Lambda/EC2 principal is wired to it (none expected at this stage -- state so).</step>
    <step>Deployment sequence per the protocol: write Terraform -> git commit -> terraform plan -> terraform apply -> verify 0-diff plan -> git tag (shared-infra-v{X.Y.Z} -- run `git tag -l "shared-infra-v*" | sort -V | tail -5` first to find the real next version) -> push --follow-tags. Notify COO + the DS feeder lanes (DS~A for WS-B/WS-E, DS~B for WS-C/WS-D.2) on bucket-ready so WS-B can run its --upload and close AC4.</step>
  </scope>

  <compiler_tools_mandate>
    <phase id="1" when="before write">
      <step>
        <run>comp-iam gaps -- if any Lambda/EC2 is to be wired to opal-data-mdpf.</run>
        <expect>At Phase 2 the feeders are DS-run ad-hoc, not Lambda/EC2 -- expect N/A; state so in one line.</expect>
        <if_mismatch>Fix iam.tf before apply.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>terraform plan -- verify 0-diff after apply.</run>
        <expect>The opal-data-mdpf bucket created, 0-diff plan after apply.</expect>
        <if_mismatch>Reconcile state before tagging.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <data_reprocess_scope>
    <no_reprocess_needed>An infra TO -- a new empty S3 bucket. No data, no pipeline, no reprocessing.</no_reprocess_needed>
  </data_reprocess_scope>

  <cross_domain_coordination>
    The bucket lands in the shared-infra Terraform module -- single-owner the s3.tf edit; coordinate if shared-infra has a concurrent change in flight. The bucket is consumed by the MDPF feeder lanes (DS) + the MDPF aggregation script -- AE creates the bucket; the feeders write it. No portal/CloudFront surface (contract ruling vi -- explicitly a non-portal data bucket). Notify COO + DS~A + DS~B on bucket-ready.
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">The opal-data-mdpf S3 bucket exists, Terraform-managed in infra/aws/terraform/shared-infra/s3.tf -- versioning + encryption + public-access-block per the shared-infra convention; us-east-1; NOT CloudFront-fronted.</ac>
    <ac id="AC2">Deployed per protocol: commit -> plan -> apply -> 0-diff verify -> shared-infra git tag -> push --follow-tags.</ac>
    <ac id="AC3">The feeder prefix convention (mdpf/feeds/{artifact}/{firm_id}/{date}.parquet) is recorded; the DS feeder lanes can read/write the bucket. COO + DS~A + DS~B notified on bucket-ready.</ac>
    <ac id="AC4">No emoji; session log with the Compiler Tools section. RAVC2 to COO.</ac>
  </acceptance_criteria>

  <deliverables>
    - The opal-data-mdpf S3 bucket, Terraform-managed in shared-infra, deployed + tagged.
    - Bucket-ready notification to COO + DS~A + DS~B.
    - Session log with the Compiler Tools section. RAVC2 to COO.
  </deliverables>
</task_order>
