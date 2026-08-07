# MDPF_CANPLAT.P0-7R — **NOT-RUN BY CONSTRUCTION** (filed on the TO's own terms)

**archetype:** VALIDATE · **Author:** `0.7.0_AE_CloudOps~Z` · 2026-08-07 ~12:2xZ / 08:2x ET
**Adjudicated:** COO~Z 122140Z — *"NOT-RUN BY CONSTRUCTION is the correct filing."*
**TO:** `MDPF_CANPLAT.P0-7R.ec2-enumeration-capture.md` @a0728269c

---

## 1. Verdict

**The enumeration did not run, because the window it was defined to ride does not exist today.**
The TO's `<sequencing>` is explicit — *"during the chain's OWN 09:00 ET production-initiated
cycle… if the 09:00 ET cycle does not fire, that is a NOT-RUN report, not a re-trigger"* — and
its `<do_not>` forbids re-triggering. **This is that report.**

**I did not manually start the instance.** A hand-started box would be an ad-hoc run wearing
production's clothes, and the production window IS the point of the capture (adopted P0-7
amendment: *"enumerate during the chain's OWN start"*). Manufacturing the window would have
produced an artifact that looked like the deliverable and answered a different question.

## 2. Why the window is gone — measured, and traceable to my own authorized apply

| # | Fact | Evidence |
|---|---|---|
| 1 | The 09:00 ET floor now targets the NEW producer | `get-schedule mdpf-scheduled-floor` → `Target.Arn = …:function:mdpf-gold-lambda`, ENABLED |
| 2 | The EC2's starter retains exactly ONE rule, with **no schedule** | `list-rule-names-by-target` (mdpf-daily-trigger) → `mdpf-daily-refresh-trigger`; `describe-rule` → **`ScheduleExpression: null`**, EventPattern = S3 ObjectCreated on `opal-data-inf/gold/meta/pipeline-complete.json` |
| 3 | That marker has been **silent 7 days** | `head-object` → **`2026-07-31T14:56:49+00:00`** (135 B) |
| 4 | Instance is stopped | `describe-instances i-02448edb624a7a7cf` → `stopped` |

**POSITIVE CONTROL on fact 3** (so the marker timestamp is a real read, not a broken retrieval):
`opal-data-inf/gold/timeseries/client_performance.parquet` → `2026-08-01T14:54:24+00:00`,
15,205,598 B. The bucket and credentials resolve; the marker's age is genuine.

**Causal chain, stated plainly and owned:** last night's leg-2 atomic re-point (COO-authorized
option (b): new target in, old target removed in the SAME apply, to prevent two producers on one
floor) moved `mdpf-scheduled-floor` from `mdpf-daily-trigger` to `mdpf-gold-lambda`. That was
correct and is exactly what was asked for. **Its consequence is that the EC2 chain lost its
scheduled path**, leaving only an event source that has not fired since 07-31.

## 3. Criterion status

| Criterion | State |
|---|---|
| 1 — S3-pull pattern (Rule 12) | **N/A this filing** — nothing executed on the box |
| 2 — enumeration keys + hashes + denominators | **NOT PRODUCED** (no run) |
| 3 — criterion-1 snapshot NOT re-run, ID stated | **HELD.** Rollback baseline stands: **`snap-0fa2186f01fbc3785`**, completed 100%, StartTime `2026-08-06T20:48:38.684000+00:00`, `vol-071d4d9e2d169bbb9`. **No new snapshot minted.** |
| 4 — no termination / teardown / schedule change | **HELD.** Nothing terminated, stopped, resized, de-scheduled, or re-triggered in service of this TO. |

## 4. The implication that outlives this filing — routed, not resolved

**R12 ("nothing retires before its replacement is verified") is satisfied in the INFRASTRUCTURE
sense and NOT in the WARM-FALLBACK sense.** Pre-re-point, the old chain ran daily on the floor.
Post-re-point it has no live trigger at all. So the rollback posture that reads as *"the old
chain keeps running underneath us"* is not the measured state; **"manual start required" is.**
Nothing is deleted and nothing is retired — but the fallback is cold, not warm, and those are
different safety nets.

⚠ **Any warm-fallback design must first answer the two-producers question** (COO 122140Z): the
re-point removed the old target deliberately to prevent dual-write onto one floor. Re-warming the
old chain is therefore a deliberate act with its own shape — **never a default, and nobody's to
take on their own authority.** Ruling sits with **Andrew at the morning session**.

**Failure-mode context, so the stakes stay honest (COO 122140Z):** if today's 09:00 ET fire fails
Andrew's read, the served plane does not break — platinum holds the 03:52Z set (`as_of_last
2026-08-05`, honest carried/measured labels) and simply does not advance. **The dormancy affects
recovery SPEED options, not served correctness.**

## 5. What re-opens this TO

The enumeration need is re-scoped **if and when the old chain is ever deliberately started
again** (COO 122140Z). Until then there is nothing to capture in a production window, because
there is no production window. Filing NOT-RUN rather than holding the TO open against an event
that cannot occur.
