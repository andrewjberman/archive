# ROW STRUCTURE — the report ARTIFACT's per-row shape and its PER-ROW delta (cell RP-s-2, outcomes FWD-3/FWD-1)

Authority: `NFRA_REPORT_PRD.md` manifest row S2 (`FWD-3`, `FWD-1`), brief F1 (the measured starting
defect), and `C-AI` (the delta is COMPUTED, never GENERATED). Depends on, and renders strictly
THROUGH, `STATE_MODEL.md` (cell RP-s-1) — no second state vocabulary is invented here. RP-s-2 adds
exactly one new dimension: **the per-row DELTA against the previous edition.**

## 0. The defect this replaces (brief F1, measured)

The prior rollup was a single `max()` taken **over eight rows**, and the report's subject line
carried **the same value on every instance in the window** — a signal that cannot vary cannot answer
`FWD-1` ("does anything need Andrew today"), and it makes a fresh overnight break indistinguishable
from a month-old standing issue, because both max to the same top-line value forever. **A max() over
rows is the defect being replaced here, not a template to follow** (bound, verbatim). This cell does
not touch the rollup/verdict computation at all — that is `S4`'s cell, downstream of this one — it
replaces the UNIT the rollup would eventually be computed FROM: instead of one number for the whole
report, **every row now carries its own independent delta**, so a future rollup (built elsewhere) has
real per-row material to work from instead of one flat number repeating itself.

## 1. THE ROW STRUCTURE

Every row the report renders carries these fields, in this order:

| Field | Source | Notes |
|---|---|---|
| Property | the row's named surface (e.g. Dashboard, Website, Gateway, or a named sub-resource) | unchanged from RP-s-1 |
| Axis 1 (instrument) | `STATE_MODEL.md` §1 — one of the six ratified values | unedited, unredefined here |
| Axis 2 (world) | `STATE_MODEL.md` §2 — `OK \| DEGRADED \| BREACH`, or `—` | rendered ONLY where Axis 1 = `CHECKED` |
| 3rd axis (desired/applied/exercised) | `STATE_MODEL.md` §5 | rendered ONLY where the row is not `applied` |
| **Delta** (NEW, this cell) | computed per §2 below | **exactly one of `worse`, `better`, `unchanged`** — every row carries one, always |
| Reason / evidence | the row's own citation | unchanged from RP-s-1 |

**Every row carries a delta. There is no row without one, and there is no delta computed only on a
total.** A row whose underlying facts have not moved renders `unchanged` explicitly — "a number that
has not moved says so" (cell text, verbatim) rather than being silently omitted, which is exactly how
the old rollup hid a month-long standing problem behind a value that never appeared to change.

## 2. THE DELTA IS COMPUTED, NOT GENERATED (`C-AI`)

The delta is a **deterministic function of two states of the SAME row** — this edition's
(Axis 1, Axis 2, 3rd axis) tuple against the previous edition's tuple for the same Property. A model
may render the result in better English (e.g. "this row got worse overnight"); **it may never decide
the direction.** The function, in priority order, evaluated per row (never across rows, never on a
total):

1. **Both editions' Axis 1 = `DENY-BY-DESIGN`** → `unchanged`. This is the permanent, recorded,
   by-design state (`C-WEBSITE-BLIND`) — it is expected to hold edition over edition indefinitely, and
   is never scored on a good/bad scale because C-WEBSITE-BLIND states it is not pending and not
   awaiting a fix. **Declared limit, named rather than hidden:** if Axis 1 ever transitions INTO or
   OUT OF `DENY-BY-DESIGN` (a rare, deliberate ruling event — e.g. Andrew reverses the GoDaddy
   decision), that is NOT scored as `worse`/`better` by this function; it is a structural change this
   cell flags but does not attempt to rank, because ranking a permanent design choice as an
   improvement or a regression assumes it was a graded outcome, which contradicts what "permanent by
   design" means.
2. **Axis 1 differs between editions and neither value is `DENY-BY-DESIGN`:**
   - previous != `CHECKED`, now = `CHECKED` → `better` (an instrument gap just closed — the row can
     now be looked at where it could not before).
   - previous = `CHECKED`, now != `CHECKED` → `worse` (an instrument gap just opened — **this is
     exactly "a problem that broke overnight," caught the morning it happens rather than after a
     month of silent BLIND**).
   - neither value is `CHECKED` (moved among `BLIND`/`INERT`/`COARSE`/`UNCHECKED`) → `unchanged` at
     this grain. **Declared limit, named rather than hidden:** this function does not invent a
     severity order AMONG the four non-`CHECKED`, non-`DENY-BY-DESIGN` members — none of them is
     "more looked-at" than another in a way ruling 12 defines, and inventing one here would be a
     value judgment this cell was not chartered to make. The row's own Reason field still names which
     specific value it holds now; only the delta collapses to `unchanged`.
