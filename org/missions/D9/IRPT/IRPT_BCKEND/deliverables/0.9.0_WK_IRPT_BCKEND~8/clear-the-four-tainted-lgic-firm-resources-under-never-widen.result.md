# IB-rth-8 -- result (worktree `/c/tmp/wk-irpt-8-8`, branch `wk-irpt_bckend-8-8`)

Worker: `0.9.0_WK_IRPT_BCKEND~8`. Governing order:
`org/missions/D9/IRPT/IRPT_BCKEND/task-orders/IRPT_BCKEND.TO-IB-rth-8.clear-the-four-tainted-lgic-firm-resources-under-never-widen.md`
@HEAD `2984207254`.

## Arm (a) -- the replace semantics, measured

Fresh `.tools/terraform.exe init` + `plan -out=<tmp>` + `show -json <tmp>` on
`infra/aws/terraform/shared-infra` (the structured-plan JSON form, which carries each resource's real
`actions` array -- `plan -json`'s UI-log stream alone only ever prints a collapsed "replace" with no
delete/create breakdown, so the structured form via `-out` + `show -json` was used to actually settle
the question the order asks).

**Result: identical to `IB-rth-7`'s finding** (@`cabb11ced3`) -- `Plan: 4 to add, 0 to change, 4 to
destroy.` All four target resources show `actions: ["delete", "create"]`,
`action_reason: "replace_because_tainted"`:

- `aws_s3_bucket_policy.lgic_firm["inflection"]`
- `aws_s3_bucket_policy.lgic_firm["cottonwood"]`
- `aws_s3_bucket_versioning.lgic_firm["inflection"]`
- `aws_s3_bucket_versioning.lgic_firm["cottonwood"]`

**242 total `resource_changes` in the root's plan; 238 no-op, 4 replace (the four above), 0 elsewhere.**
The 15 `demo`/`49financial` resources present in the root all read `no-op` -- confirmed nothing outside
the four named resources is planned to change.

**The policy replace is content-free**: `change.before` and `change.after` for both
`aws_s3_bucket_policy` resources are byte-identical (sha256, normalized JSON) -- `opal-data-inflection`
both hash `2d90b2f1a01bada3...`, `opal-data-cottonwood` both hash `b095cbbfe6572ae6...`. An independent
`aws s3api get-bucket-policy` call (a different tool from Terraform's own refresh) matches both hashes
exactly. This confirms the destroy-then-create will delete and recreate the SAME already-correct policy
(the CRO's console PUT).

**`aws_s3_bucket_policy` destroy mechanism, stated with confidence:** MODERATE-HIGH that
`Delete` calls `s3:DeleteBucketPolicy` (removing the whole document -- there is only one policy per
bucket) before `Create`'s `s3:PutBucketPolicy` restores it. Basis: this is a single-purpose resource
with a 1:1 CRUD-to-API mapping and no ambiguity in which verb does what; NOT independently re-verified
against the provider's Go source in this environment (only the vendored compiled binary is present
locally, no source, no decompile attempted, no live vendor/network fetch performed -- none is
authorized). Consistent with the CTO's own framing of the identical question in `IB-rtf-5`'s CTO half
(@`89fecc6686`).

**`aws_s3_bucket_versioning` destroy mechanism, stated as genuinely UNCERTAIN, per the order's own
instruction not to assume either way:** LOW confidence on whether the destroy step is (a) a no-op,
state-only reconciliation, or (b) an actual `PutBucketVersioning(Suspended)` call before the create's
`PutBucketVersioning(Enabled)`. Neither the plan JSON, the AWS CLI, nor the vendored binary settle this
without either the provider's source or an observed apply's CloudTrail trail. **Stated as moot in
practical consequence either way**, because both buckets hold 0 keys -- no object exists to lose
version history on regardless of which behavior is true.

**Sequencing:** read directly from `s3-lgic-firm-buckets.tf` -- `aws_s3_bucket_versioning.lgic_firm` and
`aws_s3_bucket_policy.lgic_firm` carry no `depends_on` on each other, so Terraform's default parallelism
means the four replacements are NOT guaranteed serialized relative to each other (their windows may
overlap). Within any one resource's own replace, its delete completes before its own create begins --
that ordering is a Terraform invariant and is not in question.

## Preconditions, re-confirmed independently (3 of 3)

- **(i) policy match:** live `get-bucket-policy` (AWS CLI) == Terraform's refreshed `before` == the
  `after` it will create, both buckets, sha256-compared (two different instruments).
- **(ii) 0 keys:** `list-objects-v2`, both buckets, re-measured this session (not carried from any prior
  run).
- **(iii) identity exemption:** `sts get-caller-identity` -> `arn:aws:iam::313476888478:user/Andrew_Berman`,
  confirmed 1 of 3 exempted rows in `infra/logic/registry/exemptions.json` for BOTH
  `opal-data-inflection` and `opal-data-cottonwood`.

## Arm (b) -- the never-widen packet

Written and committed: `IB-rth-8_NEVER_WIDEN_PACKET.md` (this deliverables folder), naming the exact
blast radius (only the four resources, both firms, nothing else -- 238 of 242 no-op confirmed), the
measured window (s.2 above, with confidence stated per resource type), the consequence given 0 keys
(no data exposure possible; stated plainly as a compliance/security state regardless), and rollback
(a fresh `safe-apply.sh` re-converges to the same already-correct policy; no data can have been lost).

**Committed @`401f186d62`** together with `battery_ib_rth_8.py`. `battery_ib_rth_8.py --arm measure`
re-run AFTER that commit confirms the packet is present, at HEAD, and byte-identical to the working
file, and prints `IBR85-REPLACE-SEMANTICS-MEASURED-PACKET-WRITTEN` (rc=0).

**Sign-off status: NOT obtained this pass.** `battery_ib_rth_8.py --arm apply` searched
`org/tier1_exec/**/deliverables/` at HEAD for a CTO half and a COO half naming `IB-rth-8` and
`COO_HALF`/`CTO_HALF` in their filename: **0 of each found.** Per the order's own text and
`IB-rtf-5`'s precedent exactly: this is an honest STOP. No apply was attempted, no Terraform state was
touched, `--arm apply` exits 0 with "GATE NOT MET" and no token. **Obtaining the signatures is the
issuing COO's and the CTO's job after this packet lands** -- not attempted by this worker.

## Arm (c) -- NOT RUN (gate not met)

Per BOUNDS ("Both halves at HEAD BEFORE the apply, or the apply does not run"): no `safe-apply.sh` run,
no ledger leg closed, no state read beyond the plan/refresh above (which is itself a read, not a
mutation), no disarm row for `IRPT_BCKEND-W7-S2` filed by this cell (that row's own disarm depends on
the apply actually landing, per the order's arm (c) text: "Disarm row `IRPT_BCKEND-W7-S2` by citation
... " is listed under arm (c), which did not run).

## R85-AC3 -- the judgment question (for `3.0.0_SA_CVO`, no verdict from this worker)

**Question:** given the measured replace semantics from arm (a) -- a true delete-then-create, forced
purely by the taint marker rather than any attribute-level need, with the policy's before/after content
byte-identical and both buckets holding 0 keys throughout -- was the disclosed window (if any)
acceptable, or should this class of taint-clear require a different remedy (e.g. `terraform import`
instead of replace) in future?

**Both readings, stated for the record, no verdict:**

- **Reading 1 -- replace is acceptable here.** The measured facts are unusually favorable: (a) the
  policy content is provably unchanged (byte-identical hash before/after), so the replace is purely a
  state-mechanics operation with zero declarative drift; (b) both buckets are provably empty (0 keys,
  re-measured, two instruments) for the entire relevant window, so even a genuine delete-then-create gap
  on the policy exposes nothing to read, copy, or delete, and the versioning question is moot regardless
  of which provider behavior is true; (c) the applying identity is itself exempted, so no lockout
  recurs. Under these specific facts, `terraform import` (which would re-associate the existing AWS
  objects with Terraform state without ever calling `DeleteBucketPolicy`) achieves the SAME end state
  with a strictly smaller blast radius (no delete call issued at all), so it is arguably the objectively
  safer choice EVEN THOUGH the replace's actual measured risk here is very low -- the two are not
  equally safe, only both acceptable in this specific empty-bucket, content-identical case.
- **Reading 2 -- this class of taint-clear should default to `terraform import`, not replace, going
  forward.** The favorable facts in this instance (0 keys, byte-identical policy) are not guaranteed
  properties of a TAINTED resource in general -- a future tainted `aws_s3_bucket_policy` on a bucket that
  is NOT empty, or whose live policy has diverged further from the declared one, would carry the same
  delete-then-create mechanism with a materially different consequence (a real window with no Deny on a
  bucket holding data, or a genuine content change happening via delete-then-create rather than an
  in-place `PutBucketPolicy`). If the general LESSON from this incident (`W3-S45`'s taint, `IB-rth-7`'s
  and this cell's identical re-confirmation) is "prefer `terraform import` over `terraform taint` +
  replace whenever the live object already matches (or can be made to match) the declared configuration
  by import alone", that is a standing operational preference this project should carry forward, not a
  one-off judgment specific to these two buckets.

**This worker's own observation, not a verdict:** the two readings are not in tension for THIS act --
both would endorse letting the CTO+COO sign off on either remedy for these specific four resources,
given the measured facts. They diverge only on the FORWARD-LOOKING policy question (Reading 2's "should
this be the default going forward"), which is squarely `3.0.0_SA_CVO`'s to decide, not this cell's.

## Deliverable checklist

- Structured plan measurement (arm a): `battery_ib_rth_8.py --arm measure` stdout, this session, rc=0,
  `IBR85-REPLACE-SEMANTICS-MEASURED-PACKET-WRITTEN` printed.
- Never-widen packet (arm b): `IB-rth-8_NEVER_WIDEN_PACKET.md`, committed @`401f186d62`.
- Sign-off status: NOT obtained this pass (0 CTO halves, 0 COO halves found at HEAD naming `IB-rth-8`).
- Arm (c): NOT RUN, gate not met, confirmed via `battery_ib_rth_8.py --arm apply` (rc=0, "GATE NOT MET",
  no token, no state touched).
- R85-AC3 judgment write-up: above.
