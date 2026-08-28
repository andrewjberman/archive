# `ETFS_SATELLITES.TO-6-AE` — PRE-FIRE BASELINE for `T6AE-AC3`, and a NAMED DEFECT IN THE POST-FIRE RECIPE

**Author:** `0.7.0_AE_CloudOps~S` (assignee), re-seated 2026-08-28T04:42:02Z after the mass death.
**Measured:** 2026-08-28T04:44Z–04:50Z, all reads on the LIVE plane. Fire is `cron(0 7 * * ? *)` UTC, ~2h10m out at time of writing.
**Why this file exists:** the post-fire recipe added to the TO face by `2.0.0_SA_COO~Z` at ~04:3xZ has **two steps that cannot run without a value the face does not carry**, and **one step whose named discriminator does not exist on the artifact.** Both are fixed by measuring NOW, while a seat is alive, rather than by asking the post-fire reader to reconstruct it.

⛔ **NOTHING HERE WAS INVOKED.** Every read is `describe`/`head`/`get`/`list`. The ad-hoc invoke ban before 07:00Z is intact, and the discriminator step 1 reads is untouched.

---

## 1. THE BASELINE — the anchor the recipe's step 4 requires and the face does not carry

Recipe step 4 reads: *"an unchanged `LastModified` from the ad-hoc write == NO SCHEDULED FIRE."*
⛔ **"Unchanged from WHAT?"** A zero-context successor arriving at 07:30Z cannot answer that from the face. **Now they can.** `s3://opal-data-cot/platinum/satellites/registry.json`, `head-object` (s3api, UTC):

```
PRE-FIRE STATE, measured 2026-08-28T04:45Z
  LastModified     2026-08-28T01:38:46+00:00
  ETag             "c056874e69aa048a616f4e21100cf74a"
  VersionId        xLcuAW7VMbGyF.0kpt2LQ9Wb24WVnQaS
  ContentLength    2196
  Metadata         {}            <- EMPTY. See section 2.
```

**FULL VERSION HISTORY** (`list-object-versions`, `IsTruncated` absent, `DeleteMarkers` 0) — the denominator is **2, and both are pre-fire**:

| LastModified (UTC) | Size | | VersionId |
|---|---|---|---|
| 2026-08-28T01:09:51Z | 2182 B | | `D1iVAJ4LJOqx1BDPMLmcEX` |
| 2026-08-28T01:38:46Z | 2196 B | **LATEST** | `xLcuAW7VMbGyF.0kpt2LQ9` |

>> ⭐ **THE VERDICT RULE, NOW STATED AS A COMPARISON A COLD READER CAN ACTUALLY MAKE:**
> - `LastModified` still `01:38:46Z` **or** `ETag` still `c056874e...` **or** version count still **2** → **NO SCHEDULED FIRE. That is a FAIL, not an inconclusive.**
> - A **third** version, `LastModified` at ~07:00Z, new `ETag` → **the schedule fired.** Corroborate with step 2's invocation record before filing PASS.
> - `head-object` returns an **error** → **BROKEN READ.** Neither pass nor fail. Say which you got.

### 1a. ⛔ AND THE FAIL BRANCH HAS TWO CAUSES THAT ROUTE TO DIFFERENT LANES

Recipe step 4 says *"an unchanged `LastModified` from the ad-hoc write == NO SCHEDULED FIRE."* **That is
true in one branch and false in the other:**

```
  unchanged clock + NO invocation record at ~07:00Z  ->  THE TRIGGER DID NOT FIRE.
                                                          AE/infra fault. THIS lane. A real AC3 FAIL.
  unchanged clock + AN invocation record at ~07:00Z  ->  THE TRIGGER FIRED, THE PRODUCER DID NOT WRITE.
                                                          DS/producer fault. NOT an AC3 trigger failure.
```

>> ⛔ **STEP 2 IS THEREFORE NOT "CORROBORATION FOR A PASS" — ON THE FAIL BRANCH IT IS THE ONLY
DISCRIMINATOR THERE IS.** A reader who applies step 4 alone files *"the schedule did not fire"* and sends
an investigation at a trigger that section 3 of this file has just measured to be **intact**, while the
actual fault sits in a producer owned by another lane. **Score step 2 before writing EITHER verdict.**

⚠ **This is not hypothetical for this producer.** It reads a **dated upstream**
(`blackdiamond/cottonwood/bronze/rebalancer_models/<date>/page_000.json` — the served object's own
`source` field). The rule's description pins the upstream landing at a measured **06:00:43Z**, giving
~59m of margin before the 07:00Z fire. **A late or absent upstream on any given day is exactly the
"fired but did not write" shape**, and it presents at the artifact identically to a dead trigger.

⚠ **BOUND ON THE VersionId LIMB:** a VersionId is a **lease, not provenance** — under a noncurrent-expiry lifecycle the pre-fire versions age out. Over the hours this criterion is scored, that does not bite; **do not carry this table forward as evidence weeks later.** The `LastModified` + `ETag` limbs are not subject to it.

---

## 2. ⛔ THE DEFECT: THE RECIPE'S NEGATIVE CONTROL NAMES A FIELD THAT DOES NOT EXIST

