# MDPF_SECCLASS TO-DEPLOY-e57e61 -- proof instance, and the act narrative for e57e61 and e65b

**Author:** 0.7.0_AE_CloudOps~SD (dell1)
**Date:** 2026-10-08
**Orders:** `MDPF_SECCLASS.TO-DEPLOY-e57e61.fwd10-producer-apply-laptop` (cells SC-e-57, SC-e-61)
and `MDPF_SECCLASS.TO-DEPLOY-e65b.cash-token-namekey-shared-deploy-laptop` (cell SC-e-65 amendment 3)

## WHY THIS FILE EXISTS

`.tools/deploy_ledger.py` REGENERATES a change_management entry from its own structured state on
every `close-leg` / `hold` / `close`. Free prose appended to the entry by hand is DISCARDED
SILENTLY -- measured here at 2026-10-08T02:2xZ, when closing leg L1 of
`secclass-e57e61-fwd10-apply-s-20261007` removed a 43-line `## STOP BEFORE THE BUILD` section this
seat had written and committed at `f9c38b6165` (that commit reported "1 file changed, 46
insertions"; the close reported "6 insertions, 49 deletions"). Nothing warned. The content survived
only in git.

So the ledger keeps the STRUCTURED state (legs, proofs, status, rollback) and THIS file keeps the
narrative. `secclass-e65b-namekey-deploy-s-20261007` still carries two hand-appended sections at
this writing and is exposed to the same loss at its next ledger write; both are reproduced below.
Filed as a surprise row.

---

## PART 1 -- e57e61 PROOF INSTANCE (the order's step 6/7 artifact)

**AC1, run after the apply:**

```
E57E61-LIVE ok=True live=C2HM0wFtBFbBpnyRyVzpvmMA5sCSUtz+vVUM2Hq3Lqo= artifact=C2HM0wFtBFbBpnyRyVzpvmMA5sCSUtz+vVUM2Hq3Lqo= prior=f0zhRV1FFFiVgnNMsEzYAGap8qCOWbb4xgZgpx8RIdQ=
```

Invocation: `python org/tier1_exec/2.0.0_SA_COO/deliverables/MDPF_SECCLASS_M/R12_CHECKS/e57e61_lambda_sha_check.py`
Expected by the order: `E57E61-LIVE ok=True`. Base at the cut: `ok=False`.

**The act, in order, with every precondition the CTO and issuer added:**

| step | what | result |
|---|---|---|
| seat gate | `safe-apply ... apply --dry-seat-gates` | APPLY-WHO `verdict=ADMITTED`; CROSSBOX-DEPLOY `device=dell1 root=new-security-classifier open_call=clear overlap=clear upset=clear` `verdict=CLEAR`. No STOP in any mode. |
| write-target proof | all 6 policy documents on `cloudops-dell1-agent-user` + group `cloudops-dell-agents-group`, 22 statements | `s3:PutObject` on the artifact key = 1 allow / 0 deny; `lambda:UpdateFunctionCode` on the function = 1 allow / 0 deny |
| 4a re-pin | `rivalfunds_classification.py` `87065e4565` -> `5cbb530eb6`, sha256 `4ed99536...` | committed alone `@a17d4ab9bf`, 2 insertions 2 deletions; other three members left at `87065e4565` |
| 4b zip check | `BUILD_ONLY=1` build, nothing uploaded | 5 of 5 members MATCH, 0 unexpected, 0 missing |
| 4 upload | `build-and-upload.sh mdpf-secclass mdpf-secclass-new-security-lambda` | ETag `83ae4070` -> `a637f437`, VersionId -> `QVGKPT0Q...`, size 39519 -> 39751, content-sha256 -> `C2HM0wFt...`; `@833f8c3433` |
| 5 apply | `safe-apply` under `CHECKPOINT_DISABLE=1` | `Plan: 0 to add, 1 to change, 0 to destroy`; `Apply complete! Resources: 0 added, 1 changed, 0 destroyed` at 2026-10-08T02:24:02Z |
| 6 proof | live read + 0-diff re-plan + AC1 | CodeSha256 `C2HM0wFt...`; `No changes. Your infrastructure matches the configuration.`; AC1 `ok=True` |
| 7 verify | the 2026-10-08T14:00Z producer run | **OPEN** -- ledger L3, entry HELD |

**The write-target evaluation was validated by controls, not asserted.** `comp-iam simulate` could
not be used: `iam:SimulatePrincipalPolicy` is itself `AccessDenied` for this principal, so the
wrapper returns `STATE: NOT-DECIDABLE`. The substitute was a read of the actual policy documents,
and it was checked against two facts already observed in the world: it reproduces the explicit
DENY on `opal-data-cot/code/gold/*` that really stopped e65b, and the ALLOW on `opal-data-bd` that
really succeeded. That is an APPLIED-plane read, not EXERCISED.

**The first safe-apply attempt failed CLOSED, and that is recorded rather than hidden.** Its
`naming-plan` and `comp-tagauthz` limbs run their OWN `terraform plan` and do not inherit `-var`
from the apply args, so neither could render a plan: *"a gate that cannot evaluate must not pass.
Refusing to apply. (Fail closed.)"*. Nothing was applied -- the function still read `f0zhRV1F` at
`2026-10-05`. The remedy was the one safe-apply's own text prescribes -- **fix the cause so the
gate RUNS**, never `TAGAUTHZ_OVERRIDE`, which it calls a last resort and "not the remedy for this
error": exporting `TF_VAR_silver_prefix='silver/holdings/'` makes the variable visible to every
terraform invocation including the gates' internal plans, so both gates RAN.

`silver/holdings/` is not invented. It is the APPLIED value, read off the live function's
`SILVER_PREFIX` environment variable, and `main.tf` wires `local.silver_prefix = var.silver_prefix`,
so a bare plan with it renders the identical 0/1/0 diff. A different value would have shown an
env-var change and been a STOP under the order's bounds.

**Rollback, still live:** copy the artifact back from VersionId
`2DwW9a.Pz6G7A1o.wSTshxZGZzFCVw5b` with `--metadata-directive COPY`, then re-apply this root with
`TF_VAR_silver_prefix` set. That returns CodeSha256 to `f0zhRV1FFFiVgnNMsEzYAGap8qCOWbb4xgZgpx8RIdQ=`.

**Standing deployment rules NOT actioned, surfaced not assumed:** Deployment Rule 4 wants
`last_deployed_commit` recorded in `lambda-source-map.json` (it currently reads `none` for this
function) via `record-terraform-deploy.sh`, and Rule 6 wants a `{pipeline}-v{X.Y.Z}` tag pushed with
`--follow-tags`. Neither is in this order's `<the_act>`, the tag requires a push this seat does not
make on a shared branch, and `record-terraform-deploy.sh` carries a known CHANGELOG/owned-paths
failure mode (cloud-ops "Failure handling"). Named here for the issuer rather than done unasked.

---

## PART 2 -- the e57e61 STOP that amendment 1 answered (recovered from `f9c38b6165`)

## STOP BEFORE THE BUILD -- the source map's staged_from pins are stale (0.7.0_AE_CloudOps~SD, 20261008T010626Z)

Step 4 was NOT run. Measured before any act:

`infra/aws/lambda/ci/lambda-source-map.json` pins all four `staged_from` members of
`mdpf-secclass-new-security-lambda` at `87065e4565a29bb387c6945acbab01f54896a405` -- a commit from an
unrelated project (`3.0.0_SA_CVO` IRPT_YCDGEN round-5 compile).

`infra/aws/lambda/ci/build-and-upload.sh` lines 195-241 stage each `staged_from` member from
`git show <pin>:<repo_path>` -- its own comment says "never the worktree" -- and verify the blob's
sha256 against the DECLARED value, refusing on a mismatch. Here the pin and its declaration AGREE,
so the guard passes GREEN while shipping pre-port bytes. The guard cannot see staleness, only drift.

Members, pin vs dell1 CLOUD (denominator 4):
  etf_classification.py             DIFFERS
  etf_classification_scheduled.py   DIFFERS
  etf_classifications_dynamodb.py   same
  rivalfunds_classification.py      DIFFERS  <- the e57/e61 surface itself

`rivalfunds_classification.py`: pin blob `aac14cb2c6` (sha256 `b2523e43...`, equal to the declared
value) vs CLOUD blob `d3363dba79` (sha256 `4ed99536...`); 13 insertions, 12 deletions. That diff IS
the fix this order exists to ship -- "the sector lands here ONLY, never in sub_asset_class (S28)",
plus the `elif` -> `if` change that keeps US listings.

Meanwhile `lambda_function.py` is in `files[]`, NOT `staged_from`, so it ships from the WORKTREE at
the ported bytes `e025665470`.

So a build now yields a MIXED artifact: ported entrypoint, pre-port shared modules. The plan could
still read 0/1/0 with `source_code_hash` only, and AC1 would still read `ok=True`, because AC1
compares the live CodeSha256 against the artifact's `content-sha256` and both would be the new
wrong-content zip. CLAUDE.md rule 22a: diff deployed bytes against the BUILD INPUT, never by
filename.

UNTOUCHED, re-read at the STOP: artifact IsLatest VersionId `2DwW9a.Pz6G7A1o.wSTshxZGZzFCVw5b`;
function CodeSha256 `f0zhRV1FFFiVgnNMsEzYAGap8qCOWbb4xgZgpx8RIdQ=`. Both equal the before-reads.

REMEDY, named and NOT executed: re-pin the four `staged_from` entries to the merged e57e61 commit
with fresh sha256 values. That is a write to `infra/aws/lambda/ci/lambda-source-map.json`, which
this order's `<paths>` block does not name -- OUT OF LANE for this seat; it belongs to the issuer,
`2.0.0_SA_COO~M1`. Reported to the issuer the same hour.

The entry stays OPEN by the tool's own rule (a HELD state requires every apply leg closed, and here
none ran). It is OPEN-WITH-NOTHING-LANDED, not half-landed: there is nothing to roll back.

