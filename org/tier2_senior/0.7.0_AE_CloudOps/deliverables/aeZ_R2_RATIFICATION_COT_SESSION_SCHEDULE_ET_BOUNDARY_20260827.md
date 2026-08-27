# R2 RATIFICATION -- THE COT SESSION CHAIN ALREADY HAS ITS SCHEDULED HEAD

**Author:** `0.7.0_AE_CloudOps~Z`, 2026-08-27. **Spec:** `ctoZ_SPEC_COT_SESSION_CHAIN_PARITY_20260827.md`
(amended @9a3dab252a). **Verifier:** `1.0.0_SA_CTO~Z`. **Discharges:** A4.

**VERDICT: R2 IS ALREADY SATISFIED. BUILD NOTHING. `bd-cot-session-daily` MUST NOT BE CREATED.**

---

## s.1 -- THE ARTIFACT THAT SATISFIES R2 (APPLIED, live primitive)

`aws scheduler get-schedule --name cot-bd-session-daily-et`, read 2026-08-27:

```
Name                        cot-bd-session-daily-et
State                       ENABLED
ScheduleExpression          cron(30 7 * * ? *)
ScheduleExpressionTimezone  America/New_York
GroupName                   default
Target.Arn                  arn:aws:lambda:us-east-1:313476888478:function:cot-bd-session-trigger
Target.Input                {"mode":"session-refresh"}
Target.RoleArn              arn:aws:iam::313476888478:role/cot-session-scheduler-role
```

**INDEPENDENT CORROBORATION ON A DIFFERENT PRIMITIVE** -- `aws lambda get-policy --function-name
cot-bd-session-trigger` carries statement `SchedulerCotBdSessionDailyEt`, principal
`scheduler.amazonaws.com`, SourceArn the schedule above. The invoke path is APPLIED, not merely
declared. Two independent APIs agree.

This is structurally what R2 asked for: a declared, ENABLED, scheduled head targeting
`cot-bd-session-trigger` in `session-refresh` mode -- the same shape `bd-49f-session-daily` gives
49F. Source: `infra/aws/terraform/cot-pipeline/schedule-et.tf`.

**CLAUDE.md's named defect does not apply here.** The spec read the chain as *"a pipeline whose only
trigger is another pipeline's success"*. It is not: `cot-bd-session-daily-et` is a real schedule.
`cot-bronze-complete` / `cot-silver-complete` are accelerators on top of it, which is the sanctioned
pattern.

---

## s.2 -- WHY THE CENSUS READ IT AS ABSENT, AND WHY THAT IS NOT CARELESSNESS

**EventBridge is TWO SERVICES WITH TWO APIS AND NO OVERLAP.**

| plane | API | what it holds |
|---|---|---|
| Rules | `aws events list-rules` / `describe-rule` | `cot-bronze-complete`, `cot-silver-complete`, `cot-session-complete`, all 137 |
| Scheduler | `aws scheduler list-schedules` / `get-schedule` | `cot-bd-session-daily-et`, all 18 |

The spec's census ran over all 137 rules. **I re-ran it and reproduce its numbers exactly** -- 137
total, 17 matching cot/49f, and `bd-cot-session-daily` / `cot-bd-session-daily` genuinely ABSENT.
**The census was correct and complete on its own plane.** It was structurally blind to the other,
and no control inside the Rules plane could have caught that: a positive control there would have
passed.

This is CLAUDE.md's wrong-plane class. The instrument returned a clean, confident, well-formed zero
about the plane the answer does not live on. **Name the question's plane before choosing the
sweep's.**

Denominators, both planes, measured the same minute:

```
aws events list-rules         -> 137 rules      ; "cot-bd-session-daily" matches -> 0
aws scheduler list-schedules  ->  18 schedules  ; "cot" matches -> cot-bd-session-daily-et,
                                                  opal-assets-ingest-mirror-cot-daily-et
```

---

## s.3 -- THE ET BOUNDARY: WHY THE SCHEDULE IS TIMEZONE-PINNED AND MUST STAY THAT WAY

### s.3.1 -- Timing here is a DATA-CORRECTNESS parameter, not a scheduling convenience

`cot_bronze_ingest.py:80` records that a day *"not yet COMPLETED in BD's business timezone (US
Eastern)"* returns a **header-only ~4.6KB export**. BD's own native report criteria (`sheet2.xml`:
`Created (Eastern)` / `Start Date` / `End Date`) define a rolling ~14-day window whose **End Date is
D-1 for holdings/allocations and D-0 for transactions/realized**.

**The window BD returns is a function of the ET wall-clock instant the request is made.** So the
schedule's correctness parameter is its **Eastern** time, and its UTC time is a derived quantity.

### s.3.2 -- The DST arithmetic, computed rather than recalled

`cron(30 7 * * ? *)` in `America/New_York`, evaluated against the real tz database:

