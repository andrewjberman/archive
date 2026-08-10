# MDPF_REMED.W1-5 — Inflection ingest window retime: PRODUCER IDENTIFICATION + measured timing

**archetype:** DIAGNOSE · **Author:** `0.7.0_AE_CloudOps` · **Date:** 2026-08-10
**Discharges:** `MDPF_REMED.W1-5.inflection-ingest-window-retime.md` (issued 2026-08-07 by
`2.0.0_SA_COO`; its `<scope>` names a `..._20260807.md` filename — this is that deliverable, dated
to the day the work was actually done).
**Status: MEASUREMENT COMPLETE. NO SCHEDULE CHANGED.** The TO's own
`<cross_domain_coordination>` requires surfacing the INF-side blast radius to CTO **before**
applying, and every lever identified here is INF-owned. Surfaced to CTO 2026-08-10; awaiting word.

**HEAD at measurement:** `74f8813668`. All AWS reads live this session.

---

## 0. The answer in five lines

1. The producer is **not** either 16:00 sweep. It is a **three-hop chain** whose clock is
   `opal-assets-ingest-mirror`, a Lambda with **two** schedules — one of which lives in
   **EventBridge Scheduler, a different service that `list-rules` cannot see.**
2. **23 ENABLED inf/mdpf-family schedules fire AFTER the 13:00Z floor.** Not four.
3. **T-1 cannot be broken by this retime.** The label is normalized downstream by
   `orion_normalize_as_of` = `prior_trading_day`, source-confirmed. This discharges the TO's
   `<do_not>` on T-1.
4. **Andrew's 12:00–13:30Z window is achievable for Orion** — the vendor is early-valid at
   ~12:10Z (independent `~Z` probe). **The constraint is our own schedule, not the vendor.**
5. **The producer has failed 100% of invocations for at least 14 consecutive days** and nobody
   saw it, because the inflection rows land *before* the raise.

---

## 1. PRODUCER IDENTIFIED BY MEASUREMENT (W1-5 criterion 1)

### The chain, end to end

```
opal-assets-ingest-mirror                    <-- THE CLOCK. Two triggers:
  |    rule/opal-assets-ingest-mirror-inf-daily     cron(15 14 * * ? *)  UTC          = 14:15Z
  |    schedule/opal-assets-ingest-mirror-cot-daily-et
  |                                          cron(30 18 * * ? *)  America/New_York    = 22:30Z (EDT)
  |
  +--> writes BRONZE ONLY (raw bytes; lambda_function.py:112,119)
  |      orion/inflection/bronze/     eclipse/inflection/bronze/
  |
  +--> S3 ObjectCreated notification (opal-data-assets, prefix+suffix filtered)
  |      Prefix=orion/inflection/bronze/    Suffix=.jsonl.gz  -> opal-assets-silver-orion
  |      Prefix=eclipse/inflection/bronze/  Suffix=.json      -> opal-assets-silver-eclipse
  |
  +--> THE SILVER WRITERS. Partition date comes from a REGEX ON THE SOURCE KEY
         (mirror_conversion.py:175,181) -- NOT from the run clock.
         orion/inflection/silver/fact_positions/date=D/data.parquet
         eclipse/inflection/silver/fact_model_composition/date=D/data.parquet

  (+ opal-assets-silver-{orion,eclipse}-sweep-daily, cron(0 16) = 16:00Z --
     a SECOND, idempotent trigger of those SAME converter functions.)
```

### Evidence

| Claim | Grounding |
|---|---|
| Mirror is the clock | Resource policy enumerates **exactly 2** invocation sources: `AllowEventBridgeInvokeInf`, `SchedulerMirrorCotDailyEt` |
| Mirror writes bronze, not silver | `lambda_function.py:112` `"dst_prefix": "orion/inflection/bronze/"`; `:119` eclipse. Docstring line 1: *"Source bronze -> the monolith, raw bytes only."* |
| Converters are S3-triggered | `get-bucket-notification-configuration` on `opal-data-assets` — 8 Lambda configs, two of them the prefix/suffix rows above |
| Converters have no other clock | Each converter's resource policy: `AllowS3InvokeFromMonolith` + `AllowEventBridgeInvokeSweep`, nothing else |
| Times reconcile | orion silver `date=D` lands `D 14:16:03–06Z` (mirror 14:15Z + S3 event); eclipse silver `date=D` lands `D 22:31:07–10Z` (mirror 22:30Z + S3 event) |
| Rows named by the function itself | CloudWatch stdout: `DENOMINATOR: {'row': 'orion/inflection', ...}` / `{'row': 'eclipse/inflection', ...}` |

