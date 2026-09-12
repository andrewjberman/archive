# `battery_ib_rt_9.py` -- RT9-AC1, FIVE ARMS OF SIX

**Invocation the task order names, run verbatim:**

```
timeout 900 python org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~3/battery_ib_rt_9.py
```

**rc 0 | checks failed: 0 | ARMS RUN: 5 of 6 | `grep -c IBRT9-BROKER-FENCED` on the output = 0**

Full output: `IB-rt-9_RT9-AC1_battery_output.txt`. Arm (a) excerpt of the same run:
`IB-rt-9_RT9-AC1_arm_a_output.txt`.

> **RT9-AC1 IS NOT MET AND THE TOKEN IS ABSENT ON PURPOSE.** The criterion needs arms (a)
> through (f) in ONE run. Arm (e) is BLOCKED by row `IRPT_BCKEND-W3-S26`. The `<expect>` is
> graded as a REGEX over this output, so a line reading `<token>: NOT ASSERTED` would MATCH
> and grade an incomplete run PASS -- which is why the token appears nowhere, in no form,
> including negated. It goes in only in the edit that makes arm (e) run.

---

## The arms, and what makes each one discriminate

A passing arm that would also pass if the mechanism were broken proves nothing. Every arm
below carries the control that separates those two worlds, and the control is named beside
the result.

### (a) THE CUTOVER, EVERY READER -- `5 of 5`

```
DENOMINATOR: 33184 file(s) scanned (git ls-files, tracked) | 64 name the secret | 10 are CODE
             | 6 of those RESOLVE it (a Secrets Manager read API) | 4 only MENTION it
             | 1 of the resolvers is this cell's OWN TEST HARNESS, listed and excluded
a1 readers migrated or retired: 5 of 5
a2 legacy any-non-403 probes remaining: 0      (6738 code files scanned, 6185 stripped)
a3 new predicate correct on every recorded case: 14 of 14   (old predicate wrong on 10)
a4 END TO END: every probe 400 -> verdict=STALE, SessionFresh=[0.0]
```

* **Discriminator, a1:** a READER is code that calls a Secrets Manager read API; a MENTION is
  not. 4 of the 10 code files that name the secret only mention it.
* **Discriminator, a2:** the detector carries a POSITIVE control (it fires on the retired
  predicate verbatim) and a NEGATIVE control (it stays silent on `ycharts_session.js:272`,
  a correct `403 -> refused` line that an earlier shape of this detector wrongly flagged).
* **Discriminator, a3:** the old and new predicates DISAGREE on 10 of 14 recorded cases. A
  matrix on which both agree would prove nothing.
* **Discriminator, a4:** the same recorded run under the OLD predicate reports FRESH. The
  cutover is measured on the deployed path, not on `classify()` alone.
* The arm moved TWICE this session and was answered by DECLARING the new member, never by
  widening the discriminator: rows `W3-S29` (the battery counting itself once its own file
  became tracked) and `W3-S33` (the new broker, caught before it was declared). The HARNESS
  exclusion carries its own control asserting it removed 0 declared estate readers.

### (b) FENCING -- 3 of 3 race cases, on the runner's OWN `persistSession`

```
b1 SIMULTANEOUS   lease A ok=True fence=1 | lease B ok=False CONDITIONAL_CHECK_FAILED
                  loser raises LeaseError (LEASE_NOT_HELD); 1 put call; digest unchanged
b2 SLOW RUNNER    A fence=1 -> lease expires -> B takes over fence=2 -> B publishes
                  A's late write: FenceError/FENCED my_fence=1 stored_fence=2
                  published digest aa2dd8a25ea8 == aa2dd8a25ea8  (UNCHANGED by the loser)
b3 NO LEASE       a persist with no held lease reaches the secret 0 times
```

* **The published version is compared over its BYTES** (SHA-256 prefix of the stored value),
  not over a field that a partial write could leave looking right.
