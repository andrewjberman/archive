# ADVI_PERFRP -- THE 7 NON-SERVING FAMILIES, CLASSIFIED. **5 ARE CRASHES, NOT REFUSALS.**

**Author:** `0.7.0_AE_CloudOps~G` · **Ruled by:** `1.0.0_SA_CTO` 90939 / 90977 · **Dispatched:**
`2.0.0_SA_COO` 90947 s.2 · **Date:** 2026-09-01 ~07:4xZ · **Plane:** BUILD (dry-run + one direct
emitter run). Nothing published by this work.

## 0. The ask

> Each of the 7 non-serving families is classified **RULED-REFUSAL** (cite the authority) or
> **UNMET-PRECONDITION** (name the missing input). Seven of seven, denominator printed. **A family
> whose refusal reason nobody can cite is UNMET-PRECONDITION by default — absence of a citation is
> not a design decision.** (`1.0.0_SA_CTO` 90939)

## 1. RESULT — 7 of 7

```
  DENOMINATOR: 11 families in the manifest | 7 emitter_refused | 7 of 7 classified

  UNMET-PRECONDITION (6)                     RULED-REFUSAL (1)
    perfrp_activity_relationship               perfrp_transactions_relationship
    perfrp_activity_account
    perfrp_allocation_relationship
    perfrp_allocation_account
    perfrp_performance_relationship
    perfrp_roster_relationship
```

**STABLE ACROSS TWO RUNS at different input vintages** — all 7 refuse identically at 03:1xZ and
07:2xZ. The only cross-run status change was `published -> unchanged` on the three D5 exercised,
which is D5 working. The classification is not an artifact of one run.

## 2. ⛔ FIVE ARE NOT REFUSALS IN ANY SENSE — THEY ARE UNHANDLED EXCEPTIONS

`activity_{rel,acct}`, `allocation_{rel,acct}`, `performance_relationship`:
**rc=1, raw Python traceback, `botocore.errorfactory.NoSuchKey`.** No `REFUSED` string, no reason,
no authority. **The emitter RAN and DIED.**

> **`emitter_refused` "BY DESIGN" was reporting a CRASH as a DESIGN DECISION.** A crash and a
> sovereign deferral produce the SAME STATUS STRING, so the manifest showed seven considered
> decisions where there was one decision and five bugs.

## 3. ROOT CAUSE — **ONE MECHANISM, 6 UNGUARDED CALL SITES** (settled at the third state)

> ⛔⛔ **THIS SECTION WAS WRONG TWICE AND IS NOW SETTLED. §3a CARRIES THE FULL CENSUS AND THE FINAL
> ANSWER — READ IT BEFORE CITING ANYTHING BELOW.** The states, in order, so no reader mistakes one
> for the record:
> **(1)** *"one mechanism, five families"* — this lane, from **n=1**. Right conclusion, inadequate
> grounding. **(2)** *"three paths, a `_read_gold` fix restores 2 of 5"* — this lane retracting onto
> `3.0.0_SA_CVO` 90994, which rested on a **truncated (`head -12`) grep** later reversed by its own
> author. **WRONG.** **(3)** *"one mechanism, 6 unguarded vs 3 guarded"* — full census, no `head`,
> run independently at four seats. **SETTLED.**
> ⚠ The original n=1 sentence is preserved below at §3c, dated and scoped, because deleting it would
> hide how a right answer was reached by a wrong method.
>
> ⚠ **THE PARAGRAPH THAT FOLLOWED HERE WAS STATE (2)'s RETRACTION NOTE. Its verdict is SUPERSEDED by
> §3a; its LESSON about grounding stands and is why it is kept:**
> *Written 08:0xZ after `3.0.0_SA_CVO` 90994 — "the wrong sentence originated HERE, in 90962 s.2 and
> in this file; CVO amplified a claim this lane had already overstated; do not book it as a grading
> failure." The attribution half of that is still correct. The **verdict** half — that "one mechanism"
> was wrong — is not.*
> **AND THE LESSON THAT SURVIVES BOTH REVERSALS:** this file said plainly *"obtained by running one
> emitter directly."* **One emitter, five families.** The n=1 was disclosed in the same breath as a
> conclusion that exceeded it — **a disclosed sample size does not license generalising past it; it
> only makes the overreach auditable.** The census that would have settled it at 90962 — call sites of
> each gold-read helper, occurrences CLASSIFIED rather than counted, no `head` — is the discipline
> this lane applied to every `comp-find` denominator tonight and did not apply to its own root cause.
> **That remains true even though the conclusion turned out right.**

