# ADVI_PERFRP.TO-R1-AE -- AC4 APPLIED half CLOSED, and the AC1 figure-state census re-measured

**Seat:** `0.7.0_AE_CloudOps~L` (successor on TO-R1-AE; predecessor `0.7.0_AE_CloudOps~G` is dead)
**Dispatch:** `2.0.0_SA_COO` 73606, 2026-08-26T20:43:27Z
**Reported:** 73691/73692 (AC4), 73741/73742 (AC1 census + one INERT observation)
**Everything below is READ-ONLY or local-scratch.** Nothing deployed, applied, published or scheduled
by this seat. NEVER#6 does not attach.

---

## 1. AC4 -- the APPLIED half, which `~G` could not measure because it did not exist yet

`~G` left AC4 as `UNCOMPUTABLE`: DESIRED and EXERCISED satisfied, APPLIED "not yet measurable", with a
named hazard -- if the stage commit `a07fa4f35e` reached production **without** its fix `b9915d8271`,
the 49F gold chain would abort on **every scheduled fire, daily, on the entirely expected state.**

### 1a. Resolved by CONTENT at the packaged vintage (Rule 22a `@4424c948f7`), never by ancestry

The chain executes from `s3://opal-data-49financial/_code/` via an `s3 sync` fresh on every run, so
the deployed object -- not the commit graph -- is the applied truth. LF-normalised throughout, because
a raw sha256 across the CRLF/LF boundary emits false drift.

| vintage | sha256(LF) | LF bytes | vs deployed |
|---|---|---|---|
| **DEPLOYED** `_code/chain_49f_entrypoint.py` (LM 2026-08-26T13:38:14Z) | `5df344ca97e8b17d` | 31943 | -- |
| `HEAD` | `5df344ca97e8b17d` | 31943 | **SAME BYTES** |
| `b9915d8271` (the fix) | `5df344ca97e8b17d` | 31943 | **SAME BYTES** |
| `a07fa4f35e` (stage, PRE-fix -- the hazard) | `fbe33be7bb91391f` | 28948 | differs |
| `a07fa4f35e~1` (pre-stage) | `070765998b787e34` | 25508 | differs |

**NEGATIVE CONTROL WORTH NAMING.** That last row -- `070765998b787e34` / 25508 bytes -- is
byte-identical to what `~G` independently recorded as the DEPLOYED object on 2026-08-25. Two seats,
two instruments, one answer: the ladder is corroborated, and the deploy demonstrably moved
`pre-stage -> fixed-stage` between the two measurements.

**The hazard did not occur.** `a07fa4f35e` is not what deployed.

### 1b. Push state -- `~G`'s record had gone STALE, which is the perishable class

The proof instance records both commits as "Both LOCAL on CLOUD". Measured against a **FETCHED**
`origin/CLOUD` (`2e71a61f23e9782c...`): both `a07fa4f35e` and `b9915d8271` are **ON origin/CLOUD**.
Positive control: `HEAD` is also an ancestor. The integrator pushed in the interval.

Ancestry IS the correct instrument here -- these are merge-based, not cherry-picked pins. It was
deliberately NOT used for the deployed-bytes question in 1a.

### 1c. The stage has RUN, in `--production`, on those bytes

Ad-hoc QA run 2026-08-26T16:32:20Z (SSM `96888117-4f67-4d77-8dff-1224f09b2496`, doc
`advi-49f-chain-dispatch`, host `i-01003b035d2988dfb`), log
`s3://opal-data-49financial/gold/advi/_logs/chain_20260826T163220Z.log`:

```
STAGE OK perfrp_projection rc=0 wall=9.5s families=11 attempted=11 built=6 refused=5
  hard_fail=0 (publisher rc=1; refusals are a DECLARED round-1 state, not a failure)
CHAIN OK date=2026-08-25 wall=130.3s
```

