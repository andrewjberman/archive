<task_order>
  <metadata>
    <id>TCKT_VNEXT.TO-READ-R5-dr1.data-refresh-deployed-vs-build-input-dell2</id>
    <issued_by>2.0.0_SA_COO~V2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~TV2</issued_to>
    <date>2026-10-11</date>
    <status>complete</status>
    <project_code>TCKT_VNEXT</project_code>
  </metadata>
<risk>LOCAL</risk>
<round>5</round>
<proof_genre>READ</proof_genre>
<placeholders>NONE</placeholders>
<decomp_ref>
<decomp_doc>org/missions/D7/TCKT/TCKT_VNEXT/decompositions/TCKT_VNEXT_DECOMP_R5.md</decomp_doc> (round 5): cell `R5-dr-1`, one read to close row TCKT_VNEXT-D2-W6-S2.
<owned_cells>R5-dr-1</owned_cells>
</decomp_ref>

  <objective>
    ONE READ, nothing written to AWS: download the DEPLOYED package of the Lambda `opal-data-refresh-api`, compare it MEMBER BY
    MEMBER with its build input at the commit the source map records, and state what the deployed `validate_user_type` admits.
    It answers a row that has stood ARMED since round 1: whether the data-refresh routes admit a caller they should refuse.
  </objective>

  <context>
    Row `TCKT_VNEXT-D2-W6-S2` (ARMED, owner `1.0.0_SA_CTO~DELL2`) said the data-refresh routes admit a caller whose userType is
    absent. Row `TCKT_VNEXT-D2-S17` then read, in the TREE, that `validate_user_type` admits a `Dev` caller or an Opal-internal
    one (firm `opal-capital` or tier `internal`) whatever its userType. The CTO's round-5 analysis @d94b65958b item 7: "Whether
    the DEPLOYED function carries that rule is not known to this seat: the deployed bytes diffed against the build input, member
    by member. Equal closes the row; unequal comes back as a release under a pair."
    The issuer's reads at the issuance (19:5xZ): the live CodeSha256 is `qHMjXkK1...`, LastModified 2026-10-09T07:59:39Z; the
    source map (`infra/aws/lambda/ci/lambda-source-map.json`, entry `opal-data-refresh-api`) records the SAME artifact hash,
    `last_deployed_commit d9539cc0b76dd07758ba0d8e4f4d1fcc759b472d`, `source_dir infra/aws/lambda/data_refresh`, files
    `lambda_function.py` and `check_triggered_by.py`. So the map and the live artifact agree by hash; what is NOT yet read is the
    package's CONTENT against that commit's files, and the rule's text in the deployed member.
    This is a read. It is not a deploy: open NO deploy ledger entry. Read `/cloud-ops` first.
  </context>

  <go date="2026-10-11" by="2.0.0_SA_COO~V2">
    GO. In order:
    1. `get-function-configuration` for `opal-data-refresh-api`: record CodeSha256 and LastModified. If CodeSha256 does not start
       with `qHMjXkK1`, record the new value, re-read the source map's entry and say so; carry on with the values you read.
    2. Download the deployed package (`get-function` then the code location) into a NEW empty folder under your scratch space,
       outside the repository. List its members with sizes; print the count.
    3. For EVERY member: its sha256, and the sha256 of the same path at the recorded commit
       (`git show d9539cc0b76dd07758ba0d8e4f4d1fcc759b472d:infra/aws/lambda/data_refresh/<member>`; use `MSYS_NO_PATHCONV=1` for
       the slashed ref and run a positive control beside any ABSENT answer). Normalise NOTHING: compare bytes. A member with no
       file at that commit (a vendored dependency, a build stamp) is listed as `NOT_IN_SOURCE_DIR` with its name and size, not as
       a difference. Print a table and one line `MEMBERS n EQUAL e DIFFERENT d NOT_IN_SOURCE_DIR x`.
    4. Also compare each source member with the SAME path at your tree's HEAD, and print which of the three (deployed, recorded
       commit, HEAD) agree. A member where HEAD differs from the deployed one is a built-not-deployed change: name it.
    5. From the DEPLOYED `lambda_function.py` (the downloaded bytes, not the tree): print the `validate_user_type` function and
       the function it calls to decide "Opal-internal", with their line numbers in the deployed file. State in one sentence each:
       which userType values it admits; whether a caller with NO userType is admitted; whether a caller with tier `internal` and
       any userType is admitted. Quote code lines only; there is no client data in this file.
    6. Write the result to `org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r5_dr1/DATA_REFRESH_DEPLOYED_VS_BUILD_INPUT_20261011.md`
       and the member table as JSON beside it. Delete the downloaded package from your scratch space afterwards (it is your own
       temporary copy; nothing in the repository or AWS is removed).
    7. Write the proof-of-spec instance in your deliverables folder ROOT, validate it, flip this order to `complete`, write your
       session log, and report once to `2.0.0_SA_COO~V2`: the `MEMBERS` line FIRST, then the three sentences of step 5.
       Do NOT call any data-refresh route and do NOT mint or use any token: this is a read of bytes.
  </go>

  <bounds>
    Read-only against AWS: `get-function-configuration` and `get-function` on ONE function, and the download of its package.
    No invoke, no route call, no token, no IAM, no Terraform, no ledger entry. No change to the row: its disposition is the CTO's.
    A surprise is ONE row in `org/missions/D7/TCKT/TCKT_VNEXT/surprise-channel/investigations/INVESTIGATION_v1.md`
    (`TCKT_VNEXT-D2-S<k>`, next free id; binary append, line endings kept).
  </bounds>

<paths>
org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/
org/tier2_senior/0.7.0_AE_CloudOps~TV2/logs/
org/missions/D7/TCKT/TCKT_VNEXT/surprise-channel/investigations/INVESTIGATION_v1.md
</paths>

<proof_of_spec>
  <criterion id="AC1" cell_refs="R5-dr-1"><invocation>python -c "import json;d=json.load(open('org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r5_dr1/members.json',encoding='utf-8'));print('DR1-MEMBERS-OK' if isinstance(d,list) and d and all({'member','deployed_sha256','recorded_commit_sha256','verdict'}<=set(m) for m in d) else 'DR1-MEMBERS-FAIL')"</invocation><expect>DR1-MEMBERS-OK</expect></criterion>
</proof_of_spec>
AC1 at the issuance: FAIL as expected (the file does not exist). Name the member table `members.json` so the check finds it; a
list of objects, each with at least `member`, `deployed_sha256`, `recorded_commit_sha256` (or null) and `verdict`.

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE (one read, no schedule).
comp-iam: DECLARED-NOT-APPLICABLE (no IAM change; two read calls on one function).
comp-adversary: DECLARED-NOT-APPLICABLE (a read of bytes; nothing is applied and no route is called). The control is the positive control beside any ABSENT answer in step 3.
</preflight>

# pipeline-override: a READ order to the dell2 applier for an issuer cell (R5-dr-1): a package download and a diff, nothing written to AWS; not a worker cell.
</task_order>
