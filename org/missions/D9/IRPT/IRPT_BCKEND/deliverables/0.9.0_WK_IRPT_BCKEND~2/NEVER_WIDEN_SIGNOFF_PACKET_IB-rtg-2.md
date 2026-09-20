# NEVER-WIDEN SIGN-OFF PACKET -- IB-rtg-2

Cell `IB-rtg-2` (round 7, the recut on the round-6 analysis @fa2ff4f0dd). Function: `irpt-status`
(`module.irpt_status.aws_lambda_function.this`, `infra/aws/terraform/investor-reporting/ops/lambda.tf`).
Source commit this packet covers: `764b4a83d2` (`ops/status_loader.py` new; `ops/entry.py` wiring
edit; `infra/aws/lambda/ci/lambda-source-map.json` `files[]` addition), on branch
`wk-irpt_bckend-7-2`.

---

## K-CODE x 1 -- `irpt-status`

- **Rebuilt under a build ledger:** `infra/aws/lambda/ci/build-and-upload.sh investor-reporting
  irpt-status`, run this turn against commit `764b4a83d2`. Output: 13 packaged `.py` file(s),
  import-closure OK ("every top-level import satisfied by package/stdlib/runtime/layer"); 10 of
  13 staged from pinned blobs (unchanged pins -- this order edited none of the `staged_from`
  entries), `status.py`/`status_loader.py`/`manifests.py`/`entry.py` tracked directly under
  `ops/`. Uploaded to `s3://opal-313476888478-lambda-artifacts/investor-reporting/irpt-status.zip`,
  new S3 object version `2ER4lGvdlY7ftm5mPgEYt6pnXbozOeIG` (`LastModified`
  `2026-09-20T15:43:39Z`), size 146288 bytes.
- **Prior live `CodeSha256` READ LIVE, as the rollback source:** `aws lambda get-function
  --function-name irpt-status` -> `CodeSha256 = O3TyGqfqjiwZP9OSXmryonnAst+SbYMLzyuSGphOyCE=`,
  `LastModified = 2026-09-19T17:16:34.000+0000`, `Role = arn:aws:iam::313476888478:role/irpt-status-role`,
  `State = Active`. **Build-store version for that exact rollback target, found by matching
  `Metadata.content-sha256` across the object's version history**
  (`aws s3api list-object-versions` + `head-object --version-id` per candidate): S3 version
  `z8VnRXEPFTioTwjwWlR_TCCQYiqU6mmV` (uploaded `2026-09-19T15:58:00Z`, 141785 bytes) carries
  `Metadata.content-sha256 = O3TyGqfqjiwZP9OSXmryonnAst+SbYMLzyuSGphOyCE=` -- an EXACT match. That
  is the rollback artifact.
