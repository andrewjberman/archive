# NEVER-WIDEN SIGN-OFF PACKET -- IRPT_BCKEND.TO-IB-rtf-13

**THE DIRECTORY-SEARCH ZIP CARRIES ITS CONTRACT.** Cell `IB-rtf-13`, row `S103`. Worker
`0.9.0_WK_IRPT_BCKEND~1`. Written per CLAUDE.md Rule 5 (`NEVER move served output without
never-widen sign-off`) and this order's arm (c): a K-CODE + K-ENV packet on `irpt-directory-search`
carries its own never-widen halves, or it does not deploy.

This packet is the ACT's blast-radius description. It does not itself constitute a sign-off --
`2.0.0_SA_COO~B` (this project's issuer) and `1.0.0_SA_CTO` each sign their own half against the
`blob <hash>` this file carries at HEAD, per Rule 5's mechanism (`org/tier1_exec/<seat>/
deliverables/NEVER_WIDEN_SIGNOFF_{COO,CTO}_HALF_IRPT_BCKEND_IB-rtf-13_*.md`). **As of this pass
BOTH halves are ABSENT** (checked this run: `org/tier1_exec/2.0.0_SA_COO~B/deliverables/` and
`org/tier1_exec/1.0.0_SA_CTO/deliverables/` carry no file naming `rtf-13`) -- this order's arm (d)
does not run this pass; this packet is committed so the halves have something to sign against.

## THE ACT

Deploy `irpt-directory-search` with ONE new packaged member --
`contracts/DirectoryEntry.schema.json`, staged at build time from the COMMITTED, sha256-verified
blob of `docs/contracts/investor-reporting/v1/DirectoryEntry.schema.json` (pin
`6e764ef0aa48a01f922931d66413477a2eff05a4`, sha256
`7ed220ff87a787c6b596bcc66bc90a8a5a69fe2ec7da88e145207297011aab24`, 12967 bytes) -- plus ONE
Terraform environment line, `IRPT_CONTRACTS_DIR = "/var/task/contracts"`, on the `directory` root.
No other function's bytes are touched by this act; no other route deploys; no `_authz/`, `_scope/`,
`_ids/`, `directory/` SOURCE file is edited.

## THE KEY -- THE ONE SERVING FUNCTION'S BYTES

`N = 1`. Only `irpt-directory-search` gains this member; this order's arm (a) census (13 functions
x sites; battery `battery_ib_rtf_13.py`, output `IB-rtf-13_R70-AC1_battery_output.txt`) confirms no
other of the 7 serving functions' `staged_from`/`files[]` is touched by this act.

| # | function_name | prior `CodeSha256` (rollback target, read live this run) | LastModified (live) |
|---|----------------|------------------------------------------------------------|----------------------|
| 1 | irpt-directory-search | `PUjH3OjDe8Yj3RwdIO0KT3GXsYGfvUCmzG/aHsi6e1c=` | 2026-09-19T17:15:28Z |

Read via `.tools/aws.cmd lambda get-function-configuration --function-name irpt-directory-search
--query "{CodeSha256:CodeSha256,LastModified:LastModified}"`, this run, 2026-09-19. **This matches
the face's own citation of the prior live value verbatim** (`PUjH3OjD...`), confirming this is the
same running byte the order was cut against. The ROLLBACK is "re-publish this exact `CodeSha256`"
(Terraform `filename`/`source_code_hash` pinned back to the pre-deploy zip; NEVER `aws lambda
update-function-code`, per CLAUDE.md NEVER-9). The build-store rollback source (the S3 object
version under `investor-reporting/irpt-directory-search.zip` at the moment BEFORE this order's
build ran) is `VersionId=elK9Z3qtolvKrVJhSuMrmlFJZT.77_Dk`, `LastModified=2026-09-19T18:54:54Z`,
read via `.tools/aws.cmd s3api list-object-versions` this run.

**BUILT THIS RUN** (K-CODE): `CodeSha256`/`artifact_sha256` `76LeVyYNfhdyDnQNXR3LzrqSv7k7Vr3POSjpcBzww6E=`,
128K, via `infra/aws/lambda/ci/build-and-upload.sh investor-reporting irpt-directory-search`.
**VERIFIED AT REST**: the built zip downloaded from S3 and re-hashed matches the declared
`artifact_sha256` (`match=True`); 13 of 13 declared members are byte-equal to their declared blob
(the pinned commit for a `staged_from` member, HEAD `19ccf82226` for a directly-tracked one) --
**never the working file** (this box has `core.autocrlf=true`). The served-byte delta against the
prior 12-member set is EXACTLY the one added member,
`['contracts/DirectoryEntry.schema.json']` -- `m = 1` of 1. `import-closure`: 9 of 9 packaged `.py`
files' top-level imports satisfied by package/stdlib/runtime/layer.

**TERRAFORM PLAN, DIRECTORY ROOT** (this run, vendored `.tools/terraform.exe`, saved to
`.scratch/ib_rtf_13_directory.tfplan`, canonical digest of the saved planfile
`sha256:fda208df40d62efe19658c12256e00df61aa07a36d85aa8717380c6d63c5b111`): **`Plan: 0 to add, 1 to
change, 0 to destroy.`** `terraform show -json` on the saved plan: `module.irpt_directory_search
.aws_lambda_function.this` -- `before.source_code_hash = PUjH3OjD...` (== the prior live
`CodeSha256` above), `after.source_code_hash = 76LeVyYN...` (== the built sha above), `actions =
["update"]`. `module.irpt_directory_refresh.aws_lambda_function.this` (the SAME root's other
resource) -- `before == after`, `actions = ["no-op"]`: the refresh function is genuinely untouched
by this act despite sharing this root.

**THE OTHER SIX ROOTS RE-TAKEN** (this run, same binary, no apply): `export`, `holdings`,
`intake`, `narrative`, `ops`, `performance` each read **`No changes. Your infrastructure matches
the configuration.`** -- 0 to add, 0 to change, 0 to destroy on every one. No plan noise this pass
(the rtf-12-class artifact drift the round-6 face names elsewhere is not reproduced here).

## THE CONTRACT DESCRIBED

`DirectoryEntry.schema.json`: a JSON Schema document (`$schema:
https://json-schema.org/draft/2020-12/schema`), 12967 bytes, 9 top-level `properties` (excluding
`contract_version`). Zero credential fields; zero secrets; zero PII beyond what a DirectoryEntry
document already legitimately carries in the projected response it types (this member is the
SCHEMA, not data). Writers of this file at its repo path: the L4 PRD/contract-authoring track only
(`docs/contracts/investor-reporting/v1/`) -- this order does not edit it, only stages a build-time
copy of the committed blob.

