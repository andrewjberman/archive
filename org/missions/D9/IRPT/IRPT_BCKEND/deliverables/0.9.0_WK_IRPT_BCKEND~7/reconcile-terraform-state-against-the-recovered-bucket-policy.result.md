# IB-rth-7 -- result (re-hand, worktree wk-irpt_bckend-8-7b)

Worker: `0.9.0_WK_IRPT_BCKEND~7`. Governing order:
`org/missions/D9/IRPT/IRPT_BCKEND/task-orders/IRPT_BCKEND.TO-IB-rth-7.reconcile-terraform-state-against-the-recovered-bucket-policy.md`
@HEAD `8d36fcdb60`.

## Arm (a) -- the plan (leg L3)

Fresh `.tools/terraform.exe init` + `plan -input=false -no-color -refresh=true`, no `-target`, on
`infra/aws/terraform/shared-infra`. Result: **NOT** `0 to add / 0 to change / 0 to destroy`.

Verbatim summary line: `Plan: 4 to add, 0 to change, 4 to destroy.`

The four changed resources are exactly `aws_s3_bucket_policy.lgic_firm["cottonwood"]`,
`aws_s3_bucket_policy.lgic_firm["inflection"]`, `aws_s3_bucket_versioning.lgic_firm["cottonwood"]`,
`aws_s3_bucket_versioning.lgic_firm["inflection"]` -- each printed `is tainted, so must be replaced`.
This is precisely the contingency the order's own arm (a), third bullet, named in advance ("does the
plan show TAINTED resources for versioning/bucket_policy on either firm, left over from the original
2026-09-18 half-landed apply (W3-S45)? If so, that is itself drift and falls under the STOP branch
above."). It fired.

Per BOUNDS ("no terraform apply, no terraform import, no state mutation of any kind, regardless of
what arm (a) finds -- a STOP with a filed row is the only response to drift, never a same-cell fix"):
**no `terraform untaint`, no apply, no state edit was performed.** Full plan output is captured in
`battery_ib_rth_7.py`'s own stdout (this instance's `R83-AC1` acceptance row) and in the fresh run this
session. Ledger leg L3 stays OPEN (no proof recorded).

BLOCKING row filed: `IRPT_BCKEND-W7-S2` (ARMED, disarm_owner `2.0.0_SA_COO~B`).

## Arm (b) -- the negative control (leg L4)

`describe-instances` on `i-02448edb624a7a7cf`: state = `stopped`.

Per BOUNDS ("The host is never started by this cell") and the order's own STOPPED branch, the SSM
negative-control exercises were **not run**. Recorded UNEXERCISED (non-verdict), following
`IB-rtf-5`'s own `R62-AC3` precedent exactly: never a FAIL for a control nobody ran. Ledger leg L4
stays OPEN, host state + reason + owner (`2.0.0_SA_COO~B`, the issuer) recorded in the ledger's Log.

## Arm (c) -- leg L1, the judgment question (for `3.0.0_SA_CVO`, `R83-AC3`)

**The question:** does a clean 0-change plan mean L1 is satisfied by convergence, or does closing L1
properly require an actual (no-op) `safe-apply.sh` run (or a `terraform import` of the two policy
resources) so the state file itself reflects reality?

**This round's plan is not even clean** (see arm a) -- so the narrower question ("if the plan reads
0/0/0, is that alone sufficient?") is not this round's live branch; it is the one the CVO's ruling
should settle for the NEXT run, once the taint is resolved by whatever remedy the COO/CTO choose.
Both readings and their consequences, stated for the record:

- **Reading 1 -- convergence-by-plan suffices.** If a future 0/0/0 plan is treated as sufficient proof
  that Terraform's state already matches AWS (because `aws_s3_bucket_policy`/`aws_s3_bucket_versioning`
  etc. are already IN state from the original 2026-09-18 apply -- only the bucket POLICY BODY diverged,
  and only until the CRO's manual PUT re-converged it), then L1 could close on that plan alone, with no
  further Terraform action. Consequence: the state file was never touched by anything OTHER than the
  original (half-landed) `safe-apply` run and the out-of-band console PUT. The next genuine plan on this
  root is not mis-informed (state already lists these 10 resources with IDs matching what's live), so a
  future `terraform destroy` scoping is accurate. The residual risk is narrow: the TAINT this round found
  (arm a) shows state CAN still diverge from "what a human would call converged" in ways a bare 0/0/0
  reading masks nothing of -- taint is visible IN the plan, so this reading does not hide it.
- **Reading 2 -- L1 needs an actual apply/import.** If "L1: activation ... proof required: apply output +
  resource list" is read literally (the manifest's own words), then nothing satisfies it except a real
  `safe-apply.sh` run that PRODUCES that apply output -- even a no-op one. Consequence: a deliberate no-op
  apply (once the plan is genuinely 0/0/0, taint resolved) is cheap and produces the artifact the ledger's
  own manifest already demands; skipping it means L1 closes on a proof type (`terraform plan output`) that
  is explicitly leg L3's proof, not L1's -- conflating two legs' evidence.

**This worker's own read:** Reading 2 is closer to the ledger's own text -- L1's `proof_required` column
literally says "apply output + resource list", and L3 is the SEPARATE leg whose proof is "terraform plan
output". Reusing L3's evidence to close L1 collapses a distinction the manifest itself drew. But this is
explicitly NOT this worker's call to make (spine v3 L9: judgment criteria are graded by the CVO, never
self-graded) -- `R83-AC3` carries no verdict from this cell.

