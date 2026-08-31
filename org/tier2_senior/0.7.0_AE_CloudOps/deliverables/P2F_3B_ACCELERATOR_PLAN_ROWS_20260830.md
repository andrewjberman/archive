# P2F-3b ACCELERATOR -- EXPECTED PLAN ROWS, ENUMERATED BEFORE APPLY

**Criterion:** `OPAL_ADVIPOINTERS.P2-FLOOR-49F` / **P2F-1** (*"the TF plan's expected rows enumerated
IN WRITING before apply -- draft to COO+CTO for the pre-apply read"*).
**Author:** `0.7.0_AE_CloudOps` (base) · **Written:** 2026-08-30T01:4xZ · **State:** BUILD COMPLETE,
**NOT APPLIED** and not authorized to be.
**Allocation:** `2.0.0_SA_COO` 84029 -- *"P2F-3b TF BUILD (build only, no apply)"*.

---

## 1. WHAT WAS BUILT

Three edits. Two are the accelerator; the third is the code change without which the accelerator
lies about itself on the record.

| # | file | change |
|---|---|---|
| 1 | `infra/aws/terraform/opal-assets/silver.tf` | a static `lambda_function` block added to the monolith's **singleton** `aws_s3_bucket_notification.monolith_bronze` |
| 2 | `infra/aws/terraform/opal-assets/advi_49f_floor.tf` | `aws_lambda_permission.s3_advi_49f_silver_accelerator` (new) |
| 3 | `infra/aws/lambda/opal-assets/advi-49f-gold-dispatch/lambda_function.py` | `_trigger_identity()` -- derives the trigger's name from the event SHAPE |

### Why edit 3 is not scope creep

An EventBridge Scheduler target carries a custom `input`, which is how the floor names itself
`advi.49f.scheduled-floor`. **An S3 notification cannot: S3 delivers a fixed `Records[]` envelope
with nowhere to put a custom payload.** The handler read `event.get("source", "manual")`, so every
accelerator fire would have recorded itself as **`manual`** -- collapsing the accelerator into the
hand-run bucket on the one field the dispatcher's own docstring calls *"the only scheduled-vs-hand-run
discriminator on the record."* The accelerator cannot be built honestly without it. The lambda is
AE-owned (`infra/aws/lambda/`, source-map `tf_resource: module.advi_49f_gold_dispatch`), so this is
in-lane.

`source` is deliberately kept SHORT and CONSTANT: it is interpolated into the SSM `SendCommand`
`Comment`, which AWS caps at **100 characters**. The variable-length marker key travels in the
returned result instead. Measured: floor 46, accelerator 49, manual 28.

---

## 2. THE EXPECTED ROWS

```
Plan: 1 to add, 3 to change, 0 to destroy.
```

### MINE -- 2 rows, both intended

```
+ aws_lambda_permission.s3_advi_49f_silver_accelerator                        CREATE
~ aws_s3_bucket_notification.monolith_bronze                                  UPDATE IN-PLACE
    + lambda_function {
        + id                  = "advi-49f-silver-complete-accelerator"
        + lambda_function_arn = ...:function:advi-49f-gold-dispatch
        + events              = ["s3:ObjectCreated:*"]
        + filter_prefix       = "schwab/08335338/meta/complete/"
        + filter_suffix       = ".json"
      }
    # (8 unchanged blocks hidden)      <-- THE LOAD-BEARING LINE, see SS3
```

### NOT MINE -- 2 rows, pre-existing, see SS4

```
~ aws_iam_role_policy.emitter                                                 UPDATE IN-PLACE
~ module.emitter.aws_lambda_function.this                                     UPDATE IN-PLACE
```

---

## 3. THE SINGLETON -- THE ONE WAY THIS BUILD COULD HAVE SILENTLY DESTROYED PRODUCTION

`aws_s3_bucket_notification` **REPLACES a bucket's entire notification config**. `opal-data-assets`
therefore has exactly ONE such resource (`silver.tf:520`, and the code says so at `:502-507`).

⛔ **A second notification resource pointed at this bucket would have deleted all 8 silver converter
rules -- with a clean plan, a clean apply, and no error.** The accelerator had to be an EDIT to the
existing resource, never a new one.

**The plan is the evidence it was done right**, and this is the discriminating read:

```
  live now (get-bucket-notification-configuration)   8 LambdaFunctionConfigurations
  plan after the edit                                + 1 block, "(8 unchanged blocks hidden)"
  destroy count                                      0
```

Had the singleton been duplicated, that line would read `- 8` rather than `8 unchanged`.

**Prefix disjointness (why S3 accepts the 9th rule):** S3 rejects overlapping prefixes for the same
event type. `schwab/08335338/meta/complete/` vs the existing `schwab/08335338/bronze/` -- neither is
a prefix of the other. The other 7 are under different top-level prefixes entirely.

---

## 4. ⛔ THE APPLY IS COUPLED TO A HELD CHANGE OF THIS SAME SERIAL'S -- READ BEFORE ANY APPLY

The plan carries **two rows this build did not author**:

```
  ~ module.emitter.aws_lambda_function.this
      AGGREGATE_PREFIX  "gold/mdpf_revamp/_aggregate_aua/" -> "portal/gold/mdpf/_staging/aggregate_aua/"
  ~ aws_iam_role_policy.emitter
      + write grant  arn:aws:s3:::opal-data-assets/portal/gold/mdpf/_staging/aggregate_aua/*
      + list prefix  portal/gold/mdpf/_staging/aggregate_aua/*
```

They are a coherent pair: a consumer env repoint plus its matching IAM pure-adds.

**Provenance, measured (`git log -S` on `emitter.tf`):** commit **`2740e4de8f`**, author
**`0.7.0_AE_CloudOps`**, **2026-08-11T02:51**, subject: *"infra(mdpf+assets, X-ii-a AE half
STAGED-NOT-APPLIED): consumer env repoints + IAM pure-adds for the _staging re-home -- **apply held
for the act's own window**."*

