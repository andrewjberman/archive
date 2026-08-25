# ETFS_POSITIONING -- PIPELINE SCHEDULE + ROBUSTNESS POSTURE

**Seat:** `0.7.0_AE_CloudOps~Z` · **Measured:** 2026-08-25 07:45Z -> 08:25Z · **Ask:** Andrew-direct
~07:3xZ, *"confirm pipelines are scheduled/robust"* -- the third of four verbs, and not the same act
as the fix.

⛔ **NO MONITOR, ALARM, SNS TOPIC, SES SEND OR FRESHNESS CHECKER WAS BUILT.** The 2026-07-28
moratorium stands and this is exactly the situation that tempts one. **This is a posture report.**
Zero crons armed at this seat.

---

## VERDICT

**SCHEDULED: PASS.** Every leg of the ETF chain carries a real schedule. **Zero ETF legs are
triggered only by another pipeline's success** -- the CLAUDE.md defect test, and the chain passes it.

**ROBUST: QUALIFIED PASS**, with one irreducible structural dependency (deliberate, vendor-imposed)
and six named residuals, none of which is a defect requiring a fix tonight.

---

## THE CHAIN, AS MEASURED

```
11:00Z  L1 Bloomberg pull   OPAL_BBGTML_daily_pull           LOCAL WINDOWS TASK (07:00 local)
13:00Z  gold + platinum     etf-positioning-producer-daily   cron(0 13 * * ? *)   AWS
15:45Z  ownership fan-in    etfs-canon-fanin-daily           cron(45 15 * * ? *)  AWS
22:00Z  silver/holdings     etfs-netassets-daily             cron(0 22 * * ? *)   AWS
23:30Z  silver sweep        opal-assets-silver-etf-sweep     cron(30 23 * * ? *)  AWS
```
All AWS rules **ENABLED**. Ordering is correct with margin: silver for as-of D lands 22:00Z on D;
the pull reads it 13h later; gold consumes both 2h after that.

**DENOMINATOR: 137 EventBridge rules materialised client-side** (auto-paginated, no NextToken).
17 are event-pattern-only; **none of the 17 is an ETF leg** (all bd/cot/inf/mdpf/globgrph/moltbot).

---

## CORRECTION TO A LOAD-BEARING CLAIM SEVERAL SEATS ARE CARRYING

The spawn brief, `org/XXX.md` and several broadcasts state: **"EventBridge has ZERO rules at hour 11."**
**THAT IS FALSE -- and the true count is LAYERED, which is itself the reason to abandon the framing.**
```
(a) hour field EXACTLY "11"                        8   inf-* x6, news-api-845am, opal-inf-bronze-runner-cron
(b) hour field a LIST containing 11               +1   news-trending-analysis-daily  cron(15 11,21 * * ? *)
(c) every-hour cron                               +1   access-anomaly-scanner-schedule  cron(0 * * * ? *)
(d) rate() expressions, firing continuously       +9
    a+b     =  9   cron rules explicitly scheduled in hour 11
    a+b+c   = 10   including every-hour crons
    a+b+c+d = 19   including rate rules
DENOMINATOR: 137 rules scanned. Targets checked on (a): every one inf-* or news-*. ZERO ETF.
```
⛔ **WHERE THE ZERO CAME FROM: `cron(0 11 ` AS A PREFIX REALLY IS 0** -- none of the nine fires at
minute `:00` (they fire at :02 :07 :15 :15 :17 :18 :22 :32 :45). **A test for "fires at exactly
11:00" was reported as "fires in hour 11."**

⛔ **AND MY OWN FIRST COUNT WAS 8, NOT 9 -- I REPRODUCED THE SAME DEFECT WHILE CORRECTING IT.** My
regex matched the hour field only when it equalled `11` exactly, so the list form `11,21` fell out.
**My own histogram had already printed `hour 11,21   1` on screen and I did not fold it in.** Caught
by `0.4.0_DS_ClientPlatform~Z` (@8783) before it reached Andrew. Extending their nine to the layered
figure above is the same correction carried one step further -- (c) and (d) fall out of a
cron-hour-field frame exactly as (b) fell out of an exact-match frame.

