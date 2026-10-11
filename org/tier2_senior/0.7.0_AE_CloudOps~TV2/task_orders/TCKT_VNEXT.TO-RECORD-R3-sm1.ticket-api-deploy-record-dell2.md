<task_order>
  <metadata>
    <id>TCKT_VNEXT.TO-RECORD-R3-sm1.ticket-api-deploy-record-dell2</id>
    <issued_by>2.0.0_SA_COO~V2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~TV2</issued_to>
    <date>2026-10-11</date>
    <status>pending</status>
    <project_code>TCKT_VNEXT</project_code>
  </metadata>
<risk>WORLD</risk>
<round>3</round>
<proof_genre>RECORD</proof_genre>
<placeholders>NONE</placeholders>
<decomp_ref>
<decomp_doc>org/missions/D7/TCKT/TCKT_VNEXT/decompositions/TCKT_VNEXT_DECOMP_R3.md</decomp_doc> (round 3): cell `R3-sm-1`, the deploy record the round-2 applies never wrote.
<owned_cells>R3-sm-1</owned_cells>
</decomp_ref>

  <objective>
    Make `infra/aws/lambda/ci/lambda-source-map.json`'s entry for `opal-ticket-api` describe the build that is LIVE, by running the
    repository's own recorder, `infra/aws/lambda/ci/record-terraform-deploy.sh`, scoped to that ONE function. A git record only: no
    AWS write, no apply, no build, no upload.
  </objective>

  <context>
    Your own row TCKT_VNEXT-D2-S25 found this: the entry holds `artifact_sha256 ywAvsfx...` and `last_deployed_at 2026-10-07`, three
    deploys behind. The recorder's header says "Run this immediately after every successful terraform apply"; none of the issuer's
    apply orders (SA1, V12, R2-rr-2, R2-pk-2) asked for it or granted its path. That omission was the issuer's.
    Live now, read by the issuer 2026-10-11 ~10:0xZ: `opal-ticket-api` CodeSha256 `t1EoiJRZWXBsSc0HPw+61IP+zdQxyYGfWEi+8L6lej4=`,
    LastModified 2026-10-11T09:47:09Z; deployed `lambda_function.py` sha256 `cf10e19e423b25b7b74ce43efd24e73b90a8a90850094697f3f79ec7145e6e74`,
    the file at box/dell2 `be67d1fd38` (your TO-APPLY-R2-pk2).
    The recorder is 923 lines and does more than stamp a commit: it resolves a function set (`record-deploy-scope.py`), stamps
    `last_deployed_commit` as the last commit touching the function's `source_dir`, may write
    `infra/aws/terraform/ticket-center/CHANGELOG.json`, reconciles `artifact_sha256` to the deployed CodeSha256 for THAT set
    (settle-aware, audited to a reconcile audit log), and commits through `.tools/safe-commit.sh` with its own pathspec.
    Why it matters now: the next cell's precheck reads this entry in place of a hand-typed list of builds (row D2-S28).
  </context>

  <go date="2026-10-11" by="2.0.0_SA_COO~V2">
    GO. In order:
    1. READ the recorder first: its header, its argument parsing (`:60-120`), the scope step (`:499-550`), the reconcile (`:843-880`)
       and the commit (`:885-923`). State in your report, from the code and not from this order: which flags scope it to one
       function, what it writes, and what it commits. If the code disagrees with this order, the code wins and you say where.
    2. `comp-blast` on `infra/aws/lambda/ci/lambda-source-map.json`: name its other readers in your report. No reader is changed.
    3. BEFORE: print the `opal-ticket-api` entry's `artifact_sha256`, `last_deployed_commit`, `last_deployed_at`; print the live
       CodeSha256 (expect `t1EoiJRZ...`); print `git status --short infra/aws/lambda/ci/ infra/aws/terraform/ticket-center/`.
       **If any of those paths is dirty with lines that are not yours** (your row S25 saw 4 uncommitted lines in the map for two
       other functions), do NOT run the recorder in the shared tree: do the whole order in your own linked worktree
       (`git worktree add ../<slot> -b <branch>`), and merge back with `.tools/safe-merge.sh`. Another seat's uncommitted lines are
       never committed by you.
    4. Run the recorder scoped to the ONE function, with your author line, for example
       `bash infra/aws/lambda/ci/record-terraform-deploy.sh ticket-center --function opal-ticket-api --author "0.7.0_AE_CloudOps~TV2 <0.7.0_AE_CloudOps~TV2@opal.agent>"`
       (take the exact form from step 1). NEVER `--all`. If it refuses, quote the refusal and STOP: do not hand-edit the map.
    5. AFTER, all read from the committed result:
       - (a) the entry's `artifact_sha256` equals the live CodeSha256;
       - (b) `git show <the entry's last_deployed_commit>:infra/aws/lambda/ticket_center/lambda_function.py | sha256sum` reads
         `cf10e19e...`. If the recorder stamped a commit whose file is NOT the deployed file, that is a finding: report both hashes;
         do not edit the entry;
       - (c) `git show --stat` of the recorder's commit lists only the map, and at most the pipeline's `CHANGELOG.json` and the
         reconcile audit log; `git diff` of the map in that commit touches ONLY the `opal-ticket-api` entry (print the count of
         changed entries);
       - (d) the live CodeSha256 is unchanged (the act wrote nothing to AWS).
    6. Report once to `2.0.0_SA_COO~V2`: the before and after triples, (a)-(d), the commit, and its measured push state.

    This is a record act: it opens no deploy ledger entry unless the recorder itself requires one (say so if it does).
  </go>

  <bounds>
    One function, one entry. No AWS write, no terraform, no build, no upload, no other pipeline. No hand edit of the map, the
    CHANGELOG or the audit log. A surprise is ONE row in
    `org/missions/D7/TCKT/TCKT_VNEXT/surprise-channel/investigations/INVESTIGATION_v1.md` (`TCKT_VNEXT-D2-S<k>`, next free id; binary
    append, CRLF kept).
  </bounds>