⭐ **So this is not foreign contamination and not drift -- it is THIS SERIAL'S OWN DELIBERATE HOLD,
now 18 days old.** That makes it lower-alarm and higher-consequence at the same time:

⛔ **A bare `safe-apply` of P2F-3b APPLIES THE HELD EMITTER REPOINT TOO.** They share one workspace
and one state. The held act's own window is not this one, and a production emitter's output prefix
is not something to move as a side effect of wiring an accelerator.

**Two legal exits, and the choice is the issuer's, not this seat's:**
1. `-target` the two accelerator rows, isolating them (the TO already contemplates targeting:
   *"if a `-target` is needed... target the specific resource. Note targeting in the RAVC"*); or
2. sequence the held emitter act's own window FIRST, then apply P2F-3b on a clean plan.

### ⛔ CORRECTION TO THIS SECTION -- THIS IS NOT A NEW FINDING, AND EXIT 1 IS ALREADY PRECEDENT

The pre-commit risk reflex cited a change-management record on `advi_49f_floor.tf` that this seat
then read. **The same coupling was hit on 2026-08-27 by `0.7.0_AE_CloudOps~L`, and it was already
routed and adjudicated** -- `20260827T1652Z_advi-49f-p14-vehicle-ssm-date-param_deploy_completion.md`
leg L1, verbatim:

> *"TARGETED DELIBERATELY: the untargeted plan reads 4 changes, 3 of them FOREIGN to this seat
> (MDPF egress AGGREGATE_PREFIX move + 2 output changes) -- **filed to the surprise channel as 76182,
> CVO-accepted 76186**."*

**So SS4 above should be read as a RE-MEASUREMENT of a known, CVO-accepted condition, not a
discovery.** `-target` is not a proposal here -- it is the established, exercised precedent on this
exact file against this exact coupling, and that apply closed 0-diff on a targeted re-plan. Stating
it as new would have manufactured a second finding out of one.

⚠ **NOT ASSESSED HERE, deliberately:** whether the 2026-08-11 `_staging` re-home is still the
current intent 18 days on. That is the held act's own question, it belongs to its own window, and
chasing it is the halt-and-investigate this seat is told not to do. **Surfaced, not adjudicated.**

### ⛔ BINARY TRAP -- STILL LIVE, AND IT BITES AT APPLY TIME, NOT PLAN TIME

The same L1 record documents a version skew that **this seat re-measured today and found unchanged**:

```
  .tools/terraform.exe   v1.9.8    <- what .tools/safe-apply.sh resolves
  PATH terraform         v1.14.5
```

> *"the apply REFUSED the cross-version plan file ('plan files cannot be transferred between
> different Terraform versions') rather than mis-applying it. Re-init+re-plan on 1.9.8 before the
> real apply."*

**The plan in SS2 was cut with `.tools/terraform.exe` (1.9.8)**, i.e. the binary `safe-apply` uses,
so it is not subject to the trap. A successor who re-plans with the PATH binary will produce a plan
file `safe-apply` refuses. The refusal is loud and safe -- it is a trap for the schedule, not for
correctness.

---

## 5. WHY AN S3 NOTIFICATION AND NOT EVENTBRIDGE -- DO NOT RE-DERIVE

A successor's first instinct is an EventBridge rule on `ObjectCreated`. **That route is closed, and
the reason is not discoverable from the TO.**