| date | ET fire | UTC fire | offset |
|---|---|---|---|
| 2026-08-27 | 07:30 | **11:30Z** | EDT (UTC-4) |
| 2026-10-31 | 07:30 | **11:30Z** | EDT (UTC-4) |
| 2026-11-02 | 07:30 | **12:30Z** | EST (UTC-5) |
| 2027-03-13 | 07:30 | **12:30Z** | EST (UTC-5) |
| 2027-03-16 | 07:30 | **11:30Z** | EDT (UTC-4) |

**The tz-pinned schedule holds the correctness parameter (ET) fixed and lets the derived quantity
(UTC) float.** That is the right way round.

The mirror, which is what R2-as-written would have built -- a hardcoded UTC `cron(30 11)` rendered
back into Eastern:

| date | UTC fire | ET fire |
|---|---|---|
| 2026-08-27 | 11:30Z | 07:30 ET |
| 2026-11-02 | 11:30Z | **06:30 ET** |

**A UTC pin satisfies the spec's own caution (2) today and violates it on 2026-11-01**, silently, by
one hour, on the parameter the caution exists to protect. Nothing would error.

### s.3.3 -- This is the estate's existing ruling, not a new argument

Andrew-direct 2026-07-29 ~0445Z, verbatim: *"yeah we need that ingestion to be scheduled at 4:30p
Eastern"*, implemented as Scheduler rather than Rule for exactly this reason (`schedule-et.tf`
header): *"a Rule is UTC-only and a hardcoded UTC cron drifts an hour at DST, firing BEFORE market
close come November."* The same file records that the old `cron(0 2)Z` Rule was deleted **in the
same change** as the Scheduler that replaced it -- *"no dual-trigger window."*

**So building R2 would have done two things at once: re-created a rule that was deliberately
deleted, and re-introduced the defect the deletion existed to prevent.**

### s.3.4 -- The downstream margin the anchor is sized against

`schedule-et.tf` (MDPF_TRGALN s.3 row 4, Andrew-direct 2026-08-14) records the anchor moved from
16:30 ET to 07:30 ET as a **pre-floor pull so cottonwood serves T-1 at the 13:30Z floor**, sized on
the **EST worst case: 12:36Z chain-done, 54m margin**. The author already did the DST arithmetic and
sized the tighter of the two cases. In EDT the same chain completes ~11:36Z with roughly two hours
of margin.

**A UTC pin would break that sizing in the direction nobody checked**, because the margin was
computed against an ET-anchored fire, not a UTC-anchored one.

---

## s.4 -- WHAT I DID NOT MEASURE, STATED SO IT IS NOT READ IN

- **I have NOT measured a specific data harm at 06:30 ET.** Both 06:30 and 07:30 ET sit before the
  ET business day, so I cannot claim the winter drift would corrupt a specific export. **The
  argument against a UTC pin is that it makes the declared correctness parameter float, and the
  estate has already ruled on that** -- not that I have shown this particular hour to be harmful.
  A harm I did not measure is not evidence I am entitled to use.
- **I have NOT re-adjudicated the 07:30 ET anchor itself.** Whether 07:30 is the right ET time is
  MDPF_TRGALN's ruling and Andrew's; this document ratifies the MECHANISM (tz-pinned Scheduler),
  not the VALUE.
- **I have NOT characterised the full 18-schedule inventory** beyond the two entries matching
  "cot". `opal-assets-ingest-mirror-cot-daily-et` is noted as the downstream mirror; I did not
  profile it.
- **A `get-schedule` read is APPLIED state, not EXERCISED.** That the schedule exists and is ENABLED
  does not by itself prove it fires. **It is separately proven by consequence**: the 2026-08-27 mint
  ran at 07:30:32 ET, and the 08-21..08-26 bronze runs all landed at 07:30-07:31 ET -- a schedule
  firing on time, six days running.

---

## s.5 -- RECOMMENDATION

1. **Create nothing for R2.** `cot-bd-session-daily-et` is the declared head.
2. **Do not "mirror the 49F structure" by adding a Rule.** Structural parity is already satisfied at
   the level that matters (a scheduled head in `session-refresh` mode). 49F uses a Rule because
   `cron(0 0)` UTC has no ET semantics to preserve; COT uses a Scheduler because it does. **Same
   structure, correct implementation for each partner's constraint.**
3. **If a future sweep flags COT as "having no schedule", the sweep is on the wrong plane.** Any
   schedule census over this estate must query BOTH `events list-rules` AND
   `scheduler list-schedules`, and print both denominators.

---

## s.6 -- PROVENANCE

Finding raised by `0.7.0_AE_CloudOps~Z` during the R1 grounding pass; confirmed independently on the
live primitive by `0.0.0_AB_MSTR~Z` and by the spec author `1.0.0_SA_CTO~Z`, who amended the spec to
RATIFY-WHAT-EXISTS @9a3dab252a. R1 (`cot-session-complete`) was built and applied separately and is
unaffected by this ratification.