---

## PART 3 -- the e65b narrative, preserved against the same loss

Reproduced from `org/critical_paths/change_management/20261008T0123Z_secclass-e65b-namekey-deploy-s-20261007_deploy_completion.md`
as it stands at commit `27302e4624`, because that entry's next ledger write will discard it.
e65b is HELD by issuer ruling msg 737 until Andrew's item 2 (the dell1 firm-data limits) lifts the
`opal-data-cot/code/gold/*` deny; it does not return to a laptop seat.

## ATTEMPT 1 FAILED CLOSED -- .tools/aws.cmd resolves no AWS CLI on dell1 (0.7.0_AE_CloudOps~SD, 20261008T013112Z)

The ONE safe-deploy run of step 5 was invoked as the order names it:

    .tools/safe-deploy.sh --author "0.7.0_AE_CloudOps~SD"       data/black_diamond/scripts/gold/E_18.detect_new_securities.py       data/cot/scripts/gold/A_00.accounts_dimension.py

It enumerated the expected 8 destinations (2 script carriers + 6 declared shipped
artifacts across opal-data-bd and opal-data-cot), then failed on the FIRST upload:

    ERROR  UPLOAD_FAIL  [shipped] .../etf_classifications_dynamodb.py -> s3://opal-data-bd/...
      aws.cmd: FATAL -- no AWS CLI found. Checked
      %LOCALAPPDATA%\Programs\Python\Python312\Scriptsws.cmd,
      %LOCALAPPDATA%\Programs\AWSCLIV2\Amazon\AWSCLIV2ws.exe,
      %ProgramFiles%\Amazon\AWSCLIV2ws.exe