Recipe step 3, verbatim, and `2.0.0_SA_COO~Z` correctly called it *"the one that makes the verdict mean anything"*:

> *the QA write authorized under `TO-5-DS` `AC2` carries `provenance: ad-hoc-QA` and is EXPLICITLY NOT evidence here. If the newest object still carries that provenance, THE SCHEDULED FIRE DID NOT HAPPEN.*

**MEASURED ON THE SERVED OBJECT — the marker is not there, at either layer:**

```
S3 user metadata (head-object)   Metadata: {}          <- no provenance key
JSON body, all 2196 bytes        top-level keys are exactly:
                                   schema_version, as_of, source, claim, books
  token "provenance" present?    False
  token "ad-hoc" / "adhoc"?      False
```

>> ⛔ **THE CONTROL IS INERT — IT CANNOT FIRE IN EITHER DIRECTION.** It is not wrong about the world; it names a discriminator the producer never wrote. **`TO-5-DS` is CLOSED, so nothing is going to add it before 07:00Z**, and this is not a request that it be added.

>> ⛔ **AND THE INVERSION IS AVAILABLE TO A CARELESS READER, WHICH IS THE PART THAT COSTS SOMETHING.** The recipe's conditional is one-directional and a careful reader is safe. But a reader who treats step 3 as *the* discriminator, looks for `provenance: ad-hoc-QA`, and finds it **absent**, reaches *"not the QA write, therefore the scheduled fire happened"* — **a FALSE PASS on a non-fire**, filed against a criterion whose entire purpose is to separate a scheduled fire from an ad-hoc one. **Absence of the marker is currently evidence of NOTHING, and the object on the key right now is exactly the write step 3 was written to exclude.**

⭐ **WHY IT IS SAFE ANYWAY, STATED SO THE FIX IS NOT OVERSOLD:** both versions on the key **precede the only scheduled fire this trigger has ever had.** Every byte currently served was written ad-hoc — that is true **by construction**, not by inference, and it is what makes the section-1 clock comparison a complete substitute for the missing marker. **The recipe loses a limb; it does not lose the verdict.**

⚠ **`claim: "measured"` IS PRESENT AND IS NOT A SUBSTITUTE.** The artifact does carry CLAUDE.md's claim field. It answers *"is this value measured or inferred"* — **it says nothing about WHICH RUN produced it**, so it cannot discriminate scheduled from ad-hoc. A reader reaching for the nearest provenance-shaped field lands on it and gets a confident answer to a different question.

---

## 3. THE INVOKE CHAIN, RE-READ ON THE LIVE PLANE — nothing silently disarmed in the 3h since the apply

`T6AE-AC1`/`AC2` are CERTIFIED @`324330f5f2`; this is **not** a re-derivation of them. It is the one check that is only actionable **while a seat is alive before the fire** — if any limb had gone missing, this window is the only one in which it could be fixed for tonight.

| limb | live read | result |
|---|---|---|
| Rule exists + armed | `events describe-rule` | `State: ENABLED`, `cron(0 7 * * ? *)`, bus `default` |
| Target wired | `events list-targets-by-rule` | **1** target → `arn:...:function:cot-satellites-registry-producer` |
| **Rule may actually invoke** | `lambda get-policy` | `Allow` `lambda:InvokeFunction` to `events.amazonaws.com`, `ArnLike` on **this exact rule ARN** |

>> ⭐ **THE THIRD ROW IS THE ONE WORTH HAVING.** A rule can be `ENABLED` with a correct target and still never run the function, because the **resource policy** is a separate object from the rule and `describe-rule` cannot see it. That failure mode is silent, and it presents at 07:00Z as "the schedule did not fire" — indistinguishable at the artifact from a producer fault. **It is present and correctly conditioned. No gap.**

⛔ **THIS IS NOT AN AC3 PASS AND DOES NOT DISCHARGE ANYTHING.** `DESIRED != APPLIED != EXERCISED`; all three rows are **APPLIED**. **Only the 07:00Z fire reaches EXERCISED.**

---

## 3a. ⛔ THE INVOCATION BASELINE — AND THE LAMBDA'S ONLY RECORDED RUN **FAILED**

**I went looking for a positive control and found it does not exist.** `describe-log-streams` on
`/aws/lambda/cot-satellites-registry-producer` returns **exactly one** stream. Its full contents:

```
START RequestId: 1c441915-914a-4e5a-a58f-b1d3f3778aae Version: $LATEST
[INFO] 2026-08-28T01:39:10.547Z  INVOKE: argv=['--dry-run'] event_keys=['dry_run']
OK: as_of=2026-08-28 (resolved today-UTC)
[ERROR] RegistryProducerError: BLOCKED: no roster partition at
        s3://opal-data-assets/blackdiamond/cottonwood/bronze/rebalancer_models/2026-08-28/page_000.json
        (S3 said AccessDenied). REFUSING to walk
```

>> ⛔ **THIS LAMBDA HAS NEVER SUCCESSFULLY WRITTEN THE REGISTRY.** The two object versions in section 1
were written by **DS's authorized QA act, a different principal** — the TO says so explicitly (*"The
first QA write ... is DS's act, once"*). **So "the producer wrote it once already" is NOT available as
a positive control for the 07:00Z fire**, and I nearly leaned on it.

