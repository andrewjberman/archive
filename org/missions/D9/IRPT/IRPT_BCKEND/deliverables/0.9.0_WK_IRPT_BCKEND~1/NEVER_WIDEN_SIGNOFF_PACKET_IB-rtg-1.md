# NEVER-WIDEN SIGN-OFF PACKET -- IRPT_BCKEND.TO-IB-rtg-1

**THE EXPORT RECEIPT ALIGNS TO THE WRITER AND THE TAXONOMY TESTS THE CODE.** Cell `IB-rtg-1`,
rows `S105`+`S106` (ONE cell per the CTO ruling @0110b9de01 -- do NOT split). Worker
`0.9.0_WK_IRPT_BCKEND~1`. Written per CLAUDE.md Rule 5 (`NEVER move served output without
never-widen sign-off`) and this order's arm (c).

This packet is the ACT's blast-radius description. It does not itself constitute a sign-off --
`2.0.0_SA_COO~B` (this project's issuer) and `1.0.0_SA_CTO` each sign their own half against the
`blob <hash>` this file carries at HEAD, per Rule 5's mechanism (`org/tier1_exec/<seat>/
deliverables/NEVER_WIDEN_SIGNOFF_{COO,CTO}_HALF_IRPT_BCKEND_IB-rtg-1_*.md`). **AS OF THIS PASS BOTH
HALVES ARE ABSENT** (checked this run: `org/tier1_exec/2.0.0_SA_COO~B/deliverables/` has no
directory/file, `org/tier1_exec/1.0.0_SA_CTO/deliverables/` and a repo-wide
`**/*IB-rtg-1*` glob return only this order's own task-order file and this worker's own
deliverables) -- this order's arm (d)/(e) do NOT run this pass; this packet is committed so the
halves have something to sign against. **This is the order's own stated expected first-pass
outcome.**

## THE ACT

Two source edits on `irpt-export-render` (handler `entry.lambda_handler`), ONE cell:

  1. **S106** -- `export/entry.py`'s `_load_receipt` except-clause now decides refusal off the
     modeled S3 error CODE (`isinstance(exc, botocore.exceptions.ClientError)` then
     `exc.response["Error"]["Code"] in ("NoSuchKey", "AccessDenied", "NoSuchBucket")`), never the
     exception CLASS NAME. A genuinely unclassified `ClientError` code or a non-`ClientError`
     exception still propagates.
  2. **S105** -- `RECEIPT_KEY_TEMPLATE` realigned from `investor-reporting/export/{firm}/
     {export_id}/receipt.json` (outside every declared prefix family, matched 0 of 7 GetObject
     ARNs, `KeyCount 0`) to `firms/{firm}/generations/{export_id}/receipt.json` -- the DECLARED
     `generations` family, addressed by the one opaque token (`export_id`) the route's caller and
     writer both hold. `handler.py` gains `receipt_key()` (the identical builder) and
     `persist_receipt()` (write + read-back, the same shape `persist_bundle()` already proves),
     wired into `finalize_export(..., persist=True)` -- Step 7 of this module's own header
     ("the artifact VALIDATED and the receipt WRITTEN"), which never actually wrote one before this
     cell. **See row `IRPT_BCKEND-W1-S42`: the literal deeper family the order's prose names
     (matching the bundle's own `generations/<gen>/attempts/<a>/exports/<rev>/` directory) is NOT
     reconstructable by this route from `(firm, export_id)` alone -- this is the nearest workable,
     measured substitute, and the signers should read that row before signing.**

No Terraform `IRPT_EXPORT_RECEIPT_KEY` override (ruling REFUSED). No other function's bytes.

**PLUS ONE NECESSARY, MEASURED COMPANION FIX**, not itself S105/S106's remedy (filed as row
`IRPT_BCKEND-W1-S44`, already disarmed this commit): `infra/aws/lambda/ci/lambda-source-map.json`'s
`irpt-export-render` entry never packaged `keys.py`, so `handler.py`'s PRE-EXISTING
`bundle_key()`/`artifact_key()` (and this cell's new `receipt_key()`) would `ImportError` at
runtime. `keys.py` is added to both `files[]` and `staged_from[]`, staged from the SAME
`_keys/keys.py` blob (pin `6e764ef0aa48a01f922931d66413477a2eff05a4`, sha256
`56ee3cc22e802579ebb8d4cba53edec8045603396a48fe952d6b83df0f08ab2a`) the four sibling
investor-reporting functions already stage -- verified byte-identical to this worktree's current
`_keys/keys.py` before adding it.

**PLUS ONE NEW, NARROW IAM GRANT** on the export function's OWN role (`irpt-export-render-role`),
never the bucket, never a firm's whole prefix -- see "THE NEW GRANT" below.

## THE KEY -- THE ONE SERVING FUNCTION'S BYTES

`N = 1`. Only `irpt-export-render` gains new bytes.

| # | function_name | prior `CodeSha256` (rollback target, read live this run) | LastModified (live) |
|---|----------------|------------------------------------------------------------|----------------------|
| 1 | irpt-export-render | `9IMayS94if11cyKq51TbcyBG8cUwbbUWlQMlT9XhiaQ=` | 2026-09-19T17:20:04.000+0000 |

Read via `.tools/aws lambda get-function-configuration --function-name irpt-export-render --query
"{CodeSha256:CodeSha256,LastModified:LastModified,Version:Version,Handler:Handler}"`, this run,
2026-09-20. `Handler` confirmed `entry.lambda_handler`, `Version` `$LATEST`. ROLLBACK is
"re-publish this exact `CodeSha256`" (Terraform `source_code_hash`/`s3_object_version` pinned back;
NEVER `aws lambda update-function-code`, per CLAUDE.md NEVER-9). The build-store rollback source
(the S3 object version under `investor-reporting/irpt-export-render.zip` immediately BEFORE this
order's build ran) is `VersionId=dECFEZtZArSJYdPy4.ImeVHBv6Q.jxBH`,
`LastModified=2026-09-19T15:58:35Z` -- **VERIFIED AT REST this run**: `head-object` on that version
reads `Metadata.content-sha256 = 9IMayS94if11cyKq51TbcyBG8cUwbbUWlQMlT9XhiaQ=`, an EXACT match to
the live `CodeSha256` above (`.tools/aws s3api list-object-versions` + `head-object`, this run).

**BUILT THIS RUN** (K-CODE): `CodeSha256`/`artifact_sha256`
`cn8YKEP2oQdfvAjdpa32Wfp9oJqhAIMGkECv+H4vUg4=`, 156K (157997 bytes), via
`infra/aws/lambda/ci/build-and-upload.sh investor-reporting irpt-export-render`. **VERIFIED AT
REST**: the S3 object this build produced, `VersionId=xOvsKB19MIqM7gB3caGQaw768tmTYtc3`
(`LastModified=2026-09-20T15:23:42Z`), read back via `head-object` this run: `Metadata.content-sha256
= cn8YKEP2oQdfvAjdpa32Wfp9oJqhAIMGkECv+H4vUg4=` (matches the build's own report) and
`ContentLength = 157997` (matches). Build script's own report: `OK: import-closure -- 18 packaged
.py file(s), every top-level import satisfied by package/stdlib/runtime/layer.`

**THE SERVED-BYTE DELTA, EXACTLY THE EDITED MEMBERS** -- both zips downloaded this run
(prior version `dECFEZtZArSJYdPy4.ImeVHBv6Q.jxBH` vs new version
`xOvsKB19MIqM7gB3caGQaw768tmTYtc3`), unpacked, every member sha256'd and diffed:

```
ADDED:   ['keys.py']
REMOVED: []
CHANGED: ['entry.py', 'handler.py']
total old files: 19   total new files: 20
```

`m = 3` of 20 packaged members touched: the two edited (`entry.py`, `handler.py`) plus the one
necessary companion (`keys.py`, row `W1-S44`) -- nothing else.

## THE NEW GRANT -- `aws_iam_role_policy.export_render_receipt`

The ALIGNED receipt address, `firms/<firm>/generations/<export_id>/receipt.json`, does **NOT**
match the role's existing `export_render_evidence` grant (`firms/*/generations/*/attempts/*/
exports/*` -- requires the literal `attempts`/`exports` segments the shallow receipt address
deliberately omits). Proven this run (Python `fnmatch`, the same `*`-across-`/` semantics IAM's own
resource matching uses):

```
firms/49financial/generations/EXP-aaaa/receipt.json  vs  firms/*/generations/*/attempts/*/exports/*  -> False
```

So this cell adds its OWN statement, `ReadWriteExportReceiptOnly` (GetObject+PutObject) +
`ListOnlyTheReceiptAddresses` (ListBucket, prefix-conditioned), on the SAME role, for this ONE new
address only.

**MEASURED, NOT ASSUMED, AND TIGHTENED BEFORE IT EVER LANDED**: a bare `firms/*/generations/*/
receipt.json` resource was the first draft, and this run's own `fnmatch` check showed it ALSO
matches `ycharts/generate/job.py:324-325`'s DIFFERENT, DEEPER receipt shape
(`firms/<firm>/generations/<request_id>/attempts/<revision>/receipt.json`, cell B9/IB-s-9's OWN
generation job, under the SAME `generations` family) -- a genuine, measured over-grant this role has
no business holding. The resource is pinned instead to the `EXP-` NAMESPACE
(`firms/*/generations/EXP-*/receipt.json`), a SHAPE `export/identity.py`'s `EXPORT_NAMESPACE`
mints and nothing else in the corpus does (per `_keys.OPAQUE_ID_RE`), proven this run to admit every
`export_id` this cell's own writer mints while excluding the ycharts shape and the bundle/artifact
deep shape:

```
firms/49financial/generations/EXP-aaaa/receipt.json                        -> True   (this cell's own shape)
firms/49financial/generations/REQ123/attempts/7/receipt.json               -> False  (ycharts job.py's shape)
firms/49financial/generations/GEN-1/attempts/1/exports/r1/bundle.json      -> False  (the bundle/artifact shape)
```

`terraform fmt -check` clean on the edited file; `terraform validate` (local, `-backend=false`)
Success both before and after the tightening.

## TERRAFORM PLAN, EXPORT ROOT (real backend, this run)

Saved to `.scratch/ib_rtg1_export.tfplan`
(sha256 `f67dd37bb29d5089c65e35e4d5ee647669aff1362684dd5cc79f1c283c2eef70`, NOT committed --
`.scratch/` is this worker's own scratch, per CLAUDE.md; a fresh plan is regenerated at arm (d)
per the W1-S37 lesson, this one is evidence for THIS packet only). `terraform show -json` on the
saved plan, `resource_changes` array read (W1-S37 subtraction gate): **11 entries total, 9 `no-op`,
2 real** -- `aws_iam_role_policy.export_render_receipt` `["create"]` and
`module.irpt_export_render.aws_lambda_function.this` `["update"]` (`source_code_hash`:
`9IMayS94if11cyKq51TbcyBG8cUwbbUWlQMlT9XhiaQ=` -> `cn8YKEP2oQdfvAjdpa32Wfp9oJqhAIMGkECv+H4vUg4=`;
`s3_object_version`: `dECFEZtZArSJYdPy4.ImeVHBv6Q.jxBH` -> `xOvsKB19MIqM7gB3caGQaw768tmTYtc3`).
`Plan: 1 to add, 1 to change, 0 to destroy.` Nothing outside the subtraction set (no
`data.aws_s3_object` volatile field) appears on either changed resource beyond the fields named
above plus `last_modified` (`known after apply`, a Lambda-managed timestamp).

**THE OTHER NINE ROOTS RE-TAKEN** (this run, same binary, real backend, no apply):
`directory`, `intake`, `narrative`, `ycharts`, `core`, `api` each read **`No changes. Your
infrastructure matches the configuration.`** `holdings`, `ops`, `performance` each showed exactly
ONE Lambda function update (their OWN function -- `module.irpt_holdings...`,
`module.irpt_status...`, `module.irpt_performance_adapter...` respectively; `source_code_hash`/
`s3_object_version` only) and **NOTHING TOUCHING THE EXPORT FUNCTION, THIS ROOT, OR THIS ROLE**.
**This is NOT an effect of this order's edits** (`git status` this worktree: only `export/iam.tf`
modified; no holdings/ops/performance source touched) -- it is round 7's OTHER THREE cells
(`IB-rtg-2`/`3`/`4`) independently running their own `build-and-upload.sh` in their own worktrees
during this same window, visible here because the artifact bucket is shared AWS state, not
worktree-isolated. **Filed as row `IRPT_BCKEND-W1-S45`** so a reader of this "other roots" section
does not mistake sibling in-flight work for a defect of this act.

## THE BLAST RADIUS -- BOTH BRANCHES

  * **APPLIED, WITH the fix (forward branch).** A denied `GetObject` on the aligned receipt
    address (e.g. IAM/bucket-policy `AccessDenied`, or a genuinely absent `NoSuchKey`) now serves
    `ExportRefused` / public reason `NOT_FOUND` -- a policy-shaped answer -- instead of propagating
    to `UNEXPECTED` (S106). A `submit-export` call that reaches `handler.py`'s `finalize_export`
    (see row `W1-S43` -- it currently CANNOT, on the deployed function) would persist a receipt at
    the SAME address the aligned reader computes, so a subsequent `export-receipt` read for that
    `export_id` would return the just-written receipt rather than `NOT_FOUND`.
  * **APPLIED, WITHOUT ever reaching `submit-export`'s controller (today's actual live shape, per
    row `W1-S43`).** No receipt is ever written by the deployed function regardless of this fix
    (entry.py's own wired `submit_export` unconditionally raises `NOT_READY`), so an
    `export-receipt` read stays `NOT_FOUND` for every `export_id` -- but now for the HONEST reason
    (truly nothing has been written at the aligned address) rather than the OLD dishonest one (the
    address itself was outside the declared layout and the role's grant).
  * **NOT APPLIED (rollback / current live state).** Unchanged from today: the OLD address (outside
    every declared family, 0 of 7 GetObject ARNs matched) and the OLD class-name taxonomy (a denial
    reads `UNEXPECTED`) both persist.
  * **UNAFFECTED.** Every other function's served behavior (0 of 9 other roots' OWN state touched
    by this act, confirmed above); the role's three pre-existing grants (`export_render_evidence`,
    `export_render_dispatch`, `export_render_ownership_map`/`export_render_directory_read`) are
    untouched (plan shows them `no-op`); the render host's IAM (`render_host_export_evidence`, a
    different root's resource).

## ROLLBACK

Re-publish `irpt-export-render` at `CodeSha256` `9IMayS94if11cyKq51TbcyBG8cUwbbUWlQMlT9XhiaQ=` via
Terraform (`source_code_hash`/`s3_object_version` pinned to the pre-deploy zip, build-store
`VersionId=dECFEZtZArSJYdPy4.ImeVHBv6Q.jxBH`), never `aws lambda update-function-code`, and remove
`aws_iam_role_policy.export_render_receipt` (additive and reversible: deleting it returns the role
to exactly its pre-this-cell grant set). Verified by `served CodeSha256 == 9IMayS94...` read back
after rollback, the same discriminator arm (e) would use to verify the forward deploy.

## WRITERS OF THE SERVED PROPERTY

The property served at the aligned address (`firms/<firm>/generations/<export_id>/receipt.json`):
**`W = 1`** -- `handler.py`'s `persist_receipt()`, called only from `finalize_export(persist=True)`,
this cell's own new code. **`R = 1`** -- `entry.py`'s `_load_receipt()`, this cell's own edited
code. No other writer in the corpus produces THIS address: the broader "receipt.json" census S105
already ran (3 sites: `ycharts/generate/job.py:324-326,477-479`, `intake/poller.py:418-420`) all
build a DIFFERENT, deeper shape under the same `generations` family (proven non-colliding with the
`EXP-`-pinned grant above, this run). The `44/19` ownership/relationship re-derive constraint
(s.R7.3) does **NOT APPLY to this cell**: neither S105 nor S106 reads, asserts, or serves any
account/relationship count -- this fix is S3-address and exception-taxonomy only. Confirmed nothing
was inherited: a guessed ownership-map location (`opal-data-ycharts/platinum/49financial/
ownership_map.json`) returned `NoSuchKey` this run, and no `33/18`-or-`44/19`-shaped number appears
anywhere in this packet's own evidence.

## THE FORWARD-LOOKING-CRITERION BAR AND THE IDENTITY LINE PER ARM

Every claim above is bound to a CONTENT HASH read AT THE EVENT this run (`CodeSha256`, the built
`artifact_sha256`, the plan's `source_code_hash`/`s3_object_version` before/after, the byte-diff's
ADDED/REMOVED/CHANGED sets, this packet's own `blob <hash>` below) -- none is a prediction of what a
future build or plan WILL show. Arm (e) (NOT run this pass, and per row `W1-S43`, cannot pass on the
deployed path even after arm (d) applies this packet, until a further cell wires
`entry.py`'s `submit_export` to `handler.py`'s) is the one arm that runs under the DEPLOYED ROLE AND
BYTES as the function's own identity (`irpt-export-render-role`); arms (a)-(c) here run under this
worker's own identity (`0.9.0_WK_IRPT_BCKEND~1`) against read-only AWS/Terraform state and the
committed git object store.

## EXPECTED OUTCOME, BOTH BRANCHES (READ FROM THE PRODUCER'S OWN RULE, PER RULE 5)

  * If both never-widen halves are SIGNED before this order's next pass: arm (d) generates a FRESH
    plan (not this packet's saved one, per the W1-S37 lesson) against the export root, applies it,
    verifies `served == CodeSha256 == built (cn8YKEP2oQdfvAjdpa32Wfp9oJqhAIMGkECv+H4vUg4=)`, and arm
    (e) is attempted -- and, per row `W1-S43`, is EXPECTED to still show `NOT_READY` on
    `submit-export` until that row's blocker is separately closed; R72-AC1 stays open on that half
    even after a clean apply, and this is named here so a later pass is not surprised by it.
  * If a half is REFUSED: no deploy occurs from this packet; `irpt-export-render` stays at
    `CodeSha256` `9IMayS94if11cyKq51TbcyBG8cUwbbUWlQMlT9XhiaQ=` (its current, pre-fix state); rows
    `S105`/`S106` stay `ARMED`/`UNDER_INVESTIGATION` and this order stays open.

## VINTAGE

Written `0.9.0_WK_IRPT_BCKEND~1`, first pass, 2026-09-20, on worktree branch
`wk-irpt_bckend-7-1` after the source-edit + manifest + IAM commit. This file's own `blob <hash>`
(read via `git hash-object` after commit) is what each half's sign-off names.
