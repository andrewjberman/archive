# Never-widen ask -- OG-m-2, the 49F gold dispatcher remedy (NFRA_OPLGTW E11)

> **AMENDMENT A1 (2.0.0_SA_COO~O, 2026-09-29 ~01:2xZ, on row NFRA_OPLGTW-Z-W15-S1).** The dispatcher reads the
> marker at the event's `versionId` (the exact PUT that fired). S3 authorizes a versioned GET with
> `s3:GetObjectVersion`, not `s3:GetObject`, so as first asked every accelerator fire would read AccessDenied and
> skip, qualified ones included. The ONE change: `s3:GetObjectVersion` is added on the marker prefix only. It is
> read-only, on the same single-firm prefix, with no ListBucket. Dropping the version pin was rejected: reading
> the latest version would let one incomplete PUT's event see a later qualified body and dispatch again. The
> CTO half @c7510ec012 was signed against the pre-amendment bytes and is re-asked.

By: `2.0.0_SA_COO~O` (issuer), 2026-09-29. Order: `org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-m-2.dispatch-classifier-remedy.md`.
Scope ruled by `1.0.0_SA_CTO~O`, msg 26305, option (a). Read it rests on: OG-m-1
(`deliverables/0.9.0_WK_NFRA_OPLGTW~13/MARKER_STORM_READ.md`, merged @70f45e7675), rows Z-W13-S1, Z-W13-S2.

**Halves owed:** `1.0.0_SA_CTO~O` (CTO half, signed against THIS file, per msg 26305) and `3.0.0_SA_CVO~O` (second,
non-acting half). The worker's PHASE B does not start until both are signed. PHASE A (code, tests, targeted PLAN)
changes nothing in AWS and runs before them.

## 1. Blast radius -- what the act may touch

