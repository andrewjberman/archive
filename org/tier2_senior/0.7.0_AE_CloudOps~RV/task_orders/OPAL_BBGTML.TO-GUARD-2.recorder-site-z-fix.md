<task_order>
  <metadata>
    <id>OPAL_BBGTML.TO-GUARD-2.recorder-site-z-fix</id>
    <issued_by>2.0.0_SA_COO~Z</issued_by>
    <issued_to>0.7.0_AE_CloudOps~RV</issued_to>
    <date>2026-10-06</date>
    <status>complete -- issuer-ruled 2026-10-06 ~18:2xZ: AC1 PASS (recorder exit 0 @4ddd25eee8), AC2 PASS (last_deployed_commit 513b25f522), AC3 PASS under AMENDMENT 1 (the third file is the recorder's own canonical CHANGELOG append); fix @8be38c9dec; rows Z-S8/Z-S9 @07d1cadca5; Z-S7 graduation is the CVO's</status>
    <project_code>OPAL_BBGTML</project_code>
  </metadata>
<risk>LOCAL</risk>
# pipeline-override: outside the canonical pipeline -- the disarm of surprise row OPAL_BBGTML-Z-S7 (@39b6a62b56), raised by TO-GUARD-1's post-deploy hygiene on a closed project; owner seated per 1.0.0_SA_CTO~Z msg 30157; not a round

  <objective>
    Make infra/aws/lambda/ci/record-terraform-deploy.sh run on site Z, then close deployment Rule 4's loop for the guard
    deploy, so lambda-source-map.json reads the deployed commit 513b25f522 for yang-model-portfolio-benchmarks.
  </objective>

  <context>
    Row OPAL_BBGTML-Z-S7 in org/surprise_channel/OPAL_BBGTML/INVESTIGATION_v1.md @39b6a62b56 carries the defect and the evidence.
    The fix, per 1.0.0_SA_CTO~Z msg 30157:
    - detect node first, as build-and-upload.sh already does;
    - quote the four $JSON_TOOL sites (lines 250, 348, 448, 463);
    - compare the basename at lines 249 and 446.
    The yang-pipeline-v1.5.9 tag may be cut LOCALLY. Pushing it is 0.0.0_AB_MSTR~Z's act, on Andrew's word.
  </context>

  <paths>
    C:/Users/Opal Bloomberg/Desktop/ajb_workspace/infra/aws/lambda/ci/record-terraform-deploy.sh
    C:/Users/Opal Bloomberg/Desktop/ajb_workspace/infra/aws/lambda/ci/lambda-source-map.json
    C:/Users/Opal Bloomberg/Desktop/ajb_workspace/org/surprise_channel/OPAL_BBGTML/INVESTIGATION_v1.md (the Z-S7 disposition only)
  </paths>

  <acceptance_criteria>
    <criterion id="AC1">The recorder runs on site Z. Run: bash infra/aws/lambda/ci/record-terraform-deploy.sh yang-pipeline
      --function yang-model-portfolio-benchmarks --version yang-pipeline-v1.5.9 --author "0.7.0_AE_CloudOps~RV &lt;0.7.0_AE_CloudOps~RV@opal.agent&gt;".
      Expect: exit 0, with no "Is a directory" line.</criterion>
    <criterion id="AC2">The source map reads the deployed commit. Run: python -c "import json;print(json.load(open('infra/aws/lambda/ci/lambda-source-map.json'))['functions']['yang-model-portfolio-benchmarks']['last_deployed_commit'])". Expect: last_deployed_commit starts 513b25f522.</criterion>
    <criterion id="AC3">The diff is bounded. Run: git diff --stat over the commit. Expect: only the two named files under infra/aws/lambda/ci/
      change, and the source-map diff touches only functions.yang-model-portfolio-benchmarks plus the recorder's own top-level _updated and _last_deploy_recorded keys.</criterion>
  </acceptance_criteria>

<proof_of_spec>
  <criterion id="AC1" cell_refs="GUARD-2"><invocation>bash infra/aws/lambda/ci/record-terraform-deploy.sh yang-pipeline --function yang-model-portfolio-benchmarks --version yang-pipeline-v1.5.9</invocation><expect>exit 0, no "Is a directory"</expect></criterion>
  <criterion id="AC2" cell_refs="GUARD-2"><invocation>python -c &quot;import json;print(json.load(open('infra/aws/lambda/ci/lambda-source-map.json'))['functions']['yang-model-portfolio-benchmarks']['last_deployed_commit'])&quot;</invocation><expect>starts 513b25f522</expect></criterion>
  <criterion id="AC3" cell_refs="GUARD-2"><invocation>git show --stat HEAD -- infra/aws/lambda/ci/</invocation><expect>2 files; source-map hunks only in the one entry plus _updated/_last_deploy_recorded</expect></criterion>
</proof_of_spec>

  <gates>
    Commit with .tools/safe-commit.sh under your own author line; every .py or .sh edit passes the commit gate. Mark Z-S7 RESOLVED in
    its own row, citing the fix commit.
  </gates>

  <amendment id="1" by="2.0.0_SA_COO~Z" at="2026-10-06T18:2xZ">
    AC3 as written was path-scoped to infra/aws/lambda/ci/ and so could not see infra/aws/terraform/yang-pipeline/CHANGELOG.json
    (+48, one entry). That file's own header says it is "Appended by record-terraform-deploy.sh after every terraform apply": the
    entry is the recorder's canonical output, not a deviation of the fix. The issuer adds it to the bound and grades AC3 PASS: the
    commit @4ddd25eee8 moves exactly the source-map entry and that one CHANGELOG entry. No gate limb graded this amendment; the
    order carries a pipeline-override.
  </amendment>

  <report>
    Report once to 2.0.0_SA_COO~Z: each criterion's verdict with the output above it, commit hashes and push state, and the Z-S7
    disposition. Leave the status flip to the issuer.
  </report>
</task_order>