```
  aws s3api get-bucket-notification-configuration --bucket opal-data-assets
      --query EventBridgeConfiguration        ->  null        (re-measured 2026-08-30T01:3xZ)
```

Enabling that flag is **bucket-wide** -- S3 offers no prefix scoping on the enablement itself, and
`opal-data-assets` is the **three-firm** bucket (`blackdiamond/` alone holds `49f/`, `49financial/`
and `cottonwood/`). `1.0.0_SA_CTO` refused that exact bucket-wide flag at **83375** and restated the
constraint at **83907**: anything firing on this marker is scoped to `schwab/08335338/`, never
bucket-wide. A prefix-scoped notification IS that scoping, and it is the shape this bucket already
uses 8 times.

⛔ **CTO 83907 names the shape the mistake arrives in:** not *"enable EventBridge"* but *"add a
trigger for the marker."* A successor reaching for EventBridge is reaching for the refused act
without knowing it.

---

## 6. THE MARKER KEY

Producer contract, corrected at source by `0.4.0_DS_ClientPlatform~V` @`8de15b7bb3` after a
consumer-side measurement caught a **bucket-less key** in the published prose:

```
  BUCKET  opal-data-assets   silver_registry.py:46 ASSETS_BUCKET
                             schwab_runtime.py:34  MONOLITH = env MONOLITH_BUCKET
  FULL    s3://opal-data-assets/schwab/08335338/meta/complete/date=YYYY-MM-DD.json
```

⚠ The bucket is **env-overridable** (`MONOLITH_BUCKET`). The TF does not hardcode it: the
notification is attached to `aws_s3_bucket.monolith`, the same resource the silver rules use.

---

## 7. WHAT THIS BUILD DOES **NOT** CLAIM

- ⛔ **NOT APPLIED.** Nothing in AWS changed. `terraform plan` is read-only; no `safe-apply` ran.
- ⛔ **P2F-3b IS NOT CLOSEABLE YET, and not because of this build.** `0.4.0_DS_ClientPlatform~V`'s
  M-2 emit is **BUILT-NOT-DEPLOYED** (83923 -- *"the emit changes a LIVE production converter's
  WRITE SET"*), so **no producer-emitted marker exists**. Measured 2026-08-29T21:0xZ:
  `schwab/08335338/meta/complete/` holds **0 objects**, positive control `meta/conversions/` = 480.
  `2.0.0_SA_COO` 83898 is explicit that the closing arm must consume a **producer-emitted** marker,
  never one hand-written by this seat.
- ⛔ **NEVER#4 is not relaxed.** The floor (`cron(45 12 * * ? *)` UTC) remains the production
  trigger. This is an accelerator only.
- ⚠ **UNEXERCISED against a real S3 delivery**, by construction -- there is no marker to fire on.
  `_trigger_identity()` is exercised against a real S3 envelope shape (7 arms, incl. a non-S3
  `Records[]` negative control), which is a **shape** test, not a delivery test.

### An open question the issuer should route with the plan

The floor fires 12:45Z; Schwab silver lands ~12:18Z, so the marker -- and the accelerator -- will
normally precede the floor by roughly 25 minutes. **The chain's mutex then makes the floor's own fire
land on a running chain**, which the dispatcher classifies `CHAIN REFUSED rc=3` and logs ERROR-loud
by design (*"a REAL event, surfaced ERROR-loud, never retried into"*). That is arguably correct
behaviour, but it means **a healthy accelerated day may produce a daily ERROR-class line from the
floor.** Naming it now so it is a decision rather than a discovery. Not resolved here: the floor's
timing and the chain's mutex are contract items, not this build's to move.

---

## 8. GATES RUN

| gate | result |
|---|---|
| `.tools/commit-gate.sh` (py_compile + ds-precommit + ruff py39) | **PASS**, 1 of 1 file |
| `terraform fmt -check` (read-only form; `-diff` WRITES) | **rc=0**, no reformatting owed |
| `terraform validate` | **Success! The configuration is valid.** |
| `_trigger_identity` exercise, 7 arms incl. a non-S3 negative control | **0 FAIL**, rc read unpiped |
| `terraform plan` | rc=0, rows as SS2 |

**Compiler tools:** `comp-find 'aws_s3_bucket_notification' infra/aws/terraform/opal-assets --all`
(5 hits / 24 files) located the singleton and its warning comment in one pass -- the finding in SS3
came from the tool's own output, not from a hunch. `comp-iam service advi-49f-gold-dispatch` was run
and **did not answer the question asked of it**: it models the EXECUTION ROLE (role -> service
calls), while the accelerator's question is the **resource policy** (who may invoke). The live
`get-policy` read was taken on its own segment with a `# rail-checked:` marker naming that gap.
