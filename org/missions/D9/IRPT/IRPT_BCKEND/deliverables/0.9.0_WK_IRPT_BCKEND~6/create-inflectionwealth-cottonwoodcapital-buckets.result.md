# TO-IB-rth-6 -- result: STOPPED before any registry edit or apply

**Assignee:** `0.9.0_WK_IRPT_BCKEND~6` | **Worktree:** `wk-irpt_bckend-8-6` off CLOUD HEAD `fa3b70b267`

## What Andrew asked for

> "We need to keep moving so if there is no mechanism for us to access these buckets, and our
> work is dependent on these buckets existing, then we need to create
> opal-data-inflectionwealth and opal-data-cottonwoodcapital and take care to not create them
> with restrictive bucket policies that land us in this situation."

## (a) MEASURE FIRST -- confirmed as ordered

- `infra/logic/registry/exemptions.json`: `opal-data-inflection` carries exactly 3 rows
  (`Andrew_Berman`, `Andrew_Berman_Console`, `Opal_Terminal`); `opal-data-cottonwood` carries the
  same 3, identical shape. Denominator: 3 of 3 each, both firms.
- `infra/logic/registry/scopes.json`: `inflection` row -- `bucket: "opal-data-inflection"`,
  `bucket_provisioned: true`, `bucket_managed_by: "s3-lgic-firm-buckets.tf"`; `cottonwood` row --
  identical shape with its own bucket name. Both stale "does not exist yet" alias notes present
  (`opal-data-inf` and `opal-data-cot` aliases) -- located but NOT edited (see below).
- `org/critical_paths/.open_deploys/irpt-bckend-ib-rte-3-lgic-firm-buckets.json`: still `OPEN`,
  opened `2026-09-18T19:49:17Z`, all 4 legs unproven -- the original lockout ledger, never closed.
- `infra/aws/terraform/shared-infra/s3-lgic-firm-buckets.tf` read in full: `for_each` over
  `local.lgic_managed_firm_buckets` (keyed by the registry row's `key` -- currently `"inflection"`
  / `"cottonwood"`, unchanged by `bucket_provisioned`/`bucket_managed_by`), each resource's
  `bucket` attribute reading `each.value.bucket` directly from the registry. `terraform state
  list` (backend `s3://opal-313476888478-terraform-state/shared-infra/tfstate`) confirms the 10
  resources this file already manages under those same keys are LIVE in state, matching the open
  ledger's L1 leg exactly.

## (b)/(c) THE NAMING AND THE REGISTRY EDIT -- STOPPED, not silently forced