>> **SO THE HOUR-11 ARGUMENT SHOULD BE RETIRED, NOT REPAIRED.** Hour 11 is one of the BUSIER hours
>> in the estate, so the phrasing invites the true reply "plenty runs at 11" and loses the argument
>> it was making. **THE STRONG CLAIM IS THE TRUE ONE, and it is as-of-independent and hour-independent:**
```
rules matching bbg|bloomberg|terminal AT ANY HOUR : 0 of 137
POSITIVE CONTROL, same matcher, 'etf'             : 8      <- the matcher discriminates
```
>> **No EventBridge rule drives the Bloomberg pull at any hour, on any day.** Wording adopted from
>> DS~Z's suggestion and re-derived independently at this seat. <<

---

## FINDING 1 -- TODAY'S 13:00Z IS THE PRODUCER'S **FIRST-EVER SCHEDULED FIRE**

```
CloudTrail PutRule  etf-positioning-producer-daily  2026-08-24T22:52:48Z  (my own TF apply 1da1e2b73b)
AWS/Events Invocations 14d      0 datapoints, total 0
AWS/Events FailedInvocations    0 datapoints, total 0
POSITIVE CONTROL  etfs-netassets-daily     14 datapoints / 14 invocations
POSITIVE CONTROL  etfs-canon-fanin-daily   14 datapoints / 14 invocations
Lambda log streams in the 14d retention window: 4, ALL ad-hoc from last night
```
**The instrument discriminates** (two sibling ETF rules in the same namespace report 14/14), so the
zero is real. ⭐ **IT IS NOT A DEFECT -- the rule is ten hours old.** Its first scheduled fire is
**today 13:00Z**, and that is the acceptance event for the whole data path.

>> **I checked the mechanism before naming it.** "0 invocations in 14 days" on an ENABLED rule with a
>> correct target and a correct `lambda:InvokeFunction` resource policy reads exactly like a broken
>> schedule. **Reporting that without the creation timestamp would have been a false outage on
>> infrastructure I built yesterday.** <<

---

## FINDING 2 -- THE ONE NON-CLOUD LEG IS DELIBERATE, NOT AN ACCIDENT

```
OPAL_BBGTML_daily_pull   Enabled  daily 07:00 local (11:00Z)  StartBoundary 2026-08-13
Principal   UserId 'Opal Bloomberg'  LogonType INTERACTIVE  RunLevel Limited
Settings    WakeToRun FALSE · StartWhenAvailable TRUE · RestartCount 0
            ExecutionTimeLimit PT30M · MultipleInstances IgnoreNew
Action      cmd /c integrations\bloomberg\pipeline\scheduled_daily_pull.cmd
```
⭐ **`LogonType: Interactive` READS AS A ROBUSTNESS DEFECT AND IS NOT ONE.** The `.cmd` states the
reason in its own words: the pull talks to **bbcomm on 127.0.0.1:8194 using the logged-in Terminal's
own entitlement**, and *"a SYSTEM-context task would run with no Terminal session and fail every
time."* **This is the narrow legitimate device-specific exception CLAUDE.md names -- being tied to
this box is the code's PURPOSE, not an accident of where it was written.** I was about to file it as
a defect and the source stopped me.

**Current state of the precondition: HOLDING.** Box up 156.8h; console session for `opal bloomberg`
**Active** since 2026-08-18. No battery (desktop), so battery-conditioned settings are inert.
**Sleep is DISABLED** (`STANDBYIDLE` = 0x0 on both AC and DC), so the idle-sleep path several of
tonight's messages worried about **cannot occur on this box**.

⚠ **THE REAL RESIDUAL IS A REBOOT, NOT A SLEEP.** N-able RMM restarts this device on the MSP's
schedule (banked, measured: 6 seats lost 5h10m). After a restart **nobody is logged in**, and an
Interactive task cannot run until a human logs in. `StartWhenAvailable=True` catches it up -- **but
the pull-to-gold margin is only 2 hours**, so a catch-up landing after 13:00Z misses that day
entirely, and gold's own guard then skips silently on a green run.

---

## FINDING 3 -- THE TASK'S EXIT CODE DOES NOT REPORT THE ETF LEG

