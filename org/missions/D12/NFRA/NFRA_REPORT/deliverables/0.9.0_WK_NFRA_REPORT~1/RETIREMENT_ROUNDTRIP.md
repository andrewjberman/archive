# RETIREMENT ROUND-TRIP -- across two real editions (cell RP-s-18, manifest row S8, outcome FWD-7)

Authority: `NFRA_REPORT_PRD.md` manifest row S8 (`FWD-7`: *"Someone can retire a dead thing and have
the report stop raising it, on the record... DONE WHEN EXERCISED -- something has actually been
retired and the next edition stopped raising it."*), this cell's own bound (verbatim, task order
`NFRA_REPORT.TO-RP-s-18`): *"IF NOTHING IS GENUINELY RETIRABLE, SAY SO... A CARRIED item suppressed
from daily re-derivation is the honest demonstration if no RETIRED one exists."* Depends on, and
exercises directly, `RP-s-15` (`compose_edition.py`) and `RP-s-16` (`run_gate.py`), both observed
complete in this worktree before this cell touched anything.

## 0. THE HONEST STARTING FACT, UNCHANGED BY THIS CELL

`RETIREMENT_REGISTER.md` (`RP-s-8`, round 1) carries **0 `RETIRED` rows and 5 `CARRIED` rows**, and
0 `RETIRED` is the TRUE number: `DEPRECATION.md`'s ten-candidate terminus walk confirmed nothing dead.
**This cell does not add a `RETIRED` row, does not add a sixth register row of any kind, and does not
edit any of the five existing rows.** `RETIREMENT_REGISTER.md` is byte-identical to how `RP-s-8` left
it. Manufacturing a retirement to demonstrate the mechanism would put a false row in a permanent
register -- the bound forbids exactly that, and this document does not do it.

What IS genuinely available, per the bound's own named alternative: **a `CARRIED` item, already
recorded with owner, reason and date, suppressed from being re-derived from scratch on the next
edition.** That is what this document exercises, twice, for real, against the real composer and the
real trading-day gate -- not a description of the mechanism, a RUN of it.

**Named limit, stated once and not hidden:** `FWD-7`'s own `DONE WHEN` line reads *"something has
actually been retired"* -- literally, a `RETIRED` row. This round-trip does not produce one, because
none exists to produce honestly. This document demonstrates the round-trip on the one row-type that
IS genuinely available this round (`CARRIED`), per the cell's own bound. Whether that satisfies
`FWD-7`'s `EXERCISED` bar in full, or only its suppression half, is a judgment call for L9
(`3.0.0_SA_CVO`, first engagement) -- not self-graded here.

## 1. THE FIVE `CARRIED` ROWS, OWNER + REASON + DATE TOGETHER (quoted from `RETIREMENT_REGISTER.md` sec.3, unedited)

| Item | Status | Owner | Reason | Date |
|---|---|---|---|---|
| `INF_D_00.portal_aggregates.py` | `CARRIED` | `0.9.0_WK_NFRA_REPORT~1` | Writes 2 platinum keys; `comp-platinum` returns only `[SPECULATIVE]` catch-all matches, no confirmed route -- walk could not resolve to a terminus | 2026-09-09 |
| `INF_D_03.composition_artifacts.py` | `CARRIED` | `0.9.0_WK_NFRA_REPORT~1` | Same `[SPECULATIVE]`-only shape on both its platinum keys | 2026-09-09 |
| `INF_D_02b.top_holdings.py` | `CARRIED` | `0.9.0_WK_NFRA_REPORT~1` | Same `[SPECULATIVE]`-only shape | 2026-09-09 |
| `INF_D_07.concentration_risk.py` | `CARRIED` | `0.9.0_WK_NFRA_REPORT~1` | `comp-pipescript`'s static parser cannot see this script's write at all (dynamic key concatenation) -- the walk could not even confirm the write, let alone a terminus | 2026-09-09 |
| `INF_C_01.canonical_nna.py` | `CARRIED` | `0.9.0_WK_NFRA_REPORT~1` | Same static-parser miss; textually a heavily-governed production chokepoint, not a deprecation candidate, but not terminus-walk CONFIRMED | 2026-09-09 |

**Owner, reason and date, together, on the same row -- all three, per the bound.** No row in this
table has one without the other two. Two of these five rows (`INF_D_00`, `INF_D_07`) are also
composed into `compose_edition.py`'s `ROW_FACTS` and therefore appear in the actual edition; the
other three (`INF_D_03`, `INF_D_02b`, `INF_C_01`) are recorded in the register but not composed into
a row this round -- `COMPOSER.md` sec.2 declares only "four of the ten walked candidates" were
composed, and this cell does not widen that (widening `ROW_FACTS`' candidate coverage is a separate
cell's work, not this one's).