**What breaks later if state is never reconciled by an apply:** nothing observable TODAY (arm a's plan
already reads the 10 resources correctly against IDs), but the record itself stays permanently silent on
whether the CRO's break-glass PUT was ever formally absorbed by the IaC pipeline -- a future engineer
reading only the ledger (L1 forever OPEN, no apply output ever recorded) would reasonably conclude the
bucket program was NEVER completed through Terraform, which is true in the narrow apply-output sense and
misleading in the practical convergence sense. That ambiguity is exactly what this judgment row exists to
resolve.

## Arm (d) -- the fence-pattern finding, row `IRPT_BCKEND-S116` (carried, measured not re-derived)

**Fence pattern (measured, `infra/aws/terraform/modules/opal_name/generated_locals.tf:65-70`
@`8d36fcdb60`):** `"inflection" = ["arn:aws:iam::313476888478:role/*-inf-*"]`,
`"cottonwood" = ["arn:aws:iam::313476888478:role/*-cot-*"]` -- both require a HYPHEN immediately before
the firm token (`-inf-` / `-cot-` as a literal substring), confirming row S116's carried finding exactly.

**Measured, this session:**

- `infra/aws/terraform/inf-pipeline/`: **28** `resource "aws_iam_role"` declarations (denominator: 28 of
  28 `aws_iam_role` blocks in the directory, `comp-find` content-search cross-checked). Every role name
  begins literally with `inf-` (e.g. `inf-gold-layer-ec2-role`, `inf-api-positions-role`,
  `inf-otp-relay-lambda-role`) -- NONE carry a hyphen before `inf`, so NONE match `*-inf-*`. 0 of 28
  already `opal-inf-*` shaped (estate-wide `name = "opal-inf-"` search: 0 hits).
- `infra/aws/terraform/cot-pipeline/`: **8** `resource "aws_iam_role"` declarations. **7 of 8** begin
  literally with `cot-` (`cot-bd-session-trigger-lambda-role`, `cot-gold-layer-ec2-role`,
  `cot-exporter-ec2-role`, `cot-satellites-characteristics-producer-role`,
  `cot-satellites-registry-producer-role`, `cot-session-scheduler-role`,
  `cot-etf-ownership-daily-role`) -- none match `*-cot-*`. The 8th, `bd-cot-keepalive-role`, IS
  `bd-cot-*` shaped and is excluded per the order's own exclusion list.
- Estate-wide: 0 `name = "opal-inf-*"` roles, 0 `name = "opal-cot-*"` roles anywhere
  (`comp-find` content search, denominators 37008/37009 files scanned, 0 hits both).

**Total: 35 IAM roles (28 inf-pipeline + 7 cot-pipeline, excluding the one already-shaped
`bd-cot-keepalive-role`) carry a name matching `*inf-*`/`*cot-*` but NOT the fence's actually-admitted
`*-inf-*`/`*-cot-*` pattern, and NOT already `opal-inf-*`/`opal-cot-*`/`bd-cot-*` shaped.**

**Do they need write/read access to `opal-data-inflection`/`opal-data-cottonwood` GOING FORWARD?**
Measured: today, NO -- `infra/aws/terraform/inf-pipeline/iam.tf` (and every other inf-pipeline `.tf`)
grants these 28 roles access only to `opal-data-inf` (the LEGACY short-name bucket; e.g.
`Resource = "arn:aws:s3:::opal-data-inf/*"`, 8+ distinct statements). `comp-find 'opal-data-inflection'`
scoped to `infra/aws/terraform/inf-pipeline/` returns **0 of 45 files** scanned. Symmetric for
cot-pipeline/`opal-data-cottonwood` (0 of 19 files). This matches the estate's own standing note that
legacy `bd`/`inf`/`cot` buckets stay the ACTIVE channel until the D14 full-name migration -- the two new
full-name buckets this project created (IB-rte-3) are empty, un-read, un-written by any pipeline today.

**GOING FORWARD (post-D14 cutover):** these are precisely the firm's OWN inf/cot pipelines -- the ones
that will need to read/write `opal-data-inflection`/`opal-data-cottonwood` once the migration happens.
At that point, on today's `fence_patterns()`, all 35 roles would be DENIED by the Deny-fence's own
`ArnNotLike` condition (none matches `*-inf-*`/`*-cot-*`), unless `fence_patterns()` is fixed or the
roles are renamed first. This is an EXPOSURE (Rule 22's negative mirror): real, not yet fired (no
inf-/cot- pipeline has attempted a write to the new buckets since neither pipeline references them yet).

**Reported to the COO, not landed:** `fence_patterns()` lives in
`infra/aws/terraform/modules/opal_name/generated_locals.tf`, a shared-infra module outside this
project's lane -- no edit made here, per BOUNDS.

## Deliverable checklist

- Plan output (full, both resources named): `battery_ib_rth_7.py` stdout, this instance's `R83-AC1` row.
- Ledger L3/L4 rows: left OPEN with reasons recorded in the ledger's Log (both the `.md` entry and the
  `.open_deploys/` sentinel).
- L1 judgment write-up: above, arm (c).
- S116 measurement: above, arm (d).
