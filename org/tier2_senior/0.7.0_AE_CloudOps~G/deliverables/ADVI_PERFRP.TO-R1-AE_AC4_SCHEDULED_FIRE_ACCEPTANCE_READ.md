# ADVI_PERFRP.TO-R1-AE -- AC4 CLOSED on the SCHEDULED plane: two fires read, and the negative control is a fire that ran without the stage

**Seat:** `0.7.0_AE_CloudOps~G` (re-seated 2026-08-28 ~16:0xZ by `2.0.0_SA_COO` 78244 under CTO D2-D3
ledger row 10; predecessors on this TO: `0.7.0_AE_CloudOps~L`, `0.7.0_AE_CloudOps~K`, both dead)
**Reported:** 78263 / 78264 (state at re-seat), CTO confirmation 78266
**Everything below is READ-ONLY.** Nothing deployed, applied, published, enabled or scheduled by this
seat. No Terraform ran. NEVER#6 does not attach. The one thing executed is a LOCAL two-armed harness
over a SCRATCH COPY of the deployed bytes, with `subprocess` and every S3 helper stubbed.

---

## 0. What was open, and why this closes it

`0.7.0_AE_CloudOps~L` closed AC4's APPLIED half on 2026-08-26 by CONTENT at the packaged vintage and
named the remaining sub-clause in one sentence: *"The first SCHEDULED fire carrying the stage is
2026-08-27 12:45Z UTC."* `org/projects/ADVI_PERFRP.json` records that read was never taken (zero ADVI
commits on 08-27). **Two such fires have now occurred.** Both are read below.

⛔ **`0.7.0_AE_CloudOps~K`'s 72788 synthesis -- "3 open criteria collapse to ONE gate: the P4I-3
publish activation" -- WAS TRUE ON 2026-08-26 AND IS NOT TRUE NOW.** It was written 19 hours before
the first fire that could carry the stage. AC4 was never in that collapse; it gates on a fire, not on
a publish. The correction is recorded here and on the instance **with the date it became true**, so a
successor does not inherit a FULLY-BLOCKED reading of a lane that had a read available.

---

## 1. THE ACCEPTANCE READ -- three scheduled fires, and the one without the stage is the control

Logs from `s3://opal-data-49financial/gold/advi/_logs/` (`s3api`, UTC -- **never `s3 ls`, which
renders LOCAL time**). Denominator: 22 `chain_*` log objects in the prefix; the three below are every
`12:45Z` scheduled fire from 08-26 forward.

| scheduled fire (UTC) | log object | `CHAIN START ... stages=` | `perfrp_projection` | chain verdict |
|---|---|---|---|---|
| **2026-08-26T12:45:42Z** | `chain_20260826T124542Z.log` (9,404 B) | **16** | **ABSENT** | `CHAIN OK date=2026-08-25 wall=113.0s` |
| **2026-08-27T12:45:42Z** | `chain_20260827T124542Z.log` (10,943 B) | **17** | **PRESENT, line 113** | `CHAIN OK date=2026-08-26 wall=122.5s` |
| **2026-08-28T12:45:42Z** | `chain_20260828T124542Z.log` (11,659 B) | **17** | **PRESENT, line 119** | `CHAIN OK date=2026-08-27 wall=110.7s` |

**The stage line, verbatim, from the 2026-08-28 fire (line 119):**

```
STAGE OK perfrp_projection rc=0 wall=10.1s families=11 attempted=11 built=6 refused=5
  hard_fail=0 (publisher rc=1; refusals are a DECLARED round-1 state, not a failure)
  refused_keys=['perfrp_gainloss_relationship', 'perfrp_gainloss_account',
                'perfrp_transactions_relationship', 'perfrp_roster_relationship',
                'perfrp_book_advisor']
```

This is byte-for-byte the healthy line `0.7.0_AE_CloudOps~G` predicted on 08-25 and wrote into the
instance for whoever watched the first fire. The 08-27 fire's line is identical but for `wall=8.8s`.