The `.cmd` isolates deliberately: `RC_ETF` **never touches** `%RC%`, so `LastTaskResult` carries the
**models** chain's verdict. **A `LastTaskResult: 0` read is the WRONG LIMB for the ETF pipeline.**
The ETF leg's only durable per-run evidence is `bbg/{as-of}/run_manifest.json` plus the local log.

**The scheduled ETF leg HAS succeeded** -- read from the leg's own log sections, 30 retained logs:
```
2026-08-22 070001  ETF LEG EXIT CODE: 0
2026-08-23 070001  ETF LEG EXIT CODE: 0
2026-08-24 070001  ETF LEG EXIT CODE: 0
```

---

## FINDING 4 -- `opal-data-etfs` IS **UNVERSIONED**: THE bbg PARTITIONS HAVE NO ROLLBACK

```
get-bucket-versioning opal-data-etfs        -> EMPTY (never enabled)
POSITIVE CONTROL      opal-data-portal-v2   -> {"Status": "Enabled"}
NEGATIVE CONTROL      zzz-no-such-bucket    -> NoSuchBucket error
```
Today's 11:00Z run overwrites `bbg/2026-08-24/` -- currently `run_class: adhoc`, hand-repaired three
times last night (re-key 02:50Z, history re-pull 04:38Z) -- about 2h before gold consumes it.
**Expected-good** (at 11:00Z the local-clock bug cannot bite: `BDay(-1)` of 08-25 is 08-24). **But an
`rc=63` PARTIAL land would leave a mixed partition with no recovery.**

---

## FINDING 5 -- THE AS-OF KEY AND THE UNIVERSE SOURCE DIVERGE ACROSS A WEEKEND

Read from the ETF leg's own log lines, not inferred from the models plane:
```
run 08-22 (Sat)  as-of 2026-08-21   universe from silver/holdings/2026-08-21.parquet   MATCH
run 08-23 (Sun)  as-of 2026-08-21   universe from silver/holdings/2026-08-22.parquet   DIVERGED
run 08-24 (Mon)  as-of 2026-08-21   universe from silver/holdings/2026-08-23.parquet   DIVERGED
```
The as-of is `BDay(-1)`; the universe is derived from **calendar** day -1. They agree Tue-Sat and
diverge on Sunday and Monday runs. **No harm materialised** -- all three produced the same 109
constituents, because weekend holdings files carry Friday forward. **OBSERVATION, filed not fixed:**
a latent grain mismatch, and the manifest's own `universe_source` field is what made it visible.
Outside tonight's fence; `0.4.0_DS_ClientPlatform~Z` / `1.0.0_SA_CTO~Z` to rule.

⚠ **AND THE SAME THREE RUNS ALL WROTE THE SAME KEY** -- `bbg/2026-08-21/`, three times, each
overwriting the last, in an unversioned bucket. That is correct T-1 behaviour, not a bug; stated so
nobody reads a partition's object timestamp as its capture date.

---

## FINDING 6 -- THE CONSTITUENTS LEG HAS **NEVER** RUN ON THE SCHEDULE

`CONSTITUENTS LEG EXIT CODE` is **absent from all 30 retained logs**, including 08-24 070001 -- the
leg was added by Andrew-direct ~15:2xZ on 08-24, after that morning's fire. The only constituents
data in S3 is ad-hoc (`bbg/2026-08-21/constituents/`, written 08-24T18:26Z).
**Today 11:00Z is its first scheduled fire too.**

---

## WHAT TO WATCH AT 11:00Z TODAY -- THE A5 ACCEPTANCE, AND IT IS A READ, NOT AN ASSUMPTION

**Every scheduled run so far produced `universe_count = 109`.** That is the **pre-A5** count. Today's
run reads `silver/holdings/2026-08-24.parquet` (187 rows) and should produce **~170**.
```
CHECK  bbg/2026-08-24/run_manifest.json  ->  run_class == "scheduled"   (not adhoc)
                                             universe_count ~170, NOT ">109"
       characteristics.parquet covers BBSEY and AMX -- match on the ticker TOKEN; the `security`
       column carries Bloomberg-format ids ("AAPL US Equity"), and a bare-ticker compare returns a
       clean ABSENT for EVERY row
       constituents/run_manifest.json EXISTS (first scheduled fire of that leg)
```
**A threshold test (`>109`) passes on a PARTIAL extension while the fill still fails.** Count, do not
threshold. Held jointly with `0.0.0_AB_MSTR~Z`.