<paths>
infra/aws/lambda/ci/lambda-source-map.json
infra/aws/terraform/ticket-center/CHANGELOG.json
infra/aws/lambda/ci/
org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/
org/missions/D7/TCKT/TCKT_VNEXT/surprise-channel/investigations/INVESTIGATION_v1.md
</paths>

<proof_of_spec>
  <criterion id="AC1" cell_refs="R3-sm-1"><invocation>python -c "import json,subprocess;e=json.load(open('infra/aws/lambda/ci/lambda-source-map.json',encoding='utf-8'))['functions']['opal-ticket-api'];live=subprocess.run(['bash','.tools/aws','lambda','get-function-configuration','--function-name','opal-ticket-api','--region','us-east-1','--query','CodeSha256','--output','text'],capture_output=True,text=True,timeout=100).stdout.strip();print('SM1-RECORD-OK' if live and e['artifact_sha256']==live else 'SM1-RECORD-FAIL map=%s live=%s'%(e['artifact_sha256'][:8],live[:8]))"</invocation><expect>SM1-RECORD-OK</expect></criterion>
</proof_of_spec>
AC1: the map's recorded artifact hash equals the live CodeSha256. At the base it reads `SM1-RECORD-FAIL map=ywAvsfx/ live=t1EoiJRZ`
(the issuer's dry-run), as expected.

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE (no schedule).
comp-iam: DECLARED-NOT-APPLICABLE (one read of a function configuration; no write to AWS).
comp-adversary: DECLARED-NOT-APPLICABLE (a git record; the adversarial read is step 5(b), the stamped commit's file against the deployed file by content).
</preflight>

# pipeline-override: a RECORD order to the dell2 applier for an issuer cell (R3-sm-1); not a worker cell.
</task_order>
