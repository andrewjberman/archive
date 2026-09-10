# NFRA_OUTSET.TO-OS-s-21 -- THE CADENCE: result, v2 (the ACCEPT)

**Assignee:** `0.7.0_AE_CloudOps~W` · **Issuer:** `2.0.0_SA_COO` · **Cell:** `OS-s-21` ·
**Written:** 2026-09-10T14:0xZ.
**v1** (`the-cadence-scheduled-publish.result.md`, @`732c69f8c1`) recorded the BUILD. **This
document records the ACCEPT** and supersedes nothing in v1.

---

## THE ONE-LINE ANSWER

The freshness half's cadence **fired on its own schedule today and the fire is attributable to the
schedule rather than to a hand**. `O21-AC1` prints `OS21-CADENCE-FRESH`, **rc=0 unpiped**, 6 arms,
6 evaluated, 0 FAIL. **The DRIFT half's cadence has never fired** and this document does not claim
it does.

## WHICH DAY THIS GRADES, AND WHY IT IS NOT THE ONE PRD v0.8 NAMED

v0.8 re-pointed this criterion onto TO-OS-s-24's **manual served day**. The freshness artifact
latest at that run (00:18:59Z) was written by a build whose CodeBuild `initiator` is
`Andrew_Berman` -- **a hand publish**. The face says in terms:

> a pass read against a hand-published artifact is INVALID

> This criterion CANNOT pass before the first scheduled fire that lands AFTER OS-s-20's switch is
> live on the served day

The **2026-09-10 13:00Z run is that first eligible fire**, published at 13:34:36Z. So this battery
grades the SCHEDULED run. The v0.8 re-point was written at 22:2xZ on 09-09, when no such fire
existed. **This is the harder reading, and the only valid one.**

## THE ARMS

### (a) THE SCHEDULE, READ LIVE FROM THE SCHEDULER

| | |
|---|---|
| `estate-report-seam-freshness-0830et` | **State ENABLED** |
| Expression | `cron(30 8 * * ? *)` `America/New_York` = **12:30Z** |
| Target | the `estate-report-seam-freshness-publisher` CodeBuild project |
| Margin | fires **30 min before** the 13:00Z run |

Read from the scheduler itself, never from the face. The fire time is derived from the expression
the scheduler holds, not from a number typed into the battery.

### (b) THE VINTAGE PRECEDES THE RUN START

`outset/comp_heat_freshness_tools.json` @`z3hGZ.BdeShGiNSN..`, 63,826 B, LastModified
**2026-09-10T12:31:14Z**, against the run's `started_at` **13:01:01Z** -- **1,787 s (29.8 min)
earlier**. LastModified is read with `s3api head-object` in UTC; `aws s3 ls` renders LOCAL and is
not used.

### (c) THE ATTRIBUTION -- the fire's own event, not a timestamp

⛔ **A TIMESTAMP INSIDE A SCHEDULE'S WINDOW IS EXACTLY WHAT A HAND PUBLISH AT THE SAME MINUTE
WOULD PRODUCE.** So the arm reads CodeBuild's own `initiator`:

| build window (UTC) | status | initiator |
|---|---|---|
| **12:30:10 -> 12:31:17** | SUCCEEDED | **`estate-report-seam-freshness-scheduler/29d3681c...`** |
| 00:17:54 -> 00:19:02 | SUCCEEDED | `Andrew_Berman` |
| 16:53:42 -> 16:54:42 (09-09) | SUCCEEDED | `Andrew_Berman` |
| 15:37:35 -> 15:38:14 (09-09) | **FAILED** | `Andrew_Berman` |

**DENOMINATOR: 4 builds read, 1 scheduler-initiated, 3 hand-initiated.**

The artifact's LastModified (12:31:14Z) falls **inside** the scheduler-initiated build's window.

⛔ **AND THE CONTROL IS WHAT MAKES `initiator` EVIDENCE**: the same project's three earlier builds
carry a human's name, so the field **discriminates** rather than always agreeing. A field that read
the same on every row would have proven nothing. The FAILED hand build is a second control that
arrived free: it wrote **no artifact at all**, so a failed publish is visibly not a publish.

### (d) THE SEAM PREFIX, ENUMERATED LIVE -- under a clause the ISSUER RE-CUT at 13:59Z

**BOTH DENOMINATORS, as the re-cut requires:**

| reading | result |
|---|---|
| **LITERAL** (the original clause) | **6 keys present against an allowance of 3 -- it would read FAIL** |
| **ATTRIBUTED** (the re-cut clause) | **6 of 6 map to a named authorizing cell; 0 UNATTRIBUTED -- PASS** |

| key | authorizing cell |
|---|---|
| `outset/comp_heat_freshness_tools.json` | OS-s-21, seam key 1 |
| `outset/comp_fedobs_coevolution.json` | OS-s-23, group B source 2 |
| `outset/comp_heat_drift.json` | OS-s-18; RETIRED as a read by OS-s-22, object survives under **PRD R-5** |
| `outset/laptop/comp_heat_drift.json` | **O21-AC1's own re-cut clause (3)**, one key per device |
| `outset/_os22_probe_device/comp_heat_drift.json` | OS-s-22, the QA fixture |
| `outset/_os18_red_arm_probe.json` | OS-s-18, the red-arm probe |

⛔ **THE CLAUSE WAS STALE AND ITS OWN RE-CUT IS WHAT STALED IT.** "the seam prefix ... holding ONLY
the two seam keys plus the untouched R2 probe (a fourth key is a FAIL)" was written before the
15:2xZ re-cut added "ONE KEY PER DEVICE" three paragraphs below it. Read literally the arm fails on
changes this face itself ordered.

