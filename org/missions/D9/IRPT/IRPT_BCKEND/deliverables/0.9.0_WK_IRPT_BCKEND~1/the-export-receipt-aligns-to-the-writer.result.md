# RESULT -- IRPT_BCKEND.TO-IB-rtg-1, second pass (arms (d) + (e))

**Worker:** `0.9.0_WK_IRPT_BCKEND~1` · **Branch:** `wk-irpt_bckend-7-1-apply` · **Run:** 2026-09-20/21

## PLUGIN CACHE

Option (c), PRIVATE: `TF_PLUGIN_CACHE_DIR=/c/tmp/tf-cache-irpt-rtg7` (pre-existing, ~704 MB,
populated). Set before every `terraform init` across all 10 roots. No re-download observed;
`df -h /c` moved from ~31 GB free (start) to ~22-23 GB free after the 10-root init+plan sweep
(the plan-time per-root `.terraform/providers` copy on this box, consistent with the task
order's ~686 MB/root estimate), stabilizing at 22 GB after the export apply. The fallback
(deleting non-applied roots' `.terraform/providers` after saving their plan) was NOT needed --
free space stayed above the ~8 GB threshold throughout.

## ARM (d) -- APPLY

Pre-apply re-verify: packet blob `74a1004fde6e649c321f43d62cfbda5b61489b98` at HEAD == both
halves' named blob == the packet's own worktree hash-object; built artifact `head-object`
confirmed `cn8YKEP2oQdfvAjdpa32Wfp9oJqhAIMGkECv+H4vUg4=` at rest (and consistent across the four
most recent object versions in the bucket, since a sibling process re-uploaded the same bytes
after the packet was written -- content hash unchanged). Live `CodeSha256` read
`9IMayS94if11cyKq51TbcyBG8cUwbbUWlQMlT9XhiaQ=`, matching the packet's rollback target; the
build-store rollback version `dECFEZtZArSJYdPy4.ImeVHBv6Q.jxBH` verified at rest to carry that
exact sha.

Change-management ledger `irpt-bckend-ib-rtg-1-export-apply` OPENED before the apply (commit
`b2b2912e91`), CLOSED after verification (commit `0330c5b79c`).

Fresh 10-root plan (private plugin cache), subtraction gate: **132 entries compared, 0 paths
subtracted** (no `data.aws_s3_object` version drift this run). Export root: exactly 2 real
changes after subtraction -- `aws_iam_role_policy.export_render_receipt` `["create"]` and
`module.irpt_export_render.aws_lambda_function.this` `["update"]`
(`9IMayS94if11cyKq51TbcyBG8cUwbbUWlQMlT9XhiaQ=` -> `cn8YKEP2oQdfvAjdpa32Wfp9oJqhAIMGkECv+H4vUg4=`)
-- matching the packet's declared set exactly. The 3 sibling round-7 roots (holdings, ops,
performance) and the 6 non-round-7 roots (api, core, directory, intake, narrative, ycharts) all
read EMPTY after subtraction -- already applied+drained; no pending sibling round-7 roots
remain; this was round 7's last apply.

`safe-apply.sh` on the export root's saved plan required `HALT_ACK=1` (25 pending general-fabric
messages, none naming this act/export/irpt-export-render/IB-rtg-1 -- reviewed individually).
`Apply complete! Resources: 1 added, 1 changed, 0 destroyed.` Post-apply re-plan: `rc=0`,
`No changes.` Served `CodeSha256` read back == `cn8YKEP2oQdfvAjdpa32Wfp9oJqhAIMGkECv+H4vUg4=`.
IAM policy `irpt-export-render-receipt-policy` read back via `get-role-policy`: exactly the two
statements the packet declares (`ReadWriteExportReceiptOnly` GetObject+PutObject,
`ListOnlyTheReceiptAddresses` ListBucket, both pinned to `firms/*/generations/EXP-*/receipt.json`).

## ARM (e) -- PROVEN LIVE

`battery_ib_rtg_1.py` written to reuse the bounded-principal mechanism of
`battery_ib_rtf_10.py` (K1/K1b DynamoDB, real login, real HTTP, full delete lifecycle incl.
refresh-refusal and post-exp 401), graded on the EXERCISABLE SUBSTANCE per the disclosed
partial (row `IRPT_BCKEND-W1-S43`): the deployed `submit_export` still raises
`NOT_READY` unconditionally, so the served `submit -> receipt` round trip through `POST /export`
cannot be exercised end-to-end -- confirmed live in this run (`POST /export -> POLICY http 200
code NOT_READY`, disclosed, not counted).

Graded instead: (1) KEY ALIGNMENT -- `export/identity.py`, `export/handler.py` and
`export/entry.py` imported as real production code (a module-name collision guard added: the
sibling `export/handler.py`'s own `sys.path.insert(0, .../directory)` shadows `export/entry.py`
with `directory/entry.py` for any `import entry` issued AFTER `handler` -- both dirs carry an
`entry.py` -- so `entry`/`identity`/`handler`/`receipt` are imported in a fixed, asserted order
at module load, before any function can trigger the shadow); a real `export_id` was minted via
`identity.identity_for()`, and the writer's key (`handler.receipt_key()`) equaled the reader's
key (`entry.RECEIPT_KEY_TEMPLATE.format(...)`) -- both EXACT to
`firms/49financial/generations/EXP-.../receipt.json`. (2) A receipt built via the real
`receipt.build()` was persisted at that exact address via the real `handler.persist_receipt()`
(this worker's own S3 credentials, standing in for the deployed submit path per the disclosed
partial). (3) A fresh bounded test principal (epoch `1789957994`) logged in for real. (4) A real
HTTP `GET /api/scoped/investor-reporting/export/{exportId}` through the deployed route, under
`irpt-export-render`'s own execution role `irpt-export-render-role`, returned `SERVED` with the
just-written receipt (`export_id` and `artifact.sha256` matched what was persisted) -- no
`NOT_FOUND`. (5) Taxonomy on two REAL wire errors, never a constructed `ClientError` stub: (a)
an export id outside the new IAM grant's `EXP-*` resource pattern produced a real S3 403
`AccessDenied` from the deployed role, and the route answered `NOT_FOUND` (not `UNEXPECTED` --
this is the exact S106 fix); (b) a real `EXP-*` id the grant allows but that was never written
produced a real S3 404 `NoSuchKey`, and the route again answered `NOT_FOUND` (the
pre-existing-correct case, proven still correct). (6) Rollback: the test receipt object, K1b
and K1 all deleted and verified gone; the issued refresh token refused; the access token refused
(401) after its `exp`; a post-rollback prefix scan found 0 residue in all three tables.

`IB-rtg-1_R72-AC1_battery_output.txt` sha256
`7f9d663331f8bbc41b30ea76c142b964f3562599c78952f8acd1eef303200868`. 8 of 8 arms PASS, 0
UNEXPECTED. Token `IBR72-EXPORT-RECEIPT-ALIGNED-AND-TAXONOMY-BY-CODE` printed -> R72-AC1
PASS-by-output.

## ENDPOINT CONSEQUENCE (carried, not resolved here)

Per both never-widen halves: FWD-2's export leg does NOT fully realize this round -- the
submit-wiring (`entry.py`'s `submit_export` -> `handler.py`) is a named follow-on cell for
round 8 or the round-7 analysis, out of this order's BOUNDS. Not a rider on this order.