### 3a. ⛔ THE "THREE PATHS" CORRECTION WAS ITSELF WRONG — **IT IS ONE MECHANISM**

**THIS SECTION HAS BEEN WRONG TWICE. Read the whole of it before citing any part.**

`0.4.0_DS_ClientPlatform~G` 91026 reversed its own 90989 within twenty minutes and named the cause
against itself: it grepped a line range through `head -12` and concluded from the top of it —
**Rule 21's own "Never `head` ANY census" clause, in the same file that clause was written about.**
`3.0.0_SA_CVO`'s three-path retraction, and this lane's, both rested on that truncated read.

**FULL CENSUS, run at this seat, no `head`** (and independently re-run by `3.0.0_SA_CVO` and
`1.0.0_SA_CTO` — four seats, same source):

```
  _read_gold_meta(  = 10 = 1 def + 9 calls. EVERY occurrence classified:
    :122   inside _read_gold wrapper        UNGUARDED literal asof  -> _activity:291,292
    :521   _performance, RELATIONSHIP grain UNGUARDED literal asof
    :523   _performance, RELATIONSHIP grain UNGUARDED literal asof
    :623   _allocation                      UNGUARDED literal asof
    :624   _allocation                      UNGUARDED literal asof
    :648   _allocation, relationship branch UNGUARDED literal asof
    :168   inside _read_gold_le             GUARDED -- resolves true_date FIRST
    :241   inside _read_twr_window          GUARDED -- catches NoSuchKey as a missing day
    :1083  _book, flow_ledger               GUARDED -- NoSuchKey caught at :1084
```

>> **6 UNGUARDED, 3 GUARDED. ONE MECHANISM: a literal `asof` handed to `_read_gold_meta` without
   either guard.** And the corrected finding is STRONGER than the original — **the file already
   contains the correct pattern in three places.** This is not "the aliasing contract was never
   designed"; it is six sites not following a guard three sibling sites already implement, with a
   working reference for both variants (resolve-true-date, or catch-NoSuchKey). <<

⚠ **FIX SCOPE:** a TO naming `_read_gold` is scoped to ONE of the six (`:122`) and would leave
`_performance` and `_allocation` crashing behind a green report.

### 3b. ⛔ MY OWN READ WAS TRUE BUT INCOMPLETE, AND I AM NOT CLAIMING VINDICATION

I verified `_performance:387 -> _read_twr_window(window_dates)` and reported it. **That line is real.**
But `_performance` ALSO calls `_read_gold_meta(asof)` at **:521/:523**, 134 lines further down, in the
relationship-grain branch — **which is the branch that crashes.** I read the line I was pointed at and
treated it as the function. That is `1.0.0_SA_CTO` 91013 s.2's own lesson — *a source read scoped to
the wrong object* — committed while quoting that lesson approvingly.

>> **THE ORIGINAL "one mechanism" IS NOW CONFIRMED. IT WAS STILL ASSERTED FROM n=1 WHEN WRITTEN.**
   A conclusion that turns out right after being reached from one sample is not a method that worked
   — it is a bet that landed. **The retraction was wrong AND the original grounding was inadequate;
   both are true and neither cancels the other.** What should have happened at 90962 is the census
   only run at 08:2xZ. <<

**WHAT SURVIVES UNCHANGED THROUGHOUT ALL THREE STATES:** the 7-of-7 classification (§1) and "5 of 7
are unhandled crashes" (§2). Neither ever depended on the call-site count.

### 3c. The original n=1 text, kept dated rather than deleted

⚠ **STATE (1) of three.** Its conclusion is CONFIRMED at §3a; its GROUNDING (one emitter) was not
adequate to it. Kept because deleting it would hide how a right answer was reached by a wrong method.
The `_read_gold`/`_activity` path it describes is real and is **1 of the 6 unguarded sites**, not the
whole mechanism.

Obtained by running one emitter directly (the manifest cannot show it — see §5), then read at source:

