# E4.3 FORWARD-REBUILD SPEC — a defensible multi-month FAIL trend, built forward

**Author:** 0.7.0_AE_CloudOps
**Date:** 2026-07-30
**Commissioned:** 2.0.0_SA_COO 20260730T063456Z, decision (a) over (b), on the grounds that
(a) carries a time-dependency and (b) does not
**Status:** SPEC — not built. Elements 1 and 5 need an arch word (`1.0.0_SA_CTO~C`); element 1
is the one whose cost rises daily.
**Depends on:** E4.1.3 (`631e71f4b9`), E4.2 (`a580011c3d`), traps (`39dffb3af7`, `eb5438f2d3`)

---

## 1. Why forward-only — the finding this spec exists to answer

E4.3 asked for C5's `12.14% -> 6.14%` re-derived independently. **It is not re-derivable, and
that is the result, not a failure to deliver one.**

| corpus | rows | span | rc column | re-verdictable |
|---|---|---|---|---|
| `org/compiler-tools-log.md` (RETIRED 2026-07-29) | 26,248 | 2026-04 .. 07 | **NO** | **NO** |
| `org/mcp/comp-tool-runs.jsonl` | 10,303 | 2026-07-14 .. 07-30 (16.15d) | yes | yes |

The markdown reproduces C5 exactly (12.30 / 12.74 / 9.37 / **6.14**) so there is no doubt
which population the headline came from. But it carries no `rc`, and its `result` cell is free
text (`PASS`, `FAIL`, `PARTIAL`, `WARN`, `1162 nodes/940 edges`), so there is nothing to
re-derive a verdict *from*. **The corpus that carries the trend cannot be corrected; the
corpus that can be corrected cannot carry the trend.** No amount of care closes that — it is
a missing column, not a missing effort.

So a corrected multi-month trend must be **accumulated forward**. Nothing recovers it
backwards.

## 2. The time-dependency, quantified

Rows are landing right now at a mean of **606/day** over 17 observed days — and highly
variable (56 on 07-27, 889 on 07-29), so the mean is a poor planning number and any window
claim must state its own per-day denominators rather than assume a rate.

Every day run without the basis pinned at write time is a day of rows whose verdict basis is
**inferred later rather than recorded**. If the contract surface then moves — and it will, 51
tools are pending declaration — those rows need re-baselining, which reintroduces exactly the
"was it the logic or the estate?" ambiguity that `verdict_basis` was built to close. **The
cost of element 1 rises every day it is deferred; the cost of everything else here is flat.**

A 90-day trend started today reads out in late October. Started a month from now, late
November. That is the whole argument for sequencing (a) first.

---

## 3. Design

### Element 1 — STAMP `verdict_basis` AT WRITE TIME *(the load-bearing one)*

Today `comp_log_auto` writes `result` with no record of which contract surface produced it.
The basis is reconstructed at re-baseline time, which only works while the surface has not
moved.

**Change:** the appender stamps the basis id on every row as it writes it.

```
rec["verdict_basis"] = "derived@v1+f09dab0e757496ea"   # version + content hash
```

`comp_output_contract.derived_basis_id()` already exists and already carries both halves
(the content hash is load-bearing: a hand edit that does not bump `version:` still changes
every derived verdict). Reuse it; do not write a second one.

**Cost, measured, not estimated:** 0.104 ms per call (read + sha256 of a 33,234-byte yaml),
about **66 ms/day** across the whole fabric at current volume. `comp_log_auto` runs as a fresh
process per tool call so the existing `lru_cache` gives one hash per process, not per row.
This is not a performance question.

**What it buys:** every row from that moment is permanently self-describing. No future
re-baseline is ever needed for it, under any contract change. The dual-basis machinery from
E4.1.3 stays as the tool for the 07-14..now rows that were written *before* the stamp — the
honest seam — and becomes unnecessary going forward.

**R8-compatible:** an additive optional key, exactly like `fail_kind` and `synthetic`. Does
not touch the route-id path.

### Element 2 — corpus profile as a PRECONDITION, not a courtesy line

`corpus_profile()` (built, `631e71f4b9`) prints rows / earliest / latest / span_days /
months_present / device scope / trend capability. **Make a trend claim structurally unable to
ship without it**, the same way `series()` already cannot return an aggregate without
`by_tool`.

Concretely: the trend entry point returns a dict that *contains* the profile, and a test goes
RED if the profile key is absent or if `months_present` has fewer entries than the number of
months the claim spans. A claim of "four months" over a one-month corpus should fail as a
type error, not be caught by a reader.

### Element 3 — the PREDICATE lives in the schema, not in convention

C5 said April FAIL `221 / 12.14%`. A `startswith("FAIL")` predicate gives `224 / 12.30%`. The
delta is **exactly the 3 `FAIL->FIXED` rows.** Neither number is wrong; they answer different
questions, and an unstated predicate makes them look like a discrepancy.

`series()` already emits `fail_predicate`. The forward rebuild is the moment to **fix it in
the artifact schema** so a stored series carries the predicate that produced it and cannot be
re-read under a different one silently. A stored series without its predicate is not a
measurement.