### 1a. ORDERING -- read from the fire's OWN log, not from the source

| fire | `STAGE OK c04_validation` at line | `STAGE OK perfrp_projection` at line |
|---|---|---|
| 2026-08-27 | 97 | **113** |
| 2026-08-28 | 103 | **119** |

The projection is AFTER the battery in the execution record of both fires. **Log order is the
APPLIED truth; the source is only the DESIRED one.**

### 1b. ⛔ THE NEGATIVE CONTROL IS A REAL FIRE, NOT A CONSTRUCTED ONE

The 08-26 fire ran the full chain to `CHAIN OK` with `c04_validation` PRESENT and
`perfrp_projection` ABSENT at `stages=16`. **So the absence is discriminating, not an unreadable
log:** an instrument that could not see the stage would have failed to see `c04_validation` too.
And s.2 shows the 08-26 fire's bytes did not contain the stage -- so source and log agree in BOTH
directions, on three fires.

---

## 2. WHICH BYTES EACH FIRE ACTUALLY RAN -- measured by S3 OBJECT VERSION, never inferred from an interval

`opal-data-49financial` has **versioning ENABLED** (`get-bucket-versioning` -> `Enabled`), so the
object live at each fire is a thing that can be FETCHED, not a thing bracketed between two
`LastModified` readings. 20 versions of `_code/chain_49f_entrypoint.py` exist; the three that were
latest at a 12:45:42Z fire were pulled by `--version-id` and hashed.

LF-normalised throughout -- a raw sha256 across the CRLF/LF boundary emits false drift
(`reference_digest_needs_its_normalisation_crlf_vs_lf`).

| fire | version-id live at that moment | version `LastModified` | LF sha256 | LF bytes | `_run_perfrp_projection` in those bytes |
|---|---|---|---|---|---|
| 08-26 12:45Z | `E_I103B_frOcXCQ6p.1CiUW_ut27vrlk` | 2026-08-25T07:17:36Z | `070765998b787e34` | 25,508 | **False** |
| 08-27 12:45Z | `jRckhCWP9aW45Ezmb5PpYSFM450dLr9y` | 2026-08-26T13:38:14Z | `5df344ca97e8b17d` | 31,943 | True |
| 08-28 12:45Z | `FGvWchopqxXt.d415Z8znam3jsIXYm8J` | 2026-08-27T23:17:36Z | `fc829256f45187bf` | 33,416 | True |

**Tied to the tree, with negative controls that fire:**

| vintage | LF sha256 | LF bytes | vs the bytes live at the 08-28 fire |
|---|---|---|---|
| working tree (clean for this path) | `fc829256f45187bf` | 33,416 | **SAME** |
| `HEAD` = `b5e05eee78` (DS~U, P14-STAMP c02 mirror) | `fc829256f45187bf` | 33,416 | **SAME** |
| `9644276a3a` | `6d622a6020dd859d` | 32,794 | differs |
| `43a2b1d872` | `b2459d6a8b2d56d1` | 32,790 | differs |
| `b9915d8271` (the AC4 fix; ran the 08-27 fire) | `5df344ca97e8b17d` | 31,943 | differs |
| `a07fa4f35e` (stage, PRE-fix -- the hazard) | `fbe33be7bb91391f` | 28,948 | differs |
| `b9a665364f` (pre-stage; ran the 08-26 fire) | `070765998b787e34` | 25,508 | differs |

⛔ **THE DEPLOYED OBJECT MOVED SINCE `0.7.0_AE_CloudOps~L` MEASURED IT, AND THAT IS THE POINT.** That
seat recorded `5df344ca97e8b17d` / 31,943 B as deployed. It is now `fc829256f45187bf` / 33,416 B --
`0.4.0_DS_ClientPlatform~U` landed three edits to this file on 08-27 (`43a2b1d872`, `9644276a3a`,
`b5e05eee78`, the P14-PRECOND / P14-STAMP work) and they deployed at 20:07Z-23:17Z. **A stale
deployed-bytes hash is the perishable class; re-measured rather than carried forward.** The stage
survived three foreign edits to its own file, which is stronger evidence than one fire on frozen code.

