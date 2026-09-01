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

## 3. ⭐ ROOT CAUSE — ONE MECHANISM, NOT FIVE INPUTS

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
calendar. **One mechanism accounts for every observation.**

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