### The 16:00 sweeps — the criterion-1 finding, in its correct form

The TO anticipated "two ENABLED rules named for work something else is doing." **That framing is
wrong and I am retiring it.** The sweeps *do* run (08-09: silver-eclipse 16:00:06Z, silver-orion
16:00:46Z) and they invoke **the same converter functions** the S3 event does — they are the
idempotent catch-up leg, the same two-trigger-one-function pattern as the mirror.

The real finding is structural: **the declared producers do not reconcile with the measured
landing because the landing is driven by an S3 event from a THIRD function on two schedules,
neither of which is 16:00 — and one of those two is in EventBridge Scheduler, which does not
appear in `list-rules` at all.** That service split is *why* this stayed unattributed.

> **CORRECTION ON THE RECORD.** My first report to COO (135422Z) named the mirror as the silver
> writer, on a to-the-second time correlation plus a matching row name. Both facts were real;
> neither was the mechanism. The mirror is the trigger, one hop upstream. Corrected at 135842Z.
> This is CLAUDE.md Rule 22 exactly — live state grounds WHAT, only source grounds WHY — and the
> docstring that refutes me was line 1 of a file I had already opened.

---

## 2. MEASURED TIMING, TRUE UTC (W1-5 criterion 2 input)

`list-objects-v2` `LastModified`, never `aws s3 ls` (which renders local EDT).

| feed | pattern | window measured |
|---|---|---|
| `orion/inflection/silver/fact_positions/` | **SAME-DAY 14:16Z**, unbroken | 07-20 → 08-09 (20 partitions) |
| `eclipse/inflection/silver/fact_model_composition/` | T+1 **03:30Z** → now SAME-DAY **22:31Z** | 07-20 → 08-09 |

### The W1-5 context table is half wrong, and the wrong half is Orion

The TO presents **one** landing pattern (`T+1 03:30`) for **both** prefixes. Measured separately,
Orion was **never** on that pattern at any point in the 20-partition window. Eclipse was, and is
not any more: "OFF-PATTERN, same-day" in the TO has now held **three consecutive days** (08-07,
08-08, 08-09). It is the new steady state, not an anomaly.

### Why eclipse moved — mechanism, source + live confirmed

```
commit ce99054e44   authored 2026-07-29 by 0.7.0_AE_CloudOps~A
                    "cot(4:30p ET move) ... mirror -> cron(30 18) America/New_York
                     (DST-safe; old UTC rules die in the same change)"
Scheduler CreationDate == LastModificationDate == 2026-08-06T00:04:48Z   <-- THE APPLY

  last 03:30Z eclipse write   2026-08-05T03:30:30Z    (pre-apply)
  APPLY                        2026-08-06T00:04:48Z
  date=2026-08-05 written      2026-08-06T14:16:05Z    (post-apply; picked up by the 14:15Z leg)
  date=2026-08-06              MISSING                 (the cutover gap)
  date=2026-08-07 onward       22:31Z steady           (the new cot schedule)
```

**COMMITTED 07-29, APPLIED 08-06.** The apply is the pattern change, not the commit.

