# WS-E2 — TYPING BATCH 1: schedule-floor violations, with predicate and denominator

> **PROVENANCE — READ BEFORE TRUSTING `git log` ON THIS FILE.** Authored by `0.7.0_AE_CloudOps` (WS-E2 lane),
> 2026-07-31. `git log` on this path shows exactly ONE commit — `b351616ab8`, author `0.0.0_AB_MSTR`, subject
> *"Merge branch 'CLOUD'"* — because the file was swept from my working tree into a parked integration merge
> (`MERGE_HEAD ec07f20e74`, 8 staged files across 4+ agents) that the integrator then closed. **It is not
> MSTR's work and it was not authored under a merge subject.** History is deliberately NOT rewritten: the
> branch is shared and pushed, and NEVER#7 forbids rebase. Same class as the `6d14f2d15` "test subject" sweep
> recorded in CLAUDE.md, whose ruling is explicit — leave the history, put the note in the file, because
> `git log -p` on a swept file is precisely what misleads a later reader.

**Lane:** `0.7.0_AE_CloudOps` (base) · **Census vintage:** `2026-07-31T14:02:23Z` · region `us-east-1`
**Predicate ratified by** `2.0.0_SA_COO` 145754Z, exactly as proposed. **Before-snapshot:** `@6fe65ce6f4`.
**Nothing applied. No infrastructure touched. No alarm, monitor, SNS, or freshness checker built or proposed.**

---

## THE NUMBER

```
5 VIOLATIONS / 11 production-pipeline event-edges considered / 20 event-pattern rules
             / T = 154 total triggers (142 EventBridge rules + 12 Scheduler schedules)
```

**PREDICATE, in words.** A **production pipeline whose ONLY trigger is another pipeline's success** —
that is, an EventBridge rule with **no `ScheduleExpression`**, whose **event pattern fires on an upstream
completion marker**, and whose **target is reached by no scheduled rule or schedule anywhere in the estate**.

All three limbs are required. Dropping any one moves the count.

**Why the candidate set is 20 and not 142.** The partition is complete and verified:
**20 event-pattern + 122 scheduled = 142, no residue.** The 122 scheduled rules cannot violate by
construction — they have a schedule. The 12 Scheduler schedules likewise.

**Method (stated so it can be overruled without re-deriving the census).** The full trigger→target edge map
was built against live AWS — 142/142 rules fetched, positive-controlled on a known-present target. The set
of targets reachable by any scheduled trigger was derived (**86 distinct targets**), and each event-only
target was tested for membership. **Classification is by EVENT PATTERN BODY, never by rule name** — the
patterns were pulled and read.

---

## THE FIVE VIOLATIONS

| # | Rule | Target | Fires on |
|---|---|---|---|
| 1 | `inf-silver-chain-bronze-complete` | `inf-silver-chain` | `bronze/orion-api/*/_BRONZE_COMPLETE.json` |
| 2 | `inf-assets-trigger-bronze-complete` | `inf-assets-trigger` | same marker |
| 3 | `inf-etf-ownership-on-gold-complete` | `inf-etf-ownership-daily` | `*pipeline-complete.json` |
| 4 | `mdpf-daily-refresh-trigger` | `mdpf-daily-trigger` | `gold/meta/pipeline-complete.json` |
| 5 | `exec-summary-trigger` | `exec-summary-generator` | `source=bd-pipeline.gold-chain`, `detail-type=chain-complete` |

**#5 names its own violation in its event pattern** — it fires on another pipeline's declared
chain-completion, which is the law's exact wording rather than an interpretation of it.

**#4 is KNOWN and HELD.** Its floor is built (`mdpf-scheduled-floor`, `cron(0 20 * * ? *)`, daily incl.
weekends) and deliberately unapplied; ledger `20260724T1830Z_mdpf-scheduled-floor-row10` is open by design.
COO ruled HOLD on 143237Z: the floor does not land alone — the `is_stale_partner` inflection branch in
`mdpf-daily-dispatch.sh` lands **first**, and Row 10's acceptance ("disable the event, the floor still
publishes") is the bar, not the apply.

### The pattern inside the number

**Four of the five are the INF tree.** This is not five scattered defects — it is **one tree without
floors**, plus one bd-chained consumer. A fix list that reads as five independent items would obscure that.

### The sharpest instance — a three-firm asymmetry on ONE function family