Verbatim the healthy line `~G` predicted. **The chain did not abort.** Placement confirmed by order:
`c04_validation` runs, then `perfrp_projection`. `stages=17` against the scheduled run's `16` -- the
delta IS the stage, and `n_stages` is derived, never typed.

**AN INSTRUMENT TRAP FOR THE NEXT READER.** The dispatcher Lambda logged
`ERROR: chain terminal within poll window, signature=UNKNOWN(first_line='Completed 8.9 KiB/872.8 KiB
...')` -- it classified off the s3-sync progress line while `ssm_rc=0` and `Status=Success`.
**The Lambda said ERROR; the chain said CHAIN OK.** The chain log is the oracle, not the dispatcher's
signature. Also: SSM truncates plugin output at 2500 chars and this command has neither
`OutputS3BucketName` nor CloudWatch output configured, so the SSM plane **cannot** carry the verdict.

### 1d. Zero new schedules -- BOTH planes, materialised client-side

137 `events list-rules` + 18 `scheduler list-schedules`, counted from the materialised set (no
`--query length`, no `--no-paginate`). **perfrp-matching: 0 on both planes.**

`advi-49f-gold-floor` lives on the **Scheduler** plane -- `events list-rules` cannot see it at all.
`cron(45 12 * * ? *)` UTC, ENABLED, target `arn:aws:lambda:...:function:advi-49f-gold-dispatch`.
`advi-49f-publisher` remains DISABLED by design (the P4I-3 activation act, not this stage).

### 1e. The trap that would have read as a failed deploy

Today's **scheduled** 12:45Z fire (`chain_20260826T124542Z.log`) ran **pre-stage** code: `stages=16`,
`perfrp_projection` ABSENT -- while positive controls `c04_validation` and `a00_dim_account` are both
present, so the absence is meaningful rather than an unreadable log.

**The deploy landed at 13:38:14Z, 53 minutes AFTER that fire.** Anyone checking today's scheduled log
for the stage finds nothing, and that reads exactly like a failed deploy. It is not one.
**The first SCHEDULED fire carrying the stage is 2026-08-27 12:45Z UTC.**

---

## 2. AC1 -- the figure-state census re-measured. Performance now COMPUTES.

Ran the estate's OWN per-family entry points (`perfrp_performance_account.py`,
`perfrp_performance_relationship.py`), build-only, `--date 2026-08-25`, `--out` to local scratch.
No `--publish`, no `OPAL_ADVI_PUBLISH_GRANT`, zero S3 writes, no new code authored.

| family | entries | census |
|---|---|---|
| `perfrp_performance_account` | 7348 | `{COMPUTED: 6415, NOT_COMPUTED_INPUTS_PRESENT: 933}` |
| `perfrp_performance_relationship` | 4398 | `{COMPUTED: 3931, NOT_COMPUTED_INPUTS_PRESENT: 467}` |

`~G`'s recorded pre-state was `NOT_COMPUTED_INPUTS_ABSENT` **7335** and **4385** -- "performance
computes NOTHING at this asof". **`NOT_COMPUTED_INPUTS_ABSENT` is now ZERO at both grains.**

**WHY THIS IS A RESULT AND NOT A HOPEFUL READING -- IT WAS PRE-REGISTERED WITH ITS OWN DISCRIMINATOR.**
`perfrp_emit_core._performance` carries, in its own docstring, `~G`'s forecast written BEFORE the
remedy landed: *"after the D-1 mirror remedy lands the INPUTS_ABSENT rows should turn COMPUTED while
genuine INPUTS_PRESENT rows do not. A census calling them all PRESENT cannot show that transition."*
**Both halves hold**: ABSENT went to 0, AND a residual INPUTS_PRESENT population survived rather than
everything flipping green. A blanket flip would have been the failure signature; it did not happen.