**Ancestry deliberately NOT used for the deployed-bytes question** (Rule 22a `@4424c948f7`); it is
used only where it is the correct instrument, which is not here.

---

## 3. ⛔ THE EXERCISED ARM WAS AT A STALE VINTAGE, SO IT WAS RE-RUN

AC4 requires *"a forced c04 failure leaves the projection UNRUN -- exercised."* That was exercised on
2026-08-25 against `b9915d8271`. **Those bytes are three commits and 1,473 LF bytes behind what is
deployed.** A structural read of the deployed source is not an exercise, and a fail-closed guard on a
client-facing performance number is exactly the claim that should not rest on a superseded vintage.

**Re-exercised against the deployed bytes.** Subject: `fc829256f45187bf`, S3 version
`FGvWchopqxXt.d415Z8znam3jsIXYm8J`, staged into the same **bundle layout the EC2 runner uses**
(`HERE/lib/trading_calendar.py`) and asserted byte-identical to the fetched object before the run.
Harness preserved at
`org/tier2_senior/0.7.0_AE_CloudOps~G/deliverables/ADVI_PERFRP.TO-R1-AE_AC4_FAILCLOSED_EXERCISE.py`
so the next reader re-runs it at the NEXT vintage instead of quoting this one.

**The arms were transcribed from the CRITERION before the implementation was read** -- a harness
copied out of the code scores its own blind spot as a pass
(`feedback_harness_transcribed_from_implementation_scores_blind_spot_as_pass`). The only thing that
varies between arms is `c04_validation_battery.py`'s return code.

```
[ARM A  c04 PASSES] c04_rc=0 -> main_rc=0 | c04_invoked=True | perfrp_projection_ran=True
[ARM B  c04 FAILS ] c04_rc=3 -> main_rc=3 | c04_invoked=True | perfrp_projection_ran=False

  PASS  ARM A: c04 was actually invoked (arm is live, not skipped)
  PASS  ARM A: projection RAN when c04 passed
  PASS  ARM B: c04 was actually invoked (arm is live, not skipped)
  PASS  ARM B: projection did NOT run when c04 failed
  PASS  ARM B: main() returned c04's rc (3), not 0
  PASS  ARMS DIFFER on the field under test

VERDICT: PASS (6/6 arms+assertions)
```

**ARM A is load-bearing and is not decoration.** Without it, ARM B's silence is equally consistent
with the call site having been REMOVED by one of the three foreign edits -- an absent stage and a
fail-closed stage produce the identical observation on the failing arm alone. The `c04_invoked`
assertion is the second half of the same discipline: an arm that skipped the battery entirely would
also report `perfrp_projection_ran=False` and read as a pass
(`feedback_verifier_arms_must_be_reachable_from_different_truths`).

**The mechanism, at the deployed vintage, `:502-531`** -- the guard is CONTROL FLOW, not a flag:

```python
        if r.returncode != 0:
            print(f"CHAIN ABORT stage=c04_validation rc={r.returncode} wall={w:.1f}s", flush=True)
            rc_final = r.returncode or 1
            return rc_final                      # <-- the battery block RETURNS
        ...
        if upload:
            rc_proj = _run_perfrp_projection(workdir, date)
```

Gated on the same `upload` condition as c04, so the invariant is total: **this stage having run
IMPLIES c04 ran and passed.**

---

## 4. ZERO NEW SCHEDULES / RULES -- BOTH PLANES, materialised client-side

`aws events list-rules` **cannot see** `aws scheduler list-schedules`; a one-plane sweep returns a
well-controlled answer about the wrong population. Both were listed in full and counted from the
materialised set -- **no `--query length()`** (which returns the PAGE count), no `--no-paginate`.

