# G-1 — Who actually writes the three silver prefixes

**archetype:** DIAGNOSE · **Author:** `0.7.0_AE_CloudOps` · **Date:** 2026-08-10
**GO:** `1.0.0_SA_CTO` 182558Z — G-1 against `docs/architecture/MDPF_PIPELINE_TRUTH.md` v1 @629d252535.
**Fence: REPORT, do not diagnose. Read only.**

> **ALL THREE WRITERS NAMED AND PROVEN — AND THE `*-sweep-daily` RULES ARE NO-OPS.**
> Measured: today's 16:00Z smartx sweep ran **668 ms and wrote nothing**.
> **CTO's headline survives and is better grounded. The LEVER changes.**

---

## 1. The answer

| prefix | WRITER | how established | **actual write time** |
|---|---|---|---|
| `smartx/platform/silver/` | **`opal-assets-silver-smartx`** | the function's own stdout lists every key it wrote | **13:41:51Z** |
| `orion/inflection/silver/` | **`opal-assets-silver-orion`** | S3 notification + resource policy + second-level time tie-out | **14:16:0xZ** |
| `eclipse/inflection/silver/` | **`opal-assets-silver-eclipse`** | same | **22:31:0xZ** |

### smartx — proven on the writer's own log, 2026-08-10T13:41:51Z

```
convert_day 2026-08-10: rmids=11 allocations=9706 accounts=7066
OK  smartx/platform/silver/fact_model_aum_daily/date=2026-08-10/data.parquet  rows=4422
OK  smartx/platform/silver/fact_model_allocation_roster/…                     rows=9706
OK  smartx/platform/silver/fact_model_holdings/…                              rows=164
OK  smartx/platform/silver/fact_model_performance/…                           rows=6654
OK  smartx/platform/silver/fact_model_changerequests/…                        rows=1078
OK  smartx/platform/silver/fact_allocation_account_map/…                      rows=7262
```

**`rows=4422` ties EXACTLY to the row count I independently read from that parquet.** The writer's
claim and the artifact agree — two derivations, not one asserted twice.

## 2. ⛔ The sweeps are NO-OPs — the finding that changes the remedy

**Today's `opal-assets-silver-smartx` 16:00:12Z invocation, its ENTIRE log:**
```
INIT_START … START RequestId: 2ec98355-… END RequestId: 2ec98355-… REPORT Duration: 668.45 ms
```
**Zero output lines. No `convert_day`. No `OK … wrote`.** It ran for 668 ms and wrote nothing.

⇒ In all three cases the sweep is a **second, idempotent trigger of the same function**, firing after
the work is already done. `opal-assets-silver-*-sweep-daily` is correctly *named* — it IS wired to the
real writer — but **it does not write, and its 16:00Z timing is causally irrelevant to the data.**

> **THE HEADLINE SURVIVES; THE LEVER DOES NOT.** "Three silver legs land after the floor" is TRUE —
> at **13:41Z / 14:16Z / 22:31Z**, not 16:00Z. **A remedy aimed at the 16:00 sweeps would move a
> no-op and change nothing while appearing to.** That is the wrong-lever failure CTO named, and it
> was one apply away from being shipped.

*This closes, from the opposite direction, the item I retired this morning: I had reported the sweeps
as "a second trigger of the same converters" from the notification wiring. That was right about the
**wiring** and said nothing about **behaviour**. The 668 ms empty run is the behavioural proof —
config told us what could happen; only the log tells us what did.*

## 3. The number that matters most — the axis source

**`smartx/platform/silver/` — THE AXIS SOURCE — is written at 13:41:51Z. The floor fires at 13:00Z.**

**The axis source is written 41 minutes AFTER the thing that reads it.** That is why the floor reads
yesterday's partition, why the frontier lands on 2026-08-06, and — until the cross-firm axis fix —
why inflection is handed a date it never carried.

Upstream chain, today: `smartx-rest-pull` **13:17:28Z** → `smartx-assets-daily-pull` **13:30:51Z**
(JWT mint via ROPC + vendor pull) → converter **13:41:51Z**.

## 4. Bounds and loose ends — named, not smoothed

⚠ **THE 13:41Z INVOKER IS NOT ESTABLISHED.** The converter's resource policy carries only
`arn:aws:s3:::opal-data-assets` and its sweep rule, and **no S3 notification routes any smartx prefix
to it** — re-read all **8** configs on the bucket (blackdiamond, eclipse, etf ×3, orion, schwab ×2;
**smartx absent**). So the 13:41Z invocation is **neither the sweep nor an S3 event**.
`smartx-assets-daily-pull` finishing 76 s earlier is the obvious candidate — an identity-based invoke
needs no resource-policy statement — **but no invoke line was found in its log and I am not asserting
it.** OPEN.

⚠ **A GRANTED-BUT-UNWIRED TRIGGER.** That `arn:aws:s3:::opal-data-assets` statement permits S3 to
invoke `opal-assets-silver-smartx`, and **no notification exists to do so.** A dead grant, flagged in
both directions: a least-privilege sweep would delete it as unused, and a reader checking permissions
would conclude the S3 path is live when it structurally cannot fire.

⚠ **CALENDAR FRAME CARRIED.** `wsb-49f-model-aua-pull-daily` and `wsd-49f-partner-held-etf-pull-daily`
are **`cron(30 3 ? * TUE-SAT)`** — weekday-masked, not daily. Nothing above rests on a masked job.

## 5. Compiler Tools

| Tool | Result |
|---|---|
| `aws logs get-log-events` (writer stdout, both invocations) | The decisive instrument — **an empty 668 ms run is only visible in the log**; no config read could show it |
| `aws lambda get-policy` × 3 | Invocation sources per function — surfaced the granted-but-unwired S3 statement |
| `aws s3api get-bucket-notification-configuration` | 8 configs, denominator printed; **smartx's absence is what made the 13:41Z invoker an open question rather than an assumed one** |
| parquet row-count (boto3, prior read) | Independent tie-out of `rows=4422` against the writer's own claim |

**Method note:** the sweep question was answerable **only from behaviour**. Its name says "sweep," its
wiring says "invokes the writer," its schedule says "16:00Z" — and all three are true while the run
does nothing. *Name, wiring and schedule are three config-layer facts that agree with each other and
with a false conclusion.* Only the log discriminated.

## 6. State

Read only. **Nothing applied, re-run, or repaired.** No remedy proposed — the 16:00-sweep lever is
retired on evidence, and the real ordering lever sits with CTO's ruling and DS's lane.
