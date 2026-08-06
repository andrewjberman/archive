<task_order>
  <metadata>
    <id>2.0.0_SA_COO~Z-2026-08-06-canplat-p2-1</id>
    <issued_by>2.0.0_SA_COO~Z</issued_by>
    <issued_to>0.7.0_AE_CloudOps~Z</issued_to>
    <date>2026-08-06</date>
    <status>pending</status>
    <project_code>MDPF_CANPLAT</project_code>
    <supersedes>MDPF_CANRTE.P2-1 (body ADOPTED @a6ae64326, deltas below)</supersedes>
    <governing>PRD @24d3eb2f8 · CONTRACT @a3106d585 (A6/D7 config hashes; R13)</governing>
  </metadata>

  <standing_instruction>
    ⛔ PRD §0, VERBATIM — THE OPERATING INSTRUCTION FOR THIS ENTIRE PROGRAM:

    > **ANDREW-DIRECT, 2026-08-06, VERBATIM:**
    > *"This is exactly correct. I need you to persist this exactly as laid out here as a PRD and issue that
    > to COO for decomposition. I just terminated every fabric agent's session on this device aside from you
    > and mstr~z because I want them respawned with this being fresh context and instruction. **I do not want
    > them to go off the rails on hunting down errors, just do what is described here.**"*

    **BUILD WHAT §2 DESCRIBES. DO NOT HUNT ERRORS.**

    - **A number that surprises you is NOT a finding.** The business logic is **correct and live**. This is
      a **SHAPE** project.
    - **The only defects in scope are SHAPE divergences.** Everything else is out of scope, however
      interesting.
    - **If you find something that looks wrong: REPORT IT, DO NOT CHANGE IT.** One line to COO~Z. Then
      continue the work. Do not open an investigation. Do not widen a task order.
    - **Prior context is deliberately not being restored. Do not go looking for the previous session's
      threads.**

    > **TREATING A CORRECT NUMBER AS A FINDING IS HOW A WORKING PIPELINE GETS "FIXED."**

    SURPRISE CHANNEL: ONE LINE to 2.0.0_SA_COO~Z, subject beginning `SURPRISE:`, then continue.
  </standing_instruction>

  <objective>
    Make the committed configuration deployable (adopted objective @a6ae64326, verbatim force):
    `route_bindings.yaml` as a Terraform-managed S3 object with a content hash and an exact read grant;
    `partner_roster.json` as a BUILD-GENERATED, HASH-TIED copy with NO S3 read leg at all; plus the exact
    write grants `mdpf-gold-lambda` needs for the A4 grammar. Both config hashes are recorded in every run
    manifest (CONTRACT A6) and publish manifest (CONTRACT D7).
  </objective>

  <adoption>
    **The body of `MDPF_CANRTE.P2-1.deployable-config-and-iam.md` AS COMMITTED @a6ae64326 IS ADOPTED AS
    THIS TO's CONTENT** — context, compiler_tools_mandate (incl. the comp-iam necessary-not-sufficient +
    simulate-principal-policy one-ARN-per-call discipline), acceptance criteria, scope, requirements,
    do_not — subject to these DELTAS, which win on conflict:

    - **Δ1 · THE fee_scope 1→DECLARED MIGRATION IS NOT AUTHORIZED IN THIS BUILD.** PRD §6: P1-1 collapses
      the two hardcoded maps to one; the migration to declared data is this TO's *axis to consider on a
      future authorization*, and **nobody populates `data/firm_registry.json` on this program's
      authority.** If the adopted body reads as authorizing that migration anywhere, this delta wins.
    - **Δ2 · WRITE GRANTS TARGET THE A4 GRAMMAR** (`portal/gold/mdpf/{scope}/{artifact-type}/…` on
      opal-data-assets), plus A7's preserved `gold/mdpf_revamp/_aggregate_aua/` until the emitter
      re-point. Any NEW key/ARN is verified on the live primitive per Rule 22a (one `--resource-arns` per
      call; positive control in a SEPARATE invocation).
    - **Δ3 · PROGRAM CODE.** References to MDPF_CANRTE waves resolve to MDPF_CANPLAT; the hard ordering
      "P2-1 lands before P3-1 deploys" carries into this generation unchanged.
  </adoption>

  <acceptance_criteria>
    Adopted criteria @a6ae64326 stand (incl. "8. NO NEW ALARM, SNS TOPIC, OR MONITOR IS CREATED —
    hash-in-manifest is a RECORD, not a detector"). Rubric rows this TO must make passable:
    - **A6** (config hashes present in the run manifest) and **D7** (publish manifest) — the hash fields
      exist and are populated from this TO's objects.
    - **R13** "Terraform full un-targeted plans zero-diff; tags after — oracle: plan output." Apply via
      `.tools/safe-apply.sh` only; commit before apply; tag after 0-diff; source map updated
      (`infra/aws/lambda/ci/lambda-source-map.json`).
  </acceptance_criteria>

  <cross_domain_coordination>
    <shared_resource>`config/mdpf/` prefix + build-generated roster copies</shared_resource>
    <also_in_to>MDPF_CANPLAT.P3-1 (publisher deploys only AFTER these objects exist) · MDPF_CANPLAT.P1-1 (gold reads the same committed authority, symmetric build copy)</also_in_to>
    <last_write_owner>0.7.0_AE_CloudOps~Z</last_write_owner>
    <required_action>⛔ P2-1 LANDS FIRST — HARD (adopted). MCP DS~Z on the roster-copy build mechanics so
    gold and publisher hash the SAME committed commit.</required_action>
  </cross_domain_coordination>

  <do_not>
    <rule>Everything in the adopted &lt;do_not&gt; @a6ae64326 — verbatim force (incl. no alarms/SNS/SES/
    monitors; no roster S3 read leg).</rule>
    <rule>DO NOT populate data/firm_registry.json; DO NOT migrate fee_scope to declared data (PRD §6).</rule>
    <rule>NO error-hunting (§0). SURPRISE: line to COO~Z, then continue.</rule>
    <rule>Commit to your lane on SITEZ; push is MSTR~Z's (:55–:00); never rebase.</rule>
  </do_not>

  <deliverables>
    <deliverable type="commit">Config objects TF + IAM grants + source-map update, committed to your lane</deliverable>
    <deliverable type="document">simulate-principal-policy evidence per new ARN (one ARN per call, isolated positive controls)</deliverable>
    <deliverable type="document">Session log with a Compiler Tools section</deliverable>
  </deliverables>
</task_order>
