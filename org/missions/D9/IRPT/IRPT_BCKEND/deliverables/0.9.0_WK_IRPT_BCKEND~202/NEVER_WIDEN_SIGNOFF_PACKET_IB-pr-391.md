# Never-widen sign-off packet -- IB-pr-391: release packet for IB-pr-386 -- the NEW function `irpt-commentary-composition-read-lambda` (the svc-commentary composition read), nothing existing moves

Prepared by 0.9.0_WK_IRPT_BCKEND~202 for 2.0.0_SA_COO~P2 / 1.0.0_SA_CTO (CTO msg 2507 (b)). Nothing here was uploaded, deployed, applied or run against a live write: BUILD_ONLY from a clean tree, offline replays, AWS reads only.
Files beside this packet: `IB97-4_release_census.json`, `IB97-4_release_replay.json`, `IB97-4_source_map_entry.json` (the entry the pair registers), `replay/` (the scripts). Model: `../0.9.0_WK_IRPT_BCKEND~189/NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-380_381.md`.

**READ THIS FIRST (rows IRPT_BCKEND-D2-W202-S1 and -S2, both INERT).**
(1) The function has NO row in `infra/aws/lambda/ci/lambda-source-map.json`, so `release-census.py` exits 2 for it and the builder cannot build it from the committed map (row W197-S2 left the registration to the pair). The sha256 below is of a build from a scratch copy of the map plus ONE drafted entry
(`IB97-4_source_map_entry.json`, 16 members), with `BAU_PARITY_SKIP=1` because `source_dir` is the shared `reports/` package. The pair must register exactly that entry and build with the parity skip, or any other member set builds a different sha256.
(2) The IB-pr-386 change to `repository.py` and `retention.py` reaches NO existing function at the pin: the four functions that package `reports/repository.py` stage it from older pinned blobs, so the census of "existing functions whose repository.py changed" is empty. This release changes the served bytes of nobody.

## The pin and the artifact

- **Release pin P: `9c995243f7c41d0850024a451b71a4536d6dd91e`** (the worktree HEAD of branch `wk-IRPT_BCKEND-202`: the issuance merge `ae687597ec` on box/dell2). IB-pr-386's code commit `20534db618` is an ancestor; it is the owner of three members (`commentary_composition.py`, `repository.py`, `retention.py`).
- **Artifact `irpt-commentary-composition-read-lambda`** (python3.12, handler `commentary_composition.lambda_handler`, no layer, S3 key `investor-reporting/irpt-commentary-composition-read-lambda.zip`):
  - **Built sha256 `ZZmWOFSA/GjO0d/cKHSm9G5+xDc5sNfEHOpbmfIabQ0=`** (hex `659996385480fc68ced1dfdc2874a6f46e7ec43739b0d7c41cea5b99f21a6d0d`, 136,840 bytes, 16 members).
  - **live_before: `ABSENT`** (read live: `aws lambda get-function --function-name irpt-commentary-composition-read-lambda` -> ResourceNotFoundException). There is no prior CodeSha256 and no prior S3 object version; every member is "added".
  - Build: `BUILD_ONLY=1 BAU_PARITY_SKIP=1 BAU_SOURCE_MAP_OVERRIDE=<scratch copy of the map + the drafted entry> bash infra/aws/lambda/ci/build-and-upload.sh investor-reporting irpt-commentary-composition-read-lambda` rc 0, run TWICE from a porcelain-empty tree: byte-identical (same sha256 both times). Porcelain 0 lines after (the builder's staged empty directories under `reports/` were removed with `rmdir`; the kept zip lived in a scratch directory outside the worktree). Gates that ran: staged_from sha256 verification (12 rows), import-closure (8 packaged .py files). Gate skipped: ADHC_DRIFTD.002 parity (row S1).
  - Members and owners (full commits in the census file): `commentary_composition.py`, `repository.py`, `retention.py` by `20534db618` (IB-pr-386); `composition.py` `2aa217ec58`; `acceptance.py` `090c819803`; `submission.py` `03ea5980cc`; `keys.py` `48313e9c0e`; `lib/opal_naming.py` `e15671f611`; `org/standards/NAMING_SCHEMA.json` `eb29bf7f37`; the seven registry files `infra/logic/registry/{exemptions,remediations,reporting_policies,resources,scopes,systems,tiers}.json` at their last commits. The packaged registry resolves `irpt-x10-v1` ACTIVE and the `REQUEST_COMPOSITION` destination (checked in the flat import arm).
- **Existing functions whose packaged `reports/repository.py` changed: NONE.** Found by reading the map (229 functions, 4 stage `reports/repository.py`) and `release-census.py <fn> --pin P` for each: `irpt-export-render` 0 changed; `irpt-performance-adapter` 2 (`holdings_gold.py`, `loaders.py`); `irpt-ycharts-generate` 5 (`generate_installed.py` + 4 added custody modules); `irpt-status` 4 (`canonical_profile_reads.py`, `loaders.py`, `maintained_sources.py`, `served.py`). None is `repository.py` (staged pins `b905df2c60`, `605c4cd4ac`, `2aa217ec58`, `80a79a7462`; live repository.py sha256 prefixes `f255335beb26` and `f01fcf549e8e`). The other changed members are other cells' (IB-pr-385/387 hosts, custody and holdings work) and are NOT in this release. No bundle packages `reports/repository.py` (the runner bundle holds the gold scripts), so no bundle is censused.

## What the release does

A new invoke-only Lambda. Request `{tenant, request_ref}`; it reads `analysis#<id>#1` in the tenant partition, takes `composition_ref`, and calls `ArtifactRepository.get()` as the named service subject `svc-commentary` bound to that tenant (REQUEST_COMPOSITION only, read-only, retention check kept on both sides of the blob read). It returns the document with the two ownership members removed, the retained artifact's own `sha256` (the one the READY item's `composition_ref` carries; the returned JSON does not hash to it because the owner is stripped, row W197-S1) and a refusal code otherwise. No route, schedule, event source, alarm, SNS or SES.
DESIRED Terraform: `infra/aws/terraform/investor-reporting/export/commentary_composition.tf` -- role `irpt-commentary-composition-read-role` with ONE inline read-only policy (`dynamodb:GetItem` on irpt-requests with LeadingKeys = the served firms; `s3:GetObject`/`GetObjectVersion` on the REQUEST_COMPOSITION prefixes; `kms:Decrypt` via dynamodb and via s3 only; own log stream), log group, the function (module `irpt_commentary_composition_read`), and the caller's `irpt-commentary-composition-invoke-policy` (`lambda:InvokeFunction` on this one function).