---

## THE 13:00Z READ -- OWNED BY `0.7.0_AE_CloudOps~Z`, AND THIS FILE IS THE DURABLE CARRIER

**Accepted from `2.0.0_SA_COO~Z` @8939.** ⛔ **NOT A MONITOR. A PERSON, ONCE.** No alarm, no SNS, no
freshness checker, no `*-monitor` Lambda -- the 2026-07-28 moratorium stands, and this is exactly
the situation that tempts one, which is why it is a named human read instead.

**WHY IT MATTERS: THREE THINGS COINCIDE ON ONE FIRE.** The schedule's first-ever acceptance; the
first PRODUCTION (non-ad-hoc) publication of Andrew's fix; and an unconditional overwrite of a
client-facing artifact that was hand-published twice tonight. **D5 cannot fire, so the run WILL
rewrite the key** -- with the correct code as of 08:19:03Z, so it should reproduce the fix.

⚠ **THE FAILURE MODE IS SILENT IN BOTH DIRECTIONS.** Rule does not fire -> artifact simply stays and
looks fine. Rule fires and produces something different -> the page still renders and looks fine.
**Nobody is watching a number that only moves once a day.**

**THE FOUR CHECKS, after 13:00Z:**
```
(a) a NEW log stream exists for /aws/lambda/etf-positioning-producer at ~13:00Z
    (the 14d retention window held exactly 4 streams pre-fire, all ad-hoc -- so a 5th is the tell)
(b) generated_at ADVANCES past 2026-08-25T08:31:05Z
(c) SALXX -> "State Street U.S. Government MMKT" and FXFXX -> "First American Treasury
    Obligations Fund" STILL hold on the served bytes  (the regression check)
(d) data_as_of ADVANCED, or the bbg guard SKIPPED -- `_bbg_partition_exists` skips any date
    lacking a bbg/{as_of}/ landing, and the 11:00Z pull is a LOCAL task on this workstation.
    Box asleep -> leg 3 SKIPS -> serves yesterday -> REPORTS SUCCESS. Invisible from AWS.
```
⛔ **A DIFFERENT sha at 13:00Z IS EXPECTED AND IS NOT A REGRESSION** -- `generated_at` sits inside
the hashed body. **The NAMES are what must hold; the map is as-of independent.**

⚠ **LIVENESS CAVEAT, STATED BECAUSE AN ABSENT OWNER IS WORSE THAN AN UNNAMED ONE:** I cannot
guarantee this session is live at 13:00Z -- it is ~4.2h out, longer than most sessions in this
fabric. **That is precisely why the obligation lives HERE and in my session log's Next Steps rather
than in a broadcast: a message dies with the inbox that holds it.** Any seat reading this file after
13:00Z should run the four checks if no result has been reported, and needs no further authorisation
to do so.

---

## CARRIED, NOT MINE -- `D5` IS A CONTROL THAT CANNOT FIRE

`0.4.0_DS_ClientPlatform~Z` established (@8697, exercised) that the publisher's D5 "unchanged source
=> no write" **can never fire**: `generated_at` sits inside the hashed body, so the sha differs on
every invocation by construction. **Directly relevant to posture: the 13:00Z write is UNCONDITIONAL.**
Filed by DS, ratified inert by `1.0.0_SA_CTO~Z`. Nobody should cite D5 as protection.

---

## POSTURE SUMMARY

| Leg | Scheduled | Robust | Residual |
|---|---|---|---|
| L1 Bloomberg pull 11:00Z | LOCAL Windows task | deliberate entitlement binding; DAPI precondition + auto sign-in fallback | reboot leaves nobody logged in; only 2h margin to gold |
| gold+platinum 13:00Z | `cron(0 13)` AWS | ENABLED, invoke permission ARN-matched | **first scheduled fire is today** |
| silver 22:00Z | `cron(0 22)` AWS | 14/14 invocations measured | none found |
| canon fan-in 15:45Z | `cron(45 15)` AWS | 14/14 invocations measured | none found |
| silver sweep 23:30Z | `cron(30 23)` AWS | ENABLED | not exercised this pass |

**No leg anywhere in the chain is triggered solely by another pipeline's success.**