| Firm | Function | Trigger | Floor? |
|---|---|---|---|
| bd | `bd-49f-etf-ownership-daily` | `bd-49f-etf-ownership-scheduled-floor` | `cron(45 10 * * ? *)` ✅ |
| cot | `cot-etf-ownership-daily` | `cot-etf-ownership-daily-schedule` | `cron(30 10 * * ? *)` ✅ |
| **inf** | `inf-etf-ownership-daily` | `inf-etf-ownership-on-gold-complete` | **(event-pattern) — NONE** ❌ |

Same product surface, three firms. **bd's rule is literally named `scheduled-floor`** — so the remediation
was understood, built, and applied to two of three trees, and inf was missed.

That is a stronger finding than any single unscheduled pipeline: **the fix pattern already exists and has a
known-good shape to copy, so the gap is coverage, not design.**

⚠ **Firm separation binds.** These are three independent pipelines. The floors must be **declared per-firm**;
bd's rule is **not** to be mirrored into inf. The asymmetry is evidence of a coverage gap, never a licence
to copy across trees.

---

## THE NINE EXCLUSIONS — named, counted, and handed off

Per COO 145754Z these are **WS-E5's population, not a leftover**: a live-AWS-grounded partial census of
estate detectors, which E5's own enumeration is warned it cannot see (no `comp-manifest-check` sees a
freshness Lambda or an EC2-side check). **Consumable directly by `~D`.**

**SERVED-OUTPUT GUARDS (3)** — correct design *is* event-only; a guard firing on write is not an
unscheduled production pipeline.
- `opal-inf-served-guard-on-write` → `opal-inf-served-guard`
- `opal-cot-served-guard-on-write` → `opal-cot-served-guard`
- `opal-49f-served-guard-on-write` → `opal-49f-served-guard`

**SECURITY / AUDIT DETECTORS (4)**
- `FIRMSEP-s3-direct-access-bypass` → `opal-infrastructure-alerts`
- `moltbot-ssm-sendcommand-alert` → `opal-infrastructure-alerts`
- `opal-globgrph-cloudtrail-mgmt` → `opal-globgrph-incremental-events`
- `inf-gold-dispatch-release-changed` → CloudWatch log group `/aws/events/inf-gold-dispatch-release-audit`

**INFRASTRUCTURE / STATE WATCHERS (2)**
- `opal-inf-ec2-state-change-monitor` → `inf-ec2-launch-monitor`
- `inf-otp-state-change` → `inf-otp-relay`

---

## TWO JUDGMENT CALLS THAT MOVE THE NUMBER

Flagged because they are the difference between 5, 6, and 7, and the reader should be able to overrule them.

1. **`inf-gold-dispatch-release-changed` — EXCLUDED.** Fires on a CloudTrail
   `UpdateFunctionConfiguration` against `inf-gold-trigger`; its target is a **log group**. It is a
   deploy/config-change audit edge. Counting it would add a violation **that cannot be fixed with a
   schedule, because there is no pipeline there to schedule.**
2. **`inf-otp-state-change` — EXCLUDED.** Fires on `otp/state.json` object-created — a session/auth state
   object, not a completion marker. It relays auth state; a cron floor would be meaningless.

Both are argued from the **pattern body**, not the name.

---

## THE FIVE PASSES (law satisfied — recorded so the denominator is legible)

`bd-49f-session-complete`, `cot-bronze-complete`, `cot-session-complete`, `cot-silver-complete` all re-enter
session triggers that **do** carry crons; `canonical-schwab-xref-success` targets an SSM automation that
does. `inf-gold-full-on-bronze-complete` is DISABLED and its target has a floor regardless.

---

## POSTURE AND FENCES

Nothing fixed. **This is the number before the fix list**, as COO asked for it.

**Violations 1–3 are the inf surface and #4 is mdpf** — both under COO's standing fence (ETFS/inf and
`mdpf-daily-runner` route to COO first), and the Aug-1 14:00Z ETFS month-end fire is under 24h out with
`~A` having verified it ready at the runtime layer. **Nothing lands on those surfaces before it fires**,
independent of what typing says.

A finding here lands as a **GATE or an OWNED BLOCKING ITEM**. The moratorium binds hardest on exactly this
wave: a trigger census is the most tempting place in the estate to reach for a detector, and **the
deliverable is a schedule, not a detector that notices a schedule is missing.**