## THE BLAST RADIUS -- BOTH BRANCHES

**`irpt-directory-search` IS DEPLOYED UNWIRED** (its own `lambda.tf`: "no API route, no CloudFront
behavior ... point at it here"; confirmed this run -- `infra/aws/terraform/investor-reporting/api/
routes.json` and `api/routes.tf` carry no reference to `irpt_directory_search` or a `directory`
route). **So the blast radius of this act, TODAY, is direct-invoke only** -- no portal request
reaches this function through any wired route; the exposure is bounded to whoever invokes the
function directly (a battery, an operator diagnostic, or a future route once IB-s-15 wires one).

  * **INVOKED, WITH the member and the env (forward branch).** `directory/entry.py:74-83`
    `_document_fields()` finds `contracts/DirectoryEntry.schema.json` under `IRPT_CONTRACTS_DIR`
    (`/var/task/contracts`), reads the 9 declared properties, and `search()`/`resolve()` answer BY
    POLICY -- a projected document set (whole-entry, partial-entry withheld and counted under
    `status`), or a refusal on the declared reason codes (`UNPROJECTED_GRANT`, `EMPTY_GRANT`,
    `INVALID_INPUT`) -- never `RuntimeError: BLOCKED` for this cause. This is row `S103`'s fix.
  * **INVOKED, WITHOUT the member (as today, the negative control / rollback state).** The same
    call raises `RuntimeError: BLOCKED: the DirectoryEntry contract is not readable from this
    runtime`, uncaught by `entry.py`'s own `search()`/`resolve()` (no `try`/`except` around
    `_document_fields()` there) -- this propagates to `_authz`'s dispatcher, which is why the
    class shows as `UNEXPECTED` at the boundary rather than a declared policy reason. Unchanged by
    a rollback: rolling back is a return to this branch, not a NEW failure mode.
  * **UNAFFECTED.** Every other function's served behavior (0 of 6 other functions' manifests
    touched, confirmed by arm (a)'s cross-check and the 6-roots "No changes" plan); the `directory`
    root's OTHER resource, `irpt-directory-refresh` (confirmed `no-op` in the same plan); the 28
    existing CloudFront behaviors and 14 pre-existing scoped routes (none reference this function).

## ROLLBACK

Re-publish `irpt-directory-search` at `CodeSha256` `PUjH3OjDe8Yj3RwdIO0KT3GXsYGfvUCmzG/aHsi6e1c=`
via Terraform (`filename`/`source_code_hash` pinned to the pre-deploy zip, build-store
`VersionId=elK9Z3qtolvKrVJhSuMrmlFJZT.77_Dk`), never `aws lambda update-function-code`, and revert
`directory/lambda.tf`'s `IRPT_CONTRACTS_DIR` line. Verified by `served == CodeSha256` read back
after rollback, the same discriminator arm (e) will use to verify the forward deploy.

## WRITERS OF THE SERVED-BEHAVIOUR PROPERTY

`W = 1`. The ONLY writer of what `irpt-directory-search` serves is a Lambda code deployment of its
own zip (`build-and-upload.sh`, this cell's `staged_from` addition). `Grep` this run,
`cache_ttl|CachingEnabled|cache_enabled|cache_cluster` over
`infra/aws/terraform/investor-reporting`: 0 hits -- no API Gateway response caching on this
project's routes (moot today since this function has no route at all). No CloudFront behavior, no
Lambda@Edge, and no shared warm-cache construction in `entry.py`'s `Entry(...)` call carries a
second writer.

## THE FORWARD-LOOKING-CRITERION BAR AND THE IDENTITY LINE PER ARM

Every claim above is bound to a CONTENT HASH read AT THE EVENT this run (`CodeSha256`, the built
`artifact_sha256`, the plan's `source_code_hash` before/after, the packet's own `blob <hash>`
below) -- none is a prediction of what a future build or plan WILL show. Arm (e) (not run this
pass) is the one arm that runs under the DEPLOYED ROLE AND BYTES as the function's own identity;
arms (a)-(c) here run under this worker's own identity (`0.9.0_WK_IRPT_BCKEND~1`) against read-only
AWS/Terraform state and the committed git object store.

## EXPECTED OUTCOME, BOTH BRANCHES (READ FROM THE PRODUCER'S OWN RULE, PER RULE 5)

  * If both never-widen halves are SIGNED before this order's second pass: arm (d) applies the
    saved plan (`0 to destroy`, `1 to change`) from THIS packet's planfile, verifies `served ==
    CodeSha256 == built`, and arm (e) proves search/resolve answer by policy under
    `irpt-directory-role` with `0` UNEXPECTED for the exercised firm.
  * If a half is REFUSED: no deploy occurs from this packet; `irpt-directory-search` stays at
    `CodeSha256` `PUjH3OjDe8Yj3RwdIO0KT3GXsYGfvUCmzG/aHsi6e1c=` (its current, pre-fix, unwired
    state); row `S103` stays open and this order stays open.

## VINTAGE

Written `0.9.0_WK_IRPT_BCKEND~1`, first pass, 2026-09-19, on worktree HEAD `19ccf82226963ef06605c
ed97daa01ebcfdee85c` after the manifest+env commit. This file's own `blob <hash>` (read via `git
hash-object` after commit) is what each half's sign-off names.
