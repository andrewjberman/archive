# RETIREMENT REGISTER — suppression as recorded state, owner + reason + date (cell RP-s-8, outcome FWD-7)

Authority: `NFRA_REPORT_PRD.md` manifest row S8 (`FWD-7`: *"suppression/deprecation as recorded
state"*), brief F10 (216 security findings, no suppression state, the same items re-reasoned daily),
and the standing bounds: **this project CLASSIFIES; it does not delete.** Depends on `DEPRECATION.md`
(`RP-s-7`), whose real result is the register's real input.

## 0. THE REAL INPUT, NOT AN ABSTRACT ONE

`RP-s-7`'s walk found **NOTHING DEAD**: of ten candidates, **5 confirmed ALIVE, 3 AMBIGUOUS, 2
UNRESOLVED-BY-THIS-WALK, 0 confirmed dead.** A register designed only for the RETIRED case has no home
for the 5 of 10 that are neither alive-confirmed nor dead-confirmed — **the majority of the actual
material**, not an edge case. Building only the two-state (retired/live) shape here would ship a
register that still cannot answer brief F10's own complaint for most of what it was built to hold.

## 1. TWO ENTRY TYPES, MECE, NEITHER A GUESS AT THE OTHER

- **`RETIRED`** — a named owner has DECIDED this item is dead, said why, and put their name and a date
  to it. This is the cell's literal ACT. **`RETIRED` is a decision, never a default** — nothing is
  retired by drifting into this register; an owner puts it here.
- **`CARRIED`** — the determination could not be settled (`AMBIGUOUS` or `UNRESOLVED-BY-THIS-WALK` per
  `DEPRECATION.md`'s own vocabulary), and recording that fact stops the item being re-reasoned from
  scratch tomorrow, **without calling it dead.** `CARRIED` is suppression of RE-DERIVATION, never
  suppression of the underlying uncertainty — the register says "this was already looked at and could
  not be resolved," not "this is fine."
- **No third row type for a confirmed-ALIVE item.** There is nothing to suppress and nothing to record
  — `DEPRECATION.md` already answers it, and duplicating a settled answer here is exactly the kind of
  second vocabulary the battery finding warns against minting.

## 2. THE SHAPE — reused from the estate's own working instance, build-ladder rung 2

**This project's own surprise-channel already IS an append-only register that records disposition
through a resolving row, carries owner and grounding per row, and is never edited in place** — this
worker alone has used it five times today. Reusing its proven shape rather than minting a second
storage mechanism: every register entry is **append-only**; a later determination for the same item is
a **NEW row**, never an edit to an old one; every row carries **owner, reason, date, and a citation** to
where the determination was made.

**THE NAMED COST OF THAT SHAPE, NOT INHERITED SILENTLY.** The coordinator's own measurement: an
append-only channel cannot flip a field in place, so a row's own `hazard_standing` reads `ARMED`
forever even after a LATER row resolves it — only the resolving id, followed by a reader, tells the
difference. **If this register displayed a raw row's own status field the same way, a `CARRIED` entry
from three weeks ago would still read `CARRIED` today even if a later row had retired it** — which is
precisely the "still looks like a live problem" failure `FWD-7` exists to stop (*"stop seeing it every
morning"*).

**THE FIX, STRUCTURAL, NOT A REMINDER TO CHECK THE POINTER:** the register has two separate things, and
only one of them is what a daily reader sees:

- **THE LOG** (append-only, exactly the channel's shape) — the full, permanent, citable history. This is
  what *"anyone can later look up what was retired, by whom, and why"* means, and it is never pruned or
  edited.
- **THE CURRENT-STATE VIEW** (what the daily report actually renders) — **a QUERY, never a stored field:
  for each item id, take the LATEST log row and show only that.** There is no separate "current status"
  field that can go stale, because nothing is ever read except through this derivation. A reader of the
  daily report never sees a raw historical row and never needs to follow a resolving id to know whether
  it is current — "current" is the definition of what gets shown, not a property one row claims about
  itself.

## 3. THE REGISTER, WORKED — real rows, from `RP-s-7`'s real result

**0 `RETIRED` rows.** True as of this vintage: `RP-s-7` confirmed nothing dead among its ten candidates,
so nothing in this project has yet been decided dead by a named owner. An empty `RETIRED` set is stated
as a fact, not an oversight.

**5 `CARRIED` rows** (current-state view — one row per item id, each the latest and only entry so far):

| Item | Status | Owner | Reason | Date | Citation |
|---|---|---|---|---|---|
| `INF_D_00.portal_aggregates.py` | `CARRIED` | `0.9.0_WK_NFRA_REPORT~1` | Writes 2 platinum keys; `comp-platinum` returns only `[SPECULATIVE]` catch-all matches, no confirmed route — walk could not resolve to a terminus | 2026-09-09 | `DEPRECATION.md` §2 |
| `INF_D_03.composition_artifacts.py` | `CARRIED` | `0.9.0_WK_NFRA_REPORT~1` | Same `[SPECULATIVE]`-only shape on both its platinum keys | 2026-09-09 | `DEPRECATION.md` §2 |
| `INF_D_02b.top_holdings.py` | `CARRIED` | `0.9.0_WK_NFRA_REPORT~1` | Same `[SPECULATIVE]`-only shape | 2026-09-09 | `DEPRECATION.md` §2 |
| `INF_D_07.concentration_risk.py` | `CARRIED` | `0.9.0_WK_NFRA_REPORT~1` | `comp-pipescript`'s static parser cannot see this script's write at all (dynamic key concatenation) — the walk could not even confirm the write, let alone a terminus | 2026-09-09 | `DEPRECATION.md` §2; surprise row `NFRA_REPORT-Z-W1-S2` |
| `INF_C_01.canonical_nna.py` | `CARRIED` | `0.9.0_WK_NFRA_REPORT~1` | Same static-parser miss; textually a heavily-governed production chokepoint by its own comments, the opposite of a deprecation candidate, but not terminus-walk CONFIRMED | 2026-09-09 | `DEPRECATION.md` §2; surprise row `NFRA_REPORT-Z-W1-S2` |

**Owner, here, means accountable for THIS RECORDED CLASSIFICATION** — that it accurately states "carried,
not retired, not confirmed alive," citable and reviewable — **not** a claim of ownership over eventually
resolving the underlying ambiguity, which is separate future work this register does not assign or
perform. Any of these five rows is superseded, never edited, the day a later determination resolves it
— a new row, same item id, later date, and the current-state view (§2) then shows only that one.

## 4. RETIREMENT IS A RECORD, NEVER A DELETE ORDER

**A `RETIRED` row classifies; it does not remove anything.** `THIS PROJECT CLASSIFIES; IT DOES NOT
DELETE` (bound, verbatim). Retiring anything that is SERVED OUTPUT still requires **never-widen sign-off
(CTO+COO)** per CLAUDE.md's hard stop, independent of and in addition to this register — a `RETIRED` row
in this register is the RECORD of a retirement decision, not the mechanism that authorizes or executes
one. If a future owner retires one of the five `CARRIED` items above, the register grows a new row; the
artifact itself is untouched by that act alone.

## 5. What this document does NOT do

- Does not retire anything itself — 0 `RETIRED` rows, honestly, because nothing has been decided dead.
- Does not authorize or perform deletion of any served artifact — never-widen sign-off (CTO+COO) governs
  that, separately and always, per §4.
- Does not mint alerting, a notification, or any live suppression MECHANISM — the standing moratorium
  binds this cell exactly as it bound `RP-s-6`; this is a RECORD, not a control that fires.
- Does not collapse `CARRIED` into `RETIRED` to give the register a tidier two-column look, and does not
  give a confirmed-ALIVE item a register row it does not need — both would be a MECE violation of §1.
- Does not display a raw historical log row as if it were current status — §2's current-state view is a
  computed latest-per-item query, never a field a reader could mistake for one.