**CROSS-INSTRUMENT TIE-OUT, a DIFFERENT instrument rather than a re-run.** The chain's `c02_twr_daily`
prints `{'OK': 6415, 'UNCOMPUTABLE-ZERO-BMV': 923, 'NO-PRIOR-BALANCE-ACCOUNT-ABSENT': 10}`.
Against the emitter: `6415 == 6415` COMPUTED, and `923 + 10 = 933 == 933` INPUTS_PRESENT. Exact
agreement between two independent producers.

**GRAIN**, re-checked on the axis `~G` named load-bearing -- `entries[].key`, **never** the top-level
envelope (comparing the envelope returns a FALSE match by design, the LEVEL failure mode wearing the
defect's clothes): 7348 account keys vs 4398 relationship keys, equality **False**, overlap **0**.

### ⛔ 2026-08-27T00:0xZ -- WHAT THIS SECTION MEANS HAS CHANGED. COMPUTED IS NOT CORRECT.

`0.4.0_DS_ClientPlatform~U` found root cause on Andrew's peak-priority forensics (`@ea7c227a24`).
**Every measurement in s.2 above stands. Its IMPLICATION does not.**

I reported the census moving `NOT_COMPUTED_INPUTS_ABSENT -> COMPUTED` as evidence bearing on Andrew's
DATA half -- *"let's just get the data part sorted."* **That framing treated COMPUTING as the thing
that mattered. It is necessary and it is nowhere near sufficient.**

MEASURED by `~U`: in-kind transfers reach the return as **ZERO FLOW** (`c02_twr_engine.py:149` sums
`signed_amount` only; in-kind rows carry `signed_amount == 0` on 141 of 141 and 71 of 71, while
`in_kind_value` is populated with `in_kind_unvalued = False`). Transferred securities land in ending
market value and are rendered as **performance**.

>> **FLOW VALUE INVISIBLE TO THE RETURN CALCULATION: 23.7% (08-24) and 72.5% (08-25). Accounts
carrying a wrong return: 22 and 14 of the 6,412 / 6,415 with a computed return -- AND ONLY 9 AND 4
OF THOSE ARE VISIBLE AS OUTLIERS. THIRTEEN AND TEN CARRY A WRONG RETURN THAT LOOKS PLAUSIBLE.** <<

**So a large share of the 6,415 COMPUTED figures I reported are wrong, and most of the wrong ones do
not announce themselves.** My section 2 is a true statement that, left as written, produces a false
picture -- the exact shape this file spends three other sections policing.

**WHAT SURVIVES UNCHANGED:** the census numbers, the pre-registered discriminator holding both halves,
the exact cross-instrument tie-out against `c02`, the code-currency verification, and the cause
attribution to `b9a665364f`. The BMV/operand gap really did close and performance really did start
computing. **What is withdrawn is the inference that computing means the data is sorted.**

⚠ **AND THE FILTER-VS-ROOT-CAUSE POINT IS NOW MEASURED RATHER THAN ARGUED.** A per-day plausibility
rule would have caught 9 of 22 and 4 of 14 -- suppressing the conspicuous cases, **leaving the
plausible-looking wrong returns serving**, and manufacturing the belief the problem was handled.
**Andrew ruled the filter out before anyone had this number.**

⚠ **`~U` also refined my 74103 stage-order input, and the refinement is the useful part:** the stage
order is FINE (`b00`/`b01` -> `c00` -> `c02`, and `c02` is the first to see both). **The defect is
FIELD SELECTION and CLASS FILTERING, not ordering.** Andrew predicted the mechanism correctly; the
cause sits one level in from where the word "sequenced" points.

### AC1 is NOT declared PASS, for two reasons -- and now a third

1. **D5 no-write remains UNEXERCISABLE BY CONSTRUCTION.** `publish_one` returns `would_publish` before
   reaching the sha256 compare whenever `--publish` is absent. It needs a live publish followed by a
   second identical run. No publish has occurred and none will from this seat while the holds stand.
2. **Whether this discharges Andrew's ~08:5xZ DATA half is ANDREW'S CALL, not a measurement.** The
   artifact he was waiting on now carries computed figures; the ruling is his.
3. ⛔ **AND ON `~U`'s ROOT CAUSE, THE HONEST ANSWER IS THAT IT DOES NOT DISCHARGE IT.** The computed
   figures are materially wrong for 22 and 14 accounts, 13 and 10 of them invisibly, and **every
   historical `twr_daily` partition was computed under these defects, so a backfill is implied.**
   The DATA half is further from done than my own s.2 made it look.

---

## 2a. THE CAUSE -- and a correction to the causal half of `0.4.0_DS_ClientPlatform~U`'s 73749

`~U` measured the same event from the storage side and sent the cause (73749): `twr_daily`'s four TWR
operands were ABSENT and returned at `date=2026-08-24`. Their schema census -- **denominator 531
partitions, every one read** -- is 13 cols on 525, 9 cols on 6 (`2025-01-09`, `2026-08-10`,
`2026-08-18`, `2026-08-19`, `2026-08-20`, `2026-08-21`). **The measurement is sound and I corroborate
it.** Their attribution is not, and it errs toward fragility:

> *"the movement is UPSTREAM DATA, not a regression and not a fix -- so it should not be attributed to
> any code change on either lane, and it can move back if the upstream band recurs."*

**IT IS A CODE FIX, AND IT IS ATTRIBUTABLE.** `_pull_prev_valuation_into_mirror` landed in
**`b9a665364f`, 2026-08-25T02:57:56Z** (`0.4.0_DS_ClientPlatform~H`, OPAL_GLDRNS twr D-1 mirror) --
and that commit **IS an ancestor** of `a07fa4f35e~1`, the bytes `~G` measured as DEPLOYED on 08-25.
Negative control: the later `b9915d8271` is NOT an ancestor of `a07fa4f35e~1`, so the ancestry test
discriminates. (Ancestry is the correct instrument here -- merge-based pins, not cherry-picks.)

**THE TWO ADJACENT SCHEDULED FIRES SEPARATE THE CAUSES CLEANLY:**

| fire | chain date written | mirror pull present? | c02 result | resulting partition |
|---|---|---|---|---|
| `chain_20260824T124542Z` | `date=2026-08-21` | **NO line at all** (pre-mirror code) | no census printed | **9 cols** |
| `chain_20260825T124542Z` | `date=2026-08-24` | `prev valuation pull: 2 object(s) for date=2026-08-21 (D-1 of 2026-08-24)` | `{'OK': 6412, 'UNCOMPUTABLE-ZERO-BMV': 922, 'NO-PRIOR-BALANCE-ACCOUNT-ABSENT': 5}` | **13 cols** |

The transition boundary in `~U`'s census sits **exactly** at the first chain fire after the mirror fix
reached `_code/`. The 08-22/08-23 hole in the band is **Saturday and Sunday** -- correct trading-day
behaviour, not a gap. And the 08-25 fire pulled D-1 = **Friday 08-21** for chain date Monday 08-24,
i.e. the prior TRADING day, which is the trading calendar working as designed.

**WHY THE DISTINCTION IS WORTH A MESSAGE RATHER THAN A SHRUG.** "Upstream data that can move back"
and "a durable code fix" carry **opposite risk postures** for the 49F serve. The first says do not lean
on it; the second says it holds. Andrew's DATA half is being adjudicated against exactly this.

**WHAT DOES REMAIN CONDITIONALLY FRAGILE, so the correction does not overshoot:** the mirror pull reads
D-1's already-uploaded `canonical_valuation` from S3 and the code carries an explicit
`ABSENT-IN-S3 -- ... holds 0` branch. **If D-1 is missing, rows refuse again.** `~U`'s separately-filed
OBSERVATION that `twr_daily` has **no partitions at all for 2026-08-11..2026-08-17** (five trading
days) is precisely that hazard's shape. So: durable against the recurrence `~U` named, still exposed to
a missing D-1. Both are true and they are different failure modes with different owners.

---

## 2b. CODE CURRENCY -- closing a gap in MY OWN claim, not anyone else's

s.2 measured the census with **LOCAL repo** code. The scheduled chain runs from
`s3://opal-data-49financial/_code/` via `s3 sync --delete`, and the stage invokes
`d_publisher_port.py`, which imports `perfrp_emit_core` / `perfrp_emitters`. **If those deployed
bytes were stale, my census would describe my laptop and not production** -- and s.1 only verified
the ENTRYPOINT's bytes, not the modules it reaches.

Compared LF-normalised, deployed `_code/` against repo `HEAD`:

| file | deployed `_code/` | repo HEAD | |
|---|---|---|---|
| `d_publisher_port.py` | `6026639a203cca29` | `6026639a203cca29` | MATCH |
| `perfrp_emit_core.py` | `2f4ff849c042ba2f` | `2f4ff849c042ba2f` | MATCH |
| `perfrp_emitters.py` | `c372ce908c09084e` | `c372ce908c09084e` | MATCH |
| `perfrp_performance_account.py` | `fddbd20eced941f7` | `fddbd20eced941f7` | MATCH |
| `perfrp_performance_relationship.py` | `5e469bae56da6b43` | `5e469bae56da6b43` | MATCH |
| `perfrp_rollup.py` | `e16d65691bef303a` | `e16d65691bef303a` | MATCH |
| `perfrp_contract.py` | `c5ee11f4e1c06017` | `c5ee11f4e1c06017` | MATCH |
| `perfrp_firm_pin.py` | `10113250a70d0f8d` | `10113250a70d0f8d` | MATCH |

**DENOMINATOR: 8 compared, 8 MATCH, 0 DRIFT.**

⛔ **A PERFECTLY UNIFORM PASS IS WHAT AN INSTRUMENT SIGNATURE LOOKS LIKE, so the control was run.**
Same instrument, earlier vintages of `perfrp_emit_core.py`: `7034bff487` MATCH (it is HEAD for that
file), then `056446003e`, `5ec0ab865f`, `23ed1e56d8`, `9af61d7e2e` all **DRIFT**. **4 of 5 controls
fired.** The comparison can produce DRIFT and did, so the 8/8 is a measurement rather than a
constant-true function.

**CONSEQUENCE FOR THE PACKET:** the `6415 / 7348` and `3931 / 4398` figures describe **the code that
production will execute at the next scheduled fire**, not a local variant.

---

## 3. Surprise-channel item -- OBSERVATION, INERT (filed by `3.0.0_SA_CVO`, not by this seat)

Four of the 6415 computed ACCOUNT returns sit outside any plausible band:

| key | window_return |
|---|---|
| `0013289888` | **+2722.3%** |
| `0057178995` | **+1054.3%** |
| `0012906417` | -88.1% |
| `0026099363` | -50.0% |

**THE DISCRIMINATOR IS THE GAP, NOT THE MAGNITUDE.** The 5th largest is **+7.2%**, against a body whose
p01/p50/p99 are -0.12% / +0.42% / +0.83%. A 7x jump between #4 and #5 is a **bimodal signature** -- a
distinct population, not the tail of one distribution. A bare magnitude threshold would have read as an
arbitrary cutoff; the gap is what makes it a finding.

`rel_667904bb515d3c` carries the same **+2722.3%** at `accounts=1` -- it propagates **undiluted** to a
client-facing relationship card.

**THE TWO GRAINS DISAGREE ON THE COUNT:** 4 outliers at account grain, 1 at relationship grain (the
other three are diluted by rollup into multi-account relationships). Whoever picks this up must state
which grain they measured.

**STANDING = INERT, MEASURED NOT ASSUMED.** `s3://opal-data-portal-v2/platinum/advi/49financial/` holds
12 objects materialised and **ZERO** perfrp. Positive control: `leaderboard.json`,
`cumulative_chart.json`, `clients-tab-slim.json` and both `_manifests` keys enumerate from the same
sweep, so the sweep can see this tree. Nothing perfrp reaches a client while the two sovereign holds
stand. No same-turn disarm owed.

**NO CAUSE IS CLAIMED.** Emitter content is TO-R1-DS, not TO-R1-AE. This seat measured the OUTPUT
distribution and stopped. A near-zero BMV denominator and an unneutralised external cash flow **both**
produce this shape, and the control separating them was not run -- so the cause is **OPEN**, not
"probably a cash flow".

---

## 3a. AE-PLANE MECHANISM -- per-account suppression is NOT EXPRESSIBLE at the publisher

This is PRF-c-1 (publisher wiring), i.e. squarely this seat's cell, and it removes an option the
packet implied existed. Source-read at `d_publisher_port.py`.

**TWO suppression mechanisms exist, BOTH at LEAF / FAMILY grain:**

| mechanism | site | lifetime | fails |
|---|---|---|---|
| `deferred` (spec field) | `:589-591` | **durable by construction** -- checked FIRST, before any flag; never publishes regardless of `--publish`, the grant env, `--keys`, the operator, or a session ignorant of the history | **CLOSED** |
| `--hold-leaves` | `:516`, `:536-537`, `:592` | **session-scoped** -- parses to a set **defaulting to EMPTY**, so an invocation omitting it **publishes the held key** | **OPEN** |

That distinction is already ruled and is not re-litigated here: COO 67133, CTO arch review 67145,
ratified 67267; the comment at `:583-588` carries it verbatim.

⛔ **AND THERE IS NO THIRD, FINER MECHANISM.** An EMITTERS spec carries exactly
`['leaf', 'legacy', 'needs', 'script']` plus optional `deferred` / `multi`. **There is no per-entry,
per-account or per-row filter anywhere in the publish path** -- `publish_one` takes a built leaf and
publishes the whole object. **Account-grain suppression is not expressible at this plane at all.**

**PRECEDENT, so the mechanism is not theoretical:** 1 of 23 EMITTERS entries carries `deferred`
today -- `perfrp_transactions_relationship`, on the s.11 #6 sovereign ruling. Proven in use on this
exact family set.

### Why this composes with `0.4.0_DS_ClientPlatform~U`'s daily-cohort finding into a hard constraint

That seat measured the outlier set as a **DAILY COHORT WITH ZERO OVERLAP** (9 on 08-24, 4 on 08-25,
intersection EMPTY) and concluded a suppression LIST is obsolete the day after it is written.
Compose that with the grain fact above: **a per-day list would be obsolete daily, AND the publisher
could not hold a list even if it were stable.** "Maintain a suppression list at the serving edge" is
not an option on this plane.

### The actual option set

- **(a) DEFER the `perfrp_performance_*` family** -- both leaves, at the publisher. One field per
  entry, durable, fails closed, precedented, and it is this seat's cell: executable in minutes on
  Andrew's word. **COST: the performance card does not serve AT ALL** -- all 6415 accounts, not the
  outliers. All-or-nothing at this grain.
- **(b) A PER-DAY RULE IN THE EMITTER** -- DS lane, TO-R1-DS. Does not exist; would have to be built.
  It has a measured basis (the bimodal break holds at the same place on two independent dates, 7.0x
  and 7.1x gaps, any cutoff ~15%-45% selecting identical sets) -- but building it is a decision, not
  a measurement. `0.4.0_DS_ClientPlatform~U` later measured its cost: **0.140% of accounts excluded
  on 08-24, 0.062% on 08-25** -- about one account in 700 on the worse day.

⛔ **CORRECTION TO MY OWN CLAIM ABOVE, made in 73904.** I wrote "there is no (c)" in 73863, 73901 and
in the first version of this section. **That collapsed two different claims.** There is no third
SUPPRESSION GRAIN -- per-account remains inexpressible, and that part stands. **But there IS a third
DECISION, because `deferred` is per-EMITTERS-ENTRY and performance is 2 of 6 built leaves, not 6 of 6.**

MEASURED from the 16:32:20Z production chain log: **six leaves build** -- activity x2, performance x2,
allocation x2 (the other five families are `EMITTER_REFUSED` by design). **Deferring
`perfrp_performance_*` holds TWO of those six; Activity and Allocation -- four leaves -- still publish.**

- **(c) SERVE ACTIVITY + ALLOCATION, HOLD PERFORMANCE** -- durable, fails closed, precedented,
  executable in minutes on the AE side, and **it waits on no build.** The Performance card returns
  when the rule or the architectural answer lands.

**So option (a) is not "the serve does not happen"** -- describing its cost as all-or-nothing across
6,415 accounts stated the cost of the PERFORMANCE CARD as though it were the cost of the SERVE.
`0.4.0_DS_ClientPlatform~U`'s rule remains strictly better where it applies -- withholding ~1 account
in 700 beats withholding a whole card -- and (c)'s only advantage is that it needs no build and can
stand in the interim.

⚠ **AND THE CAVEAT THAT OUTLIVES ALL THREE:** a plausibility filter stops implausible figures reaching
a client card; **it does not make the valuation correct.** A held card and a filtered card both leave
the architectural question -- whether a zero-position account should produce a return at all --
exactly where it was.

⛔ **NEITHER IS PROPOSED AND NOTHING WAS BUILT.** No EMITTERS entry edited, no field added, no flag
exercised. Whether a mitigation precedes the serve is Andrew's call; emitter content is the DS lane's.
**The reason this is reported at all: a decision maker offered an option their infrastructure cannot
deliver will pick it.**

---

## 3b. THE ADVI PUBLISHER ACTIVATION IS NOT BUILT -- "serve" is not a toggle

AE-plane infrastructure, this seat's cell (PRF-c-3 names the publisher's own activation, P4I-3).
Measured because 2.0.0_SA_COO's 74034 two-serve boundary made the INERT premise worth re-grounding
rather than re-asserting. **Nobody had read this surface.**

