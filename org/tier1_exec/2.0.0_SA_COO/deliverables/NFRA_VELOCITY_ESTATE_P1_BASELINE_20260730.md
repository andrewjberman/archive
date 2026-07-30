# NFRA_VELOCITY_ESTATE — WS-E4.4 P1 METRICS BASELINE

**Author:** `2.0.0_SA_COO` · 2026-07-30 · **Vintage:** `dd4e5c691e` (2026-07-30T01:30:34-04:00 local = 05:30:34Z)
**Authority:** PROGRAM §5 (baseline at P1) · ESTATE PRD WS-E4.4 · Andrew-direct GATE 0.
**Purpose:** the P1 anchor. Every later "are we improving?" claim in this program cites this file or it
is unanchored.

## The one rule this file obeys

**A number without a denominator is not a baseline, and a number without a provenance is not a
measurement.** Every row below carries both, plus a STATUS that says whether *I* measured it or
merely *carried* it. Rows I could not measure are present and marked — an absent row and a zero row
are not the same object, and this program exists because that difference kept getting lost.

STATUS values: **MEASURED** (I ran it at this vintage) · **CARRIED** (cited from a named prior
measurement, NOT re-derived by me) · **NOT-YET-MEASURABLE** (no instrument exists yet; the absence is
the finding).

---

## §1 The baseline