* **Discriminator:** the SAME runner, the SAME bundle, the SAME code path, with a CURRENT
  fence (3) DOES publish and the digest changes. So the refusal is the fence doing its job
  and not a fake that refuses everything.
* **b2 is the case that matters.** A runner whose lease expired mid-capture still holds a
  lease object that looks valid and a session that looks fresh. Nothing at the LEASE can see
  that; only the fence at the WRITE can, which is exactly where the library puts it.
* **Bound, stated:** a real capture attempt includes a browser login and no login runs in this
  order. What is driven is the half that damages the world -- the race and the publication.

### (c) ROTATION -- the new version is used, the old one is refused

```
2 published version(s) of ycharts/session/current | AWSCURRENT now ...-v0002
read 1: state=OK fence=7 generation=capture-generation-0001
read 2: state=OK fence=8 generation=capture-generation-0002
next invocation's capture_generation: capture-generation-0001 -> capture-generation-0002
token VALUES rotated, cookie NAME set unchanged: fingerprint 828c02de839d -> 0efc96f0fce5
THE OLD VERSION: fence 7 against an accepted fence of 8 -> STALE_FENCE
resume onto the OLD generation, via transport.resume_allowed -> False
```

* "The next invocation uses it" is read off `recipe.step_identity`, the same verifier the job
  itself uses -- not off the bundle the battery handed in.
* **Token-value rotation is MEASURED, not claimed,** and no cookie value is printed: the
  evidence is a SHA-256 fingerprint over the whole jar, which moves iff a value moved.
* **Discriminator:** the SAME read of the SAME superseded bundle, unpinned, reads `OK`. So
  `STALE_FENCE` is the fence's doing and not a defect in the bundle.
* The read vocabulary is closed and COVERED, not just its happy member: a legacy flat
  cookie-string bundle reads `NOT_VERSIONED` (graded neither fresh nor stale -- it is not the
  contract), an unset secret `NOT_CONFIGURED`, a non-JSON value `UNPARSEABLE`.

### (d) EVICTION / SELF-HEALING -- on `job.GenerationJob`, the deployed class

```
evicted at step=read_back status=401 -> transport.decision=REFRESH
the JOB'S OWN why for that same step was 'SETTINGS_DRIFTED'   (row W3-S31)
verified three ways: identity_verified=True schema_verified=True transport_verified=True
a 401 mid-job -> ONE broker refresh (refreshes_used=1) -> outcome RECOVERED
resumed at the checkpoint and completed: resumed=True ok=True
NO-RESUBMIT DIFFERENCE CONTROL: 1 create POST with the recovery vs 2 with a restart
a REPEAT eviction -> RETRYABLE_ATTENTION; second refresh refused:
    "refreshes_used==2 (the rule allows exactly 1); generation UNCHANGED"
    request PRESERVED: {"job_id": ..., "request_id": "REQ-ab...", "revision": 0}
CONTROL: a 422 CONTRACT failure at the same step -> NOT_AN_EVICTION, 0 refreshes
```

* **The eviction point is the read-back** -- the first vendor read AFTER the portfolio exists.
  That is the only place where a recovery that restarts instead of resuming is OBSERVABLE, and
  it is observable as a second `POST /model_portfolios/fixed/` counted on the transports' own
  evidence records: **1 with the broker's recovery, 2 with a restart.**
* **The resume is the job's OWN code:** `job.resume()` reconciles the owned object from the
  vendor by its deterministic name, then `job.after_create()` carries on. The broker supplies
  a verified session and a re-entry point, never a replacement chain, and `job.py` was not
  edited.
* **The ONE-refresh rule is CALLED, never restated:** `transport.resume_allowed`. A refusal
  names WHICH conjunct failed, because "the rule returned False" is not something anyone can
  act on.
* **The three verification booleans are EARNED on two different routes** -- schema from the
  transport's own constructor plus an integer fence, identity from `/dashboard/` with the
  library's wrong-user-id control rejected in the same call, transport from a contracted 200
  JSON on `/custom_pdf_reports/generate/...`. Three literal `True`s would have satisfied the
  rule by construction and proved nothing.
