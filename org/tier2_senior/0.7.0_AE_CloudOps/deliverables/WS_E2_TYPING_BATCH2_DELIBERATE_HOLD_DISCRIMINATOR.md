# WS-E2 — TYPING BATCH 2: the deliberate-hold discriminator (STOP-class, pre-fix-list)

**Lane:** `0.7.0_AE_CloudOps` · **Written:** 2026-07-31 ~15:46Z · **Status:** HELD ON DISK, UNCOMMITTED —
the shared worktree is mid-merge (MERGE_HEAD `ec07f20e74`, 8 staged files, 4+ agents) and per COO 153809Z
lanes hold finished work on disk rather than fight the index. **Nothing applied. Nothing touched.**

---

## THE FINDING

> **A pipeline that is DELIBERATELY DISARMED and a pipeline that was NEGLECTED have the SAME CENSUS
> SIGNATURE.** Both read as *"production pipeline, no live schedule."*

E2's mandate is **zero unscheduled production pipelines**. Applied mechanically to the INF tree, that
mandate **re-arms a safety control somebody deliberately closed.**

---

## GROUNDING — both halves checked live, and they came out DIFFERENTLY

A `comp-blast` on `opal-assets-daily-emitter` fired a corpus HOLD citing
`memory/project_opal_assets_emitter_frozen_by_design_not_broken.md` — *"OPAL_ASSETS is DOOR 3 of the INF
`canonical_nna` deletion trap"* (COO `[STOP]` `b7bce51bd`, CTO-ratified). The memory is 18 days old, so
**both halves were re-verified against live AWS rather than repeated.**

**HALF 1 — STALE, RESOLVED.** The record says the mdpf/emitter chain is FROZEN at `run_date=2026-07-10`.
**It is not, any more.** `s3://opal-data-portal-v2/platinum/mdpf/aggregate_aua/` carries `2026-07-29`,
`2026-07-30` and `2026-07-31` keys, the last written **today at 10:59**. Consistent with the MDPF flip
landing 07-29. *The freeze premise is dead — do not let a future reader re-derive from it.*

**HALF 2 — LIVE, AND DELIBERATE.** The corridor disarm is still in force. **All three** rules targeting
`inf-gold-trigger` are DISABLED, exactly as the ratified fix prescribed:

| Rule | State | Schedule |
|---|---|---|
| `inf-canonical-prices-daily` | **DISABLED** | `cron(47 14 * * ? *)` — the trap fallback, payload `mode:full` |
| `inf-gold-full-on-bronze-complete` | **DISABLED** | (event-pattern) |
| `inf-gold-incremental-daily` | **DISABLED** | `cron(0 18 * * ? *)` |

Three rules — matching the record's *"THREE EventBridge rules target it — not one."* The disarm closed the
corridor all three doors open onto.

**A stale record and a live one sat in the same memory file.** Verifying only the half that was convenient
would have produced a confident, wrong answer in either direction.

---

## WHY THIS IS STOP-CLASS FOR E2

The record already names this exact shape: *"Disarming bronze-complete ALONE would RELEASE the cron — **the
requested remedy would have armed the gun.**"*

The four INF violations (`inf-silver-chain`, `inf-assets-trigger`, `inf-etf-ownership-daily`, plus
`mdpf-daily` off the same chain) are **not** `inf-gold-trigger` itself. But they sit on that tree, and two
fire on the very `bronze-complete` marker whose dispatch lock the record describes as winning a
**16-minute race** against the trap cron. *That coupling is not visible from the trigger graph alone.*

### Third instance of one pattern, in a single session

1. `mdpf-scheduled-floor` — **BUILT and deliberately NOT APPLIED** (COO/CTO-gated).
2. `inf-gold-trigger`'s three rules — **deliberately DISABLED** (safety hold).
3. The general case — any pipeline whose schedule was removed **on purpose**.

In all three, **"no schedule" is a DECISION, not a defect.** A census cannot see the difference. I nearly
misread it twice today; both times only grounding the mechanism at source caught it.

The record even prescribes the remedy for its own instance: the staleness alarm ships **only with a
`frozen-by-deliberate-hold` discriminator**, so *"legitimately frozen"* and *"broken"* can never share a
signature. **E2 needs the same discriminator at the TRIGGER layer, or its fix list is a list of loaded guns.**

---

## PROPOSED (routed to COO 154605Z — not taken unilaterally)

Every violation in the E2 census carries a **required third field** beside the edge and the predicate:

```
DELIBERATE-HOLD STATUS: { none known | held-by-ruling <cite> | disarmed-by-control <cite> }
```

sourced from the corpus HOLD set, change-management ledgers, and TF `state = "DISABLED"` with its commit
rationale. **A violation carrying a hold cite is not a FIX candidate — it is a REVIEW candidate for the
hold's owner.**

Cost: one pass over the existing 5. **Not a detector** — the moratorium binds; this is a field in a census
already being written, populated from records that already exist.

---

## THE SENTENCE FOR THE RECORD

> **"Zero unscheduled production pipelines" is the right goal and a dangerous instruction, because the one
> thing it cannot see is INTENT. E2 must distinguish a pipeline that LOST its schedule from one that was
> RELIEVED of it.**

---

## TEMPORAL-ORDERING PASS — suspended, and why that is the correct outcome

The pass that surfaced all of this was a check for edges firing against topological order. Two candidate
inversions were visible from cron times alone:

- `opal-assets-mdpf-portal-publisher-daily` **16:15** fires *before* `opal-assets-daily-emitter-daily` **17:15**
- `opal-assets-silver-etf-sweep-daily` **23:30** fires *after* the emitter it may feed

**Neither is asserted as a violation.** Ordering candidates derived from cron times are meaningless without
the declared D2 producer→consumer paths, and the one instrument that would have supplied them
(`comp-blast`) crashed before rendering its blast radius (below). **A cron-time inversion is a question,
not a finding** — and on this tree, an ordering "fix" is exactly the class of change the hold above governs.

---

## TOOL DEFECT (routed, one line)

`comp-blast` **crashed after printing the HOLD** — `UnicodeEncodeError` on `'→'` (a right-arrow) in a
corpus quote, cp1252 stdout, `org/modules/graph/cli.py:378` → `:364`.

The **HOLD printed first, and that design saved the outcome** (the warning was delivered; NFRA_NERVES L3b
is explicit that *"the HOLD PRINTS FIRST. A hold is not a footnote."*). But the blast radius never
rendered — **the tool failed to answer the question while still delivering its warning.** It is the exact
non-ASCII/charmap class CLAUDE.md's Code Quality rule names, occurring *inside a comp-tool reading a corpus
file that contains the arrow*.

---

## POSTURE

Nothing applied, no infrastructure touched, no ledger opened, no alarm/monitor/SNS/freshness checker built
or proposed. Fix list **not written**, pending COO's call on the third field. COO's ruling stands: nothing
applies before Aug-1 14:00Z. INF and mdpf surfaces remain fenced.
