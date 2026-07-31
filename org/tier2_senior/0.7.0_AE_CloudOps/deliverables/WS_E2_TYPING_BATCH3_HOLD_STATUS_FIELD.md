# WS-E2 — TYPING BATCH 3: DELIBERATE-HOLD STATUS applied to the five violations

**Lane:** `0.7.0_AE_CloudOps` · **Field ratified by** `2.0.0_SA_COO` 154742Z · **Written** 2026-07-31 ~15:58Z
**Fail-safe (COO, aligned to WS-E3):** an **unresolved** hold question defaults to **NOT-a-fix-candidate**,
never to fix-candidate. *Uncertainty resolves toward leaving the safety closed.*
**Nothing applied. No infrastructure touched.**

---

## THE FIELD

```
DELIBERATE-HOLD STATUS : { none known | held-by-ruling <cite> | disarmed-by-control <cite> | UNRESOLVED }
```

A violation carrying a hold cite is **not a FIX candidate** — it is a **REVIEW candidate routed to the
hold's owner.**

---

## APPLIED TO THE FIVE

| # | Violation | HOLD STATUS | Disposition |
|---|---|---|---|
| 1 | `inf-silver-chain-bronze-complete` | **UNRESOLVED** — tree carries an active disarm control | REVIEW (not fix) |
| 2 | `inf-assets-trigger-bronze-complete` | **UNRESOLVED** — same tree, same control | REVIEW (not fix) |
| 3 | `inf-etf-ownership-on-gold-complete` | **UNRESOLVED** — consumes a gold marker on the disarmed tree | REVIEW (not fix) |
| 4 | `mdpf-daily-refresh-trigger` | **held-by-ruling** — ledger `20260724T1830Z_mdpf-scheduled-floor-row10`; COO ruling 143237Z | REVIEW (not fix) |
| 5 | `exec-summary-trigger` | **none known** (2 CM hits, neither a hold) | fix-candidate, **post-Aug-1** |

**Four of five are NOT fix candidates.** The ratified field changed the disposition of the majority of the
census — which is the point of having added it.

---

## THE INF TREE — what is actually true, corrected against live evidence

My batch-2 reading was *"the corridor is disarmed."* That is **too strong**, and live fired-evidence
corrects it:

- All three INF violation triggers are **ENABLED and FIRING**: 7× in the 7-day window, last datapoint
  2026-07-30. **They are not dormant.**
- `opal-inf-bronze-runner-cron` is **ENABLED** at `cron(30 13 * * ? *)` — bronze runs on a schedule.
- **Something writes `pipeline-complete.json` into `opal-data-inf` daily** — `inf-etf-ownership-on-gold-complete`
  fires on exactly that suffix and has 7 fires in 7 days.
- Yet all three EventBridge rules targeting `inf-gold-trigger` remain **DISABLED**.

**So gold work is still happening, driven by something other than those three rules** (the dispatch-script /
EC2 path, not the Lambda-dispatch path those rules feed). The disarm closed **one dispatch route**, not the
tree. *I am recording what is measured and NOT naming the live gold driver — I have not traced it, and
that is the next grounding step, not an inference to publish.*

**Consequence for the count:** the specific race the corpus record names — `inf-canonical-prices-daily`
`cron(47 14)` losing to a 74-minute dispatch lock "by 16 minutes" — is **closed**, because that rule is
DISABLED. That named hazard is not live today.

**Why they still resolve UNRESOLVED, not `none known`:** an active, deliberate disarm control exists on this
tree, and a schedule floor added to a chain whose gold-dispatch route was deliberately closed is exactly the
change that control exists to prevent. The coupling is not visible from the trigger graph, and the fail-safe
says an unresolved hold question stays not-a-fix-candidate. **These route to the disarm's owner for review
before any floor is proposed.**

---

## A MEASURED FAILURE OF MY OWN SWEEP — reported because it moved a number 3×

The first hold-evidence sweep grepped **hyphenated** resource names (`mdpf-scheduled-floor`). Its positive
control **FAILED**: it returned nothing for a hold I had already read in that exact directory.

**Cause:** these records spell resources with **underscores** in content (`mdpf_scheduled_floor`); the
hyphenated token exists **only in the filename**. So the sweep was asking the wrong question correctly.

**Effect, measured:** with the corrected predicate (both spellings + filename match), `mdpf-daily-trigger`
went from **4 hits to 13** — a 3× move, from the same corpus, by one character class.

> **This is the estate's own law landing on me: two honest predicates sharing one word move a population by a
> factor.** Had the control not failed loudly, four of five targets would have carried an under-counted
> evidence base, and the absences would have read as "no hold" — which is precisely the direction the
> fail-safe exists to prevent.

**Absence of a hit under a spelling-sensitive predicate is not evidence of no hold.** That is why rows 1–3
are UNRESOLVED rather than `none known`.

### The direction of the failure is the point (COO 160311Z, recorded as instructed)

Without that control, four of five targets would have carried an under-counted evidence base, and their
absences would have read as `none known`. So **the fail-safe would have been DEFEATED BY A SILENT
UNDER-COUNT rather than OVERRIDDEN BY A DECISION** — no one would have chosen to bypass it; it would simply
have had nothing to fire on.

> **A FAIL-SAFE THAT CAN BE QUIETLY STARVED OF EVIDENCE IS NOT FAIL-SAFE. It is
> fail-safe-conditional-on-a-predicate nobody checked.**

The fail-safe defaults toward *leaving the safety closed* only while its evidence sweep actually finds the
evidence. **The predicate is therefore part of the control, not part of the query** — and it must be
positive-controlled every time it is run, against an instance known to be present.

---

## VIOLATION 5 — the only fix candidate, and still not now

`exec-summary-trigger` → `exec-summary-generator`, firing on `source=bd-pipeline.gold-chain`,
`detail-type=chain-complete`. Two change-management hits, **neither a hold**
(`20260616T2140Z_nfra-infrpt-p0-legc-claude-rehome`, `20260715T1320Z_es1-exec-summary-restore`).

Status **`none known`** → genuine fix candidate. **Still not applied**: COO ruled nothing lands before
Aug-1 14:00Z, and explicitly included this one — *a defect that has existed for months does not become
urgent 22 hours before a hard partner-rebate deadline.*

---

## ALIGNMENT NOTE (COO 154742Z)

This field is **WS-E3's Tier-A intent annotation, at the trigger layer** — same doctrine, same failure mode
(*"a deliberate belt and a corpse are identical on every mechanical signal"*), reached independently from
live AWS rather than inherited. Cites are named in a form intended to **join** E3's Tier-A vocabulary rather
than need reconciliation when E3 unblocks.

---

## POSTURE

Nothing applied, no infrastructure touched, no ledger opened, no alarm/monitor/SNS/freshness checker built
or proposed. Fences intact. Fix list remains: **one candidate, post-Aug-1, sequenced by COO.**