| plane | rows | matching `perfrp` |
|---|---|---|
| `events list-rules` | **139** | **0** |
| `scheduler list-schedules` | **18** | **0** |

- `advi-49f-gold-floor` -- `cron(45 12 * * ? *)`, **timezone UTC**, **ENABLED**, target
  `arn:aws:lambda:us-east-1:313476888478:function:advi-49f-gold-dispatch`. The existing rule; the
  stage rides it.
- `advi-49f-publisher` -- `cron(15 13 * * ? *)`, **DISABLED**. The P4I-3 activation act, deliberately
  not this stage, and **still disabled** -- independent confirmation that no publish was activated by
  anyone in the interval.

⚠ **DENOMINATOR MOVED AND IT IS NOT MINE:** 139 events-rules against the 137 `0.7.0_AE_CloudOps~L`
counted on 08-26. Two rules were added estate-wide in the interval by other lanes; **0 of them match
`perfrp` and 0 match this TO's surface.** Recorded rather than smoothed over -- a denominator quoted
without noticing it moved is how a census stops being a census.

---

## 5. VERDICT

**`PRFR1AE-AC4` -> PASS**, all three Rule-22a planes carried by a different instrument:

| plane | evidence | instrument |
|---|---|---|
| **DESIRED** | placement after the c04 battery at `HEAD b5e05eee78`; zero new rules/schedules declared | source read + both-plane census |
| **APPLIED** | deployed object == `HEAD`, and the exact bytes live at each fire fetched by version-id | `s3api list-object-versions` + `get-object --version-id` + LF sha256 |
| **EXERCISED** | **two consecutive SCHEDULED fires** carried the stage after `c04_validation` and reached `CHAIN OK`; a third real fire on stage-free bytes did not; fail-closed 6/6 at the deployed vintage | the fires' own logs + the two-armed harness |

**What AC4 does NOT claim.** Nothing here says a PERFRP leaf is SERVED. The stage BUILDS 6 of 11
families into a staging tree and the publisher returns `would_publish`; **zero objects were written
to `platinum/advi/49financial/`**, because `OPAL_ADVI_PUBLISH_GRANT` is unset and
`advi-49f-publisher` is DISABLED. That is GATE A below, and it is untouched.

---

## 6. Standing state of TO-R1-AE after this read

| criterion | status | held by |
|---|---|---|
| AC1 | UNCOMPUTABLE | **GATE A** -- D5 no-write residual needs a live publish + a second identical run. Also: COMPUTED != CORRECT (the in-kind root cause, `ea7c227a24`). |
| AC2 | **PASS** | closed `0.7.0_AE_CloudOps~G` 2026-08-25, read-only IAM |
| AC3 | UNCOMPUTABLE | **GATE A** -- the EXERCISED half needs a published leaf to fetch; 0 of 11 served |
| AC4 | **PASS** | **closed here, 2026-08-28** |
| AC5 | **PASS** | closed `0.7.0_AE_CloudOps~G` 2026-08-24, read-only IAM |
| AC6 | UNCOMPUTABLE | **GATE A** -- a deploy criterion cannot be evaluated before a deploy exists |

**THE OPEN SET IS NOW EXACTLY GATE A, AND IT IS ONE ACT: the P4I-3 publish activation.** Held by
Andrew-direct 2026-08-21T19:18Z (the 49F flip waits on BOTH source gaps AND schedule) and the
~08:5xZ DATA half. **`0.7.0_AE_CloudOps~K`'s one-gate synthesis is the CORRECT description of the TO
as of 2026-08-28** -- it was simply asserted 19 hours before it became true, while AC4's read was
still available. Not inferring a lift, not asking for one here.

**Nothing at this seat is blocked on this seat.** With GATE A held, TO-R1-AE has no unblocked act
remaining.
