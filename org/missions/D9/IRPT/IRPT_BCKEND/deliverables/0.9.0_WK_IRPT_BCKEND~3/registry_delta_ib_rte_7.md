# IB-rte-7 -- the registry delta for the CTO to land (steps 2-3 of its remedy)

**Author:** `0.9.0_WK_IRPT_BCKEND~3`. **Order:** `IRPT_BCKEND.TO-IB-rte-7`. **Grant note:**
`infra/logic/registry/**` is NOT in this order's `<paths>` -- this file is a DRAFT for `1.0.0_SA_CTO`
to land in its own commit (Rule 30: a builder/registry edit is the CTO's, never a worker's typed
workaround). Nothing in `infra/logic/registry/` was committed by this order; every local edit used to
produce and test this delta was restored to HEAD's bytes before this order's own commit (`git status
--porcelain -- infra/logic/registry/` printed EMPTY after each restore -- see `battery_ib_rte_7.py`
output and `IB-rte-7_R57-AC1_battery_output.txt`).

## 1. The drafted field, its name and its value token

- **Field name:** `bucket_managed_by`.
- **Value token:** `s3-lgic-firm-buckets.tf` -- the name of the Terraform file that manages a row
  carrying this value. It names a DECLARATION, never a firm: LGIC_ENFORCE DEC-6 (naming-gate.py) has
  nothing to refuse in either the field name or the value, because neither is a firm or product token
  (verified: `lib/opal_naming.py`'s `carrier()` check finds no firm/product spelling in either string,
  and `classify()` places neither as an S3 key/bucket/resource-name shape -- read at
  `.tools/naming-gate.py:614-625` and `:570-612` @HEAD).
- **Reason for this shape, one line:** the old selector's `bucket_provisioned == false` was doing two
  jobs under one flag -- "this bucket is real" (the naming gate's reading, `exemptions.json`'s own
  `_about`) and "this bucket is handled elsewhere" (`s3-lgic-firm-buckets.tf`'s reading). The new field
  answers ONLY the second question, so the flag can answer only the first, and the two registry facts
  stop fighting over one bit.

## 2. THE MEASUREMENT THAT GATES THIS SHAPE (ruling amendment, run FIRST, before any plan)

Per `2.0.0_SA_COO~B`'s ruling on this order (relaying the CTO's own precondition, msg 98090 /
`IRPT_BCKEND_STEP1_WITHDRAWN_DRAFTED_FIELD_ADOPTED_20260919.md` @80dada6d8d): the field is landable
ONLY if `python lib/opal_naming.py validate` (the same validator the naming gate runs before grading
any diff, `.tools/naming-gate.py:999-1008`) does not refuse an unknown field on a `scopes.json` row.

**Measured, not assumed:** `bucket_managed_by` was added locally (uncommitted) to the `inflection` and
`cottonwood` rows and `python lib/opal_naming.py validate` was run against that registry:

```
VALIDATE: OK 25 system row(s), 9 scope row(s), 17 warning(s) at registry@5b52a3729f4c7d21
```

**rc=0, zero refusals.** Reading `lib/opal_naming.py validate()`'s `scopes.json` loop (`:322-389`
@HEAD) confirms WHY: unlike `resources.json`'s row check (`RES_FIELDS`, `:504-506`, which explicitly
refuses `set(r) - set(RES_FIELDS)`), the `scopes.json` loop enumerates required fields and checks their
SHAPE but never computes `set(row) - <closed set>` -- there is no field-closure check on a scope row at
all. **The drafted field is landable as measured; this is the CTO's input for its own commit, not a
workaround built here.**

## 3. The unified diff (the two flags + the field, nothing else)

Applies cleanly to HEAD's bytes (`git apply --check`, rc=0, verified this order):