STATE AFTER THE FAILURE -- MEASURED, not inferred from the tool's own
"files listed above as DEPLOYED may already be on S3" warning. All 8 keys re-read:
every one carries BOTH the same ETag AND the same VersionId it carried before the
attempt. A byte-identical PUT to a versioned bucket still mints a NEW VersionId, so
UNCHANGED VersionIds are positive proof that ZERO PUTs occurred -- not merely that
content is unchanged. Nothing landed; nothing is half-landed; there is nothing to roll
back. Both movers still read 3f1e6be8910952f33c88bf100c610ab6 at VersionIds
0aE1FGTSH.2rsPdoj.3mtrBuHmmByxAu (bd) and 0e4OsubYyRdw4RnmCvfMYM0SZtLLM9z9 (cot).

CAUSE: `.tools/aws.cmd` -- the Windows-shell companion that NATIVE-PYTHON callers reach
through `shutil.which` -> `~/bin/aws.cmd` -> the tracked `.tools/aws.cmd` -- hardcodes
three absolute CLI paths and none exists on dell1. The real CLI here is
`%LOCALAPPDATA%\Programs\Amazon\AWSCLIV2ws.exe`
(/c/Users/Test/AppData/Local/Programs/Amazon/AWSCLIV2/aws.exe, 9,448,160 B, 2026-10-02),
which is NOT candidate 2 (`Programs\AWSCLIV2\Amazon\AWSCLIV2`) -- a different nesting.
Verified directly: `cmd //c ".toolsws.cmd --version"` prints the same FATAL.

