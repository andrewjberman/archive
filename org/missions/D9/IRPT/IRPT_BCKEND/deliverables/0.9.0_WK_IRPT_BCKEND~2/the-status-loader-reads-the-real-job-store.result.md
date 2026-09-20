# IB-rtg-2 -- THE STATUS LOADER READS THE REAL JOB STORE -- result

## Arm (a) -- MEASURE FIRST

Confirmed at `ops/entry.py`, `ops/status.py`, `ops/manifests.py` and `intake/checkpoint.py` at
HEAD (`8ba74b3130` before this order's own edits): `ops/entry.py`'s `_status_envelope` (this
worker's copy of HEAD had it at lines 61-74, not the face's cited 56-104 -- the face's own line
numbers had drifted by round 7; the FUNCTION named is the same one) fell to
`status._default_status_loader` whenever no `loader` and no `event["status_loader"]` were
supplied, and that default unconditionally raises `NoSuchOperation`. The reachable building
blocks are real: `manifests.TenantLease` (a thin, explicit-key generalisation of
`intake.checkpoint.ScanLease`) reads/writes the `irpt-jobs` table via `checkpoint.dynamo_store()`
or `checkpoint.MemoryStore()`.

MEASURED, PRINTED, LIVE (never inherited from round 6):

- `infra/aws/terraform/investor-reporting/ops/iam.tf`'s `irpt-status-role` ALREADY grants
  `dynamodb:GetItem`/`Query` on `irpt-jobs`, `irpt-checkpoints` AND `irpt-requests` (sid
  `ReadJobLeasesCheckpointsAndRequestRevisions`) -- sized for this composition before this cell
  existed. **No new IAM grant is needed.**
- The ONLY production writer to `irpt-jobs` today is `intake/poller.py`'s `ScanLease` on the fixed
  key `(tenant="_opal", job="mailbox-intake-scan")`. Zero deployed cells call `TenantLease` for a
  firm-scoped job (ycharts/holdings/export) -- see the packet's WRITERS section for the full
  census and its consequence for what "found" means today.
- The live `irpt-status` function's PRIOR `CodeSha256` (the rollback source) is
  `O3TyGqfqjiwZP9OSXmryonnAst+SbYMLzyuSGphOyCE=` (read live this turn) -- see the packet.

The mutant (the pre-fix shape: `_status_envelope` called with no loader and an event carrying
none) still raises `NoSuchOperation` on an exercised job -- proven by `battery_ib_rtg_2.py` arm
(a), which is what makes the later arms discriminating rather than vacuous.

## Arm (b) -- THE SOURCE EDIT

`infra/aws/lambda/investor-reporting/ops/status_loader.py` (new): `status_loader(request, scope,
store=None)` composes `manifests.TenantLease` against the (tenant, job) the request names
(`request.object_id`, then `request.params["job"/"job_id"/"jobId"]`, then `request.job_id`, in
that declared order, never inferred) and `scope["verified_request_firm_id"]` for the tenant. A
held, unexpired lease reports `RUNNING`; an expired one reports `UNCERTAIN` (never `READY` --
this loader has no completion signal to promote itself past, matching
`_default_status_loader`'s own refusal-over-fabrication rule). No lease row at all raises
`KeyError`, which `_authz/errors.reason_for` already classifies `NOT_FOUND` by TYPE (no new
boundary declaration needed). `ops/entry.py` is edited to import the module and bind it via
`functools.partial(_status_envelope, loader=_status_loader.status_loader)` on all three
operations (`analysis-report`, `status-summary`, `status-job`) in place of the bare
`_status_envelope`; `status.py` itself is UNEDITED. `lambda-source-map.json`'s `irpt-status`
`files[]` gains `status_loader.py`.

`infra/aws/lambda/ci/build-and-upload.sh investor-reporting irpt-status` (the served function
name `irpt-status` confirmed directly at `lambda-source-map.json`'s own `irpt-status` key --
`tf_resource: module.irpt_status.aws_lambda_function.this` -- `_ids/ids.py` itself carries no
`staged_from` map of its own; it is one of `irpt-status`'s STAGED MEMBERS, not the name's
source) ran clean this turn: 13 packaged `.py` files, import-closure OK,
uploaded to `s3://opal-313476888478-lambda-artifacts/investor-reporting/irpt-status.zip`
(new S3 version `2ER4lGvdlY7ftm5mPgEYt6pnXbozOeIG`), new `artifact_sha256`
`B0AmyfRKxd4uMhcfoklf3cCpPtnDQUBpLsUBADeDcQ0=` VERIFIED AT REST via `head-object`.

Existing `ops/tests/` (34 tests) and `_authz/tests/test_guarded_entries.py` (96 tests) both pass
unchanged.

## Arm (c) -- THE PACKET, and the halves check

`NEVER_WIDEN_SIGNOFF_PACKET_IB-rtg-2.md` committed at `27c5e480b3`, blob
`26360553eb7a66af4ea7c68d93f14e206e03ef60`. Checked for both never-widen halves at HEAD
(`Glob`/`Grep` for `*_{COO,CTO}_HALF_*IB-rtg-2*` and for the literal `IB-rtg-2` anywhere under
`deliverables/2.0.0_SA_COO~B/` or `deliverables/1.0.0_SA_CTO/`): **ABSENT, zero hits anywhere in
the tree** naming this cell or this packet's blob. Per the order's own text: **STOP HERE.**

## Arms (d) / (e) -- NOT RUN

Not exercised this turn, per the STOP above. This is the expected first-pass outcome named in the
dispatch. The task order's `<status>` stays `pending`; it is not flipped to `complete`.

## R73-AC1

`battery_ib_rtg_2.py`: 12 of 12 arms PASS offline (no AWS call, `checkpoint.MemoryStore()`
fixtures throughout; a bare-name import collision across the Lambda tree's several `entry.py`
files -- caused by `status.py`'s own module-level `sys.path` insertion of the sibling `directory/`
folder -- was found and pinned per-module by explicit directory, not left to search order).
Token: `IBR73-STATUS-LOADER-SERVES-ENVELOPE`. Output at
`IB-rtg-2_R73-AC1_battery_output.txt` (committed at `27c5e480b3`).

## R73-AC2 (judgment, CVO)

Recorded substance for `3.0.0_SA_CVO` at L9, no verdict: the SOURCE fix (arm b) is built and
offline-proven; the DEPLOY (arm d) and the LIVE proof (arm e) are correctly withheld because
neither never-widen half exists yet -- this is a VALID, EXPECTED state for a served-path handler
deploy's first pass, not a defect in the fix itself. The one substantive scope question for the
CVO: this loader's "found" branch is exercisable in production TODAY only for the operator's own
`("_opal","mailbox-intake-scan")` lease row (see the packet's WRITERS census) -- a firm-scoped
status request will read `NOT_FOUND` until a later cell (ycharts-generate, holdings-snapshot or
export-render) wires a `TenantLease.acquire()` call of its own. Whether that scope is sufficient
to call FWD-2's status tab "fixed" for round 7, or whether a firm-scoped writer is a companion
cell this round still owes, is the CVO's to judge.

## Surprise row filed

`IRPT_BCKEND-W2-S60` (OBSERVATION, INERT): `lambda-source-map.json`'s pre-edit `irpt-status.note`
claimed `artifact_sha256` equals the live `CodeSha256`; MEASURED this turn, the two disagreed (the
live value was found at a LATER S3 object version than the one the stale field's own value
matches on this run's sampling). Not this order's defect, not fixed here; this order's own packet
uses the live-measured value directly.