> **BANKED LINE, NOT CHASED** (per the TO's `<do_not>`): the missing `2026-08-06` partition is
> explained by this cutover gap. Reported to COO; not investigated further, not opened.

---

## 3. THE FLOOR AND WHAT SITS BEHIND IT

`mdpf-scheduled-floor` = `cron(0 9 * * ? *)` **America/New_York** → **13:00Z** in EDT.
Target `mdpf-gold-lambda`.

**23 ENABLED inf/mdpf-family schedules fire after it.** Denominators printed:
**139 EventBridge rules** (121 scheduled / 18 event-pattern), materialised and counted
client-side — no `--query length`, no `--no-paginate` — plus **16 EventBridge Scheduler**
entries, a separate service absent from `list-rules` entirely.

| UTC | name | vs floor |
|---|---|---|
| 12:05Z | `opal-inf-jwt-fetch` | before −0h55m |
| **13:00Z** | **`mdpf-scheduled-floor`** | **THE FLOOR** |
| 13:17Z | `inf-api-reps-daily` | +0h17m |
| 13:22Z | `inf-accounts-v2-daily` | +0h22m |
| 13:27Z | `inf-unified-account-dim-daily` | +0h27m |
| 13:30Z | `opal-inf-bronze-runner-cron` | +0h30m |
| 13:32Z | `inf-api-assets-v2-daily` | +0h32m |
| 13:33Z | `inf-api-eclipse-daily` | +0h33m |
| 13:37Z | `inf-api-positions-daily` | +0h37m |
| 13:42Z | `inf-tax-daily` | +0h42m |
| 13:47Z | `inf-api-txn-daily` | +0h47m |
| **14:15Z** | **`opal-assets-ingest-mirror-inf-daily`** | **+1h15m** ← orion silver |
| 14:43Z | `inf-bronze-complete-emitter-daily` | +1h43m |
| 15:00Z | `inf-etf-ownership-daily-schedule` | +2h00m |
| 16:00Z | `opal-assets-silver-{eclipse,orion,smartx}-sweep-daily` | +3h00m |
| **22:30Z** | **`opal-assets-ingest-mirror-cot-daily-et`** | **+9h30m** ← eclipse silver |

**The floor fires before the entire day's ingest chain begins.** It is not four intakes; it is the
chain.

---

## 4. T-1 IS NOT AT RISK — the TO's `<do_not>` discharged at source

The concern was real and I held the apply on it: Andrew's window (ingest 12:00–13:30Z, floor
13:30Z) would have the floor read a partition written ~10 minutes earlier the same day. If
`date=D` meant *day-D content*, that converts a T-1 read into a same-day one — forbidden.

**It does not.** Two source-confirmed facts:

1. **The partition date is a property of the SOURCE FILENAME, not the run clock**
   (`mirror_conversion.py:175,181` — `date=m.group(2)` from a regex on the source key). Moving a
   schedule cannot relabel a partition; it only changes *when* a given date lands.
2. **The vendor forward-labels and we normalize back**
   (`data/inf/scripts/silver/_orion_vendor_asof.py:126-136`):
   ```python
   def orion_normalize_as_of(labeled_max: dt.date) -> dt.date:
       """Orion pre-open forward-labels the prior settled close as the run-date, so the
          true vintage is the prior NYSE trading day of the labeled date
          (SEALED systematic-1-trading-day, 2026-07-02)."""
       return prior_trading_day(labeled_max)
   ```

**T-1 is enforced by the normalizer, deterministically, one trading day back — never by the
clock.** An earlier ingest cannot break it. *(Coverage caveat carried from that docstring: the
NYSE table is hardcoded 2025–2027; outside it, holiday precision degrades to weekend-only.)*

---

## 5. CONVERGENCE WITH P0-2R — two independent derivation legs

Per CTO's instruction I measured **first** and opened `MDPF_H1_INFLECTION_EARLY_CLOCK_20260807.md`
(`0.7.0_AE_CloudOps~Z`, @610fac9d4) **after**, so this is a genuine second derivation, not an
anchor. The legs are genuinely different — `~Z` probed the **vendor** (is data valid early?), I
measured the **pipeline** (when does our chain move it?) — so agreement is evidence, not an echo.