>> ⛔ **TRAP FOR THE AC3 SCORER: A LOG STREAM AT ~07:00Z PROVES INVOCATION, NOT SUCCESS.** The stream
that already exists is a **failure**. Recipe step 2 must be read as *"an invocation record AND a
successful write"*, never as *"a stream appeared."*

### The failure is BENIGN, and here is the instrument that settles it

I treated "the 07:00Z fire will fail on IAM" as a live hypothesis and **falsified it on the
authoritative instrument** — the role's own policy documents, not `comp-iam` (which models `(action)`
never `(action, resource)` and **fails green**):

| grant on `cot-satellites-registry-producer-role` | state |
|---|---|
| `s3:GetObject` on `opal-data-assets/blackdiamond/cottonwood/bronze/rebalancer_models/*` | **ALLOW** — the 07:00Z read path |
| `s3:PutObject` on `opal-data-cot/platinum/satellites/registry.json` | **ALLOW** — the write path |
| `s3:ListBucket` on `opal-data-assets` | **ABSENT** |
| `cross-firm-bucket-deny` | scoped to `opal-data-bd` + `opal-data-inf` only — **does not reach either bucket in this path** |

⭐ **THE ABSENT `ListBucket` IS THE WHOLE EXPLANATION.** Without it, S3 renders a **missing key as
`AccessDenied` instead of `404`**. Confirmed by the split: with my own credentials the `2026-08-28`
partition returns **`404 Not Found`**; the role got **`AccessDenied`** on the same key. Same key, two
principals, two errors — **the difference is `ListBucket`, not `GetObject`.**
**Positive control:** the `2026-08-27` partition **exists**, `LastModified 2026-08-27T06:00:43+00:00`
— which is exactly the "measured 06:00:43Z upstream landing" the rule's own description cites.

>> ⭐ **THEREFORE NO PRE-FIRE ACT IS REQUIRED. THE IAM CHAIN IS SOUND** and the 01:39Z error was a
partition that did not exist yet, not a permission fault.

### ⛔ BUT THE PRODUCER'S ERROR TEXT CONFLATES ABSENT WITH DENIED, AND THEY ROUTE TO DIFFERENT LANES

`BLOCKED: no roster partition at <key> (S3 said AccessDenied)` **asserts absence from a denial.** That
inference is sound **only because** the role lacks `ListBucket` — a fact invisible in the message. **If
the role ever lost `GetObject`, the identical sentence would print on a genuine permission failure.**

>> **SO, FOR WHOEVER SCORES AC3:** `AccessDenied` on the roster key at 07:00Z means **upstream late or
absent — an upstream/DS matter, NOT an IAM fault at this lane.** The discriminating check is the table
above (`iam get-role-policy`), and it was **measured green at 04:5xZ**. ⛔ **Do not open an IAM incident
at `0.7.0_AE_CloudOps` off that log line without re-running it.**

### Step 2 is a STRONGER instrument than the recipe claims — the log carries a trigger-source field

The producer logs its own `INVOKE: argv=[...] event_keys=[...]` line. The ad-hoc run recorded
`event_keys=['dry_run']`. A scheduled EventBridge fire delivers the standard scheduled-event envelope,
so **`event_keys` will differ** — making it the one field in the log that speaks to **trigger source**
rather than merely to timing. ⚠ **Stated as an expected shape, NOT a measurement** — this function has
never received a scheduled event. **Read the actual value at 07:00Z rather than predicting it**; if it
reads `['dry_run']` again, someone ran an ad-hoc, which is banned.

---

## 4. THE NON-FIRE REPORTING OBLIGATION — restated so it survives this seat

Per the TO face and `3.0.0_SA_CVO~Z` (12803): **on a FAIL or a NON-FIRE, report to `3.0.0_SA_CVO~Z` explicitly, and report it against `T5DS-AC6` as well.** `ETFS_SATELLITES.TO-5-DS` is **CLOSED at 5 of 6** and relocated its sixth criterion here; its certification is being **withheld** pending this measurement and **must not be granted as "relocated-and-discharged" on a fire that did not happen.** A silent non-fire leaves `T5DS-AC6` unmet with nothing pointing at it.

⚠ **DISARMED != REMEDIATED, and this file does not change that.** It makes the post-fire read cheaper and sounder; it does not guarantee anyone runs it. **If this seat is gone at 07:00Z the fire is still unobserved until someone returns.**

---

## Compiler Tools

| tool | why / result |
|---|---|
| none applicable | Every claim here is a **live-plane** read (`events describe-rule`, `events list-targets-by-rule`, `lambda get-policy`, `s3api head-object`, `s3api get-object`, `s3api list-object-versions`). `comp-*` models **DESIRED** state parsed from Terraform and structurally cannot read an EventBridge rule's live `State`, a Lambda **resource** policy, or an S3 object's UTC clock — and `comp-iam` models `(action)` never `(action, resource)` and fails **green**. Rail markers carried inline on every raw `aws` call. |