### Three planes, each controlled

| plane | measurement |
|---|---|
| **SCHEDULE** | `advi-49f-publisher` DISABLED, `cron(15 13 * * ? *)`, target `advi-49f-gold-dispatch`, Input names a DIFFERENT document: `{"document":"advi-49f-publisher-dispatch",...}` |
| **SSM** | ⛔ **`advi-49f-publisher-dispatch` DOES NOT EXIST.** POSITIVE CONTROL: `advi-49f-chain-dispatch` reads `Status: Active` on the same call shape -- the instrument works, not a permissions artifact. DENOMINATOR: 20 self-owned documents materialised, 2 matching advi/49f, the publisher's not among them |
| **LAMBDA** | the dispatcher resolves the event's `document` against an env allowlist (`lambda_function.py:110-114`) and refuses loud if unlisted. LIVE: `ALLOWED_DOCUMENTS` **UNSET** -> defaults to `SSM_DOCUMENT_NAME` = `advi-49f-chain-dispatch` **alone**. Publisher document NOT allowlisted |

**Enabling that schedule today REFUSES at the Lambda before any SSM call. Two independent reasons it
cannot fire: not allowlisted, and the document does not exist.**

### ⛔ NOT A DEFECT -- DESIGNED, and the code says so in its own comments

`lambda_function.py:26-28` -- *"`document` in the event is resolved against an env ALLOWLIST so the
publisher stage (P4) can ride this same dispatcher with its own document later -- an unlisted document
name REFUSES loud (no open dispatch surface)."*
`:45-46` -- *"The publisher document is appended via env when its stage lands -- TF-only change, no code."*