**RE-CUT BY `2.0.0_SA_COO` (the issuer) at 2026-09-10T13:59Z, msg 95207**, after this seat pitched
it at 13:55Z with a rec and did NOT act on its own reading. The clause now reads: **the prefix
holds NO KEY THAT MAPS TO NO AUTHORIZING CELL.**

⛔ **AND IT IS NOT A WEAKENING, on the test that decides that question.** The issuer's own words:
the artifact here is CORRECT -- 6 present, 6 attributed, 0 unattributed -- so nothing is wrong with
the world and the defect was in the criterion. That is the opposite of the ETFS `R-EG-8` case,
where an accept could not be met **by the artifact** and re-pointing was refused. The re-cut clause
still FAILS on a stray publish, a wrong-prefix write, and a fourth device nobody declared -- which
is everything the original existed to catch. What changed is that it now names the **PROPERTY**
(nothing publishes here unaccounted for) rather than a **PROXY** for it (a key count), and a proxy
breaks the moment the authorized population grows while the property does not.

**The literal-3 reading was offered by this seat and DECLINED**, in terms: it would spend a real
FAIL on a criterion already known to be stale, and a FAIL everyone agrees is spurious teaches a
reader to discount the next one.

### (e) THE SERVED STRATUM READS FRESH, AND THE READING IS FALSIFIABLE

Group A reads `OK`; the served citation discloses ages **13.1 h** and **21.1 h**, both under the
**26.0 h** ceiling.

⛔ **THE NEGATIVE ARM, ON THE SAME OBJECT AND THE SAME READER, WITH NO WRITE:**

```
ceiling 26.000 h -> status='OK'
ceiling  0.001 h -> status='INSTRUMENT_FAILED'  err=artifact STALE at s3://.../laptop/comp_heat_drift.json
```

So **no green here comes from a raised ceiling** -- the reader convicts when the ceiling moves, and
nothing was published, deleted or mutated to produce the negative.

### (f) THE DRIFT HALF -- CITED, NOT RE-DERIVED

`2.0.0_SA_COO` 94867: *"drift half by OS-s-25"*. `TO-OS-s-25` is TERMINAL at `520503aa98` with its
own battery and its own VALID proof instance. Re-grading it here would be a second seat's
restatement lending credibility the claim has not earned. What this day adds, and all it adds: the
device's artifact is still inside its ceiling on this run (age 14.0 h).

⛔ **AND THE DRIFT CADENCE IS NOT CLAIMED.** Row `NFRA_OUTSET-S38` stands: the device timer's first
scheduled fire (2026-09-10T11:30Z) was **SKIPPED** -- an Interactive-principal task with no
interactive session, the console logon coming 19 minutes late -- so **every drift artifact in the
bucket is hand-started**. Row `NFRA_OUTSET-S39` records that its remedy needs an elevated line only
Andrew can run.

---

## O21-AC2 -- JUDGMENT, EVIDENCE ONLY, NO VERDICT

**Where the producers run and under which identity.** The FRESHNESS half runs OFF-HOST, in
CodeBuild (`estate-report-seam-freshness-publisher`), under the scheduler role
`estate-report-seam-freshness-scheduler` invoking it and the project's own service role writing the
key. The DRIFT half runs DEVICE-SIDE on the laptop under `outset-drift-publisher-laptop`, assumed
from the principal the device already holds.

**Why that home, and it is the substantive judgment of this cell.** The two artifacts differ by
NATURE, not by convenience: `comp_heat_freshness_tools` reads TRACKED HISTORY (`git log`), whose
timestamps are identical on every clone, so it is CLONE-INVARIANT and can be promised by a cloud
schedule. `comp_heat_drift` reads `git status --porcelain` and nothing else, so its subject is the
producing machine's dirty working tree, which on a clean clone is empty **by construction** -- a
scheduled cloud publisher would emit `n=0` forever with a correct denominator and a fresh vintage:
**fresh, green and meaningless.** An off-host schedule is a STATED NON-APPLICATION for drift.

**The trigger is the producer's own** -- an EventBridge schedule invoking the build directly. Not
success-of-upstream, and not a watcher.

**The moratorium boundary as I read it.** A PIPELINE TRIGGER is not a monitor (CTO @`e18317d0e0`),
and that ruling admits the schedule and admits nothing else. No SNS topic, no CloudWatch alarm, no
metric filter and no `sns:Publish` grant appears in `seam-freshness-publisher.tf`. A freshness
CHECKER would be a monitor and is not built: **the freshness question is already answered by the
consumer's own 26 h ceiling**, which convicts a stale artifact without anything watching it -- and
arm (e) above exercises exactly that.

**What a FAILED producer publishes: nothing.** Measured, not assumed -- the 15:37:35Z build FAILED
and wrote no object. The consumer then meets the previous vintage ageing past its ceiling and reads
SILENT, which is the intended path.

---

## WHAT THIS RESULT DOES NOT CLAIM

- **The drift cadence.** Never fired. Rows S38 and S39.
- **Anything about O21-AC1 on the manual served day.** That day's freshness artifact was
  hand-published and the face makes such a pass INVALID.
- **That arm (d) passed under the clause as originally written.** It did not. It passes under the
  clause the ISSUER re-cut at 13:59Z, and both readings are printed side by side in the battery's
  own output so the re-cut is visible to a reader rather than only to the record.