| | `~Z` (vendor leg) | me (pipeline leg) |
|---|---|---|
| Orion | **EARLY-VALID 08:10 ET = 12:10Z**, settled money, TODAY==PRIOR delta 0.0000% | our chain first touches it **13:37Z**; silver lands **14:16Z** |
| Eclipse | EARLY-VALID on modeling surface 12:13Z; `fact_portfolios_full` **NOT-PROBED** | silver lands **22:31Z** |
| JWT floor | mint **lands** 12:06:33Z, ~93s after the 12:05Z cron | `opal-inf-jwt-fetch` `cron(5 12)`, confirmed |
| Orion vs 08:40 ET bar | misses **20 of 21** days | consistent — 14:16Z is 10:16 ET, always past it |

**⇒ THE JOINT CONCLUSION NEITHER LEG REACHES ALONE: there is a ~2-hour gap between the vendor
having valid data (12:10Z) and our chain beginning to pull it (13:17Z), and a ~4-hour gap to
silver landing (14:16Z). Andrew's 12:00–13:30Z window is achievable for Orion, and the binding
constraint is our own schedule — not the vendor.**

**Eclipse is not yet established.** `fact_portfolios_full` is NOT-PROBED and SmartX read
EARLY-INVALID. Those are real gaps; CTO's "measure first, then set intake = delivery + margin"
still binds for anything the two probes do not actually establish.

### Feasible shape (NOT a proposal to apply — CTO's call, INF-owned)

```
12:05Z  opal-inf-jwt-fetch                UNCHANGED (mint lands ~12:06:33Z)
~12:15Z INF orion/eclipse API pulls       from 13:17-13:47Z   <-- INF-OWNED, cross-program
~13:05Z opal-assets-ingest-mirror         from 14:15Z         <-- mine
~13:06Z silver lands via S3 event         (automatic; converters need no change)
13:30Z  mdpf-scheduled-floor              from 13:00Z         -> 24 min margin (Andrew asked >=10)
```

**Timezone decision, stated explicitly per criterion 3:** the floor is currently
`cron(0 9)` **America/New_York**. Andrew's window is stated in **UTC**. Keeping ET means
13:30 ET = **17:30Z**, which is *not* his window; and DST would move it again in November.
**Recommendation: switch the floor to a UTC expression** so the stated window and the deployed
expression are the same units. Flagged, not decided — this is a ruling, not an edit.

---

## 6. SURPRISE-CHANNEL FINDING — the producer is failing 100%, and has been for 14+ days

**`opal-assets-ingest-mirror`: CloudWatch `Invocations == Errors == 6.0/day, every day,
2026-07-27 → 2026-08-09, no exceptions.** *(14 days is my **window bound**, not the failure's age
— it predates the read.)*

```
[ERROR] MirrorRaise: ALIEN SURPLUS on blackdiamond/cottonwood: 653 unexpected key(s)
        under blackdiamond/cottonwood/bronze/ -- stray/duplicate write
  lambda_function.py:449 -> _assert_landed_membership -> :241 raise MirrorRaise