```
  perfrp_emit_core.py:291  _activity()  -> _read_gold("canonical_valuation", asof)
  perfrp_emit_core.py:111  key = "%s/%s/%s/date=%s/data.parquet" % (GOLD_ROOT, tier, table, date)
  perfrp_emit_core.py:113  o = _s3().get_object(Bucket=GOLD, Key=key)     <- S3, at the LITERAL asof
  MEASURED: gold/advi/canonical/canonical_valuation/date=2026-09-01/  ABSENT (newest date=2026-08-28)
```

>> **THE PORT ALIASES `2026-08-28 -> 2026-09-01` INTO LOCAL STAGING AND DECLARES IT ON ITS OWN FACE.
   `_read_gold` NEVER CONSULTS THAT STAGING** — it goes straight to S3 for the literal asof, which
   does not exist. No fallback, no handler, so an absent partition becomes an **unhandled exception
   rather than a declared refusal.** The port's aliasing is DEFEATED for every family whose build
   path routes through `_read_gold`. <<

**NAMED MISSING INPUT:** `gold/advi/canonical/canonical_valuation/date=<asof>/data.parquet` on
`opal-data-49financial` — absent by construction on any day the asof is not itself a real partition date.

⭐ **AND IT EXPLAINS THE INSTABILITY THAT DISCREDITED THE LABEL.** Families reading the STAGED path
publish; families reading via `_read_gold` crash **whenever asof has no real partition**. That is
**date-dependent, not design-dependent** — so the set moves between runs, `gainloss_{rel,acct}` were
listed as by-design refusals and now publish, and `performance_relationship` lives or dies by the
calendar. **One mechanism accounts for every observation.** ⭐ **THIS SENTENCE STANDS — confirmed at
the third state (§3a), NOT by the n=1 read that first produced it.** An intermediate revision of this
file struck it as REFUTED on `3.0.0_SA_CVO` 90994's three-path reading; that reading rested on a
truncated grep its own author reversed at 91026. The mechanism is a literal `asof` handed to
`_read_gold_meta` without a guard, at **6 call sites**, with 3 sibling sites guarding correctly.

## 4. THE TWO DELIBERATE ONES

| family | rc | verdict |
|---|---|---|
| `perfrp_transactions_relationship` | 2 | **RULED-REFUSAL.** *"transactions is served on a PER-RELATIONSHIP PAGED key (s.11 #6); it is not a whole-firm leaf and must not be emitted as one."* Authority: **PRD s.11 #6 (Andrew-approved), CTO 67106(2)**, and it carries the `deferred` field the publisher tests first. A genuine design decision. |
| `perfrp_roster_relationship` | 2 | **UNMET-PRECONDITION, by the default, against my own inclination.** Deliberate and reasoned — *"roster joins the BD-side `dim_account_xref`, which is outside this emitter's gold-plane reads; wiring that read is a separate act"* — but it **cites NO authority**: no ruling id, no PRD section. Missing input: the BD-side `dim_account_xref` read. |

⚠ **What roster's classification implies, because "fix the input" is the wrong reflex there:** that
input is a **CROSS-FIRM read and NEVER#2 governs it.** Wiring it is a gated act, not an input fix.
If an authority for the boundary exists it reclassifies to RULED-REFUSAL on one line; I found none.

## 5. ⚠ AN INSTRUMENT DEFECT THAT MADE THIS HARDER THAN IT SHOULD BE

`d_publisher_port` truncates the emitter's stderr to **`[-800:]`**. Eight hundred characters of
botocore boilerplate survive; **the call site and the failing key are discarded.** All five crash
rows are byte-identical in the manifest. **The manifest structurally cannot name the missing input**
— which is precisely what a classifier is asked to do. The root cause in §3 was only obtainable by
re-running an emitter directly. Surfaced, not chased; the publisher was not touched.

## 6. WHAT THIS IS NOT

- **Not an emit act and not a fix.** This is a READ. No emitter work is authorized by it and none is
  implied; the classification is the INPUT to that decision, not the decision (`2.0.0_SA_COO` 90947 s.2).
- **BUILD plane only.** Nothing was published by this work.
- `1.0.0_SA_CTO` 90977 ruled on it: **the design question DISSOLVES — one bug, not seven decisions.**
  The three families the render path needs were already designed to emit and they crash, so there is
  no consumer to redesign.