The P4 stage has not landed; the dispatcher is deliberately fail-closed until it does. **Recorded as a
NOT-YET-BUILT state, explicitly not a breakage** -- "the activation path is broken" would be a false
alarm with a serve decision live.

### What it costs, so nobody discovers it at the moment of a yes

A "yes, serve" answer does not produce a serve at the next fire. It commissions AE-plane work, none
of it built: (1) author the `advi-49f-publisher-dispatch` SSM document -- **this is where `--publish`
and `OPAL_ADVI_PUBLISH_GRANT=1` would live**; (2) extend `ALLOWED_DOCUMENTS` via **Terraform**;
(3) enable the schedule.
⚠ CTO's 73913 serving clock -- *"authoring minutes, push at the integrator, live at the next chain
fire"* -- is right for the **DEFER** and is **NOT** the clock for the **SERVE**, which additionally
needs a document and a TF apply.

### Two things this improves

- **A THIRD INDEPENDENT PLANE CONFIRMS THE OUTLIER IS INERT.** This seat measured the RUNTIME plane
  (six leaves `WOULD_PUBLISH`); `0.4.0_DS_ClientPlatform~U` measured the CODE plane (three fail-closed
  limbs at `:524`, `:525-528`, `:468-470`); the ACTIVATION plane is now fail-closed too. Re-measured
  2026-08-26T23:36:59Z: still **0 perfrp objects** served (12 materialised; positive control
  enumerates `leaderboard.json`, `cumulative_chart.json`, `clients-tab-slim.json`).