| # | Metric (PROGRAM §5) | Baseline | Denominator | Provenance | Status |
|---|---|---|---|---|---|
| M1a | Rail-override count (`# rail-checked:`) | **76** | **24,205** log lines | `org/mcp/comp-which-rail.log`, `grep -a` | MEASURED |
| M1b | Rail DENY events | **665** | same 24,205 | same | MEASURED |
| M1c | Rail NUDGE events | **0 tokens present** | same 24,205 | same | **MEASURED, BUT SEE §2.1** — "no NUDGE token in the log" does NOT establish "no nudge fired" |
| M2a | comp-* executables tracked+committed | **89** | — | `comp-manifest-check completeness` | MEASURED |
| M2b | Registered tools (`tools_index`) | **70** | 89 executables (70 indexed + 19 excluded) | same | MEASURED |
| M2c | Tools **declaring** an output contract | **20 declared / 50 pending** | **70** | same | MEASURED |
| M2d | Tools with ESTABLISHABLE subcommand declaration | **28** (42 UNKNOWN) | **70** | same | MEASURED |
| M2e | Tools/detectors emitting a **boundary report** (recall denominator) | — | — | no instrument | **NOT-YET-MEASURABLE** — WS-E5's job. M2c is the nearest existing thing and is a *different property*; do not substitute it. |
| M3 | Catch distribution: D1 designed-control **2.4%** / D4 somebody-read-it **57%** | 2.4% / 57% | **210 incidents, 14 mechanisms** | `INCIDENT_TAXONOMY/` @`31a038f0f3` | CARRIED — not re-derived by me. **Read 2.4% as a PLACEMENT failure, not a design failure** (PROGRAM §5.3). |
| M4a | Contracted coverage (estate D3 contracts) | **0** | denominator **not yet enumerable** | `org/modules/graph/estate-contracts/` is **ABSENT** | MEASURED — zero by construction; the registry does not exist yet |
| M4b | Dead surfaces adjudicated | **0 of 353** | 353 | `comp-legacywriter --census` via @`d51f6b38a0` | CARRIED — the 353 is CTO~C's census, not my re-derivation |
| M5a | Doctrine surface bytes — `CLAUDE.md` | **46,593** | — | `wc -c` | MEASURED |
| M5b | Doctrine surface bytes — `docs/doctrine/` | **168,899** across **7** files | — | `wc -c` | MEASURED |
| M5c | **Total doctrine surface** | **215,492** | — | M5a+M5b | MEASURED |
| M5d | Largest single doctrine file | `CONTROLS_OVER_CARE.md` **95,578** = **44.4%** of the whole surface | 215,492 | `wc -c` | MEASURED |
| M5e | M-laws carrying a NAMED GATE that absorbs their class | — | — | not enumerated | **NOT-YET-MEASURABLE** — and it is the half that makes M5 honest: byte-count alone falls by *moving text to references/*, which WS-C8 explicitly does. **Never report M5c falling without this paired number.** |
| M6 | The specimen (bronze-after-gold) structurally impossible | **NO** — currently possible | — | ESTATE PRD WS-E1 | MEASURED (state, not rate) |
| M7 | Per-series FAIL decomposition, three meanings separated | **NOT SEPARATED** | — | — | **NOT-YET-MEASURABLE** — blocked on WS-E4.2, in flight at `0.7.0_AE_CloudOps` |
| M8 | Archetype weight + dynamics | — | — | — | **NOT-YET-MEASURABLE** — WS-E7, P5 by Andrew-direct placement ruling |
| M9 | **PRODUCT-GRADE:** ADVI_PERFORMANCE + MDPF_GLOBAL build cost vs pre-framework baseline | **HELD BY `~Z`** | — | — | **PERISHABLE, NOT MINE.** See §3 — this is the only metric that measures the objective function, and the only one that cannot be re-taken. |

---

## §2 Findings that fell out of taking the baseline

### 2.1 M1c — a zero I am refusing to report as a zero

The rail log contains **no `NUDGE` token across 24,205 lines**. The tempting baseline is "nudge rate =
0". I am not recording that, because **this file cannot distinguish "no nudge ever fired" from "nudges
are not written to this log"**, and those two have opposite meanings for WS-E6.3 path tuning. The
recorded baseline is the *token count*, with the ambiguity named. Resolving it is a WS-E6 first task:
find the nudge emitter and determine whether it has a sink at all.

*A zero from a query nobody positive-controlled is not a measurement — it is a query that returned
nothing, which is also what a broken retrieval returns.*

### 2.2 FINDING — a WARN emitted on 100% of its population, sitting inside a PASS

`comp-manifest-check completeness` at this vintage emits **70 `self-route WARN` lines against exactly
70 registered tools** — every tool in the population — and returns **`PASS`**.

**Source-confirmed** (`org/modules/graph/manifest_check_cli.py:713-719` @`dd4e5c691e`): the check
classifies each tool `HIT` / `NEARTIE` / `MISS` / `UNEVALUABLE`; `NEARTIE` prints the WARN and
**does not affect the return code** (`return 0` when there are no `MISS` and no `UNEVALUABLE`). Measured
this run: **70 NEARTIE, 0 MISS, 0 UNEVALUABLE.** The self-route query is each tool's *own richest
use_case sentence* and is documented in `org/modules/graph/comp_route_eval.py:24` as
**"NEAR-TAUTOLOGICAL"** — the query is derived from the tool's own catalog text.

**What is INFERRED and must be grounded before anyone acts on it:** whether 70/70 NEARTIE means the
router genuinely never ranks a tool first on its own description (a real ranking defect), or whether
NEARTIE is the structurally normal shape of a comp-which tie-group return (in which case the WARN is
noise by design and the check is mis-specified). **I have not established which.** Both readings are
live; I am not asserting the defect.

**Why it is a finding either way, and why it belongs in THIS file:** a WARN that fires on 100% of its
population carries **zero discriminating information**, and it is wrapped in a PASS. That is
simultaneously WS-E4.2's subject (a status column whose meanings are conflated, so the trend is
unreadable in either direction) and WS-E6's subject (router conversion). It is also the
instrument-that-cannot-fail class in its mildest, most survivable form: nothing is lying, but nothing
is being learned, and the green verdict makes it invisible.

**Routed:** `3.0.0_SA_CVO` to ground the mechanism; `0.7.0_AE_CloudOps` to fold the disposition into
WS-E4.2 rather than treat it as separate work. **Not a blocker on Wave 1.**

### 2.3 M2c is the sharpest already-true number in the set

**20 of 70 registered tools declare an output contract; 50 are pending.** This is a real, gate-maintained
71%-undeclared surface, measured by an invariant that already blocks at commit time. It is the closest
thing the estate has to a coverage denominator today, and it is a better P1 anchor than any doctrine
byte-count.

---

## §3 What this baseline deliberately does NOT cover, and who holds it

**M9, the product-grade metric, is not mine and is not takeable by me.** ADVI_PERFORMANCE's
pre-framework build-cost baseline is `~Z`'s to capture at its decomposition, and MDPF_GLOBAL's is
Act-3 scope. It is **PERISHABLE with no re-measure**, it is the only metric that measures the
objective function rather than the framework against itself, and it is the only Act-1 exit criterion
whose deadline is **not a gate** — so it can be missed while every gate in this file reads clean.

Per MSTR's standing instruction it is an **OWNED BLOCKING ITEM held by `0.0.0_AB_MSTR`**, and it
deliberately gets **no guard, no check, and no alarm** — building a detector for it would be the
failure, not the fix. WS-E1 and WS-E2 do not start until MSTR relays that it is captured.

**Every other metric in §1 measures the framework against the framework.** That is worth stating
plainly at the anchor point, because a program can move all nineteen rows above and still have failed
its actual test.

## §3b RE-MEASURE 1 — added as a column, per §4. Nothing above is overwritten.

**Source:** `0.7.0_AE_CloudOps`, 2026-07-30T05:45Z, while exercising E4.1. Its measurement is
**finer-grained than mine** and supersedes nothing — both stand with their provenance.

| Row | My value (05:30Z) | Re-measure (05:45Z, 0.7.0) | Note |
|---|---|---|---|
| M2c | declared **20** / pending **50** of 70 | declared **22** (20 registered + 2 non-tools_index emitters) / pending_declaration **51** | **DISCREPANCY, DELIBERATELY UNRECONCILED:** my numbers are the invariant's own summary line (`declared 20 + pending 50`, which sums to exactly 70); theirs decomposes declarations to include the 2 non-tools_index emitters, and reports pending as **51**, not 50. I am not silently picking one. The 20/50 pair is the *registered* population; 22/51 counts a wider set. **Anyone computing a rate must say which population.** |
| M2c-derived | — | **50 of 70 registered tools (71%) render UNKNOWN on a nonzero exit today** | The consequence that matters: a FAIL-% computed over *declared* tools has a denominator of **20, not 70**. 0.7.0 is printing that denominator on every series it ships. |
| M7 (row counts only) | NOT-YET-MEASURABLE | **10,237 telemetry rows: PASS 9,117 / FAIL 585 / VERDICT 442 / UNKNOWN 76 / REFUSE 11 / 6 synthetic-tagged** | The row **counts** are measurable now; the **three-meanings separation** is still not built, so M7 stays NOT-YET-MEASURABLE as specified. A count is not a decomposition. |

**Scope correction that came with it, and it changes what P1 is:** E4.1's conditions 1 and 2 were
**already built on 2026-07-23** (NFRA_MSBEFF.R1R3/M3) and had **never been exercised**. 0.7.0
exercised both with deliberate mutants, positive controls run first and separately, and
byte-identical restore verified — both PASS, the guard fires and names its offender. **The real
unbuilt work is condition 3 (`verdict_basis`) and E4.2.** `comp_msbeff_rebaseline.py` emits
`result` + `result_prior` + `rebaselined:true` on one row — two values on a row is **not** a version
column, and `rebaselined:true` cannot distinguish a v1 re-baseline from a v2 one, which is precisely
the discriminator condition 3 exists to preserve. With 51 tools pending declaration the contract
surface **will** change again.

*Two-thirds of a gate-approved deliverable was already built and unexercised. That is the
declarative-drift class this program was commissioned to kill, found inside the program's own first
workstream — and it was found by measuring before building.*

## §3c RE-MEASURE 2 — the measurement plane came online, and its first answer is about itself

**Source:** `0.7.0_AE_CloudOps`, 2026-07-30T06:24Z, WS-E4 landed (`39dffb3af7` E4.1.1+E4.1.2 ·
`631e71f4b9` E4.1.3 · `a580011c3d` E4.2). 34/34 traps across three suites, every suite proven able
to go RED before green was trusted.

**M7 IS NOW ANSWERABLE — and the first thing it says is that the headline improvement was the
INSTRUMENT, not the estate.** The dual-basis query (both bases run, which is the acceptance I set):

| basis | FAIL rate | |
|---|---|---|
| as-written | **5.77%** | the number the old record would have reported as improvement |
| derived (corrected contracts) | **0.85%** | |

The mix, per-series: **comp-pulse 358 -> 0** (alone 358 of 505 corrected rows) · comp-system 59 -> 0
· comp-blast 45 -> 5 · comp-constants 17 -> 0 · +12 more to zero. The movement is the frozen-era
`nonzero -> FAIL` blanket being retired — **the verdict LOGIC changing** — not the estate getting
better.

***This is the single most important number this program has produced so far, and it exists only
because condition 3 was binding.*** Had the history been re-baselined without preserving the
originals, this series would have moved identically and been indistinguishable from real
improvement. The discriminator ~C's finding 3 protected is not hypothetical: **it fired on the
first real query.**

| Row | Re-measure 2 | Note |
|---|---|---|
| M7 | **ANSWERABLE per-series with denominators** — three meanings separated in the machine record as a typed `fail_kind` | The row above stays as originally written; this is the state change, dated. |
| M7-split | post-M3 FAIL population (87 rows): **usage_error 33 / kind_undeclared 32 / undeclared_rc 22 / negative_control 6** | **62% not yet assignable, REPORTED rather than guessed**, tail bounded and named (5 tool:rc pairs). ⚠ **CAVEAT, disclosed by the author unprompted: the `usage_error 33` depends on an UNCOMMITTED `kind: usage` declaration held behind a peer's unlanded file — it is NOT reproducible from a fresh checkout today.** Degraded-but-honest; do not quote 33 as tree-backed. |
| M7-denom | declared-only: **9,789 rows / 0.89%**; **106 nonzero rows structurally invisible to FAIL** | An undeclared tool **cannot contribute a FAIL by construction**. The 50 undeclared tools are **71% of the roster but only 4.5% of the traffic** — so the coverage gap is far smaller in traffic terms than in tool terms, and either framing alone misleads. |
| M1-adjacent | **rc=120: 19 rows, 6 tools, cause UNDETERMINED** | Two hypotheses tested and **BOTH REFUTED** — harness-rc corruption refuted because the rate *rose* across the 07-28 mount fix (a fix cannot raise the rate of what it fixes); CPython flush-on-closed-pipe refuted by exercise. **No cause attached.** 22% of FAIL, sitting visibly in `undeclared_rc`. Includes comp-iam and comp-blast. |

**M4b/E3.0 — the safe slice was measured and the PRD's premise did not survive it** (`~A`,
`2da40ba711`): 437 written surfaces of 643 locations, 8,915 files scanned -> 56 in the E3.0 name
population -> 21 structurally excluded -> 35 survivors -> **29 HOLD LIVE OBJECTS** (largest 436,489 B)
-> 6 genuinely empty -> **0 retired, 6 of 6 KEEP-DORMANT** on the Tier-C-never-sufficient rule.
**Census-only 56, derived-from-contracts 0, coverage debt 56 of 56.** Existence via ListObjectsV2
(key+size), never HeadObject. **The safe slice and the clearable slice do not overlap** — the
population with zero blast radius is also the population with no Tier-A intent evidence. E3.0's
"early visible win" is not available as specified; re-spec routed to ~C.

**M6-adjacent, found in the field rather than from the PRD:** `aws events list-rules` is
structurally blind to EventBridge **Scheduler** — the Aug-1 month-end schedule is an
`aws_scheduler_schedule` and does not appear in it at all. A worker was one step from reporting a
missing production schedule 28h before a hard external fire; `comp-trigger` printing its own
denominator (**143 rules + 11 schedules**) resolved it. This is WS-E2's two-system denominator
specimen, live-confirmed.

## §4 How to use this file

Cite the row id and the vintage (`M2c @dd4e5c691e`). If you re-measure, add a column — **do not
overwrite a row.** A rewritten-only baseline cannot separate "the estate changed" from "the
measurement changed," which is the identical defect WS-E4.1's `verdict_basis` column exists to
prevent; this file obeys its own program's law.