## 2. THE ROUND TRIP, EXERCISED -- Edition A, then Edition B, same two rows

**Edition A** -- `EDITION_SPECIMEN.md@5e2131d851` (committed by `RP-s-16`'s own build, composed-at
`2026-09-10T02:49:57Z`, verified byte-reproducible by this worktree's own dependency check before
this cell touched anything). Its two `CARRIED` rows read:

```
INF_D_00.portal_aggregates.py (deprecation candidate) | COARSE | COARSE | unchanged
  citation: DEPRECATION.md sec.2; RETIREMENT_REGISTER.md sec.3 (CARRIED)
  evidence: comp-platinum returns only [SPECULATIVE] catch-all matches for both platinum keys
  this script writes -- the walk could not resolve a confirmed terminus. Still the wrong grain
  to call it either alive or dead; recorded CARRIED, not RETIRED.

INF_D_07.concentration_risk.py (deprecation candidate) | COARSE | COARSE | unchanged
  citation: DEPRECATION.md sec.2/sec.3; RETIREMENT_REGISTER.md sec.3 (CARRIED)
  evidence: comp-pipescript's static parser cannot see this script's write at all (dynamic key
  concatenation, surprise row NFRA_REPORT-Z-W1-S2) -- the walk cannot even confirm the write,
  let alone a terminus. Recorded CARRIED, not RETIRED, not ALIVE.
```

Edition A's evidence text **quotes the walk directly** -- `comp-platinum`'s and `comp-pipescript`'s
own findings, restated in full each time. Nothing there yet demonstrates suppression: an edition that
kept re-quoting the walk verbatim, forever, would be indistinguishable from an edition that re-ran the
walk from scratch every morning -- brief F10's own complaint (*"the same items are re-reasoned
daily"*), not yet closed.