* **The 422 control is what makes the arm mean anything.** Without it, "the broker refreshed"
  could not be told from "the broker refreshes on any failure", which is the login storm the
  rule exists to stop.

### (f) NOTHING LEFT THE MACHINE

```
node  infra/aws/ec2/investor-reporting-ycharts (arm b)
  guard=netguard.js installed=True | attempts_observed=1 loopback_allowed=0 external_refused=1
  POSITIVE CONTROL: ycharts.com:443 -> refused=True, external count 0 -> 1
py    investor-reporting/ycharts/session (arms c, d)
  guard=.../netguard.py installed=True | attempts_observed=1 loopback_allowed=0 external_refused=1
  POSITIVE CONTROL: ycharts.com:443 -> refused=True, external count 0 -> 1
0 connection(s) to a non-loopback destination escaped either drive: 2 refused of 2 observed
both guards DEMONSTRABLY able to fire: 2 of 2 positive controls refused and counted
```

* **Every attempt either drive observed WAS the positive control.** Neither drive opened a
  socket of its own, which is the stronger statement -- and also exactly why a bare "0
  external" is vacuous: a guard that was never installed reports the same zero.
* Each guard is installed BEFORE anything under test is evaluated, which is why the drives are
  SUBPROCESSES rather than in-process calls.
* **DECLARED, NOT GUARDED:** arm (a4) makes one AWS control-plane read (`events describe-rule`)
  from the battery process. It is not a vendor call and it is not inside either guarded drive.
  A guard with an allow-list for "our own AWS calls" would have a hole shaped exactly like the
  thing it guards against.

### (e) ABSORBED, STOPPED, CONVERGED -- **BLOCKED, not unbuilt**

Row `IRPT_BCKEND-W3-S26`. The arm requires a `state mv` and an apply of
`infra/aws/terraform/investor-reporting/ycharts/`, and that root's plan carries an unapplied
`handler = "job.lambda_handler" -> "entry.lambda_handler"`. `entry.py` is in no zip and its
imports (`served`, `loaders`) are declared in `files[]` for 0 of 3 functions, so the apply this
arm requires takes `irpt-ycharts-generate` down at its next cold start. The remedy belongs to
cell IB-rt-2. Until it lands, **no run of this battery can satisfy RT9-AC1.**

---

## What was ADDED to the tree by this cell for these arms

| path | what |
|---|---|
| `infra/aws/lambda/investor-reporting/ycharts/session/broker.py` | the broker's Lambda half: `current` + `evict`. `publish`/`lease`/`fence` stay on the capture host. |
| `infra/aws/lambda/investor-reporting/ycharts/session/tests/run_session_suite.py` | arms (c) and (d), under the python netguard; IMPORTS the generation cell's own offline suite rather than copying its fixtures |
| `infra/aws/lambda/investor-reporting/ycharts/session/tests/fakes.py` | a VERSIONED Secrets Manager fake -- it keeps every version and moves AWSCURRENT, which is what makes "the old version is refused" a question that can be asked |
| `infra/aws/ec2/investor-reporting-ycharts/tests/fence_race.js` | arm (b), under the runner's netguard, driving the real `persistSession` and the real `FakeLease` conditional-update semantics |

**No deploy was taken by this cell and no Terraform root was applied.**

## Rows filed from this run

| id | class / hazard | what |
|---|---|---|
| `W3-S31` | OBSERVATION / ARMED | the job has no eviction outcome -- a 401 reads as `SETTINGS_DRIFTED`; `resume_allowed` had ZERO production callers |
| `W3-S32` | OBSERVATION / ARMED | `JobStore` keeps only the latest state, so the `model_portfolio_id` written at SUBMITTED is erased by the next transition |
| `W3-S33` | OBSERVATION / INERT | arm (a)'s census caught this cell's own broker before it was declared -- the table working |
