# WS-E2 — TYPING BATCH 4: the pass closed, and the half of it that CANNOT close yet

**Lane:** `0.7.0_AE_CloudOps` · 2026-07-31 ~16:35Z · **E2 is read-only.** Nothing applied, nothing touched.
Census vintage `2026-07-31T14:02:23Z`; bound stated at `@c19b42f2ab`.

---

## 1. `yang-volatility-orphan` — TYPED. It is NOT a schedule-floor violation.

Measured (model-portfolios vertical; no INF surface touched — Inflection is deferred Andrew-direct):

| Function | Live state | Triggers | Invocations (30d) |
|---|---|---|---|
| `yang-generate-volatility` | EXISTS, Active, modified 2026-05-04 | **ZERO** in the full 154-edge map | **ZERO** |
| `opal-portal-volatility-fetcher` | Active — the live successor | `volatility-daily-update` `cron(30 12 ? * MON-FRI *)` | **22** ← positive control |
| `MA-08-yang-generate-volatility` | **does not exist as a Lambda** | — | — |

**`MA-08-yang-generate-volatility` is a process/module label in the contracts, not a deployed function.**
*A contract subject is not evidence of a deployed resource.*

### The refinement, which matters

The arch-gate predicted: *"if typing says violation + deletion-candidate, its DELETE parks, its
schedule-floor typing lands."* **The DELETE parks — correct. The schedule-floor typing does NOT land.**

The law covers *a pipeline whose **only** trigger is another pipeline's success.* `yang-generate-volatility`
has **no trigger at all.** **Zero-trigger is a different class from event-only-without-a-cron-floor**, and
adding a schedule here would not enforce the floor law — it would **resurrect a function that has not run
in 30 days and has a live successor.**

**It contributes nothing to the violation count. The count stays at 5.**

### The lesson applied before the verdict

A zero-trigger function is **exactly where the producer-to-producer direct-invoke class would hide**, and
*"no trigger" is not "no invocation."* So the dormancy verdict rests on the **invocation metric**, not on
the trigger map — with the live successor run as a **separate** positive control so a zero could not be an
instrument failure. **The zero is real.**

**DELIBERATE-HOLD STATUS: `none known`.** Still not a fix candidate — the open disposition here is
*deletion*, which is the parked half (lifecycle required; all 9 process declarations are `UNDECLARED`).

---

## 2. THE TYPING PASS — one class CLOSED, one class STRUCTURALLY BLOCKED

WS-E2 names two violation classes. They have very different completion states, and reporting the pass as
simply "done" would hide that.

### CLASS A — schedule-floor (*"only trigger is another pipeline's success"*) — **COMPLETE**

```
5 violations / 11 production-pipeline event-edges considered / 20 event-pattern rules
             / T = 154 EventBridge-addressable triggers (142 rules + 12 schedules)
```
Complete because **this class is a property of the trigger itself** — it needs no external declaration to
type. Partition verified (20 + 122 = 142, no residue); one event bus; all 17 regions.
**Bounded** by §6 of the census: `T=154` is the EventBridge-addressable population, not the population of
things that can start a pipeline.

### CLASS B — topological / temporal ordering — **CANNOT BE COMPLETED. Not deferred by choice.**

The PRD types these edges **against the declared D2 paths.** Those declarations are WS-E1's output, and
here is the coverage, measured:

| | count | source |
|---|---|---|
| Chains in the estate | **138** | `comp-estate --list`, this session |
| Semantic verticals | **29** | E1 registry, census vintage 2026-07-30 |
| Verticals with declared contracts | **2** | mdpf, model-portfolios |
| Subjects declared | **14** (7 + 7) | the two `*.contracts.yaml` files |

**E2 cannot type ordering violations across an estate whose producer→consumer paths are declared for 14
subjects out of 138 chains.** This is not a scheduling problem or a slow pass — **the input does not exist
yet.**

**What I did NOT do, deliberately.** Two ordering candidates were visible from cron times alone:
`opal-assets-mdpf-portal-publisher-daily` (16:15) firing *before* `opal-assets-daily-emitter-daily` (17:15),
and `opal-assets-silver-etf-sweep-daily` (23:30) firing *after* the emitter it may feed. **Neither is
asserted.** A cron-time inversion is a **question, not a finding** — it presumes a producer→consumer
direction I have not grounded, and inferring that direction from names and clock order is precisely the
substitution this workstream keeps catching. Recorded as candidates for when E1 coverage reaches them.

> **CLASS B IS GATED ON WS-E1 COVERAGE, AND E2 SHOULD NOT REPORT A CLASS-A NUMBER AS IF IT WERE THE
> WORKSTREAM'S ANSWER.** The honest statement is: *one of E2's two violation classes is complete and bounded;
> the other has 10% of its input.*

---

## 3. WHAT E2 CAN AND CANNOT CERTIFY TODAY

**CAN:** every EventBridge-addressable production pipeline whose only trigger is another pipeline's success,
with a printed predicate, a verified partition, and a declared bound — **5, of which 4 are review-not-fix.**

**CANNOT:** *"zero unscheduled production pipelines."* **Two independent limits**, both found by measurement
and both already routed:
1. **The direct-invoke class** — outside EventBridge, invisible to `list-rule-names-by-target` and
   `get-policy` by construction (source-confirmed, census §6).
2. **Intent** — a deliberately disarmed pipeline and a neglected one share a census signature
   (the DELIBERATE-HOLD field, batch 3).

*Both are limits on the acceptance clause, not on the census.*

---

## 4. POSTURE

Nothing applied, no infrastructure touched, no deploy ledger opened, no alarm/monitor/SNS/freshness checker
built or proposed. Fix list stays at **one** candidate (`exec-summary-trigger`), post-Aug-1, COO-sequenced.
Rows 1–3 REVIEW-not-fix. **Inflection deferred (Andrew-direct); `mode=full` and `aggregator` recorded
DEFERRED with the mechanism-vs-intent separation preserved, and nothing acting on them.**