Rule 30's own tool refuses the literal edit before `address()`/`name()` are ever reached. A trial
edit (bucket field only, on the `inflection` row's `bucket` -> `opal-data-inflectionwealth`,
`long`/`key` left unchanged as the task order's BOUNDS require) was made, validated, and
IMMEDIATELY REVERTED (never committed):

```
REFUSED scopes.json[1].bucket: 'opal-data-inflectionwealth': a data bucket is opal-data-{scope}, LONG form (NAMING_SCHEMA.json bucket)
REFUSED exemptions.json exemptions.opal-data-inflection: not a provisioned bucket of a FIRM scope in scopes.json
VALIDATE: REFUSED 2 refusal(s), 17 warning(s)
```

Two structural constraints (`lib/opal_naming.py`, both unconditional for FIRM-class rows):
- `:357-358` -- a scope's `key` MUST equal its `long`.
- `:365-366` -- a FIRM/PRODUCT row's `bucket` MUST equal `"opal-data-%s" % long`.

Combined with the task order's own BOUNDS ("Do NOT touch key/short/aliases ... this is a bucket
swap, not a firm rename"), there is **no registry-legal way to change only the bucket field**:
doing so necessarily requires renaming the firm's `key`/`long` too, which is explicitly forbidden
and which -- independently measured -- cascades far beyond these two rows (cottonwood's own
`pipeline_trees.separated_from` names `"inflection"` by spelling; both rows' `monolith_scopes`
name themselves by long form for downstream `orion`/`eclipse`/`blackdiamond` consumers; every
`lookup("inflection")` call site elsewhere in the estate would need the new spelling or a
preserved alias -- and "Do NOT touch ... aliases" forecloses that route too).

Separately, and even if the registry constraint were somehow satisfied: `s3-lgic-firm-buckets.tf`
keys its `for_each` by the registry row's `key`, which is UNCHANGED, and AWS's `aws_s3_bucket`
`bucket` argument is immutable (ForceNew). Editing only the `bucket` value under the same
`for_each` key would plan a REPLACE (destroy-then-create) of the SAME resource address --
destroying the real, already-applied old bucket. That is forbidden by this order's own BOUNDS
("NO delete of the old buckets") and by arm (e)'s plan bound ("anything else in the plan is a
STOP").

Filed: `../../surprise-channel/investigations/INVESTIGATION_v1.md` row `IRPT_BCKEND-W6-S1`
(BLOCKING, ARMED, disarm_owner `2.0.0_SA_COO~B`), with the disarm condition naming three concrete
routes for the COO/CTO to choose from (a full estate-wide rename; a declared naming-law
exception; or re-attempting the ORIGINAL fix -- an exemption-list repair on the buckets Andrew
already has live -- which row S43 diagnosed and which has not been re-attempted since).

**Because this premise never resolved, arm (c).2/(c).3 (exemptions.json edits, the abandonment
note) were never performed** -- there is nothing yet to exempt or abandon, and touching
`exemptions.json` first (as the task order's own ordering insists: registry BEFORE apply, never
the reverse) would be writing exemption rows for bucket names the registry cannot yet legally
carry.

## (d)/(e) THE PACKET AND THE APPLY -- not reached

No never-widen packet was drafted and no CTO/COO signature was sought, because there is no valid
plan to sign off on: the registry premise underlying the Terraform `for_each` selection never
reached a state naming the new bucket names. No `terraform plan`/`apply` was run against
`s3-lgic-firm-buckets.tf`; no change-management ledger was opened (nothing to ledger).

## (f) THE DISCRIMINATING PROOF -- run anyway, on the ACTUAL (unchanged) state

`battery_ib_rth_6.py`, run live as `Andrew_Berman` (`arn:aws:iam::313476888478:user/Andrew_Berman`):

- Registry unchanged: `inflection` -> `opal-data-inflection` (`bucket_provisioned: true`);
  `cottonwood` -> `opal-data-cottonwood` (`bucket_provisioned: true`). Matches pre-cell baseline.
- `python lib/opal_naming.py validate` on the unchanged registry: `VALIDATE: OK 25 system row(s),
  9 scope row(s), 17 warning(s)`.
- `head-bucket opal-data-inflectionwealth` -> `404 Not Found`. `head-bucket
  opal-data-cottonwoodcapital` -> `404 Not Found`. **Neither new bucket exists** -- confirms no
  apply happened, by construction (this worker never ran one).
- `head-bucket opal-data-inflection` -> `403 Forbidden`. `head-bucket opal-data-cottonwood` ->
  `403 Forbidden`. **Both old buckets remain exactly as locked as before this cell started** -- no
  regression, no accidental widening, no accidental narrowing.

Full output: `IB-rth-6_R81-AC1_battery_output.txt` (this directory).

The criterion's `<expect>` token
(`IBR81-NEW-BUCKETS-EXEMPT-IDENTITIES-SUCCEED-OLD-BUCKETS-STILL-DENY`) is honestly UNREACHABLE
from this state and the battery does not print it. It prints the actual, contrasting state
instead and exits `1`.

## Disposition

`<status>` left as `pending -- HANDED` (task order NOT flipped to `complete`). Order stays OPEN.
`R81-AC1` grades `FAIL` (real, measured, honest -- the two new buckets were never created because
the registry premise the apply depends on is refused by its own validator). `R81-AC2` (judgment)
answered for `3.0.0_SA_CVO` below, no verdict taken.

### R81-AC2 (judgment) -- for the CVO

*Whether the registry edits correctly preserve every other firm's entry and whether the old-bucket
abandonment note is accurate* -- **N/A this round**: no registry edit was made (see above), so
there is no edit to check for preservation of other firms' entries and no abandonment note was
written. The only registry state this cell touched was a single trial edit to the `inflection`
row's `bucket` field, made and reverted in the same turn, never committed (confirmed: `git diff`
against `infra/logic/registry/scopes.json` at this deliverable's commit is empty). The live
question for the CVO/COO/CTO is the disarm condition on row `IRPT_BCKEND-W6-S1`: which of the
three named routes (full rename, declared naming-law exception, or re-attempt the original
exemption-list fix on the buckets Andrew already has) resolves the premise this cell is blocked
on.
