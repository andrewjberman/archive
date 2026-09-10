# THE COMPOSER -- the engine round 1 never built (cell RP-s-15, manifest row S2, outcome FWD-3)

Authority: `NFRA_REPORT_PRD.md` manifest row S2 (`FWD-3`, `FWD-1`), decomposition R2 section 0
("round 1 produced specifications and no engine"), and `C-AI` (every region declared
COMPUTED/GENERATED/QUOTED; a GENERATED part is never the sole carrier of a fact). Depends on,
and renders strictly THROUGH, the twelve round-1 deliverables listed in section 2 below --
no second state vocabulary is invented, per bound.

**The artifact:** `compose_edition.py`, next to this document. **Run it:** `python
compose_edition.py`. **It writes:** `EDITION_SPECIMEN.md`, next to itself. This document
describes the engine; it does not duplicate its logic -- the logic lives in the one place a
reader (or a later cell) can re-run it and get the same answer.

## 0. WHAT THIS CELL IS, IN ONE SENTENCE

Round 1 built twelve documents that each state a LAW (what a row's state means, how a delta
is computed, how a verdict is computed, how coverage/cost/deprecation/monitoring are read).
None of them RUN. `S2`'s own bound is unedited by anything downstream: *"a max() over rows is
the defect being replaced, not a template to follow."* This cell is the thing that actually
composes an EDITION out of those twelve laws -- the artifact `FWD-1`, `FWD-3`, `FWD-7` and
`FWD-12`'s `EXERCISED` bars all need before any of them can be graded at all.

## 1. THE THREE REGIONS, DECLARED (`C-AI` part 1)

| Region | What it is here | Where |
|---|---|---|
| `QUOTED` | A transcription of a round-1 finding, with a citation to the file and section it came from. Nothing here is computed; it is the composer's INPUT. | `compose_edition.py`'s `ROW_FACTS` list -- every entry's `prev`/`curr`/`citation`/`evidence` fields. |
| `COMPUTED` | A deterministic function over `QUOTED` tuples. No model, no judgment call, no step that could return a different answer on a re-run against the same input. | `compute_delta()` (implements `ROW_STRUCTURE.md` sec.2 verbatim), `compute_delta_watch()` (declared bridge, sec.3 below), `compute_verdict()` (implements `VERDICT.md` sec.1 verbatim). |
| `GENERATED` | Prose that RESTATES what a `QUOTED`/`COMPUTED` cell already carries, in readable English. Per `C-AI` part 2, never the sole carrier of a fact. | The per-row "Reading" sentence and the section-3 summary paragraph in `EDITION_SPECIMEN.md`. Every fact a `GENERATED` sentence names is also present, unabridged, in that row's own table cells -- checked by construction, not by review, because `render_markdown()` builds the `GENERATED` sentence FROM the same `delta`/`rule_note` values the table cells render, never from a separate, un-rendered fact. |