- **Built sha VERIFIED AT REST:** `aws s3api head-object --bucket
  opal-313476888478-lambda-artifacts --key investor-reporting/irpt-status.zip` (no `--version-id`,
  i.e. the just-uploaded latest) -> `Metadata.content-sha256 = B0AmyfRKxd4uMhcfoklf3cCpPtnDQUBpLsUBADeDcQ0=`,
  `ContentLength = 146288` -- MATCHES `lambda-source-map.json`'s newly written `artifact_sha256`
  for `irpt-status` exactly (both this turn's write and the S3 object's own metadata agree; the
  build tool's self-report is corroborated by an independent read of the object, not trusted on
  its own report, per CLAUDE.md's "never trust a producer's self-report").
- **Served-byte delta exactly the edited/added members:** relative to the 15-member `files[]`
  this function declared before this order, EXACTLY ONE member is NEW
  (`status_loader.py`, tracked directly under `ops/`, 0 prior versions) and EXACTLY ONE member is
  MODIFIED (`entry.py`: `+import functools`, `+import status_loader as _status_loader`, and the
  `ENTRY.operations` values rebound from bare `_status_envelope` to
  `functools.partial(_status_envelope, loader=_status_loader.status_loader)`). All other 14
  declared members (`status.py`, `manifests.py` and the 10 `staged_from` blobs at their
  PRE-EXISTING pins, plus `raw_keys.json`/`firm_registry.json`) are BYTE-IDENTICAL to the prior
  build -- this order edited none of their pins or committed content. `status.py` itself is
  UNEDITED (module docstring in `entry.py` and this order's BOUNDS both name it as such; verified
  by `git diff` on this commit touching only the three files named above).
- **Import closure:** `build-and-upload.sh`'s own check, printed above: "OK: import-closure -- 13
  packaged .py file(s), every top-level import satisfied by package/stdlib/runtime/layer. (Nested
  lazy imports exempt by design.)"

---

## WRITERS, counted

The property this loader newly READS is the `irpt-jobs` DynamoDB table's (tenant, job) lease row
(`lease_owner`, `lease_expires_at`, `fence_token`). Every code path in this tree that WRITES that
row (i.e. calls `.acquire()` through `TenantLease` or `ScanLease`), counted by
`comp-find`/`Grep` over `infra/aws/lambda/investor-reporting/**`:

- **N = 1 in PRODUCTION:** `intake/poller.py:299` -- `checkpoint.ScanLease(store, owner)` against
  the FIXED constant key `(tenant=LEASE_TENANT="_opal", job=LEASE_JOB="mailbox-intake-scan")`
  (`intake/checkpoint.py:51-52` env defaults). This is the deployed mailbox-intake scanner's own
  lease, and it is the ONLY row this table's writer side populates today.
- **N = 0 for every OTHER (tenant, job) shape.** `ops/manifests.py`'s `TenantLease` GENERALISES
  the mechanism to an explicit key so `ycharts-generate`/`holdings-snapshot`/`export-render` could
  each hold their own lease (module docstring) -- but a scoped search of
  `infra/aws/lambda/investor-reporting/ycharts/**` and `.../export/**` for `TenantLease` or
  `manifests.` found ZERO hits: no deployed cell calls `TenantLease.acquire()` for a firm-scoped
  job yet. `expired_lease_recovery()` (`manifests.py:155-192`) exercises `TenantLease` too, but
  only from `ops/tests/test_manifests.py`, never from a deployed `lambda_handler`.
- **CONSEQUENCE FOR THIS LOADER'S OWN "FOUND" PATH:** in the CURRENT system, a firm-scoped
  `status_loader(request, scope)` call (tenant = a real firm id, job = a ycharts/holdings/export
  job id) will ALWAYS read `record is None` and refuse `NOT_FOUND` -- correctly, because nothing
  ever claims that row today -- until a later cell wires one of those three writers. The ONE
  (tenant, job) pair with a real writer today is `("_opal", "mailbox-intake-scan")`, an OPERATOR
  row, not a firm-scoped job. This is the accurate, present-tense scope of "found" for this order;
  it does not change this loader's correctness (a genuinely unclaimed job SHOULD refuse), but it
  bounds what arm (e)'s "a job the intake/export/render path ACTUALLY RAN" can mean until a
  writer exists for a firm-scoped job.
- **IAM, MEASURED, not assumed (preflight's own caveat):**
  `infra/aws/terraform/investor-reporting/ops/iam.tf` sid
  `ReadJobLeasesCheckpointsAndRequestRevisions` ALREADY grants `irpt-status-role`
  `dynamodb:GetItem`/`Query` on `irpt-jobs`, `irpt-checkpoints` AND `irpt-requests` -- sized for
  exactly this composition before this cell existed (`iam.tf:10-14`'s own comment names all three
  tables as "the three tables this cell's status read depends on"). **NO NEW IAM STATEMENT IS
  NEEDED.** This loader reads only `irpt-jobs`, the one table this order's BOUNDS name; the role's
  wider grant (checkpoints, requests) is unused by this cell and is a LATER cell's, not widened
  here.

---

## BLAST RADIUS, both branches

- **WITH the fix (this order's edit, not yet applied -- see STOP below):** the three routes this
  function serves (`analysis-report`, `status-summary`, `status-job`) each return either (a) a
  validated `StatusEnvelope` in state `RUNNING` (a held, unexpired lease) or `UNCERTAIN` (an
  expired one, never `READY` -- this loader has no completion signal to promote itself past), for
  a job with a lease row, or (b) a `NOT_FOUND` refusal for a job with none, or a request naming
  neither a tenant nor a job. NO WRITE ANYWHERE: `status_loader.py` calls `TenantLease.read_current()`
  only, never `.acquire()` -- matching `iam.tf`'s own design intent ("read-only status producer;
  no write permission anywhere").
- **WITHOUT the fix (the CURRENT live state, unchanged until an apply):** all three routes always
  raise `NoSuchOperation` -> `UNSUPPORTED_OPERATION`, regardless of any job's real state (FWD-2's
  status tab, round 6). `status._default_status_loader` is UNCHANGED and still exists as
  `_status_envelope`'s own fallback for a caller that constructs it without a `loader` at all.
- **Both branches:** no S3 write, no DynamoDB write, no new IAM statement, no new table, no
  external feed.

---

## ROLLBACK

Re-publish the prior live `CodeSha256` (`O3TyGqfqjiwZP9OSXmryonnAst+SbYMLzyuSGphOyCE=`, S3 object
version `z8VnRXEPFTioTwjwWlR_TCCQYiqU6mmV`) via Terraform against
`module.irpt_status.aws_lambda_function.this` -- **NEVER** `aws lambda update-function-code`.

---

## THE IDENTITY LINE PER ARM

Arms (d) (APPLY) and (e) (PROVEN LIVE) are **NOT EXERCISED THIS ROUND**: see STOP below. There is
no live identity/role exercise to report for either arm this turn.

---

## READ FOR BOTH NEVER-WIDEN HALVES AT HEAD -- ABSENT, STOP HERE

Checked this turn (`Glob`/`Grep` over the whole worktree for
`*_{COO,CTO}_HALF_*IB-rtg-2*` and for the literal string `IB-rtg-2` combined with `HALF`):
**ZERO hits anywhere in the tree** for either the CTO's or the COO's never-widen half naming cell
`IB-rtg-2` or this packet's blob. `org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~B/`
and `.../1.0.0_SA_CTO/` carry no file mentioning `IB-rtg-2` at all as of this commit's parent
(`8ba74b3130`). Per this order's arm (c): **ABSENT -> STOP HERE.** Arm (d) (the apply, under a
change-management ledger) and arm (e) (the live-principal proof) are NOT run this turn. This is
the EXPECTED first-pass outcome named in the dispatch: the task order stays open pending both
signed halves; a FAIL on arm (d)/(e) in THIS commit would be a truthful FAIL in a VALID instance,
not a defect in this order's own work.