**Repository write set (the order's `<paths>`):**
- `infra/aws/lambda/opal-assets/advi-49f-gold-dispatch/lambda_function.py` (the dispatcher);
- `infra/aws/lambda/opal-assets/tests/test_advi_49f_gold_dispatch_remedy.py` (new, tests only);
- `infra/aws/terraform/opal-assets/advi_49f_floor.tf`, ONLY `aws_iam_role_policy.advi_49f_gold_dispatch`;
- `infra/aws/lambda/ci/lambda-source-map.json` (the build script rewrites the dispatcher's `artifact_sha256`);
- the NEVER-2 entry under `org/critical_paths/change_management/` and its sentinel
  `org/critical_paths/.open_deploys/nfra-oplgtw-dispatch-classifier-remedy.json`; the worker's deliverables and one
  channel file.

**AWS write set (three keys, all on the dispatcher):**

| key | before (read 2026-09-29 ~00:3xZ) | after | rollback |
|---|---|---|---|
| `s3://opal-313476888478-lambda-artifacts/opal-assets/advi-49f-gold-dispatch.zip` | VersionId `MLLnDY4WlZCx94GuUkxXyQWlYXR2c5kY`, content-sha256 `fEMCZ4usqXuIC1GhklcClwOn/O6vR+uV+xgbk+oj8lk=`, 8,553 bytes, built from `1abc54fa4c` 2026-08-19 | a new version built from the committed source | `s3api copy-object` of VersionId `MLLnDY4W...` back over the key WITH its `content-sha256` metadata |
| Lambda `advi-49f-gold-dispatch` code | `CodeSha256` `fEMCZ4usqXuIC1GhklcClwOn/O6vR+uV+xgbk+oj8lk=`, LastModified 2026-08-19T17:32:12Z | the new artifact's sha | after the artifact rollback, `HALT_ACK=1 .tools/safe-apply.sh -chdir=infra/aws/terraform/opal-assets apply -target=module.advi_49f_gold_dispatch`; verify `CodeSha256` reads `fEMCZ4...` |
| IAM inline policy `advi-49f-gold-dispatch-role` / `advi-49f-gold-dispatch-scoped` | 5 statements, NO `s3:` action (read by `dr.AC2.sh` at HEAD: GetObject resources 0 of 2, extra 0) | + `s3:GetObject` on `arn:aws:s3:::opal-data-49financial/gold/advi/_logs/chain_*`; `s3:GetObject` AND `s3:GetObjectVersion` on `arn:aws:s3:::opal-data-assets/schwab/08335338/meta/complete/*` (AMENDED A1, row Z-W15-S1); no ListBucket | revert the `.tf` commit on the worker branch, `safe-apply -target=aws_iam_role_policy.advi_49f_gold_dispatch` |

**Not touched, by name:** the marker writer (`conversion_manifest.py`, `schwab_runtime.py`, all four copies, and the
`opal-assets-silver-schwab` Lambda); `silver.tf` and the monolith bucket's singleton S3 notification
(`advi-49f-silver-complete-accelerator` keeps firing on every PUT; the gate is in the dispatcher); the SSM document
`advi-49f-chain-dispatch`; the floor schedule `advi_49f_gold_floor` cron(45 12 * * ? *), which stays the PRODUCTION
trigger; the host `i-01003b035d2988dfb`; the chain code under `s3://opal-data-49financial/_code/`; every other resource
in the `opal-assets` root (the apply is `-target`ed to the two addresses above).

**Rider, stated:** the live package predates `e2be5c2f42` ("BUILD ONLY -- NOT APPLIED", 2026-08-29), which added
`_trigger_identity` (the S3 event's source label and marker key). The deploy ships it. It changes the SendCommand
`Comment` label from `src=manual` to `src=advi.49f.silver-accelerator` for S3 fires and adds `marker_key` to the result;
the qualified-marker gate needs the key. Measured by diffing the live zip's `lambda_function.py` (sha256 `1fd82d38...`)
against HEAD (`7e8cc67f...`): the only differences are that function and its two call sites.

## 2. Writers and consumers of `schwab/08335338/meta/complete/` (bucket `opal-data-assets`)

Counted by OG-m-1's census: every tracked non-test code file under `data/` or `infra/` naming `meta/complete` (7) plus
the writer path read by code (2 more), each classed from its code, writers compared with the deployed package by sha256.

- **WRITERS: 1 deployed writer**, the `opal-assets-silver-schwab` Lambda (CodeSha256 `v2BztqbuhHD3gH95e...`, 2026-09-16),
  from **4 source files**: `conversion_manifest.py` and `schwab_runtime.py`, each in `data/assets/scripts/silver/` and
  `infra/aws/lambda/opal-assets/opal-assets-silver-schwab/`; 4 of 4 match the deployed bytes. This act moves NONE of them.
- **CONSUMERS: 2 deployed consumers.** (1) the S3 notification `advi-49f-silver-complete-accelerator` -> the dispatcher
  `advi-49f-gold-dispatch` (the consumer this act changes: it will read the marker body at the event's version);
  (2) the opal-gateway Schwab integration (`app/integrations/schwab/aws_roles.py`, `catalog.py`; readers, unchanged).
- **CONFIG: 3 files**, unchanged except the one policy resource: `advi_49f_floor.tf`, `silver.tf`,
  `opal-gateway/schwab_reader_iam.tf`.

N writers = 1, so one writer's rule is read below; the act changes a consumer only.

## 3. Both branches, read from the dispatcher's rule as the order builds it (never predicted from input shape)

**Accelerator path (S3 event, one per marker PUT):**
- the marker version's `closure.status` is `qualified` -> the host is ensured running and `send_command` runs ONCE,
  exactly as today;
- anything else (`incomplete`, key absent, AccessDenied, unparseable) -> NO host start, NO `send_command`; the log line
  reads `SKIP: accelerator marker key=... version=... closure.status=... -- not dispatching (only a qualified closure
  dispatches; the floor remains the production trigger)`; the result says `dispatched: false`.
- The writer's own rule (OG-c-1, deployed @2026-09-16) writes one qualified closure per date and incomplete versions
  before it (measured: 9 incomplete then 1 qualified on each of 09-23, 09-24, 09-25). So the accelerator path goes from
  about 10 dispatches per date to 1. If a date never qualifies, the accelerator dispatches 0 times and the 12:45Z floor
  runs as today.

**Classification (both paths, when the SSM invocation is terminal inside the 300 s poll):**
- the chain log `gold/advi/_logs/chain_<ExecutionStartDateTime as %Y%m%dT%H%M%SZ>.log` (TS, TS-1 s, TS+1 s) has a last
  `CHAIN ` line -> OK, REFUSED or ABORT from that line;
- no such key, or no `CHAIN ` line -> `UNKNOWN(chain_log=absent|no terminal line, key=...)`, said in the log line;
- in NO branch is `send_command` called a second time. The "running past the poll budget" branch is unchanged.

**What changes in the SERVED world:** gold outputs are not written by the dispatcher, so no served number moves. The
changes are (i) fewer chain dispatches (about 9 of 10 accelerator fires per date become SKIP; each skipped fire today
ends REFUSED by the chain lock or ABORT), and (ii) the dispatcher's log verdict for a completed chain reads OK instead of
UNKNOWN. The floor's daily run is unchanged in trigger, document and host.

## 4. NEVER-2

Slug `nfra-oplgtw-dispatch-classifier-remedy`; legs: the `tf-lambda` leg for `advi-49f-gold-dispatch` (from
`lambda-source-map.json`: `tf_resource` `module.advi_49f_gold_dispatch (yang-lambda)`) and one IAM leg for
`aws_iam_role_policy.advi_49f_gold_dispatch`. Opened and committed before the upload; closed with proofs; `dr.AC3.sh`
grades the close. One-deployer census across every worktree before the act. Window: outside 12:15-13:30Z and
09:30-10:15Z.

## 5. Signatures

| half | seat | verdict | at bytes |
|---|---|---|---|
| CTO | `1.0.0_SA_CTO~O` | | |
| second | `3.0.0_SA_CVO~O` | | |
