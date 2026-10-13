<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-RESTORE-R20a.holdings-artifact-key-aq2</id>
    <issued_by>2.0.0_SA_COO~Y2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~AQ2</issued_to>
    <date>2026-10-13</date>
    <status>pending</status>
    <project_code>IRPT_ANLREQ</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<placeholders>NONE</placeholders>
<preflight>
comp-blast: RUN -- by reading the incident and the live state: ONE S3 key (investor-reporting/irpt-holdings.zip in opal-313476888478-lambda-artifacts) gets one new version whose bytes are the live package's; the Lambda irpt-holdings is not updated; no Terraform apply; DELTA on served output = 0 (the function keeps running SWRfUfHd...). NOT seen: which Terraform root reads this key at its next plan (the restore removes the question).
comp-routes: DECLARED-NOT-APPLICABLE -- no route is added or changed. comp-cache: DECLARED-NOT-APPLICABLE. comp-schedule: DECLARED-NOT-APPLICABLE -- no schedule or trigger.
comp-iam: DECLARED-NOT-APPLICABLE -- no IAM change; the copy uses the s3 rights this applier already holds on the artifact bucket (the rights an AE_CloudOps applier holds on the artifact bucket (IB2 used them for the release-19 Lambda leg)).
comp-adversary: RUN -- by reading the incident (three wrong versions, latest is wrong) against the cell; the lens: restoring the wrong version, or deleting evidence. The order proves the source version's bytes equal the live CodeSha256 before the copy, keeps the three wrong versions, and reads the new latest back. NOT seen: any consumer of the key other than the Lambda module.
</preflight>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R20RS_Y.md</decomp_doc> round 20, workstream YR round 9: the restore of an artifact key written by a rebase worker.
<owned_cells>AR-y-215</owned_cells>
</decomp_ref>

  <objective>
    Make the latest version of s3://opal-313476888478-lambda-artifacts/investor-reporting/irpt-holdings.zip byte-identical to the LIVE package of irpt-holdings, by copying version dWoiYeH9MSXq9yOuQkApr2h_XxwrvVi8 onto the key. Nothing else changes: no Lambda update, no Terraform apply, no deletion.
  </objective>

  <context>
    Load /cloud-ops first. The incident is in the decomposition (org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R20RS_Y.md): three versions written today by status-rule rebase workers running BUILD_ONLY at commits that predate the guard. The issuer measured: version dWoiYeH9MSXq9yOuQkApr2h_XxwrvVi8 (299273 bytes, 2026-10-12T13:51:17Z) hashes to the live CodeSha256 SWRfUfHdJarO2Rhbxw/KQK88DeDNorQujkaR1jUuZc0=; versions T1NEd9G.pJu3H8SlT4x0K4K7WGk8K3_O, msFi8sD6Uq.rtbYR5nC4IO2IjeFfH5bz and QCyspt0vCl9V84mic__vTeHqKutOrKU6 (the latest) are 294243 bytes, sha256 base64 tS/APci3Mz/YRDP7pJboAVqKabShek9jYUqvQDIYwwE=. This is the same kind of act as the rollback of release 19 (copy a version onto the key). Re-read everything yourself; the issuer's numbers are leads.
  </context>

  <the_act>
    1. Open ledger irpt-holdings-key-restore-20261013 (legs R1 verify, R2 copy, R3 read-back) and commit it; read every live worktree's open deploy entries (git worktree list, then ls-tree) and print the denominator: another open entry naming irpt-holdings is a STOP.
    2. R1: `get-function irpt-holdings` CodeSha256 must read SWRfUfHdJarO2Rhbxw/KQK88DeDNorQujkaR1jUuZc0=. List the key's versions. The latest must be QCyspt0vCl9V84mic__vTeHqKutOrKU6; if a NEWER version exists, someone else wrote after the issuer's read: STOP and report. Download version dWoiYeH9MSXq9yOuQkApr2h_XxwrvVi8 and compute its sha256 base64: it must equal SWRfUfHdJarO2Rhbxw/KQK88DeDNorQujkaR1jUuZc0=. Anything else: STOP, report.
    3. R2: copy that version onto the key (`aws s3api copy-object` with `--copy-source "opal-313476888478-lambda-artifacts/investor-reporting/irpt-holdings.zip?versionId=dWoiYeH9MSXq9yOuQkApr2h_XxwrvVi8"`, same bucket, same key; do not change metadata or content type). Do NOT delete any version.
    3b. If you can run it read-only in the time, a scoped `terraform plan` for the module that owns irpt-holdings in infra/aws/terraform/investor-reporting (never apply): record its summary line; expected: no change to the function's code attributes. If it needs more than an init you do not hold, record ABSENT with the reason.
    4. R3: list versions again: a NEW latest exists; download it: sha256 base64 equals SWRfUfHdJarO2Rhbxw/KQK88DeDNorQujkaR1jUuZc0= and 299273 bytes; `get-function irpt-holdings` CodeSha256 is unchanged. Write the output files named in the criteria, close the ledger, and report once to 2.0.0_SA_COO~Y2 with the new VersionId.
  </the_act>

  <bounds>
    One S3 key, one new version. No Lambda update, no Terraform apply, no delete of any object or version (the three wrong versions stay as evidence; a delete of S3 versions needs Andrew's word), no IAM change. A STOP at any step leaves the key as it is.
    Rollback: none needed (the act adds a version; the previous latest version stays addressable by id).
  </bounds>

  <proof_of_spec>
Instance at `org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r20/IRPT_ANLREQ.TO-RESTORE-R20a.holdings-artifact-key-aq2.proof_of_spec.json`.
    <criterion id="R20a-AC1" cell_refs="AR-y-215">The source version hashed to the live CodeSha256 before the copy.<invocation>grep -c 'source version sha256 SWRfUfHdJarO2Rhbxw/KQK88DeDNorQujkaR1jUuZc0=' org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r20/R1_VERIFY_R20.txt</invocation><expect>^[1-9]</expect></criterion>
    <criterion id="R20a-AC2" cell_refs="AR-y-215">The new latest version reads back byte-identical to the live package.<invocation>grep -m1 'new latest sha256 SWRfUfHdJarO2Rhbxw/KQK88DeDNorQujkaR1jUuZc0=' org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r20/R3_READBACK_R20.txt</invocation><expect>new latest sha256 SWRfUfHd</expect></criterion>
    <criterion id="R20a-AC3" cell_refs="AR-y-215">The ledger irpt-holdings-key-restore-20261013 is CLOSED.<invocation>grep -m1 '^\*\*Status' org/critical_paths/change_management/*irpt-holdings-key-restore-20261013_deploy_completion.md</invocation><expect>^\*\*Status:\*\* CLOSED</expect></criterion>
  </proof_of_spec>
</task_order>
# pipeline-override: an APPLY order to a tier-2 applier repairing an artifact key written in error (not a worker cell); the cell AR-y-215 is the issuer's, as for TO-APPLY-R19b.