**The C-AI part-2 test, applied:** strip every `GENERATED` sentence out of `EDITION_SPECIMEN.md`
(the "Per-row reading" subsection, and section 3's prose) and what remains is: the verdict
statement (section 1, a direct `COMPUTED` render), the full row table (section 2, `QUOTED` +
`COMPUTED` columns only), and the reused `VERDICT.md` sec.3 hypothetical table (section 4,
`QUOTED`). Every citation, every axis value, every delta word and every property name survives
that strip. A reader who trusts nothing this composer SAYS about its own output can still open
`ALERT_DELIVERY.md` sec.4, or `COST_ANOMALY.md` sec.1, or any other cited section, and check
the row against it directly. **This is the specific thing `AC5` asks a judgment-only read to
confirm; this document records the mechanism, not the verdict** (a worker never self-grades a
`judgment="true"` criterion).

## 2. THE INPUT -- twelve round-1 deliverables, composed, not re-derived

| Source deliverable | What this composer took from it |
|---|---|
| `STATE_MODEL.md` | Axis 1 (six ratified values), Axis 2 (`OK`/`DEGRADED`/`BREACH`, meaningful only where Axis 1 = `CHECKED`), the 3rd axis (`desired`/`applied`/`exercised`), and its own worked specimens (Website, sentinel). |
| `ROW_STRUCTURE.md` | The delta function itself (`compute_delta()`, sec.2, verbatim rules 1-4 in the same priority order), and its own worked specimen table (sec.3), reused directly rather than re-derived. |
| `VERDICT.md` | The top-line verdict rule (`compute_verdict()`, sec.1, verbatim: `CHECKED`+`BREACH` OR any real row's delta = `worse`), and its labeled hypothetical `NOTHING` table (sec.3), reused directly in `EDITION_SPECIMEN.md` section 4. |
| `ALERT_DELIVERY.md` | Seven SNS-topic rows, their Axis 1/Axis 2 values this session AND the prior investigation's (`NFRA_OPSEC202609-Z-S151`) cited state, which is this composer's PREVIOUS-edition input for that family. |
| `MONITORED_VS_SERVED.md` | Six WATCHED/UNWATCHED-CONFIRMED/INSTRUMENT-CANNOT-SEE rows (two CloudFront distributions, three API Gateways, the gold-layer aggregate), all first-observed this session (the doc's own charter: "the standing check that NO EXISTING INSTRUMENT PERFORMS"). |
| `DEPRECATION.md` / `RETIREMENT_REGISTER.md` | Four of the ten walked candidates (two `ALIVE`-confirmed, two `CARRIED`), with the PRIOR state read from the same document's own sec.0 (ruling 6's age heuristic / the CRO's one-hop check, both named `COARSE` -- the wrong grain, not a wrong answer). |
| `COST_ANOMALY.md` | Three segment rows (`inf`, `bd`, `(untagged)`), PREVIOUS state read from brief F9 ("cost has no standard so it cannot fail" = `UNCHECKED`, deliberately not asserted). |
| `COMPUTE_MANIFEST_FINDINGS.md` | One row (the `opal-globgrph` ECS cluster), PREVIOUS state read from brief F8 ("the manifest is EC2-ONLY -- ECS absent entirely" = `BLIND` for this specific compute unit). |
| `ANOMALY_BREAKDOWN.md` | Folded into the `trade-submission-api` row as additional cited evidence (its 30-connected-resource `COMPUTED` breakdown), not a separate row -- the same live surface `MONITORED_VS_SERVED.md` already carries. |
| `COVERAGE.md` | Its own rule ("every count states what it counted out of") is practiced, not restated, by this document: every count in section 1 of `EDITION_SPECIMEN.md` (`3 of 24`, `0 of 24`) states its denominator in the same breath. |

Not composed into a row (declared, not silent): `RP-s-13` (property+owner attribution, `S13`) is
a SEPARATE cell (`FWD-4`) not yet landed at this worktree's base, so `EDITION_SPECIMEN.md` does
not group rows by business owner -- every row here is ungrouped, which is honest given `S13`
has not run, never a claim that grouping was considered and rejected.

## 3. THE ONE DECLARED EXTENSION -- the WATCHED/UNWATCHED bridge

`ROW_STRUCTURE.md`'s function is written in Axis 1/Axis 2/3rd-axis terms. `MONITORED_VS_SERVED.md`
renders "through STATE_MODEL.md's ratified vocabulary" but uses its OWN three-value axis
(`WATCHED` / `UNWATCHED-CONFIRMED` / `INSTRUMENT-CANNOT-SEE`), explicitly declared orthogonal to
Axis 1/Axis 2 by that document's own section 0. This composer does not force those six rows
through `compute_delta()` unmodified -- doing so would assert an Axis-2 finding
(`OK`/`DEGRADED`/`BREACH`) that document never asserts. Instead, `compute_delta_watch()` applies
the SAME governing principle `ROW_STRUCTURE.md`'s rule 2 already uses (whether a working check
now exists dominates what it then finds), to that family's own three values:

- no instrument ever existed -> a working check now exists (`WATCHED` or `UNWATCHED-CONFIRMED`,
  either one) = `better`.
- no instrument ever existed -> still `INSTRUMENT-CANNOT-SEE` = `unchanged` (the gap has not
  closed).
- identical value both editions = `unchanged`.

This is additive and declared, never an edit to `ROW_STRUCTURE.md` or `STATE_MODEL.md`
themselves (bound: "do not mint a second state vocabulary" -- this is not a second vocabulary,
it is one small, explicitly-scoped bridge FROM an existing, already-ratified vocabulary TO the
existing three-way delta output every other row also uses).

## 4. WHAT THE FIRST EDITION ACTUALLY SAYS (composed 2026-09-09/10, re-runnable)

25 rows (24 real + 1 explicitly-labeled illustrative). Delta counts: **14 `better`, 10
`unchanged`, 1 `worse`** (the 1 `worse` is the illustrative row only -- `ROW_STRUCTURE.md`'s
own regression specimen, excluded from the real verdict by construction). **Top-line verdict:
SOMETHING needs Andrew today** -- three real rows are `CHECKED`+`BREACH`-or-cost-`ANOMALY`
(`opal-infrastructure-alerts`, cost segments `inf` and `bd`).

**The single most important reading this composer surfaces, stated once here and shown on
every row it applies to in `EDITION_SPECIMEN.md`:** the majority of `better` rows in this FIRST
edition are `better` because round 1 built a working check where none existed, not because
what that check found is good news. `opal-infrastructure-alerts` scores `better` while
rendering `BREACH`. The cost segments score `better` while rendering `ANOMALY`. Three
MONITORED-vs-SERVED rows score `better` while rendering `UNWATCHED-CONFIRMED` on a live,
undefended surface. **This is `ROW_STRUCTURE.md`'s rule, applied literally, not this
composer softening bad news** -- and it is exactly why every row also renders its found value
in full, beside the delta word, never the delta word alone.

## 5. HOW TO RUN THIS AGAIN, TOMORROW

`python compose_edition.py` from this directory. To compose a REAL second edition (not a
second run of this same specimen), a future cell edits `ROW_FACTS`' `prev` blocks to equal
THIS edition's `curr` blocks (this specimen becomes the new previous-edition baseline) and
supplies new `curr` blocks from a fresh read of the same twelve-plus deliverables (or their
live successors, once `S3`/`RP-s-16` lands a real trading-morning run). The function
(`compute_delta`/`compute_delta_watch`/`compute_verdict`) does not change between editions --
only the `QUOTED` input does. **No alert, alarm, topic, subscription or schedule is created,
touched or proposed by this cell** -- composing and writing an edition is not minting a
notification (the standing moratorium is ARMED and unaffected here).

## 6. What this document does NOT do

- Does not re-run any live AWS read, re-walk `comp-blast`/`comp-pipescript`/`comp-platinum`, or
  re-execute `comp-find --corpus aws` -- every `QUOTED` fact is round 1's own finding, at round
  1's own stated vintage, composed here, not re-measured.
- Does not build the trading-day-aware SCHEDULE that would make this a live, running,
  every-morning artifact -- that is `S3`/`RP-s-16`, a sibling cell, downstream of this one in
  the round-2 dependency graph.
- Does not group rows by business owner (`S13`/`RP-s-13`, a separate cell, not yet landed at
  this worktree's base) or render the VERDICT rule's own rendering of it (`S4`/`RP-s-17`, also
  downstream).
- Does not edit, redefine, or add a value to `STATE_MODEL.md`'s six ratified Axis-1 values or
  `VERDICT.md`'s rule -- both are implemented verbatim, and the one place this composer extends
  past a literal transcription (`compute_delta_watch()`, sec.3) is declared, not silent.
- Does not grade its own `AC5` (C-AI part 2 at the REPORT grain) -- recorded
  `UNVERIFIABLE-BY-INSTRUMENT`, `3.0.0_SA_CVO~Z` is the named oracle at L9, per the task order.
