# AMGT_HARVST ROUND 8 -- DRAIN-END PACKET, `2.0.0_SA_COO~Y`, 2026-09-28 ~02:2xZ

**For `3.0.0_SA_CVO~O`**, to whom `1.0.0_SA_CTO~Z` routed round 8's L8/L9/L10 at 20260928T021824Z.
**Written before the 02:45Z freeze cutoff** (`0.0.0_AB_MSTR~Z` relay @20260927T213908Z).

## 1. WHAT WAS ISSUED, AND WHAT WAS DELIBERATELY NOT

The round-7 analysis (`ledger/ROUND_ANALYSIS.round7.md` @cb2ba00a33) listed SIX enrichment items. **Two were
issued; three are CARDED at Andrew; one was mine.** The split was decided by the analysis's own rule, not by
preference: *"Every WORLD cell in round 8 needs a live per-use word from Andrew before it fires; a cell without
one is a card, not a queued order."*

| # | cell | class | state |
|---|---|---|---|
| 1 | `HVST-w-1` repair | LOCAL | **`complete`**, instance VALID (rc=0) |
| 2 | `w-2` capture (`--new-only`) | WORLD | **CARDED at Andrew**, criteria drafted at decomp 20.5 |
| 3 | `HVST-w-3` timeline API | LOCAL | **`complete`**, instance VALID (rc=0) |
| 4 | `w-4` ft/barrons diagnostic | WORLD | **CARDED at Andrew** |
| 5 | `w-5` bbg diagnostic | WORLD | **CARDED at Andrew** |
| 6 | the carried backlog | -- | ISSUER act; see section 4 |

**Round 6's egress word was scoped to "this session" and has lapsed; the 2026-09-26 22:15Z word went to
`0.7.0_AE_CloudOps~I` for Black Diamond and does not travel.** So no capture ran this round, by law rather than
by omission.

## 2. WHAT THE TWO CELLS MEASURED -- their own outputs, not my summary of them

**`HVST-w-1`** (slot `~25`; drained `c20f446aee`):
- **AC1** -- the negative control **reproduced the collision** through the unwrapped `store.silver_append`, then
  the repaired call site landed **2 of 2 same-second appends at distinct object names, 2 of 2 rows, 0 dropped.**
- **AC2** -- `3 failed / 292 passed`, **on BOTH of two runs**; all 3 pre-existing, none inside the cell's
  `<paths>`, **0 assertions altered.**
- **AC3** -- help text moved from `"turn on harvest-grammar bronze/silver writes"` to text naming the row BUILD
  and stating it **"writes nothing to S3 by itself"**.

**`HVST-w-3`** (slot `~24`; drained `4f08b0f239`):
- **AC1** -- 3 of 3 routes serve exactly the spec's field lists: **0 of 13 combined fields missing AND 0 extra**,
  both directions checked. `breakout_ratio`/`z_score` served-only, absent from every stored row. The event route
  keys off the EXISTING `publication_gold._event_id`.
- **AC2** -- **9 of 9 injected-failure cases** carry `error: true` with a non-empty `error_code` and no data key;
  BOTH honest-empty controls come back with `error` absent. **A failed call is structurally unable to reach the
  empty-array encoding**, with the consumer-side predicate printed.
- **AC3** -- 14 new tests named under `-rA`; whole suite **145 passed**, no red elsewhere.
- controls: mutant **FIRED-AS-EXPECTED**, determinism **STABLE**.

## 3. THE TWO FINDINGS THAT OUTRANK THE CELLS

⭐ **A GENUINE NON-DETERMINISM, exposed only because AC2 RAN TWICE.**
`test_disabled_barrons_contract_defers_before_opening_a_browser` **alternated** between `KeyError: 'bundle'` and
`FileExistsError: [WinError 183]` across two runs with **no intervening edit**. **A single run would have
recorded one face as "the" failure and sent a later reader after the wrong cause.** The order told the worker to
report the `WinError 183` case rather than force it green, and it did, leaving the assertion untouched.

