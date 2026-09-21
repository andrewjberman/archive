# NEVER-WIDEN SIGN-OFF PACKET -- IRPT_BCKEND.TO-IB-rtg-4

**THE HOLDINGS LOADER FOLLOWS THE DIRECTORY POINTER.** Cell `IB-rtg-4`, row `S100`. Worker
`0.9.0_WK_IRPT_BCKEND~4`. Written per CLAUDE.md Rule 5 (`NEVER move served output without
never-widen sign-off`) and this order's arm (c): a K-CODE packet on `irpt-holdings` carries its
own never-widen halves, or it does not deploy.

This packet is the ACT's blast-radius description. It does not itself constitute a sign-off --
`2.0.0_SA_COO~B` (this project's issuer) and `1.0.0_SA_CTO` each sign their own half against the
`blob <hash>` this file carries at HEAD, per Rule 5's mechanism (`org/tier1_exec/<seat>/
deliverables/NEVER_WIDEN_SIGNOFF_{COO,CTO}_HALF_IRPT_BCKEND_IB-rtg-4_*.md`). **As of this pass
BOTH halves are ABSENT** (checked this run: `org/tier1_exec/2.0.0_SA_COO~B/deliverables/` and
`org/tier1_exec/1.0.0_SA_CTO/deliverables/` carry no file naming `rtg-4`) -- this order's arm (d)
does not run this pass; this packet is committed so the halves have something to sign against.

## THE ACT

Deploy `irpt-holdings` with ONE edited source member -- `holdings/entry.py`'s `_load_directory`
now follows the `latest.json` pointer (fetch the pointer at `DIRECTORY_KEY`, then fetch
`pointer["key"]` through `directory/handler.py`'s existing single-key `load_directory`, cached by
its own S3 key) instead of feeding `DIRECTORY_KEY` itself to that single-key loader and returning
the pointer document verbatim. No other function's bytes are touched by this act; no other route
deploys; `directory/handler.py`'s own `load_directory` and `lambda_handler` are UNEDITED (this
order's confined bound); `_authz/loaders.py` (the cited correct pattern) is UNEDITED.

## THE KEY -- THE ONE SERVING FUNCTION'S BYTES

`N = 1`. Only `irpt-holdings` gains this edit; the build-and-upload.sh single-function invocation
targeted `irpt-holdings` alone, and the ten-root Terraform plan below confirms no other root's
`aws_lambda_function` resource is touched.

| # | function_name | prior `CodeSha256` (rollback target, read live this run) | LastModified (live) |
|---|----------------|------------------------------------------------------------|----------------------|
| 1 | irpt-holdings | `uS+WBeNxiCkYU2pdGalaONZ74SvoWEiYx669KWYKQDA=` | 2026-09-19T17:17:55.000+0000 |

Read via `.tools/aws.cmd lambda get-function-configuration --function-name irpt-holdings --query
"{CodeSha256:CodeSha256,LastModified:LastModified}"`, this run, 2026-09-20. The ROLLBACK is
"re-publish this exact `CodeSha256`" (Terraform `filename`/`source_code_hash` pinned back to the
pre-deploy zip; NEVER `aws lambda update-function-code`, per CLAUDE.md NEVER-9). The build-store
rollback source (the S3 object version under `investor-reporting/irpt-holdings.zip` immediately
BEFORE this order's build ran) is `VersionId=U4sKRs.HJ0Jc4Ik323Y0b.qY7LsWU2Pg`,
`LastModified=2026-09-19T15:58:12.000Z`, read via `.tools/aws.cmd s3api list-object-versions`
this run.

**BUILT THIS RUN** (K-CODE): `CodeSha256`/`artifact_sha256`
`rAAn3bt7MZXpxFgric7LlrNW9uv0xXgpiZmb+MOf/y0=`, 134525 bytes (132K), via
`infra/aws/lambda/ci/build-and-upload.sh investor-reporting irpt-holdings` (run from
`/c/tmp/wk-irpt-7-4`, INSIDE the git repo -- running with `cwd=/c/` breaks
`manifest-index-check.py`'s `git show <pin>:<path>` calls, since `git show` resolves against the
current working directory's repository and `/c/` is not one; a row is filed on this). **VERIFIED
AT REST**: the built zip downloaded fresh from S3 and re-hashed matches the declared
`artifact_sha256` exactly (`match=True`); 15 of 15 declared members (`files[]`) are byte-equal to
the zip's namelist; the 3 vendored members (`errors.py`, `resolve.py`, `handler.py`) pass the
INDEX-SOURCED MANIFEST GATE (index-equal, manifest-equal, 0 CR bytes) at pin
`ccbf4ac3cb5c20ffd7ad937221a562b87abf9c76`; import-closure: 10 of 10 packaged `.py` files'
top-level imports satisfied by package/stdlib/runtime/layer. The served-byte delta against the
prior build is EXACTLY the one edited member, `entry.py` -- confirmed byte-equal between the
zip's copy and the worktree fix, and no other of the 15 packaged members changed.

**TERRAFORM PLAN, HOLDINGS ROOT** (this run, vendored `.tools/terraform.exe`, saved to
`.scratch/ib_rtg_4_holdings.tfplan`): **`Plan: 0 to add, 1 to change, 0 to destroy.`**
`module.irpt_holdings.aws_lambda_function.this` -- `source_code_hash`
`uS+WBeNxiCkYU2pdGalaONZ74SvoWEiYx669KWYKQDA=` -> `rAAn3bt7MZXpxFgric7LlrNW9uv0xXgpiZmb+MOf/y0=`
(before == the prior live `CodeSha256` above, after == the built sha above), `s3_object_version`
`U4sKRs.HJ0Jc4Ik323Y0b.qY7LsWU2Pg` -> `EyuRE2U4NQ6qQOiizueXUHc.oD3k.FuP`, `actions = ["update"]`.

**THE OTHER NINE ROOTS RE-TAKEN** (this run, same binary, no apply): `api`, `core`, `directory`,
`export`, `intake`, `narrative`, `ops`, `performance`, `ycharts` each read **`No changes. Your
infrastructure matches the configuration.`** -- 0 to add, 0 to change, 0 to destroy on every one.

## THE CONTRACT DESCRIBED

Not a new contract member (unlike `IB-rtf-13`'s packaged schema) -- this act is a PURE source-code
edit to an already-packaged file, `entry.py`, confined to its `_load_directory` function. The
edit's net effect: `_load_directory(tenant)` now performs TWO `s3:GetObject` calls (the pointer,
then the resolved artifact) where it previously performed one (against the pointer's own key,
misread as the artifact). Both calls target keys already covered by the existing
`irpt-holdings-role` IAM grant (`s3:GetObject` on `arn:aws:s3:::${b}/investor-reporting/*`,
confirmed via `comp-iam service irpt-holdings` this run) -- the live pointer document resolves to
`key = "investor-reporting/directory/2026-09-17/directory.json"`, which falls under the same
already-granted prefix. **NO IAM WIDENING**: zero new grants, zero new resources; the preflight's
conditional IAM concern (arm (c) of this order's own preflight block) does not fire.

## THE BLAST RADIUS -- BOTH BRANCHES

**`irpt-holdings` IS WIRED**: `infra/aws/terraform/investor-reporting/api/integrations.tf:36`
declares `holdings = "irpt-holdings"`, serving `GET /api/scoped/investor-reporting/holdings/
{accountSetId}`. So the blast radius of this act, TODAY, reaches every live request on that route.

  * **DEPLOYED WITH the fix (forward branch).** `opaque_firm_for` now reads the RESOLVED directory
    artifact's `firm_id_opaque` (not the pointer document's, which never carries that field), so
    `FirmBinding.proves()` receives the real declared value. A holdings request for an account the
    principal's own `resolve` just granted reaches `holdings_snapshot` instead of being refused at
    the binding step; it then serves a scope-resolved answer (or a real policy refusal carrying
    `firm_id`) rather than `FIRM_BINDING` with `firm_id` absent. This is row `S100`'s fix.
  * **ROLLED BACK to the pre-fix bytes (as today, the negative control / rollback state).** The
    same call reads the pointer document as if it were the artifact, finds no `firm_id_opaque`,
    and `FirmBinding` refuses `FIRM_BINDING` for EVERY account request on this route regardless of
    entitlement -- including one the principal's own `resolve` just granted. Unchanged by a
    rollback: rolling back is a return to this branch, not a NEW failure mode.
  * **UNAFFECTED.** Every other function's served behaviour (0 of 9 other roots' plans show any
    change, confirmed above); `directory/handler.py`'s own `search`/`resolve` route (its
    `load_directory`/`lambda_handler` two-step is UNEDITED by this act); every other route on the
    28 existing CloudFront behaviors and the API's other scoped routes (none reference this
    function's internals).

## ROLLBACK

Re-publish `irpt-holdings` at `CodeSha256` `uS+WBeNxiCkYU2pdGalaONZ74SvoWEiYx669KWYKQDA=` via
Terraform (`filename`/`source_code_hash` pinned to the pre-deploy zip, build-store
`VersionId=U4sKRs.HJ0Jc4Ik323Y0b.qY7LsWU2Pg`), never `aws lambda update-function-code`. Verified by
`served == CodeSha256` read back after rollback -- the same discriminator arm (e) will use to
verify the forward deploy once both halves are signed.

## WRITERS OF THE SERVED-BEHAVIOUR PROPERTY

`W = 1`. The ONLY writer of what `irpt-holdings` serves is a Lambda code deployment of its own zip
(`build-and-upload.sh` + this cell's `entry.py` edit). No API Gateway response caching is declared
on this route (`comp-find` this run over `infra/aws/terraform/investor-reporting` for
`cache_ttl|CachingEnabled|cache_enabled|cache_cluster`: 0 hits touching the holdings integration);
no CloudFront behavior override; no shared warm-cache construction in `entry.py`'s `Entry(...)`
call or in `snapshot.py` carries a second writer of the binding/serving decision this act changes.

## THE FORWARD-LOOKING-CRITERION BAR AND THE IDENTITY LINE PER ARM

Every claim above is bound to a CONTENT HASH read AT THE EVENT this run (`CodeSha256`, the built
`artifact_sha256`, the plan's `source_code_hash` before/after, the live pointer/ownership-map
reads, the packet's own `blob <hash>` below) -- none is a prediction of what a future build or
plan WILL show. Arm (e) (not run this pass) is the one arm that runs under the DEPLOYED ROLE AND
BYTES as the function's own identity; arms (a)-(c) here run under this worker's own identity
(`0.9.0_WK_IRPT_BCKEND~4`) against read-only AWS/Terraform state and the committed git object
store.

## EXPECTED OUTCOME, BOTH BRANCHES (READ FROM THE PRODUCER'S OWN RULE, PER RULE 5)

  * If both never-widen halves are SIGNED before this order's second pass: arm (d) applies the
    saved plan (`0 to destroy`, `1 to change`) from THIS packet's planfile under the arm-(d)
    SUBTRACTION gate, verifies `served == CodeSha256 == built`, and arm (e) proves a granted
    account reads a scope-resolved answer (or a real policy refusal with `firm_id`) under
    `irpt-holdings-role` -- never `FIRM_BINDING` with `firm_id` absent -- reusing
    `battery_ib_rtf_10.py`'s bounded-test-principal mechanism per this order's text.
  * If a half is REFUSED: no deploy occurs from this packet; `irpt-holdings` stays at `CodeSha256`
    `uS+WBeNxiCkYU2pdGalaONZ74SvoWEiYx669KWYKQDA=` (its current, pre-fix, wired-but-broken state);
    row `S100` stays open and this order stays open.

## VINTAGE

Written `0.9.0_WK_IRPT_BCKEND~4`, first pass, 2026-09-20, on worktree HEAD `8ba74b3130` before
this pass's own commit. This file's own `blob <hash>` (read via `git hash-object` after commit) is
what each half's sign-off names.
