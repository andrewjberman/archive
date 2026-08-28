# TO ETFS_SATELLITES.TO-6-AE — the SCHEDULE for the satellites registry producer (`T5DS-AC6`, lifted to its own lane)

<decomp_ref>workflows/atom_decomposition/runs/etfs-satellites/20260827T160438Z/DECOMP.md — cell `SAT-a-4` (delivery form / the served block), INFRA HALF. The producer half is discharged under `ETFS_SATELLITES.TO-5-DS`.</decomp_ref>
<certification>Decomp CERTIFIED (`3.0.0_SA_CVO~Z`). This TO carries NO new cell — it lifts an existing criterion (`T5DS-AC6`) out of a DS-lane TO into the lane Rule 13 assigns it to. No re-certification is sought because no cell is added.</certification>
<issued_to>0.7.0_AE_CloudOps~S</issued_to>
<executor_class>AE-class</executor_class>
<seating_trigger>SEATED 2026-08-28 ~01:0xZ by `0.0.0_AB_MSTR~Z` (pre-flight 1pt CLEAR / 1c 7-of-16 / 1d 0 open TOs). ⛔ **GATED ON `ETFS_SATELLITES.TO-5-DS` AC2** — there is nothing to schedule until a producer exists and has written once. Do NOT build the trigger against an absent producer.</seating_trigger>
<placement>SITE Z — D4 is SITEZ-placed until the project is done (Andrew-direct 2026-08-24, VERBATIM: *"keep D4 on sitez until the project is done"*).</placement>
<issued_by>2.0.0_SA_COO~Z</issued_by>
<issued>2026-08-28T01:0xZ</issued>
<status>ACTIVE — and the ORIGINAL GATE IS DISCHARGED; the only outstanding item is a CLOCK. Refreshed by the assignee `0.7.0_AE_CloudOps~S` 2026-08-28 ~03:3xZ. ⚠ This face previously read *"gated on TO-5-DS AC2, which is RULED OPEN"* — **AC2 was discharged at 01:09:51Z** and that gate has not bound since; the sentence was true when written and stale for two hours. Corrected here rather than left, because a stale REASON on a correctly-classified face is the same class as a stale STATUS: a reader staffing off it acts on a gate that no longer exists.
AC1 / AC2 / AC4 / AC5 are **DISCHARGED and CERTIFIED** by `3.0.0_SA_CVO~Z` @`324330f5f2`. The schedule is LIVE — `cot-satellites-registry-producer-daily`, `cron(0 7 * * ? *)` UTC, ENABLED, wired to `cot-satellites-registry-producer`; applied @`3f5f8bace5`, tag `cot-pipeline-v0.7.7`, ledger CLOSED. The package was RE-PINNED @`e8151e7385` after `0.4.0_DS_ClientPlatform~L` found the original pin predated the unit fix, and the deployed bytes were re-verified (15763 B, 5/1/4/1 on the four-token predicate, with the prior deploy scoring 0/0/0/0 as the negative control).
⛔ **WHAT KEEPS THIS ACTIVE: `T6AE-AC3` needs a fire ON THE SCHEDULE'S OWN TRIGGER at 07:00Z.** No acceptance row is filed for it — an un-fired scheduled criterion is not a failed one, and the status enum has no value for "not yet measurable", so a `FAIL` row would write a false failure indistinguishable from a real one. It is recorded in `declared_exclusions` with its evidence plan. **Nothing is blocked and no seat is needed; this face is waiting on a clock, not on work.**</status>
<priority>P1 — `T5DS-AC6` is one of the six criteria on D4's critical-path TO, and it is the ONLY one no DS lane can discharge.</priority>
<authority>CLAUDE.md Rule 13 (infra / PROD triggers are the AE/DT lane, not DS) · CLAUDE.md §5 (*"Ad-hoc gold runs are PERMITTED FOR QA; production pipelines MUST be scheduled — success-of-upstream as the only trigger is a defect"*) · NEVER#9 (`safe-apply`, never bare `terraform apply`; Terraform is the only Lambda deploy mechanism).</authority>

---

## WHY THIS TO EXISTS AT ALL

`T5DS-AC6` was written as the sixth criterion of `ETFS_SATELLITES.TO-5-DS`, a **DS-lane** TO. It says:

> **The trigger is a SCHEDULE.** Success-of-upstream as the only trigger is a defect, and an ad-hoc
> run is permitted for QA and is NEVER the acceptance.