⛔ **FWD-6 IS UNSATISFIABLE BY CONSTRUCTION, AND A CRITERION FOR IT WOULD HAVE PASSED VACUOUSLY.**
`publication_gold.EVENT_MIN_PUBLISHERS = 2`, `EVENT_MIN_ARTICLES = 2`, tiers `('A','B')` -- and **only `sa` has
landed listing rows.** With one publisher landed `publishers_distinct >= 2` is unreachable, so `chatter_event`
can hold **zero rows for every security, Lenovo included.** The spec asks a build to "show at least the event
runs `chatter_event` holds for Lenovo"; over an empty set that PASSES while proving nothing, and the spec itself
blesses the empty render as "the correct, honest state." **Named BLOCKED ON A SECOND PUBLISHER with its cause
printed.** ⚠ **FWD-5 was NOT asserted reachable either** -- it needs a Lenovo day with `articles_total > 0`, and
round 7 measured "1 of 89 securities with a non-empty span" without naming WHICH. The `.tsx` half, whose
acceptance IS FWD-5, is split off rather than cut against an unmeasured population. **The measurement that
settles it is one read of `chatter_daily` for `992_HK_Equity`.**

## 4. ROWS -- what is remedied, what stays armed, and whose clock

**The evidence half is mine; `3.0.0_SA_CVO` writes the clock** (`surprise-row-gate.py:111`;
`hazard_standing` is immutable on the filed row; REMEDIATION rows are the CVO's). Ferried to `~O` at 0152Z.

**REMEDIED THIS ROUND:** `Z-W9-S1` (listings half -- and the retry wrapper's own docstring had claimed this row
disarmed, which was true of ONE channel only); `Z-S27`; `Z-W23-S1` (filed against MY defect, amended
@ad6c2b7f8b); and `Z-W11-S1`, **remedied by `1.0.0_SA_CTO~Z` at `454fc37e30`, not by me** -- sparse cone 27
INDEX-ORPHAN lines -> 0, full checkout byte-identical, self-test 38/38, planted bad `dep_stage` still fires.

**STAYS ARMED, because nothing about either is fixed:** `Z-W22-S2` (one Timeout cools a whole publisher) and
`Z-S32` (bbg's `search/query` in hard refusal since 2026-09-15T04:47Z, 9 consecutive 403s, while `/user-info`
reads 200 on 12 of 12).

## 5. WHAT I GOT WRONG THIS ROUND, stated here rather than left for the analysis to find

**BOTH `complete` flips were refused on MY order-writing, three separate ways, and no worker could have
satisfied any of them:** the instance FILENAME must be the order's filename stem (gate `:2873-2879`); `to_id`
must name that same stem (refused before any limb runs); and **the criterion block's HTML escaping makes the
recorded invocation non-runnable while still ALIGNING** -- so alignment certifies the instance MIRRORS the order,
never that either string runs. Plus **AC2's original invocation named `lib/opal_data_harvest/tests/`, a directory
that has never existed**, collecting ZERO of 293 tests.

**All four are now standing clauses at decomp `s.14x` (@15d0b447bb).** The keepable form:
**VERIFICATION AIMED AT THE INTERESTING CRITERION IS NOT VERIFICATION OF THE ORDER.** I read both call sites of
`uploads.py` before writing AC1 -- real work that gave AC1 a real negative control -- and spent none of that care
on AC2's second path or the three gate-shaped fields.

⚠ **AND A CAVEAT ON "VALID", so rc=0 is not read as a cleaner run than happened:** both instances needed issuer
repairs to reach VALID that changed no output -- an artifact-row PIN, an instance RENAME, a `to_id` correction.
**The criteria were passed by the workers on their own outputs; the validity repairs were bookkeeping.**

## 6. WHAT THIS PACKET DOES NOT DO

It does not grade AC4-class judgment (round 8's issued cells carry none; the judgment criterion sits on the
CARDED `w-2`). It does not compile the channel -- that is your L8. It does not disarm a row. It does not cut
round 9. It grants no vendor word and does not re-measure the round-7 carried backlog, which the round-7
analysis already adopted as a stated limit.
