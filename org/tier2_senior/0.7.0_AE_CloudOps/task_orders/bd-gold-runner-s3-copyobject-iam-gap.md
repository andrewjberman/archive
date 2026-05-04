<task_order>
  <metadata>
    <id>BD_IAM_S3COPYOBJECT</id>
    <project>none (ad-hoc operational fix)</project>
    <title>bd-exporter-ec2-role — add s3:CopyObject permission</title>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-04</issued_date>
    <status>pending</status>
    <priority>P1 — coupled to DS~B ADVI_49FRECN.003 in flight; D_04 gold run will fail if not shipped before next BD gold trigger</priority>
    <estimated_effort>~30min (iam.tf edit + plan + apply + tag bump + source map)</estimated_effort>
  </metadata>

  <context>
    `comp-iam gaps` surfaced this during AE 0.7's JWTRES.002 validation run (your own RAVC4 2026-05-04
    flagged it as unrelated side-finding). Specifics:

    - Service: bd-gold-runner (EC2), role: bd-exporter-ec2-role
    - Missing IAM action: s3:CopyObject
    - Call site: data/black_diamond/scripts/gold/D_04.client_portal_summary.py:2405
    - Fix recommended by tool: add 's3:CopyObject' to bd-exporter-ec2-role policy in iam.tf

    Coupling: DS~B is currently shipping `ADVI_49FRECN.003` Track 2 fixes that touch D_04 (AQR
    filter removal + c1_recovered_accounts.json sidecar emit). Sidecar first-cut already shipped
    `e66898a64`. The s3.copy_object call may pre-date their work or may have been introduced by
    their sidecar logic — either way, the next BD gold run on D_04 fails without this IAM grant.

    Andrew GO 2026-05-04: "let's just get the IAM gap sorted out now."
  </context>

  <objective>
    Add s3:CopyObject to bd-exporter-ec2-role IAM policy. Ship via standard Lambda/EC2 deployment
    protocol (Terraform → plan → apply → 0-diff verify → tag). Update source map if applicable.
    Verify post-deploy via comp-iam gaps re-run (zero gaps remaining for bd-gold-runner).
  </objective>

  <acceptance_criteria>
    <ac id="1">
      <title>IAM policy update</title>
      <detail>
        Locate bd-exporter-ec2-role policy in `infra/aws/terraform/bd-pipeline/iam.tf` (or wherever
        it lives — verify with `comp-iam service bd-gold-runner`). Add `s3:CopyObject` to the
        existing actions list for the relevant statement. Scope the resource to the same prefix
        the role already has read/write on (likely `arn:aws:s3:::opal-data-bd/gold/*` and/or
        `arn:aws:s3:::opal-data-bd/platinum/*` — verify against existing statements).
      </detail>
    </ac>
    <ac id="2">
      <title>Terraform plan + apply</title>
      <detail>
        `terraform plan` should show only the IAM policy diff (no other drift). `terraform apply`
        produces 0-diff on subsequent plan. Per CLAUDE.md Critical Deployment Rules.
      </detail>
    </ac>
    <ac id="3">
      <title>Tag + push</title>
      <detail>
        Bump bd-pipeline tag (current latest per memory: `bd-v2.23.0`). Use patch increment:
        `bd-v2.23.1` UNLESS `git tag -l "bd-v*" | sort -V | tail -5` shows a higher patch already
        landed (per "Pipeline Tag Versioning" memory rule — verify before tagging).
        `git push --follow-tags` to remote.
      </detail>
    </ac>
    <ac id="4">
      <title>Post-deploy verification</title>
      <detail>
        Re-run `comp-iam gaps` — output must show zero bd-gold-runner gaps. Capture command + output
        in session log Compiler Tools section.
      </detail>
    </ac>
    <ac id="5">
      <title>Session log + RAVC4</title>
      <detail>
        Standard. Session log under `org/tier2_senior/0.7.0_AE_CloudOps/logs/2026-05-04/`. RAVC4 to
        COO with: iam.tf commit hash + tag name + 0-diff plan output + comp-iam gaps post-fix output.
      </detail>
    </ac>
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1" when="before_writing_code">
      <step>
        <run>comp-iam service bd-gold-runner</run>
        <expect>Lists bd-exporter-ec2-role + current allowed actions; identifies the iam.tf path + statement to amend</expect>
        <if_mismatch>If service not in registry, fall back to grep of infra/aws/terraform/bd-pipeline/iam.tf for "bd-exporter-ec2-role"</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before_commit">
      <step>
        <run>terraform -chdir=infra/aws/terraform/bd-pipeline plan</run>
        <expect>Single IAM policy diff showing s3:CopyObject addition; no other drift</expect>
        <if_mismatch>Investigate drift before applying — do not apply with non-policy diffs</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after_commit">
      <step>
        <run>terraform -chdir=infra/aws/terraform/bd-pipeline plan</run>
        <expect>0-diff (no changes) — confirms apply landed clean</expect>
        <if_mismatch>Investigate apply failure or state divergence</if_mismatch>
      </step>
      <step>
        <run>comp-iam gaps</run>
        <expect>Zero bd-gold-runner gaps; "Total: 0 gap(s)" or unrelated gaps remaining</expect>
        <if_mismatch>Fix didn't propagate or scope-mismatch — debug</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <resource>
      <path>infra/aws/terraform/bd-pipeline/iam.tf</path>
      <owners>0.7.0_AE_CloudOps (CLOUD_OPS_OR_ETL lane); no concurrent active TO touches BD IAM</owners>
      <coordination>None — sole-owner edit window. DS~B ADVI_49FRECN.003 work touches D_04 source code, NOT iam.tf — no merge conflict.</coordination>
    </resource>
    <resource>
      <path>data/black_diamond/scripts/gold/D_04.client_portal_summary.py</path>
      <owners>0.4.0_DS_ClientPlatform~B (current TO); read-only reference for AE 0.7 (line 2405 the s3.copy_object call site)</owners>
      <coordination>Do not edit D_04. Read-only reference to confirm the call signature + scope target.</coordination>
    </resource>
  </cross_domain_coordination>

  <data_reprocess_scope>
    <no_reprocess_needed>
      Reasoning: IAM-only change. No data semantics change. Historical data unaffected. Next BD gold
      run after this ships will be the first run with the grant available — no re-ingestion needed.
    </no_reprocess_needed>
  </data_reprocess_scope>

  <deliverables>
    <item>iam.tf commit (your AE 0.7 author; CLOUD_OPS_OR_ETL lane)</item>
    <item>Annotated git tag bd-v2.23.1 (or next available patch per `git tag -l` check)</item>
    <item>git push --follow-tags</item>
    <item>Session log with Compiler Tools section + 0-diff plan output + post-fix comp-iam gaps output</item>
    <item>RAVC4 MCP to COO with commit hash + tag + plan-output + gaps-output</item>
  </deliverables>
</task_order>