```diff
--- a/infra/logic/registry/scopes.json
+++ b/infra/logic/registry/scopes.json
@@ -123,7 +123,8 @@
       "short": "inf",
       "tenancy": "FIRM",
       "bucket": "opal-data-inflection",
-      "bucket_provisioned": false,
+      "bucket_provisioned": true,
+      "bucket_managed_by": "s3-lgic-firm-buckets.tf",
       "monolith_scopes": {"orion": ["inflection"], "eclipse": ["inflection"]},
       "tenant": {
         "display_name": "Inflection Wealth Management",
@@ -161,7 +162,8 @@
       "short": "cot",
       "tenancy": "FIRM",
       "bucket": "opal-data-cottonwood",
-      "bucket_provisioned": false,
+      "bucket_provisioned": true,
+      "bucket_managed_by": "s3-lgic-firm-buckets.tf",
       "monolith_scopes": {"blackdiamond": ["cottonwood"]},
       "pipeline_trees": [
         {
```

## 4. The Terraform-side reader (this order's own commit)

`infra/aws/terraform/shared-infra/s3-lgic-firm-buckets.tf` (this order's commit, hash printed in the
proof instance):

```
lgic_managed_firm_buckets = {
  for s in local.lgic_registry_scopes.scopes : s.key => s
  if s.class == "FIRM" && (
    lookup(s, "bucket_managed_by", "") == "s3-lgic-firm-buckets.tf"
    || (lookup(s, "bucket_managed_by", "") == "" && s.bucket_provisioned == false)
  )
}
```

`lookup(s, "bucket_managed_by", "")` so a registry that has not yet carried the field (every row today)
still resolves the second branch exactly as the old selector did.

## 5. The exemption rows: pointer only, NOT redrafted here

Steps 2-3 of the CTO's remedy also add six exemption rows to `infra/logic/registry/exemptions.json`
(three per bucket: `Andrew_Berman`, `Andrew_Berman_Console`, `Opal_Terminal`). **Those rows are the
CTO's** (its registry-deadlock record, `org/missions/D9/IRPT/IRPT_BCKEND/deliverables/1.0.0_SA_CTO/
IRPT_BCKEND_REGISTRY_DEADLOCK_NEW_FIRM_BUCKETS_20260918.md @9eeb9a70a8`, section "THE ROWS I HAD
WRITTEN, AND WHY THEY ARE WORTH RE-USING AT STEP 3") -- this draft does not redraft them, does not
mirror 49financial's admit set, and does not copy its `reason` text, per this order's own bound. This
order's `battery_ib_rte_7.py` built its OWN throwaway rows, in the shape the CTO's record describes, to
exercise PLAN-2 locally; those rows were never committed and are not this draft's content (see
`battery_ib_rte_7.py` and the surprise row `IRPT_BCKEND-W3-S45` for exactly what they said and why they
are not a substitute for the CTO's own six rows).

## 6. What the three plans proved about this shape

- **PLAN-1** (this order's new selector, HEAD's unmodified registry) vs the SAME plan under HEAD's
  original selector: **0 differences** in the resource/action list (both erroring identically under a
  live refresh -- the pre-existing lockout named in row `IRPT_BCKEND-W3-S43` -- and, with
  `-refresh=false`, both reading an identical `4 to add, 0 to change, 4 to destroy` from a pre-existing,
  registry-independent state taint). The new selector is a NO-OP against today's registry, as designed.
- **PLAN-2** (new selector + this delta + throwaway exemption rows, local/uncommitted): the SEMANTIC
  diff attributable to the registry edit, isolated from the pre-existing taint by comparing against
  PLAN-1's `-refresh=false` run, is EXACTLY the three exemption ARNs landing in each policy's
  `ArnNotLike` list -- nothing else. See row `IRPT_BCKEND-W3-S45` for the full account of why the raw
  literal "0 to add, 0 to destroy" bound cannot be measured today (a pre-existing, already-ARMED lockout
  blocks a live plan from completing at all, and the only completed plan carries an unrelated,
  registry-independent taint).
- **PLAN-3** (HEAD's ORIGINAL selector + this same delta, the mutant): **`0 to add, 0 to change, 10 to
  destroy`** -- every `lgic_firm` resource for both firms, each annotated "because key [...] is not in
  for_each map". This is the destroy the CTO's registry-deadlock record predicted for the OLD selector;
  the new selector (PLAN-1/PLAN-2) never produces it.

Full evidence, verbatim plan excerpts and content hashes: `battery_ib_rte_7.py`,
`IB-rte-7_R57-AC1_battery_output.txt`, and the proof-of-spec instance.