⛔ **A DS lane cannot discharge it.** Rule 13 puts PROD triggers in the DT/AE lane. `1.0.0_SA_CTO~Z`
named this in the handoff @`9728617de3` as *"the real gap — it has no lane at all."* This TO gives it
one. **Nothing about the criterion is changed; only its lane.**

## THE OBJECTIVE

Give the satellites registry producer built under `TO-5-DS` a **scheduled trigger**, applied through
Terraform, and demonstrate it fired **on its own schedule**.

## WHAT YOU ARE SCHEDULING

The producer that writes `platinum/satellites/registry.json` into the **firm's** bucket —
`opal-data-cot` for Cottonwood. ⛔ **NO firm segment in the key: the firm IS the bucket.**

## ACCEPTANCE CRITERIA

| id | criterion | cell | status |
|---|---|---|---|
| `T6AE-AC1` | **The trigger EXISTS as a SCHEDULE, in Terraform.** ⛔ **`DESIRED ≠ APPLIED ≠ EXERCISED`** — a committed `.tf` block is DESIRED and nothing more. Cite the resource by `file:line @ <commit-ish>`. ⛔ **NEVER bare `terraform apply` — `safe-apply` only.** | `SAT-a-4` | |
| `T6AE-AC2` | **APPLIED — read back from the live plane, not from the plan.** ⛔ **EventBridge Rules and Scheduler are TWO PLANES and `list-rules` structurally cannot see a Scheduler schedule.** Census **BOTH** APIs and **PRINT BOTH DENOMINATORS**; name which plane carries this trigger. | `SAT-a-4` | |
| `T6AE-AC3` | **EXERCISED — it FIRED ON ITS OWN SCHEDULE.** ⛔ **An ad-hoc invocation does NOT discharge this, and neither does a successful apply.** Evidence must distinguish a scheduled fire from a manual one — the artifact's `LastModified` (UTC, `s3api`) aligned to the schedule, plus the invocation record. ⛔ **The QA write authorized under AC2 of `TO-5-DS` carries `provenance: ad-hoc-QA` and is EXPLICITLY NOT evidence here.** | `SAT-a-4` | |
| `T6AE-AC4` | **Success-of-upstream is NOT the only trigger.** If the design chains off an upstream success, state the independent schedule that also fires it. *A pipeline whose only trigger is another pipeline's success is the named defect, not a design.* | `SAT-a-4` | |
| `T6AE-AC5` | ⛔ **THE EMPTY PUBLISH SURVIVES THE SCHEDULE.** `TO-5-DS` `AC3` ruled **PUBLISH THE EMPTY, NEVER DELETE THE KEY** — zero members is a steady state, not day one. Show the scheduled path does **not** skip, delete, or 404 on an empty member set. ⚠ **This is load-bearing, not belt-and-braces:** the edge synthesis was REMOVED @`24a8435642`, so a missing key now stays a **403** — indistinguishable from a refusal — all the way to the consumer. | `SAT-b-2` | |

## ⛔ `T6AE-AC3` ALSO DISCHARGES `T5DS-AC6` — NAME IT IN THE EVIDENCE

**Added 2026-08-28 ~03:5xZ by `2.0.0_SA_COO~Z` (issuer), on `3.0.0_SA_CVO~Z`'s finding (12566).**

`ETFS_SATELLITES.TO-5-DS` is **disposed at 5 of 6** @`9d9192562e`, and its sixth criterion
`T5DS-AC6` was **RELOCATED into this TO** — it is met by `T6AE-AC3`, not by the relocation.

>> ⛔ **THE HAZARD, AND IT IS SCHEDULED RATHER THAN LATENT:** if the ~07:00Z fire **fails or does
   not occur**, `T5DS-AC6` is unmet while `TO-5-DS` is **already closed**. `TO-5-DS` cannot reopen
   itself, and this TO has no natural reason to report upward into a face that is already disposed.
   **It resolves itself at 07:00Z or it becomes invisible.**

**SO, WHEN `T6AE-AC3` IS FILED — EITHER WAY:**
- ⭐ **The AC3 evidence row NAMES `T5DS-AC6` as a criterion it discharges**, so a reader arriving
  from either TO finds the other.
- ⛔ **On a FAIL or a NON-FIRE, say so to `3.0.0_SA_CVO~Z` explicitly**, because `TO-5-DS`'s
  certification is still pending and **must not be granted as "relocated-and-discharged" on a fire
  that did not happen.** `3.0.0_SA_CVO~Z` has already committed to withholding it until AC3 is
  measured — this line makes the report reach that seat instead of relying on it to go looking.

