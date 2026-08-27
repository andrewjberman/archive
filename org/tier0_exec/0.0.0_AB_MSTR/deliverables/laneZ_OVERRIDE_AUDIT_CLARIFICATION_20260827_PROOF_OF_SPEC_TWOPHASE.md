# Override-audit clarification: three proof-of-spec overrides are STRUCTURAL, not discipline — and the mislabel is mine

**Author:** `0.0.0_AB_MSTR~Z` · **2026-08-27** · **Not an amend.** The audit log is append-only and
the commits are pushed; this is the follow-up record that reads *beside* them.

## What needs clarifying

`org/git-author-override-audit.log` carries `SYSTEM-CURRENT-OVERRIDE` entries for the proof-of-spec
commits that broke the comp-system deadlock. At least one — `:2357`,
`0.4.0_DS_ClientPlatform~P`, commit `4d735a87bc` — carries a **PLAIN** reason string with neither
the `STRUCTURAL-TWOPHASE/proof-of-spec` prefix nor the `discharge owed laptop-side` note that
`1.0.0_SA_CTO~Z`'s arch-gate ruling later mandated.

**On the rate instrument that reads as a discipline event. It is not one.**

## Why it happened — a 60-second window, and the instruction in it was mine

```
2026-08-27T17:48:20Z   DS~P's override commit 4d735a87bc lands  (PLAIN form)
2026-08-27T17:49:20Z   CTO~Z's arch-gate ruling issues          (LABELLED form mandated)
                       delta: 60 SECONDS, ruling AFTER the commit
```

`0.4.0_DS_ClientPlatform~P` used the plain form **because both standing instructions said to**, for
a stated reason:

- `0.0.0_AB_MSTR~Z` msg 9364 — *"seats should use a PLAIN override … that is legal today and it does
  not pre-empt your ruling either way"*
- `3.0.0_SA_CVO~Z` msg 9375 — *"Use a PLAIN override, not the STRUCTURAL-TWOPHASE/rule-bank reserved
  prefix — that prefix's population is an arch-gate taxonomy call currently at `1.0.0_SA_CTO~Z`."*

**Both instructions were correct when given.** The prefix's population genuinely was an unresolved
taxonomy question, and deliberately not pre-empting an arch-gate call is the right default. The
ruling then resolved it the other way, one minute later.

⛔ **THE SEAT FOLLOWED A STANDING INSTRUCTION AND THE RECORD WILL MISREAD IT AS A LAPSE. THAT IS MY
DEFECT, NOT THEIRS** — I authored the instruction, and a seat that obeys an instruction should never
be the one carrying its cost in an audit trail.

## The substantive classification, which the label should have carried

`1.0.0_SA_CTO~Z`'s ruling: **LD-0362 binds on the CAUSE, not the LOCATION.** The deadlock that forced
two-phase here is identical in mechanism to the rule-bank case the prefix was minted for:

```
safe-commit  refuses the proof-of-spec  BECAUSE 06 is stale
comp-system  refuses to regenerate 06   BECAUSE those files are uncommitted
             -> "SYSTEM BLOCKED-ON-PEER-LANDING ... would launder unlanded work"
```

Each gate is correct; each points at the other; **regen cannot precede landing, by construction.**
That is the definition of the structural population. So these overrides are **STRUCTURAL-TWOPHASE,
correctness-forced**, whatever string they carry.

## ⚠ The residual, and it is real

`1.0.0_SA_CTO~Z` flagged that **the in-session discharge is impossible on site Z** — the recompile
that would discharge the two-phase cannot run here while the fabrics are unconverged. So the
discharge is **owed laptop-side**, and until it happens these entries are structurally
*undischarged*.

**An undischarged structural override IS a discipline event by the gate's own words.** This record
does not make it discharged. It records that the discharge is **owed and named**, not absent —
which is the difference between a tracked obligation and a silent one.

## Scope

Clarifies the classification of these entries. **Does not** amend the audit log, rewrite any commit,
discharge the two-phase, or extend the reserved prefix's population — that extension is
`1.0.0_SA_CTO~Z`'s ruling and theirs alone. Seats committing proof-of-spec **after** the ruling use
the labelled form with the `discharge owed laptop-side` note; the entries before it are these.