3. **Both editions' Axis 1 = `CHECKED`:**
   - compare Axis 2 on the fixed order `OK`(0) < `DEGRADED`(1) < `BREACH`(2), which ruling 12's own
     definitions already order (`DEGRADED` = "outside standard, contained"; `BREACH` = "outside
     standard, NOT contained" — strictly worse by ruling 12's own words, not a rank this cell
     invents): rank increased → `worse`; rank decreased → `better`; rank unchanged → proceed.
   - if Axis 2's rank is unchanged, compare the 3rd axis's SHOWN/NOT-SHOWN state (`STATE_MODEL.md`
     §5: shown only when not `applied`): shown → not-shown (i.e. `desired` → no longer rendered)
     → `better` (an intent became applied); not-shown → shown (`applied`-or-silent → `desired`
     appears) → `worse` (an enforcement was withdrawn or never landed where it previously had);
     shown-and-still-shown or not-shown-and-still-not-shown → `unchanged`.
4. **Both editions hold the identical non-`CHECKED`, non-`DENY-BY-DESIGN` Axis-1 value** →
   `unchanged`.

**This function is applied PER ROW, independently, every edition.** No step in it reads any OTHER
row's state, and no step in it is skipped or overridden by an aggregate — the bound this cell may not
cross (`the delta is computed PER ROW, never only on the total`) is structural in the function itself,
not merely a claim about it: there is no input slot in the function above for a second row's value at
all.

## 3. WORKED SPECIMENS — the same rows `STATE_MODEL.md` §7 rendered, now carrying a delta

| Property | This edition (Axis1/Axis2/3rd) | Previous edition | Delta | Why (per §2's function) |
|---|---|---|---|---|
| Website security | `DENY-BY-DESIGN` / — / — | `DENY-BY-DESIGN` / — / — | **unchanged** | Rule 1: both editions `DENY-BY-DESIGN` — the permanent, recorded, by-design state; expected to hold indefinitely per `C-WEBSITE-BLIND`. |
| Blocked-address sentinel row | `CHECKED` / `OK` / `desired` | `BLIND` / — / — (no sentinel existed yet) | **better** | Rule 2, first bullet: previous `!= CHECKED`, now `= CHECKED` — an instrument gap just closed, even though the 3rd axis still shows `desired` (enforcement is not yet applied; that is a SEPARATE, correctly-still-visible fact, not something this delta hides). |
| `opal-login-abuse-alerts` | `INERT` | `INERT` | **unchanged** | Rule 4: identical non-`CHECKED`, non-`DENY-BY-DESIGN` value both editions. |
| `comp` | `CHECKED` / `OK` (stale-instrument qualifier) | `CHECKED` / `DEGRADED` | **better** | Rule 3, first bullet: Axis-2 rank dropped from `DEGRADED`(1) to `OK`(0). |
| (illustrative regression case, not a live row) | `BLIND` | `CHECKED` / `OK` | **worse** | Rule 2, second bullet: previous `= CHECKED`, now `!= CHECKED` — the exact "broke overnight" case this cell exists to catch; under the OLD `max()` rollup this would have been invisible next to seven unchanged rows. |

The fourth column is never blank and never a repeated constant across rows by construction — each row
is computed independently from its OWN two editions, which is precisely what the old `max()`-over-eight-
rows rollup could not do (brief F1: the subject line read the same value on every instance in the
window regardless of which, if any, row had actually moved).

## 4. What this cell does NOT do

- Does not compute, define or own a REPORT-LEVEL rollup or verdict — that is `S4` (`RP-s-4`),
  downstream of this cell, and it must be built FROM the per-row deltas here, never as a replacement
  for them.
- Does not invent a second state vocabulary. Axis 1, Axis 2 and the 3rd axis are `STATE_MODEL.md`'s,
  unedited. This cell adds exactly one new field: the per-row `worse | better | unchanged` delta.
- Does not generate the delta's DIRECTION with a model. A model may only render the already-computed
  `worse`/`better`/`unchanged` value in prose; the direction itself comes from §2's deterministic
  function, per `C-AI`.
- Does not invent a severity order among `BLIND`/`INERT`/`COARSE`/`UNCHECKED` relative to one another
  — declared as a limit in §2 rule 2, not silently assumed.