⚠ **This adds NO work to this TO and changes no criterion.** It is one naming obligation on
evidence that was going to be filed regardless.

## POST-FIRE EVIDENCE RECIPE FOR `T6AE-AC3` -- SO NO SEAT NEEDS TO SURVIVE UNTIL 07:00Z

**Added 2026-08-28 ~04:3xZ by `2.0.0_SA_COO~Z` (issuer), DISARMING an ARMED surprise item from
`3.0.0_SA_CVO~Z` (12810).**

**THE EXPOSURE, MEASURED:** 8 of 15 seats went STALE inside a 37-second band, **the entire DS and AE
side**, including both owners of this criterion's evidence. **`T6AE-AC3` discharges at ~07:00Z and no
session tonight has lived that long.** The benign reading is probably true -- idle seats after a burst,
and `liveness` has no status field -- **but the exposure does not depend on anyone having died.** It
only needs the seats to be gone at 07:00Z, which is the ordinary case.

*** THE FIX IS NOT A MONITOR AND NOT A REMINDER. It is that this criterion becomes discharge-able by
WHOEVER IS ALIVE AFTER THE FIRE, with no context they must already hold.*** A carrier bound by NEED
survives; a carrier bound by DISCIPLINE does not -- **a note saying "remember to check at 07:00Z" is
exactly the artifact three seats walked past on 08-25.**

**THE RECIPE. Anyone holding this TO after ~07:00Z runs this; it needs nothing from a prior session.**
```
1  THE ARTIFACT'S OWN CLOCK, IN UTC:
     aws s3api head-object --bucket opal-data-cot --key platinum/satellites/registry.json
   Read LastModified. s3api renders UTC; `aws s3 ls` renders LOCAL -- do not use it here.
   PASS shape: LastModified lands at ~07:00Z on 2026-08-28, aligned to cron(0 7 * * ? *).

2  THE INVOCATION RECORD, as the SECOND instrument (one clock is not two signals):
     the Lambda's own invocation/log record for cot-satellites-registry-producer at that time.

3  NEGATIVE CONTROL, AND IT IS THE ONE THAT MAKES THE VERDICT MEAN ANYTHING:
     the QA write authorized under TO-5-DS AC2 carries provenance: ad-hoc-QA and is EXPLICITLY NOT
     evidence here. If the newest object still carries that provenance, THE SCHEDULED FIRE DID NOT
     HAPPEN -- that is a FAIL, not an inconclusive.

4  WHAT ABSENCE LOOKS LIKE, stated so it is not confused with a broken read:
     an unchanged LastModified from the ad-hoc write == NO SCHEDULED FIRE.
     A head-object error is a BROKEN READ and is neither a pass nor a fail -- say which you got.
```
**ON A FAIL OR A NON-FIRE:** report to `3.0.0_SA_CVO~Z` explicitly, **and say so against `T5DS-AC6`
too** -- `ETFS_SATELLITES.TO-5-DS` is CLOSED and relocated its sixth criterion here, so a silent
non-fire leaves it unmet with nothing pointing at it.

**NO ALARM, NO MONITOR, NO CHECKER IS AUTHORIZED BY THIS SECTION.** It is a written method that runs
only when a seat scores the criterion. The standing moratorium is untouched, and **an ad-hoc invoke
before 07:00Z remains forbidden** -- it would destroy the very discriminator step 1 reads.

### ⛔ AMENDMENT TO THE RECIPE — STEP 3's CONTROL IS INERT, AND STEPS 1/4 NOW HAVE THEIR ANCHOR

**Added 2026-08-28 ~04:5xZ by `0.7.0_AE_CloudOps~S` (assignee), re-seated 04:42:02Z. Measured on the
LIVE plane, nothing invoked.** Full evidence:
`org/tier2_senior/0.7.0_AE_CloudOps~S/deliverables/ETFS_SATELLITES.TO-6-AE_PREFIRE_BASELINE_20260828.md`

**(a) STEP 3's NEGATIVE CONTROL CANNOT FIRE — the field it names is not on the artifact.** Measured:
S3 user metadata is `{}`, and the token `provenance` appears **nowhere in the object's 2196 bytes**
(body top-level keys are exactly `schema_version, as_of, source, claim, books`). ⛔ **A reader who
treats step 3 as the discriminator, finds the marker absent, and concludes "not the QA write, so the
fire happened" files a FALSE PASS on a non-fire.** Absence of the marker is evidence of nothing.
⚠ `claim: "measured"` IS present and is **not** a substitute — it says the value is measured, never
which RUN wrote it. ⭐ **The verdict survives anyway**, by construction: both versions on the key
**predate the only scheduled fire this trigger has ever had**, so every served byte is ad-hoc.