### Element 4 — retention must be PINNED, because nothing currently guarantees it

Measured: there is **no rotation logic in the code** and only one sink file exists (no `.1`,
no `.gz`). So accumulation works today by default. **But `.gitignore:448` carries
`org/mcp/comp-tool-runs.jsonl.*`, which anticipates rotation** — someone planned it. A
90-day trend silently dies if that lands mid-window.

**Ask:** an explicit retention statement for this sink (either "never rotated" or "rotated
with the rollup below as the durable record"). This is a one-line decision that costs nothing
now and costs the whole window if it is discovered late. It is a latent dependency, not a
current defect.

### Element 5 — the DEVICE-LOCAL problem, and why a rollup is the answer *(needs a word)*

`comp-tool-runs.jsonl` is gitignored, therefore **device-local**. It is short by every other
device's traffic, silently. So the trend it supports is *"this device's comp-tool runs"*,
never *"the estate's"* — and the current 10,303 rows must never be cited as the latter.

Two honest options:

**(a) Accept per-device, label it forever.** Zero build. The trend is real but scoped, and
every citation must carry the scope. Fragile: the scope is exactly the qualifier that gets
dropped when a number is quoted onward.

**(b) A committed daily ROLLUP — recommended.** One small append-only artifact keyed by
`(date, tool, result, fail_kind, verdict_basis)` with counts. No raw rows, no args, no
serials — so it is tiny, mergeable across devices by construction (counts add), reviewable in
a diff, and carries no content anyone would object to committing.

I recommend (b) and I am **not building it without a word**, for two reasons worth stating
rather than assuming: it is new machinery, and the standing posture is that machinery nobody
asked for is the anti-pattern. But note what it is and is not — **it is a typed record, not a
notification**: no SNS, no SES, no alarm, no `*-monitor`, no `*-freshness-checker`. The
moratorium does not bite a rollup that renders a report and fires nothing. If the answer is
(a), say so and I will make the per-device scope a required field rather than a caveat.

---

## 4. Acceptance criteria (machine-checkable)

1. **A row written after element 1 lands carries `verdict_basis`**, and its value equals
   `derived_basis_id()` at write time. Exercised through a real shim into the real sink, not
   asserted from a unit call — a green suite describes a file, this claim is about a runtime.
2. **THE MUTANT (the acceptance test, not a nicety):** change the contract surface
   mid-window — declare one pending tool — then prove the pre-change rows still report their
   ORIGINAL basis id and the post-change rows report the NEW one, **and that the trend remains
   re-derivable across the boundary with no re-baseline of the pre-change rows.** If a
   contract change silently re-labels historical rows, element 1 is not built; report that,
   do not tune around it.
3. **A trend claim spanning N months fails** (raises / returns an error object) when
   `corpus_profile().months_present` has fewer than N entries. Positive control run
   separately: a claim within the corpus's actual span succeeds.
4. **A stored series carries its `fail_predicate`**, and a reader that supplies a different
   predicate than the stored one gets a loud mismatch, never a silent recompute.
5. **Per-series decomposition present on every aggregate** (already structural — a test goes
   RED if `by_tool` collapses).
6. **The denominator is printed on every series**, including the declared-vs-registered split:
   an undeclared tool cannot contribute a FAIL by construction, so a falling aggregate is
   partly a statement about contract coverage. Current state: declared-only 9,789 rows /
   0.89%, with 106 nonzero rows structurally invisible to FAIL, and the 50 undeclared tools
   are 71% of the roster but only 4.5% of the traffic.

## 5. Non-goals / explicitly out

- **Recovering C5 backwards.** Established impossible in §1. Any future "we reconciled to
  12.14%" is a red flag, not a result.
- **Attaching a cause to rc=120.** 19 rows, 6 tools, two hypotheses tested and **both
  refuted** (H1 harness-rc corruption: the rate *rose* across MSTR's 07-28 mount fix,
  0.120% -> 0.727%, and a fix cannot raise the rate of what it fixes; H2 CPython exit-120
  stdout-flush-on-closed-pipe: piped python exits 1, and `comp-opalbizsem --list` exits 2 both
  piped and unpiped). It stays visibly in `undeclared_rc`. Per COO 063456Z: do not close it
  out with a cause.
- **The 5 outstanding `kind:` declarations** (option (b) in COO's decision) — deferred, and
  the reason is structural: they need tool owners, and almost every worker serial is dead
  tonight.
- **Anything notification-shaped.** Standing moratorium.
- **The 50-tool declaration tail.** Bounded, visible, gate-held. Closing it is a much larger
  motion than this spec.

## 6. Sequencing

Element 1 first and alone — it is the only one whose cost rises daily, and it is a
~10-line additive change to a function that already exists. Elements 2, 3 and 6 are
test-and-shape work on code already landed. Element 4 is a one-line decision. Element 5 is a
build that should not start until (a)-vs-(b) is ruled.

**Nothing here needs Terraform**, so none of it contends with `~A`'s hard Aug-1 10:00 ET ETFS
clock or races a HALTGT checkpoint. I will ping `~A` before any apply regardless.