**This cell then edited `compose_edition.py`'s `ROW_FACTS`** for exactly these two rows (only these
two; no other row in `ROW_FACTS` was touched), per `COMPOSER.md` sec.5's own named mechanism for
producing a genuine next edition ("a future cell edits `ROW_FACTS`' `prev` blocks to equal THIS
edition's `curr` blocks... supplies new `curr` blocks from a fresh read"). **The axis values were not
changed** -- both rows are still `COARSE` -> `COARSE`, `unchanged`, `rule4`, exactly as `ROW_STRUCTURE.md`
requires: no resolution is claimed that the walk did not earn. **Only the CITED SOURCE of `curr`
changed**: instead of re-quoting the walk, the evidence and citation now point at
`RETIREMENT_REGISTER.md`'s own already-recorded `CARRIED` row -- owner, reason, date -- and states
explicitly that no re-walk was performed this edition.

**Edition B** -- composed for real, this session, by `run_gate.py --date 2026-09-10` (the same
NYSE trading day `RP-s-16` itself exercised; `2026-09-10` gates `True`), writing a fresh
`EDITION_SPECIMEN.md` at composed-at `2026-09-10T03:25:45Z`. Its two rows now read:

```
INF_D_00.portal_aggregates.py (deprecation candidate) | COARSE | COARSE | unchanged
  citation: RETIREMENT_ROUNDTRIP.md sec.2 (Edition B); RETIREMENT_REGISTER.md sec.3 row 1
  (CARRIED, owner 0.9.0_WK_NFRA_REPORT~1, 2026-09-09) -- cited via the register's current-state
  view, not re-walked this edition
  evidence: Edition A (EDITION_SPECIMEN.md@5e2131d851) quoted the comp-platinum walk directly...
  Edition B does not re-run that walk: it cites RETIREMENT_REGISTER.md's own CARRIED row -- owner,
  reason and date already recorded there -- and stops there. Still COARSE, still not RETIRED: no
  resolution is claimed, only that re-derivation is suppressed.

INF_D_07.concentration_risk.py (deprecation candidate) | COARSE | COARSE | unchanged
  citation: RETIREMENT_ROUNDTRIP.md sec.2 (Edition B); RETIREMENT_REGISTER.md sec.3 row 4
  (CARRIED, owner 0.9.0_WK_NFRA_REPORT~1, 2026-09-09) -- cited via the register's current-state
  view, not re-walked this edition
  evidence: Edition A (EDITION_SPECIMEN.md@5e2131d851) quoted the comp-pipescript walk directly...
  Edition B does not re-run that walk: it cites RETIREMENT_REGISTER.md's own CARRIED row -- owner,
  reason and date already recorded there -- and stops there. Still COARSE, still not RETIRED: no
  resolution is claimed, only that re-derivation is suppressed.
```

**This IS the round-trip FWD-7's bar asks for, at the grain that is honestly available:** an item
that was reasoned about with real instrumentation in one edition is, in the NEXT edition, no longer
re-reasoned -- it is cited, by owner, reason and date, from the register that already settled (for
now) what it is. The top-line verdict and delta-count machinery are untouched and identical in both
editions (`compute_delta`, `compute_verdict` are not edited by this cell) -- `25 rows composed; verdict
= SOMETHING needs Andrew today; delta counts: 14 better, 10 unchanged, 1 worse` in both Edition A and
Edition B. Neither `CARRIED` row has ever moved the verdict (both are `unchanged`, neither `CHECKED`
nor `worse`) -- that was already true in Edition A and remains true in Edition B; what changed is
*how* the row justifies staying `unchanged`, not whether it stays unchanged.

**Disclosed per this task order's own warning: running the composer rewrote `EDITION_SPECIMEN.md` in
this worktree.** The file on disk at the end of this cell is Edition B (composed-at
`2026-09-10T03:25:45Z`), not Edition A. Edition A remains fully recoverable at
`EDITION_SPECIMEN.md@5e2131d851` (`git show 5e2131d851:'org/missions/D12/NFRA/NFRA_REPORT/deliverables/0.9.0_WK_NFRA_REPORT~1/EDITION_SPECIMEN.md'`).
`compose_edition.py` is also changed from `RP-s-15`'s committed version -- the two `ROW_FACTS` entries
above, and only those two, carry a `# RP-s-18 round-trip edit` comment marking the change at the
point it was made.

## 3. WHAT "THE NEXT EDITION STOPS RAISING IT" MEANS HERE, PRECISELY

It does NOT mean the row disappears from the table -- `RETIREMENT_REGISTER.md` sec.2's own design
(*"anyone can later look up what was retired, by whom, and for what reason"*) requires the opposite:
a `CARRIED` or `RETIRED` item stays fully visible and citable, forever, in both the register and any
edition that reports on it. Deleting the row from view would defeat the audit trail the cell exists to
build, and would look exactly like `THIS PROJECT... DOES NOT DELETE` being violated by omission.

It DOES mean: the next edition does not re-spend a fresh `comp-platinum` or `comp-pipescript` walk on
an item that a named owner already looked at, on a stated date, for a stated reason. The COST that
gets suppressed is the RE-DERIVATION, never the VISIBILITY -- exactly `RETIREMENT_REGISTER.md` sec.2's
own distinction (*"`CARRIED` is suppression of RE-DERIVATION, never suppression of the underlying
uncertainty"*), now shown operating across a real edition boundary rather than only asserted in prose.

## 4. THE BOUND, RESTATED AND HELD

**THIS PROJECT CLASSIFIES; IT DOES NOT DELETE.** Nothing in this cell deletes, hides, or removes any
row, script, or served artifact. Retiring anything that is SERVED OUTPUT still requires **never-widen
sign-off (CTO+COO)**, independent of and in addition to this register -- this cell does not touch any
served output and does not seek or claim any such sign-off, because it retires nothing. A `RETIRED`
row, when a genuine one exists, will still be a RECORD of a decision, never the mechanism that
authorizes or performs a deletion.

**Owner, reason and date, all three, together, on the same row** -- section 1's table above restates
this for all five `CARRIED` rows unedited; this cell adds no row that lacks any of the three.

## 5. WHAT THIS DOCUMENT DOES NOT DO

- Does not add a `RETIRED` row to `RETIREMENT_REGISTER.md` -- 0 `RETIRED` remains the true, honest
  count after this cell, exactly as it was after `RP-s-8`.
- Does not add a sixth row of any kind to `RETIREMENT_REGISTER.md`, and does not edit any of its five
  existing rows -- the register file is untouched, byte-identical to `RP-s-8`'s commit.
- Does not invent a third register-entry type (`RETIRED`/`CARRIED` stays MECE, per the register's own
  section 1 and the taxonomy law) and does not collapse the two.
- Does not change any row's Axis-1/Axis-2 value, and does not change the top-line verdict or the
  delta-count summary -- both editions agree: `SOMETHING needs Andrew today`, `14/10/1`.
- Does not mint, edit or touch any SNS topic, CloudWatch alarm, subscription, EventBridge rule, or any
  other live alerting mechanism -- the standing moratorium is ARMED and unaffected; this is a record
  and a re-composition, nothing that fires.
- Does not resolve the three still-`CARRIED` rows this cell did not touch (`INF_D_03`, `INF_D_02b`,
  `INF_C_01`) -- their register entries and their absence from `ROW_FACTS` are both unchanged.
- Does not claim `FWD-7`'s `EXERCISED` bar is fully met in the sense of "something has actually been
  retired" -- section 0 names that gap rather than papering over it with the `CARRIED` round-trip.