## Writers of each changed property (the census, N printed)

1. **The set of service subjects and families (`SERVICE_READERS = {svc-commentary: REQUEST_COMPOSITION}` in `reports/repository.py`).** 1 writer: the constant itself (no registry or table row); a change is a code commit and a new zip. N rules read: 1. It ships in this one zip only.
2. **The function `irpt-commentary-composition-read-lambda` and its role/policies/log group.** 1 writer: `export/commentary_composition.tf` (module `irpt_commentary_composition_read`); no other `.tf` creates a resource of that name (the transcripts root names a different composition bucket variable). N: 1.
3. **The S3 key `investor-reporting/irpt-commentary-composition-read-lambda.zip`.** 1 writer: `build-and-upload.sh` (Terraform reads the key, never writes it). First mint: no prior object, so no prior version.
4. **The invoke grant on the function.** 0 writers today: the policy is created by the export root but attached to `outlook-global-commentary-draft-role` by NO root yet. 1 intended writer: the commentary (transcripts) root, its own pair. Until it lands the commentary role cannot call the function.
5. **The existing artifacts' `repository.py`/`retention.py` pins.** 4 rows in the source map, each staged from an older blob; this release re-pins none (row S2).

## Branch A (released)

Preconditions: IB-pr-383 closed (CTO msg 2507); `svc-commentary`'s sign-off pair amended by 2.0.0_SA_COO~V2 before the read deploys.
1. **Register the entry** in `infra/aws/lambda/ci/lambda-source-map.json` exactly as `IB97-4_source_map_entry.json` (16 `files[]`, 12 `staged_from` rows with their pins and sha256) in a commit; build without `BUILD_ONLY` and with `BAU_PARITY_SKIP=1` (or list the seven other `reports/*.py` modules, which would change the zip): the uploaded zip MUST show sha256 `ZZmWOFSA/GjO0d/cKHSm9G5+xDc5sNfEHOpbmfIabQ0=`. A different value stops the apply.
2. **Upload** the zip to `s3://opal-313476888478-lambda-artifacts/investor-reporting/irpt-commentary-composition-read-lambda.zip` (a first mint of a new key; record the returned version id in the ledger).
3. **Apply the export root** with `safe-apply`. BLAST RADIUS: the plan must read only ADDS: `aws_iam_role.commentary_composition_read`, `aws_iam_role_policy.commentary_composition_read`, `aws_cloudwatch_log_group.commentary_composition_read` (14 days), the module's `aws_lambda_function.this` (and its module-internal resources), `aws_iam_policy.commentary_composition_invoke`; 0 to change, 0 to destroy. A plan line touching any existing resource stops the apply. No existing function's code, role or served artifact changes; no served object moves.
4. **Attach the invoke policy** to `outlook-global-commentary-draft-role` from the transcripts root (its own pair; this also drops that role's standing `kms:Decrypt` on the irpt key, unused by this read).
Effect on the served bytes: none. The first invocation is the after-read or the drafter's.

## Branch B (rolled back)

- **`irpt-commentary-composition-read-lambda` (live_before ABSENT):** there is no previous version to restore; rollback is absence. Detach the invoke policy from the commentary role (transcripts root), then `safe-apply` the export root with the module, role, policy, log group and invoke policy removed (or revert the commentary_composition.tf commit and apply): the function is deleted. The log group's 14-day events go with it.
- **S3 object `investor-reporting/irpt-commentary-composition-read-lambda.zip`:** a new key with one version (the version id recorded at upload). Rollback: remove that version (an S3 delete needs human confirmation, CLAUDE.md); leaving it is inert once the function is gone.
- **Source-map entry:** revert the registering commit.
- **Existing functions:** none was changed, nothing to restore. No route, schedule, env or existing-IAM change to revert.

## The replay arm for the applier (rerun before the ledger)

Against the artifacts actually in play: extract the zip to be uploaded into an empty directory `B`, and the four LIVE zips into `L/<function>/` (`irpt-performance-adapter`, `irpt-ycharts-generate`, `irpt-export-render`, `irpt-status`), with a scratch `S` OUTSIDE the worktree; then from the repo root:
`python -B org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~202/replay/run_replay.py . B L S out.json`.
Stop the apply if the exit code is not 0 or `out.json` has any arm FAIL. Expected: 8 arms, 2 `identical` (existing `get()`/`head()`/`put()` callers over 17 scenarios through all four live repository.py versions and the built one; the 59 retained-repository/retention/family-revision tests through the built package and through live `irpt-export-render`), 6 `expected-diff` (own tenant OK with sha256 equal to `composition_ref.sha256` and owner stripped; another tenant REFUSED; the flat import; and 3 negative controls that must fire: the same surface tests over the LIVE repository.py -> ImportError on `SERVICE_READERS`; a repository.py with the user authorize check removed -> six outcomes change; a blob changed after retention -> REFUSED). Delete `S`, `B` and `L` afterwards.
This run, at P: 8 of 8 arms not FAIL; `IB97-4_release_replay.json`.

## The after-read

One invoke AS ~T2's role, holding ONLY `lambda:InvokeFunction` on this function (the invoke policy attached, nothing else for this read): `aws lambda invoke --function-name irpt-commentary-composition-read-lambda --payload '{"tenant":"<firm>","request_ref":"REQ-<24 hex>"}'` for one READY item. Read: `status` OK, `sha256` equal to that item's `composition_ref.sha256`, no `owner`, `input_owner` or account id in the answer. Then (a) the same request with another firm's `tenant` -> `status` REFUSED, `reason` UNAVAILABLE, no `composition`; (b) the same role's direct `dynamodb:GetItem` on irpt-requests and `s3:GetObject` on the composition prefix -> AccessDenied (the read is only through the function). Only after Branch A step 4.

## Rows

`IRPT_BCKEND-D2-W202-S1` (OBSERVATION, INERT: the new function has no source-map entry; the build used a drafted entry and the parity skip), `-S2` (OBSERVATION, INERT: no existing function's repository.py changed; the four rows pin older blobs). Companion rows from IB-pr-386: `W197-S1` (the stored document carries the owner; stripped on return, `binding` members not), `W197-S2` (registration and the invoke attachment are the pair's acts).