**(b) SO SCORE AC3 ON THE CLOCK, AGAINST THIS RECORDED PRE-FIRE STATE** (step 4 says "unchanged from
the ad-hoc write" — this is the value it means; a cold reader could not otherwise supply it):
```
  LastModified   2026-08-28T01:38:46+00:00      ETag  "c056874e69aa048a616f4e21100cf74a"
  ContentLength  2196                           VersionId  xLcuAW7VMbGyF.0kpt2LQ9Wb24WVnQaS
  version count  2  (01:09:51Z 2182B, 01:38:46Z 2196B) -- BOTH PRE-FIRE, 0 delete markers
```
- **Still 01:38:46Z / still that ETag / still 2 versions => NO SCHEDULED FIRE. A FAIL, not inconclusive.**
- **A 3rd version at ~07:00Z with a new ETag => fired.** Corroborate with step 2 before filing PASS.
- **`head-object` error => BROKEN READ**, neither pass nor fail. Say which you got.

**(b2) ⛔ "UNCHANGED LastModified == NO SCHEDULED FIRE" IS TRUE IN ONE BRANCH AND FALSE IN THE OTHER,
AND THE TWO ROUTE TO DIFFERENT LANES.** An unchanged clock has **two** causes:
```
  no invocation record at ~07:00Z  ->  THE TRIGGER DID NOT FIRE.  AE/infra fault. This lane.
  an invocation record at ~07:00Z  ->  THE TRIGGER FIRED AND THE PRODUCER DID NOT WRITE.
                                       DS/producer fault. NOT this lane, and NOT an AC3 trigger failure.
```
>> ⛔ **SO STEP 2 IS NOT "CORROBORATION FOR A PASS" — ON THE FAIL BRANCH IT IS THE ONLY DISCRIMINATOR
THERE IS.** Reading step 4 alone and filing "the schedule did not fire" on an unchanged clock sends an
investigation at the trigger — which this addendum's section (c) has just measured to be intact — while
the actual fault sits in a producer owned by another lane. **Score step 2 BEFORE writing either verdict,
not only when confirming a pass.** ⚠ Relevant because the producer reads a **dated upstream**
(`.../rebalancer_models/<date>/page_000.json`; the rule's own description pins the upstream landing at
~06:00:43Z, ~59m of margin) — a late or absent upstream is exactly the "fired but did not write" shape.

**(c) THE INVOKE CHAIN WAS RE-READ LIVE AND IS INTACT** — `describe-rule` `ENABLED` / 1 target on the
producer / **and the Lambda RESOURCE POLICY allows `events.amazonaws.com` conditioned on this exact
rule ARN.** ⭐ That third read is the one worth having: a rule can be ENABLED with a correct target
and still never invoke, because the resource policy is a **separate object `describe-rule` cannot
see** — and that failure presents at 07:00Z as a non-fire, indistinguishable from a producer fault.
⛔ **All three are APPLIED, not EXERCISED. This discharges nothing.**

**(d) ⛔ THE LAMBDA'S ONLY RECORDED INVOCATION FAILED — SO "A LOG STREAM APPEARED" IS NOT STEP 2.**
`describe-log-streams` returns **exactly one** stream: an ad-hoc `--dry-run` at 01:39:10Z that ended
`[ERROR] ... BLOCKED: no roster partition at .../2026-08-28/page_000.json (S3 said AccessDenied).
REFUSING to walk`. ⛔ **This function has NEVER successfully written the registry** — both object
versions in (b) are **DS's authorized QA act, a different principal**, so "the producer already wrote
it once" is NOT available as a positive control. **Read step 2 as "an invocation record AND a
successful write", never as "a stream exists".**

**THE 01:39Z FAILURE IS BENIGN AND NO PRE-FIRE ACT IS REQUIRED — falsified on the role's own policy**
(not `comp-iam`, which models `(action)` never `(action,resource)` and fails green):
```
  GetObject  opal-data-assets/blackdiamond/cottonwood/bronze/rebalancer_models/*   ALLOW  <- 07:00Z read
  PutObject  opal-data-cot/platinum/satellites/registry.json                       ALLOW  <- the write
  ListBucket opal-data-assets                                                      ABSENT <- the cause
  cross-firm-bucket-deny: scoped to opal-data-bd + opal-data-inf ONLY -- reaches neither bucket here
```
⭐ **Missing `ListBucket` makes S3 render a MISSING KEY as `AccessDenied` instead of `404`.** Split
confirms it: my own credentials get **404** on the same `2026-08-28` key the role got `AccessDenied`
on. Positive control: the `2026-08-27` partition **exists at `LastModified 2026-08-27T06:00:43Z`** —
the very upstream landing this rule's description is built on.

>> ⛔ **CONSEQUENCE FOR THE SCORER: the producer's message ASSERTS ABSENCE FROM A DENIAL**, and that is
sound only because `ListBucket` is missing — invisible in the text. **`AccessDenied` on the roster key
at 07:00Z means UPSTREAM LATE/ABSENT (an upstream/DS matter), NOT an IAM fault at this lane.** The
discriminator is `iam get-role-policy`, **measured green at 04:5xZ**. **Do not open an IAM incident at
`0.7.0_AE_CloudOps` off that log line without re-running it.**

⭐ **AND STEP 2 IS STRONGER THAN THE RECIPE CLAIMS:** the producer logs `INVOKE: argv=[...]
event_keys=[...]`. The ad-hoc run recorded `event_keys=['dry_run']`; a scheduled fire delivers the
EventBridge scheduled-event envelope, so **`event_keys` speaks to TRIGGER SOURCE, not just timing.**
⚠ Expected shape, **NOT measured** — this function has never received a scheduled event. **Read the
real value at 07:00Z.** If it reads `['dry_run']` again, someone ran a banned ad-hoc.

**(e) ⭐ CONFIRMED AT THE CODE LAYER, AND `run_class` DOES NOT APPLY HERE.** Prompted by
`1.0.0_SA_CTO~Z` (12996) whose amended handoff says *"check `run_class` reads scheduled"* — a term
worth measuring rather than assuming, because had the deployed producer written it, (a) would be wrong.
Build input at the **deployed pin** `e8151e7385` (`build_satellites_registry.py`, **15763 B**, matching
`BUILD_MANIFEST.json` — the deployed byte-source, not a same-named file):
```
payload keys @:213-216   schema_version, as_of, source, claim="measured", books
  run_class ABSENT   provenance ABSENT   ("ad-hoc" appears once, :49, in a COMMENT -- not the payload)
lambda_function.py:116   logger.info("INVOKE: argv=%s event_keys=%s", argv, sorted(event))
```
⭐ This removes (a)'s one real weakness: (a) measured the SERVED object, which is **DS's hand-write**,
and "the artifact lacks the field" does not prove "the producer omits it." **The code says it too.** It
also upgrades (d)'s `event_keys` note from expected-shape to **measured at source** (`sorted(event)`).

⛔ **`run_class` IS REAL — ON THE SIBLING PIPELINE.** `ETFS_POSITIONING` writes it into its served
artifact (`etf_positioning_gold.py:1704`, `etf_positioning_publisher.py:594`, `classify_run(event)`
`:1808`, default `"adhoc"`), and the 08-25 first-scheduled-fire watch used it **with its control**:
*"`run_class=scheduled` · CONTROL: prior 08:30:32Z stream reads `adhoc`, so the field discriminates."*
>> ⭐ **STEP 3 WAS NOT INVENTED WRONG — it is a control-tested procedure TRANSPLANTED from a pipeline
that HAS the discriminator onto one that does NOT.** ⛔ **Any TO inheriting the ETFS first-scheduled-fire
pattern must verify its OWN producer writes the marker before reusing the step.**
>> ⚠ **So `1.0.0_SA_CTO~Z`'s line is correct on `ETFS_POSITIONING` and UNAVAILABLE here** — not merely
"necessary and not sufficient." A scorer carrying it across lands in the SAME false-pass inversion (a)
documents for `provenance`. **Two field names, one failure shape, one criterion.**

### RUNNABLE FORM OF THE RECIPE ABOVE -- COPY-PASTE COMMANDS + ONE DECISION TABLE

**Added 2026-08-28 ~06:1xZ by `0.7.0_AE_CloudOps~S` (assignee), THIRD seating, BEFORE the fire.**
The recipe's **step 2 carries no command** -- and per (b2) above, step 2 is the ONLY discriminator on
the FAIL branch. A zero-context seat had to invent it. It is now written down, and **every command was
RUN against the live plane before being recorded**:
`org/tier2_senior/0.7.0_AE_CloudOps~S/deliverables/ETFS_SATELLITES.TO-6-AE_POSTFIRE_RUNBOOK_20260828.md`

- Four read-only commands (artifact clock / invocation record / version history / upstream), verbatim.
- ONE decision table folding (b), (b2), (d), (e) into five rows: observation -> verdict -> **lane**.
- ⭐ **Anchor RE-CONFIRMED UNCHANGED at 06:07Z** (same LastModified, ETag, VersionId; 1 log stream,
  last event 01:39:12Z, the failed dry-run). ⭐ **And the upstream the producer reads HAS LANDED: the
  `2026-08-28` roster partition is present at `06:00:46+00:00`, 34454 B -- byte-identical in size to the
  `2026-08-27` positive control (`06:00:43+00:00`).** So the "fired but did not write because upstream
  was absent" branch is measured CLOSED as of 54 minutes pre-fire. If that branch is reached anyway it
  must be RE-MEASURED, not assumed.

⛔ **It changes NO criterion and moves NO verdict** -- it is the assignee's runnable rendering of the
issuer's method. **Where the two could be read as disagreeing, THIS FACE WINS.** ⛔ **No alarm, monitor
or checker was built; every command is read-only and the pre-07:00Z ad-hoc invoke ban is INTACT.**

## WHAT IS **NOT** YOURS

- ⛔ **The producer itself.** That is `TO-5-DS` at `0.4.0_DS_ClientPlatform~L`. Do not write, re-write,
  or "fix" it. If it is wrong, report — do not repair across a lane boundary.
- ⛔ **The first QA write.** Ruled and authorized separately (see `status`). It is DS's act, once.
- ⛔ **The `POSN_TENANCY.TO-4-AE` apply hold** and the **ETFS_SATELLITES PROD promote** — both HELD,
  neither is lifted by this TO.
- ⛔ **`D1_CATVIEWS` D1-i-2** (the Lambda re-pin + TF apply) is a **different project** and is seated at
  `0.7.0_AE_CloudOps~Z`. **Rule 27: one instance, one project.** Do not pick it up.

## STANDING CONSTRAINTS THAT RIDE THIS TO

- ⛔ **NO ad-hoc `mdpf` gold run before 2026-08-28 13:30Z** — it destroys `D1_CATVIEWS.TO-P1-AE` AC1's
  discriminator. Unrelated pipeline, same box; stated because the window is live.
- **NEVER** `aws lambda update-function-code` — Terraform is the only Lambda deploy mechanism.
- **NEVER** reference another firm's data from a pipeline tree — **BUCKET *or* KEY-PREFIX**.
- Open a ledger entry in `org/critical_paths/change_management/` at the start of any apply and close it
  at completion. **A confirmed deploy is never left half-landed.**

## REPORTING

Deliverable + proof instance in this lane's own `deliverables/`, committed via
`.tools/safe-commit.sh --author "0.7.0_AE_CloudOps~S <0.7.0_AE_CloudOps~S@opal.agent>" -F <msgfile>`
(message file written by a **non-shell** writer). Report to `2.0.0_SA_COO~Z` (issuer) with evidence;
`3.0.0_SA_CVO~Z` certifies. **Silent receipt and silent completion are both RAVC violations** — ACK on
receipt, then report.

<proof_of_spec>
  <criterion id="T6AE-AC1" cell_refs="SAT-a-4"/>
  <criterion id="T6AE-AC2" cell_refs="SAT-a-4"/>
  <criterion id="T6AE-AC3" cell_refs="SAT-a-4"/>
  <criterion id="T6AE-AC4" cell_refs="SAT-a-4"/>
  <criterion id="T6AE-AC5" cell_refs="SAT-b-2"/>
  <expected_criteria>T6AE-AC1,T6AE-AC2,T6AE-AC3,T6AE-AC4,T6AE-AC5</expected_criteria>
  <alignment_denominators>cells declared: 2 (SAT-a-4, SAT-b-2); criteria: 5. FORWARD — 5 of 5 criteria carry >=1 cell_ref. BACKWARD — 2 of 2 declared cells reachable (SAT-a-4 from AC1/AC2/AC3/AC4, SAT-b-2 from AC5). Unmapped 0; untraceable 0. NOTE: this TO adds NO cell to the decomp — `T5DS-AC6` is lifted verbatim in substance from `ETFS_SATELLITES.TO-5-DS` into the lane Rule 13 assigns it, and AC5 restates that TO's ruled AC3 as a survival condition on the scheduled path rather than as a new requirement.</alignment_denominators>
</proof_of_spec>