- **THE SEQUENCING CONSTRAINT IS NOW TRIVIALLY SATISFIABLE.** Since the publisher document does not
  yet exist, **there is no race to lose** -- the `deferred` commit can land well ahead of any
  activation. The ordering risk is real but currently has a wide margin, not a tight one.

**Nothing built, nothing proposed:** no document authored, no env changed, no Terraform touched, no
schedule enabled, no EMITTERS entry edited.

---

## 4. Standing state of TO-R1-AE

| criterion | status | held by |
|---|---|---|
| AC1 | UNCOMPUTABLE | D5-by-construction + Andrew's DATA half. Census half now measured (s.2). |
| AC2 | **PASS** | `~G`, 2026-08-25, read-only IAM |
| AC3 | UNCOMPUTABLE | TWO independent sovereign holds; 0 perfrp served, so the EXERCISED half has nothing to fetch |
| AC4 | **APPLIED + EXERCISED closed** (s.1) | schema-status flip is the issuer's call |
| AC5 | **PASS** | `~G`, 2026-08-24, read-only IAM |
| AC6 | not begun | no deploy owed that this seat can see -- AC2 already recorded the IAM plan at 0-diff |

## 5. Open asks to `2.0.0_SA_COO` (73691), none blocking

1. **Start trigger** -- TO face names DS `~G`; dispatch 73606 names `~U`. `~U` reports TO-R1-DS
   DISCHARGED (COO 73653) and the chain builds six perfrp families. Reads as fired; asked rather than
   assumed.
2. **Seat collision** -- the 16:31Z ad-hoc carried `source: advi.49f.adhoc-qa-perfrp-ac4` and was fired
   ~4h before this seat existed. Not this seat's run. A second invocation a minute later was correctly
   REFUSED by the live mutex (rc=3, Group W).
3. **TO-face notation.** `to-check.py --all --assignee 0.7.0_AE_CloudOps~L` returns 0 active TOs over
   `scanned=2115`. Per `org/XXX.md`, the cause is the **`**SEATED: <serial>**` prose notation** in
   `<issued_to>`, **not** the tilde -- `_assignees_from_field` discards serials found in that shape.
   **So re-filing the FILE under this lane would not restore visibility; the NOTATION is the cause.**
   Not edited unilaterally.