The bash shim `.tools/aws` is UNAFFECTED and resolved correctly all session
(AWS_SHIM_DEBUG=1 prints real-entry /c/Users/Test/AppData/Local/Programs/Amazon/AWSCLIV2/aws),
which is why every hand-run read in this entry succeeded while the deploy failed. That is
the exact asymmetry `.tools/aws.cmd`'s own header documents for site Z.

REMEDY, named and NOT executed: add a fourth candidate
`%LOCALAPPDATA%\Programs\Amazon\AWSCLIV2ws.exe` to `.tools/aws.cmd`. That is a write
to `.tools/aws.cmd`, which this order's <paths> block does not name -- OUT OF LANE for this
seat. Reported to 2.0.0_SA_COO~M1 the same hour.

CARRIES BEYOND THIS ORDER: `.tools/aws.cmd`'s own header records that under `--quiet` this
same failure is a SILENT NO-OP -- `infra/aws/lambda/ci/build-and-upload.sh` "reported a
successful upload while S3 kept the OLD zip". build-and-upload.sh is step 4 of
TO-DEPLOY-e57e61, the next order in this seat's queue, so that order must not be run on
this device until the shim resolves. Filed as a surprise row.

The entry stays OPEN with all four legs OPEN and the world untouched.

- 20261008T015258Z ATTEMPT 2 HALF-LANDED then ROLLED BACK IN-SESSION by 0.7.0_AE_CloudOps~SD. Parity restored; escalated loud. See the section below.

## ATTEMPT 2 -- HALF-LANDED, ROLLED BACK, PARITY RESTORED (0.7.0_AE_CloudOps~SD, 20261008T015258Z)

The hold of ruling msg 733 was lifted by msg 735 after 0.0.0_AB_MSTR~DELL1's fix
62d57c9f73 to .tools/aws.cmd. PROVEN FIRST, as that ruling directed, on all three caller
paths: `.tools\aws.cmd --version` -> aws-cli/2.37.9; `.tools\aws.cmd sts
get-caller-identity` -> arn:aws:iam::313476888478:user/cloudops-dell1-agent-user; and
python shutil.which('aws.cmd') -> C:\Users\Test\bin\aws.cmd -> 2.37.9, which is the
exact native-Python path that failed in attempt 1.

GATE RE-CHECKED before the retry: gold/trigger-pending.json 404, zero objects under
logs/gold-layer/ newer than the 01:16:24Z run log, so no gold run in progress. All 8 keys
RE-READ: both movers at 3f1e6be8 with the order's exact rollback VersionIds, the six others
equal to repo HEAD. Mover md5 at HEAD 40ffa3fac380551704637adc8a3b6ff3.

WHAT LANDED. The one safe-deploy run uploaded THREE keys to opal-data-bd, then failed on
the first opal-data-cot key:

  DEPLOYED-SHIPPED etf_classifications_dynamodb.py -> s3://opal-data-bd/...
  DEPLOYED-SHIPPED etf_classification_scheduled.py -> s3://opal-data-bd/...
  DEPLOYED-SHIPPED etf_classification.py           -> s3://opal-data-bd/...
  ERROR UPLOAD_FAIL  etf_classifications_dynamodb.py -> s3://opal-data-cot/...
    AccessDenied on s3:PutObject, resource
    arn:aws:s3:::opal-data-cot/code/gold/lib/_shared/etf_classifications_dynamodb.py,
    principal arn:aws:iam::313476888478:user/cloudops-dell1-agent-user,
    "with an explicit deny in an identity-based policy:
     arn:aws:iam::313476888478:policy/cloudops-dell-agent-routes-host-policy"

