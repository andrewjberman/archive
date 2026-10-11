# SMARTX_DEPLOY_SURVEY -- NFRA_IAMROLES202609.TO-IAM-x-6 PHASE A (E4's act)

**Cell:** IAM-x-6, workstream `SMARTX_DEPLOY`. **Executed by:** `0.7.0_AE_CloudOps~IR`.
**Authority:** `1.0.0_SA_CTO~Z` @`20c0a85d55` (DEPLOY all three), ruled on this lane's own table
`SMARTX_DRIFT_TABLE.md` @`c951e42cae`. **PHASE A GO:** the issuance @`935b63a027`.
**Measured:** 2026-10-11 ~12:2xZ, shared tree, `-lock=false`, plan saved with `-out`.
**READ-ONLY. Nothing was applied.**

---

## 1. THE REQUIRED LINE

```
PLAN: smartx-pipeline: Plan: 0 to add, 3 to change, 0 to destroy.
```

## 2. PER FUNCTION -- the version transition, the hash, and what the apply actually changes

| function | `s3_object_version` before -> after | `source_code_hash` | **live `CodeSha256` now** | does the apply change RUNNING code? |
|---|---|---|---|---|
| `assets_daily_pull` | `XmkW9C_XX1J_6sREU2VZ2naPbfmRQa7O` -> `QNIiMQgfRzxG_KrI_6mVxJDjJbZFOnsd` | **UNCHANGED** `4Iw0TWcez71pRQoUK0GXPxGMOAsVMIgMBIGhk+JRk8k=` | `4Iw0TWcez71pRQoUK0GXPxGMOAsVMIgMBIGhk+JRk8k=` | **NO** |
| `jwt_refresher` | `lRZrP4cIcsSbeYBd8SIB6_W8No75LiDw` -> `HAmOeAkTP0mT6304E9OvUVTpk_GhC8hh` | **UNCHANGED** `MCsLEpIgbLtNDTbSDke9CnlBCmxEhN5slexYv2FIjSc=` | `MCsLEpIgbLtNDTbSDke9CnlBCmxEhN5slexYv2FIjSc=` | **NO** |
| `rest_pull` | `Way7ManCnOWA8bAdT8YIAzZ0ncPu4ino` -> `g_1WqvOSlrPbM1uf8nFcy0uG9SB4xXwb` | `SnPiO8B8AxABQOxJ2wfoPDFaCxaVeGmcDsVPv0JrzaE=` -> **`lM6cnuZTetkFwkGmxQqBFslExfqwGp+WhqFYOYM81xE=`** | `SnPiO8B8AxABQOxJ2wfoPDFaCxaVeGmcDsVPv0JrzaE=` | **YES** |

**THE LIVE HASHES PLACE EACH FUNCTION EXACTLY, and that is what makes this a one-function deploy:**

- For `assets_daily_pull` and `jwt_refresher` the live `CodeSha256` equals **both** the plan's before and after
  `source_code_hash`, so the apply moves a version POINTER at content already running. Attributes differing:
  `last_modified` and `s3_object_version` only.
- For `rest_pull` the live `CodeSha256` equals the plan's **before** value, so the running bytes are the OLD
  bytes and the apply genuinely replaces them. Attributes differing: `last_modified`, `s3_object_version` **and**
  `source_code_hash`.

**So of three planned updates, exactly ONE changes what executes.** The CTO's ruling establishes what that one
change is: the only difference is **docstring line 3 of `smartx_jwt_reader.py`** (`data/orion` -> `data/inf`),
repo source last changed by **`46d0b98aef`** -- the source map's own `last_deployed_commit`. Only the deploy
never ran.

> **THIS CORRECTS MY OWN x-3 TABLE AND I AM STATING IT AS A CORRECTION.** That table recommended **HOLD** for
> `rest_pull` on the ground that "no commit produced these bytes". The commit exists; what never ran was the
> deploy. I had established ETag inequality between the two object versions and stopped there -- "different
> bytes" -- where the answer to "different HOW" was one artifact download away, which is what the CTO did. Row
> `Z-S41` records both that correction and a second one: the 6,608-byte content first appeared **2026-07-23**,
> not 2026-08-19, and was re-uploaded five times. I had read the VERSION's `LastModified` as the date the
> CONTENT appeared; under S3 versioning those are different questions.

## 3. EVERY OTHER ADDRESS IN THE PLAN -- there are none

```
resource_changes : 47        non-no-op : 3        adds : 0        destroys : 0
non-no-op addresses that are NOT the three functions : []
```

Measured by filtering **every** `resource_change` address, not by reading the summary line. 0 replaces.

### 3a. The three output nulls, with their denominator

```
output_changes : 13 total   ->   3 with actions=['delete'],   10 no-op
  autostart_lambda_arn   delete   after=None
  autostart_role_arn     delete   after=None
  eventbridge_rule_arn   delete   after=None
```

**Exactly the three the cell names, and no fourth.** The 10 no-ops are the module's other outputs, unchanged --
printing the denominator is what shows the three deletes are not a sample of a larger removal.

Their removal was **Andrew-ratified**: `a3b36fd877` (2026-08-14, `OPAL_MDPFCLEANUP.TO-3 apply-4`) deleted the
autostart chain including these three `output` blocks, `terraform validate: Success`, ratified @`874b52729c`,
with both functions measured 74 days invocation-silent. x-3 established on two planes that the output names
appear in **0 of 21** configuration files and that their resources are absent from state. **So the nulls
complete a ratified act rather than performing a new one.**

## 4. WHAT PHASE B MUST CHECK BEFORE IT APPLIES

The plan is saved, but **the saved file lives outside the repo** (a scratch path) and PHASE B is a separate
session. The order's own condition is the right one and does not depend on the file surviving: *"safe-apply the
SAVED plan only if it still equals the survey's (0 to add, 3 to change, 0 to destroy, plus the three output
nulls); anything else stops the act."* **If the saved plan is gone at PHASE B I will re-plan and re-grade
against this survey rather than apply an unverified file** -- the equality check is the guarantee, not the
file's persistence.

**One thing PHASE B should expect to find changed, and it is not a defect:** because the module reads
`s3_object_version` from the **live latest** S3 object (row `Z-S41`), any re-upload between now and the apply
moves the after-values in this table. That is the design gap the row records, it has no owning project, and it
is why the equality check matters more here than in a module with pinned versions.

## 5. WHAT THIS SURVEY DOES NOT DO

- **It does not re-argue the ruling.** The CTO ruled DEPLOY all three on my table and corrected two of its
  claims; this survey records the corrected position and measures the plan that implements it.
- **It proposes no fix for the drift class.** `Z-S41` holds it: the module tracks the live latest object, so a
  re-upload of near-identical bytes reads as drift and a hand upload would be adopted silently on the next
  apply. Pinning the version or deriving it from the build is the module owner's choice, and **no project owns
  `smartx-pipeline`** -- which is the actual gap and is recorded as INERT with no owner by the ruling's own
  direction.
- **It takes no view on the two byte-identical functions being worth deploying at all.** They are in the
  ruling's scope, the apply is a pointer re-sync on content already running, and the risk of either is the same
  near-zero my x-3 table measured.

**PHASE A ENDS HERE. Nothing applied; no ledger opened; `-lock=false` throughout so the read could not take a
state lock another seat wanted.**