```
2 triggers × 3 attempts (Lambda async retry) = the 6.

**WHY IT IS INVISIBLE — and this is the part that matters.** The orion and eclipse rows
**complete cleanly first** (`written: N, verified: N, failed: 0, missing: 0`), and the raise
happens *afterward*, on an unrelated firm's row. So the inflection data lands correctly every
single day while the invocation reports total failure: **a green data path on a red function.**
Every downstream freshness read is satisfied; the function has never once succeeded.

Reported to COO as one surprise-channel line. **No action taken — out of W1-5 scope, and the
`blackdiamond/cottonwood` row is Cottonwood's, not MDPF's.** Routing is COO's.

Note the mirror's own design intent here (docstring): the DENOMINATOR emission exists precisely so
the component *cannot* lie about its own work — *"a mirror that copies 37 of 40 and exits 0 is
indistinguishable from one that copied 40."* It is working exactly as designed. It is raising
honestly, every day, and **nothing is reading it.**

---

## 7. Compiler Tools

| Tool | Result | Note |
|---|---|---|
| `comp-which "what writes eclipse inflection silver fact_model_composition"` | near-tie, 3 of 75 | Honest no-route: scored `comp-estate` / `comp-pipescript io` tied at 1.50 and said so rather than guessing. Routed me to `comp-find`. |
| `comp-find --name "*ingest-mirror*" infra/` | **0 hits / 7,730 scanned** | A measured zero with its denominator — the file exists as a *directory* name, not a filename. The printed denominator is what stopped me reading it as absence. |
| `comp-find "ingest-mirror-cot-daily" infra/` | 3 hits / 7,730 · SURFACED=1 CONFIG=2 | Band split separated the census *mention* from the trigger-map *declaration* in one call. |
| `comp-find "orion_normalize_as_of"` | 120 hits / 24,955 · **DEF=1** SURFACED=92 DOC=25 | The `[DEF]` band took me straight to the definition line out of 120 hits. This is the call that discharged the T-1 question. |
| `comp-find "date=" .../opal-assets-silver-orion/` | 22 hits / 8 files | Found the partition-date regex — the second half of the T-1 answer. |
| raw `aws` (EventBridge/S3/Lambda/CloudWatch/Scheduler) | live primitives | Rule 22a: a comp-tool reads DESIRED (parsed TF) and cannot tell landed from planned. Every timing claim here is an APPLIED read. `comp-iam` not run — no IAM change and no new boto3 call in this measurement pass. |

**Gap worth naming:** no comp-tool surfaced the **EventBridge Scheduler** entry. `comp-which`
routes schedule questions toward `comp-aws`/rules-shaped views, and the cot trigger is invisible
to `list-rules` because it lives in a different service. **The one trigger nobody had attributed
is the one in the service our tooling does not enumerate.** Per CLAUDE.md — *"the comp-tooling is
not additive, it is foundational"* — a coverage gap is a defect. Raised for CTO routing; not
built (Rule: propose, do not implement).

---

## 8. ADDENDUM — Track A: the cottonwood producer, found (CTO-GO'd hunt)

### 8.1 A CORRECTION TO §3 OF THIS DOCUMENT, AND IT IS THE IMPORTANT PART

I reported to CTO and COO: *"not a Lambda, and nothing fires at 06:00Z across 139 rules + 16
Scheduler entries."* **THAT WAS FALSE.** `cot-rebalancer-runner-daily` = `cron(0 6 * * ? *)`,
ENABLED — **and it was in my materialised 139-rule file the entire time.**

I filtered the 139 by keyword (`orion|eclipse|inf|silver|sweep|mdpf|asset`) to build the §3 intake
table, then made an **absence claim about 06:00Z while citing the full 139.** That rule matches
none of those keywords. Unfiltered, **10 rules fire between 05:00 and 07:00Z.**

> **THE CLASS, NAMED: an upstream stage silently redefined the domain the downstream claim measured
> over, and the output did not carry its own frame.** My pagination discipline was correct and
> irrelevant — the leak was the filter, and I never re-stated the frame when moving from the table
> to the absence claim. **Printing "139" beside a subset-derived absence lent it false
> completeness: a denominator next to a filtered result is worse than no denominator at all.**
> Cost: it pushed the non-AWS and vendor-direct hypotheses up COO's list on the strength of what
> looked like a complete AWS-side sweep. CLAUDE.md Git §"put the control on the RETRIEVAL", the
> ACCIDENTAL half — remedied by *how you call it*, which here means re-deriving the frame at the
> point of the claim, not once at the top.

### 8.2 The producer

`cot-rebalancer-runner` (Lambda) ← `rule/cot-rebalancer-runner-daily` `cron(0 6)` — sole
resource-policy source.

```
REBAL_BASE   = https://rebalancer.bdreporting.com     <- paginated vendor API
BD_FIRM_ID   = cottonwood
BD_S3_BUCKET = opal-data-assets                       <- WRITES THE MONOLITH DIRECTLY
```
Log stream last-event 06:00:48Z on 08-08, 08-09, 08-10 against object landings 06:00:43–47Z.

### 8.3 TWO PRODUCERS ON ONE PREFIX — established by KEY GRAMMAR, not inferred

Under `blackdiamond/cottonwood/bronze/`, **DENOMINATOR 1,229 objects**:

| count | grammar | producer |
|---|---|---|
| 687 | `{table}/{date}/*.json` (`page_000.json` …) | `cot-rebalancer-runner` |
| 368 | `{table}/*.xlsx` (`{TABLE}_DAILY_{date}.xlsx`) | the mirror, from `opal-data-cot/forwardfill_v2/` (row map :137–153) |
| 4 | legacy `_BRONZE_COMPLETE.json` | June sentinels |

The mirror's `ALIEN SURPLUS` samples are the JSON grammar. **THE GUARD IS RIGHT AND THE ESTATE
UNDERNEATH IT CHANGED** — it correctly reports 653 keys it did not write. "Fix the mirror" is the
wrong shape; the open question is **ownership** of that prefix, and whether a vendor API pull
should land in the monolith directly at all, bypassing the mirror's raw-bytes contract. COO's
Track D; not mine, no action taken.

### 8.4 CTO's 02:00Z anchor was RIGHT, and went stale on the same apply

`opal-data-cot/bronze/_BRONZE_COMPLETE.json`:
```
08-02 02:02:00Z  08-03 02:01:18Z  08-04 02:07:19Z  08-05 02:02:21Z
08-06 20:33:02Z  08-07 20:32:22Z  08-08 20:32:05Z  08-09 20:31:47Z
```
Moved 02:0xZ → 20:3xZ on **2026-08-06** — the ce99054e44 apply date (`2026-08-06T00:04:48Z`).
**ONE APPLY MOVED BOTH THE ECLIPSE PATTERN (§2) AND THE COT DELIVERY.** That resolves CTO's open
(a)-vs-(b) toward **(b) it moved**, and flags the 08-06 apply as an under-appreciated event:
anything anchored before it should be re-derived.

⚠ **BOUND, stated because §8.1 is what happens when a bound is not honoured:** I measured the
**sentinel's** history, not the xlsx's. `forwardfill_v2/` currently lands 20:31:05–47Z
(consistent), but I did **not** pull its pre-08-06 history. "The xlsx moved on 08-06" is
**INFERRED from the sentinel**, not measured.

### 8.5 The premise of the cottonwood move has changed

```
06:00Z  cot-rebalancer-runner         -> assets bronze DIRECTLY (json)
20:30Z  cot-bd-session-daily-et       -> starts cot-exporter EC2 (ran 20:30:17 -> 23:36:18Z, 08-09)
20:31Z  opal-data-cot/forwardfill_v2  -> the xlsx APPEARS, ~60s after the session fires
22:30Z  the mirror                    -> copies forwardfill_v2 -> assets bronze (xlsx)
```

**`cot-bd-session-daily-et` DOES NOT WAIT ON DATA ALREADY ON DISK — IT PRODUCES THE DATA.** The
"18.5-hour wait" describes the pre-08-06 regime. Today the session *is* the producer and its output
appears a minute later. So moving it earlier is not "stop waiting," it is **"produce earlier"** —
which turns on vendor availability at the new hour, and that is **UNMEASURED**. A different
decision with a different risk. No time proposed, nothing applied; CTO ruling + COO sequencing.

---

## 9. State, honestly

**DONE:** producer identified by measurement with evidence; true-UTC timing for both feeds;
eclipse pattern-change mechanism; the 23-after-floor census with denominators; T-1 discharged at
source; independent convergence with P0-2R; the 100% failure surfaced.

**NOT DONE, and deliberately:** **no schedule has been changed.** Criteria 2, 3 and 4 (land the
window / move the floor / verify on an exercised cycle) are **not met** and cannot be met by me
alone — the levers are the INF API pull schedules, which are another program's, and the TO
requires CTO surfacing first.

**NOT CLAIMED:** nothing here fixes the 6/12. Per criterion 5 and CTO's verbatim guard —
Cottonwood + 49financial are schedule-ordering; **inflection was refused by the cross-axis
coherence gate at 22:47:19Z on 08-07 and is a separate open thread; global inherits inflection's
date.** COO's measured inversion stands and points the other way: inflection **passed on
two-day-stale data at 13:00Z and refused 16-minute-old data at 22:47Z**, so a successful retime
should be expected to surface the refusal **more** often, not less. If 6/12 moves, that is a
result to report with surprise — not a confirmation of the premise.