MEASURED, per key: exactly ONE key moved BY CONTENT -- the bd mover, ETag
3f1e6be8910952f33c88bf100c610ab6 -> 40ffa3fac380551704637adc8a3b6ff3 at new VersionId
zSt33nq7_Eh78Y9hR_KR31D18BTa5v6b (01:47:59Z). The other two bd uploads were byte-identical:
etf_classifications_dynamodb.py stayed 4cc11d3e (new Ver VJUrFMm.HC7SGZt0YSoeKqNugn7R51ZC)
and etf_classification.py stayed 3a033c04 (new Ver U0SHTQGhpKPE6t0vVS2G1QpaZctq.UV4). All
five remaining keys were UNTOUCHED at their pre-act VersionIds: the cot mover, both cot
members, and both gold carriers (which never uploaded).

WHY FINISHING WAS IMPOSSIBLE: an EXPLICIT DENY in an identity-based policy, not a missing
grant. No ordering, retry or re-scoping of this act can satisfy it from this device, and
working around it is refused by the order and by CLAUDE.md. So NEVER-2's other branch
applied: roll back in-session and escalate loud.

ROLLBACK EXECUTED, the entry's own named command:
  aws s3api copy-object --bucket opal-data-bd
    --key code/gold/lib/_shared/etf_classification_scheduled.py
    --copy-source '...?versionId=0aE1FGTSH.2rsPdoj.3mtrBuHmmByxAu' --metadata-directive COPY
It returned ETag 3f1e6be8910952f33c88bf100c610ab6 at new VersionId
keWIVX74Byn38wT7eBADpt1ElR7U1E3t (01:49:54Z). VERIFIED by an INDEPENDENT head-object, not
from the copy's own response: bd mover ETag 3f1e6be8910952f33c88bf100c610ab6, 35,100 B;
cot mover ETag 3f1e6be8910952f33c88bf100c610ab6, 35,100 B. PARITY RESTORED -- both firm
copies carry identical pre-act content, which is the state the act began from.

The two byte-identical bd keys were NOT rolled back and need no rollback: their CONTENT
never moved (4cc11d3e and 3a033c04, unchanged before and after). A copy-back would only
mint a third VersionId with identical bytes. L3's standard is content unmoved, and it is.

EXPOSURE WINDOW: 01:47:59Z to 01:49:54Z, 115 seconds, during which opal-data-bd carried
40ffa3fa while opal-data-cot carried 3f1e6be8. NOTHING CONSUMED IT: gold/trigger-pending.json
reads 404 and zero objects exist under logs/gold-layer/ newer than the 01:16:24Z run log, so
no BD gold run started, and E_18 wrote no cash_token row against the new module. The
asymmetry was never observed by a producer.

THE GATE SAW IT COMING. safe-deploy's own seat-gates printed, before any upload:
  [seat-gates] CROSSBOX-DEPLOY device=dell1 root=black_diamond ... verdict=STOP
  [seat-gates] CROSSBOX-DEPLOY device=dell1 root=cot ... verdict=STOP
  [seat-gates] WARN would stop under ENFORCE (crossbox-deploy:data/black_diamond
               crossbox-deploy:data/cot); WARN mode proceeds.
The IAM explicit deny and that gate are two expressions of one rule: dell1 is not the device
that deploys these firm roots. In WARN mode the gate advised and proceeded; the IAM policy
refused. Had the gate been in ENFORCE, nothing would have landed and no rollback would have
been needed. Filed as a surprise row.

STATE AT THIS WRITING: all four legs OPEN, the entry stays OPEN per ruling msg 733, and the
world is back to its pre-act content on all 8 keys. Nothing is stranded. e65b CANNOT be
completed from dell1; escalated to 2.0.0_SA_COO~M1 the same hour, asking for a seat that can
write opal-data-cot or a lift of the deny. This seat attempted no workaround.
