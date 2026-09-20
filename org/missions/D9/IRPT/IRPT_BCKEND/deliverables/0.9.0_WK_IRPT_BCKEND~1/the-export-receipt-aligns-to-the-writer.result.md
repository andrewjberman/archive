# RESULT -- IRPT_BCKEND.TO-IB-rtg-1 (the export receipt aligns to the writer and the taxonomy tests the code)

**Worker:** `0.9.0_WK_IRPT_BCKEND~1`. **Pass:** first. **Outcome:** STOPPED at arm (c), per the
order's own stated expected first-pass outcome -- both never-widen halves are ABSENT.

## What was done

- **Arm (a) MEASURE**, printed with denominators: confirmed S105 (the OLD `RECEIPT_KEY_TEMPLATE`,
  `investor-reporting/export/{firm}/{export_id}/receipt.json`, is outside every declared prefix
  family and matches none of the role's GetObject ARNs) and S106 (the OLD except clause tests the
  exception CLASS NAME, so a modeled `AccessDenied` propagates as `UNEXPECTED`) against the live
  source at HEAD. The `44/19` ownership/relationship re-derive constraint (s.R7.3) does NOT apply
  to this cell -- S105/S106 read no account/relationship count; confirmed nothing inherited.
- **Arm (b) SOURCE EDIT**: `export/entry.py` -- S106's except clause now decides off the modeled S3
  error CODE (`isinstance(..., botocore.exceptions.ClientError)` + `Error.Code`), and
  `RECEIPT_KEY_TEMPLATE` is realigned to `firms/{firm}/generations/{export_id}/receipt.json`, the
  DECLARED "generations" family. `export/handler.py` gains `receipt_key()` + `persist_receipt()`,
  wired into `finalize_export(persist=True)` -- the write beside the bundle S105 requires.
  **Proved this run, not assumed: the reader's computed key and the writer's computed key are
  byte-identical.** Built via `infra/aws/lambda/ci/build-and-upload.sh investor-reporting
  irpt-export-render`; served-byte delta verified EXACTLY `{entry.py, handler.py}` changed plus
  `keys.py` added (a necessary, previously-missing packaging dependency, row `W1-S44`, already
  fixed and disarmed this commit).
- **New IAM grant** (`aws_iam_role_policy.export_render_receipt`) for the aligned address, since it
  does not fall under the role's existing exports-prefix grant -- MEASURED via `fnmatch`, and
  TIGHTENED to the `EXP-`-namespace shape after that same measurement showed a bare wildcard would
  also have reached a DIFFERENT cell's (ycharts generation, B9/IB-s-9) receipt objects under the
  same "generations" family. `terraform validate`/`fmt` clean; a real (backend-attached) `plan`
  shows exactly 1 IAM policy create + 1 Lambda function update, 9 other resources `no-op`, 0
  destroy.
- **Arm (c) PACKET**: `NEVER_WIDEN_SIGNOFF_PACKET_IB-rtg-1.md` written, with the prior live
  `CodeSha256` read live (rollback anchor, its S3 build-store version verified at rest), the built
  sha verified at rest, the served-byte delta, the new grant's derivation and tightening, a real
  plan on the export root (`resource_changes` subtraction: 11 compared, 9 no-op, 2 substantive),
  the other 9 Terraform roots re-taken (6 clean, 3 showing UNRELATED sibling-worker build drift --
  row `W1-S45`), the blast radius both branches, and the rollback. **Read for both halves at
  HEAD: ABSENT (0 of 2).** Per the order: arm (d)/(e) do NOT run this pass.

## Surprises filed (channel: `../surprise-channel/investigations/INVESTIGATION_v1.md`)

- `IRPT_BCKEND-W1-S42` (OBSERVATION, ARMED, disarm_owner `1.0.0_SA_CTO`) -- the order's literal
  wording for S105's alignment names path segments (`generations/<gen>/attempts/<a>/exports/<rev>/`)
  the reader's request never carries; the implemented address is the nearest workable substitute
  and the signers should read this row before signing either half.
- `IRPT_BCKEND-W1-S43` (BLOCKING, ARMED, disarm_owner `2.0.0_SA_COO~B`) -- even after this order's
  fix deploys, `entry.py`'s OWN wired `submit_export` unconditionally raises `_ExportNotWiredHere`
  and never calls `handler.py` at all, so arm (e)'s live round trip cannot pass on the deployed
  path until a further, out-of-scope cell wires the two together.
- `IRPT_BCKEND-W1-S44` (BLOCKING, INERT -- already fixed this commit) -- `keys.py` was never
  packaged for `irpt-export-render`, so the pre-existing `bundle_key()`/`artifact_key()` (and this
  cell's new `receipt_key()`) would `ImportError` at runtime; fixed in the manifest this commit.
- `IRPT_BCKEND-W1-S45` (OBSERVATION, ARMED, disarm_owner `2.0.0_SA_COO~B`) -- a sibling worker's
  `build-and-upload.sh` run is visible in every OTHER worker's `terraform plan` immediately,
  before any commit/merge/apply, because the artifact bucket is shared AWS state; a packet's
  "other roots re-taken" section can show drift that is a sibling's legitimate in-flight work.

## Proof of spec

`R72-AC1` -- **FAIL** (truthfully, per the order's own expected first-pass shape): the battery
does not print the success token this run, because arm (c) STOPs at the absent halves and arm
(e)'s live, deployed-role round trip was never attempted. `R72-AC2` (judgment) -- CVO's, not
graded here.

The order's `<status>` stays open. This is the report on it.
