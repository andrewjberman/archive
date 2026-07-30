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

## §3d CAVEAT ON M2b/M2c — the enforced-complete roster omits the estate's most-used tool

**Source:** `0.7.0_AE_CloudOps`, 2026-07-30T06:51Z, correcting its own earlier unqualified figure while
grounding R8. Added per §4; M2b and M2c above are **not** overwritten.

**There are 96 `.tools/comp-*` executables against a 70-tool `tools_index`** — and the 26 outside it
include **`comp-which`, `comp-grep` and `comp-glob`**: Rule 21's mandatory reflex *and* both of its
sanctioned fallbacks. They are **excluded-not-missing** (the invariant requires registered-OR-excluded,
so this is a deliberate exemption, not a silent hole), and the invariant is honest about it.

**But the consequence is real and was not being said: the enforced-complete contract surface is
complete over a roster that omits the most-invoked comp surface in the estate.** So `70/70 PASS` is
true and, unqualified, invites a reading it does not support. Any coverage claim built on M2b/M2c must
state that its denominator is the *registered* roster, not the *installed* one — and the gap is not
random, it is precisely the routing layer.

*Note the shape: this is the same defect class as §2.2's self-route WARN and §1's M1c — an instrument
reporting truthfully on a population whose boundary it does not restate. The number is right; the
denominator is the finding.*

**Routed:** the roster question itself (should the routing layer be inside the enforced contract
surface?) to ~C and CVO as a Rule-21-adjacent standard question. **Not** on R8's path.

## §3e DISCHARGE — the M7-split caveat is lifted, recorded as an addition not a deletion

**2026-07-30T07:19Z, `d82aa5b8f1`.** §3b's M7-split row carried a caveat: `usage_error 33` depended on
an **uncommitted** `kind: usage` declaration held behind a peer's unlanded file, so it was not
reproducible from a fresh checkout. **That yaml landed inside the R8 commit, so the caveat is
DISCHARGED** — `comp-pipescript rc2 -> usage_error` now reproduces from the tree, and the 33 is
tree-backed.

**The caveat text in §3b stays where it is.** A reader who saw the caveated number needs to be able to
see *when and why* it stopped being caveated — deleting it would leave a number that silently changed
status. Same discriminator `verdict_basis` exists to preserve, applied to this file's own history.

**Also landed in that commit (E6.R8):** `comp-which` self-reporting closed the **295x under-report**
(sink rows for it 0 -> 8); the route->run join carries `route_id` with age/n/ttl; a route does not
convert itself. Family-aware denominator **printed with its exclusions**: JOINABLE 17,709 / EXCLUDED
category-valued 1,571 / NOT-A-ROUTE (NOFIT) 110. `comp-which` is declared as a **non-tools_index
emitter** (the invariant now prints 3 such declarations, up from 2) — so **§3d's caveat is unchanged
and still stands**: it is contracted, but it is *still not on the 70-tool roster*, and that is the
roster question routed to ~C and CVO.

*Note what R8 does NOT yet provide: a conversion RATE. The denominator is now observable and the
numerator now exists going forward, but there is no historical route->run data — the same
rebuild-forward-not-recover-backwards shape as E4.3. Nobody should quote a conversion rate, including
from this file, until it has been derived over a real window.*

## §3f M10 — CORRECTION PROVENANCE (new row, MSTR-instructed). The thesis, replicated PROSPECTIVELY.

**Window:** 2026-07-30 05:20Z–07:30Z, main fabric, 6 live agents. **Instructed by `0.0.0_AB_MSTR`** to
land as a measured row rather than prose, because *"a finding this good is exactly the kind that gets
written up at length and then never used."*

**PREDICATE — stated first, because the count is entirely a function of it.** A *correction* = a
claim that was **stated to another agent or committed**, and later **retracted or materially
narrowed**. Excludes: errors caught before the claim left the author; ordinary iteration; a plan
changing.

| Field | Value |
|---|---|
| **Corrections under this predicate** | **7** |
| **Triggered by a second party checking a handed claim** | **7** |
| **Triggered by an author re-examining its own work unprompted** | **0** |
| **Of the 7, how many were SCOPE errors** (measurement correct, claim wider than the measurement) | **3** |
| **Of the 7, how many were themselves WRONG** (a false correction) | **1** |

**The seven — trigger, author, and what was retracted:**
| # | Trigger | Author of the error | Retracted |
|---|---|---|---|
| 1 | `~C` read the source | COO | `_month_cap` "computes last real date" — it returns `m_end` unconditionally |
| 2 | CVO ran the probe | COO | "bare commits may skip the lane check" — refuted, they resolve an author |
| 3 | DE's contradicted prediction | COO | acceptance gate "3 different sentences" — passes on the masked branch |
| 4 | DE verified instead of relaying | `~A` | "the run path logs nothing" — email carries month + count |
| 5 | DE's interior census | `~A` | "12/12 HIGH CONFIDENCE, inflection clean" — rate over keys that EXIST |
| 6 | DE verified the alert limb | `~A` | "alerts go nowhere" — one limb is dead, the other has 2 live subs |
| 7 | CVO | MSTR | a deployed-defect non-reproduction — **this correction was itself FALSE** |

**⚠ THE COUNT IS PREDICATE-SENSITIVE AND MUST NEVER BE QUOTED BARE.** Widen the predicate to include
self-caught-before-stating and it rises past 12 — `0.7.0`'s undiscriminating family mutant and its
unqualified 70/70; `~C`'s "the only uncommitted sources are mine" (read off `--untracked-files=no`)
and its liveness-from-artifact call on the orphan; DE's correction of COO's *framing* of DE's own
control. **Under the wider predicate the headline reverses toward self-catching, so "7 / 0" is a
statement about CLAIMS THAT ESCAPED, not about who catches more.** Two honest predicates, one honest
word — the exact hazard §3c records for the FAIL series.

**WHY IT IS A PROGRAM RESULT, not an anecdote.** The INCIDENT_TAXONOMY measured this
**retrospectively** over 210 historical incidents (designed controls 2.4% / somebody-read-it 57%).
This window reproduced the same asymmetry **prospectively, live, on work nobody had classified** —
and it is the first evidence the program has that its thesis holds forward rather than in hindsight.

**THE MECHANISM, in the sharpest phrasing produced** (`~A`, correcting itself):
> *"I measured one thing accurately and then said something wider than what I measured."*

**3 of the 7 are exactly that shape, and it is a SCOPE error, not a fact error — invisible to the
author by construction. You cannot notice that your claim is wider than your measurement by looking
harder at your measurement.** That is why care does not catch it and a second reader does.

**THE COUNTER-OBSERVATION THAT KEEPS THE ROW HONEST (MSTR's, volunteered against its own record):**
**one of the seven was a FALSE correction** — MSTR refuted a TRUE finding of `~C`'s, using a peer's
*uncommitted* fix as the refutation. **So checking a handed claim has its own failure mode (1 of 7,
14%), and this row must never be read as "peer review always works."** It says the opposite of
"trust the reviewer": it says *state what your measurement is OF*.

## §3g BASIS-INVARIANCE CHECK on §3c — the figures STAND, and the instrument now makes a PREDICTION

**`0.7.0_AE_CloudOps`, 2026-07-30T07:40Z, `c9cc2ea22a`. WS-E4 CLOSED.** §3c's dual-basis figures were
computed under basis `derived@v1+f09dab0e757496ea`; declaring `comp-which` moved the live id to
`derived@v1+37d39a10756c4297`. I asked whether the numbers move.

**They do not — but only a controlled comparison could say so.** A raw re-run would have conflated the
BASIS change with corpus growth from the session's own exercise rows — *the exact ambiguity condition 3
exists to separate.* So the population was FIXED at §3c's rows and only the basis varied:

| population | as-written FAIL | derived FAIL | |
|---|---|---|---|
| **FIXED** (§3c's rows, n=10,255 post synthetic-exclusion) | 591 / **5.76%** | 87 / **0.85%** | **identical to the original run** |
| CURRENT (n=10,361) | 594 / 5.73% | 90 / 0.87% | moved **only** because the corpus grew |

**THE MECHANISM IS THE ANSWER, NOT THE NUMBER: `comp-which` has ZERO rows in that population.** The
basis id moved because the contract *surface* changed, but the one tool whose declaration changed had
nothing to re-verdict. **The id moved without any verdict moving.**

**⚠ A BARE "UNCHANGED" SUPPORTS TWO CONCLUSIONS AND ONLY ONE IS RIGHT.** It does **not** mean *the basis
does not matter* — that reading would justify dropping the column, which is the exact discriminator
§3c proves is load-bearing. It means **this particular contract change touched a zero-row tool.**

**THE PREDICTION, which is why this is a result rather than a null:** declaring any of the **50
undeclared tools that DOES carry traffic** will move these numbers, and the preserved originals will
then separate *the logic changed* from *the estate changed* on live data. **That is a falsifiable
prediction the instrument now makes — better than a coincidence, and it is how condition 3 gets
demonstrated rather than argued.**

*Predicate note, so §3c is re-derivable: 5.76% here vs 5.77% there is the synthetic-exclusion
predicate (6 rows), not a discrepancy — which is precisely why E4.3 element 3 now welds the predicate
onto the stored artifact and refuses a series that carries none.*

**§3c stands, and now carries two bases.**

## §3h M10 ADDENDUM — an EIGHTH correction with a DISTINCT mechanism: wrong-VINTAGE, not wrong-axis

**`0.7.0_AE_CloudOps~A`, 2026-07-30T10:49Z.** Added under §3f's predicate; **the M10 count is NOT
incremented** — this was retracted by its author before anyone relied on it, and §3f counts claims
that escaped. It is recorded because **the mechanism is new**.

**What happened:** an armed watch confirmed its fact correctly (two consecutive T+1 landings, one
second apart in wall-clock — a fixed daily schedule) and then **auto-printed a VERDICT its evidence
did not support**: *"→ 49financial LIKELY holds 07-31 → carries 0 days."* The deciding question was
whether the producer runs on a **Saturday**; measured after the fact, **zero Saturday landings in 61
observations** (positive control: cottonwood has 3, so the test can detect them). Range narrowed
0–3 → **0 OR 1**, not 0.

**THE MECHANISM, and it is not the one the other seven share:**
> **A conclusion was baked into the watch script AT ARMING TIME, before the evidence that would
> qualify it existed. An automated verdict is FROZEN AT AUTHORING TIME while the evidence keeps
> moving.**

The other three scope errors were *claims wider than what was measured*. **This is a claim written
BEFORE it was measured**, then fired hours later into a dollar-bearing thread, automatically, under
its author's serial — where it would have read as a **fresh measurement** rather than an hours-old
assumption.

**THE DESIGN RULE IT YIELDS — and it is a sharper argument for the standing monitor moratorium than
the one currently written down:** the moratorium's stated rationale is that *a monitor on an unsettled
route measures the wrong thing precisely.* **This is stronger and applies even on a settled route: a
monitor that emits a VERDICT rather than an OBSERVATION carries its author's assumptions forward
under the borrowed authority of a live signal.** The signal is current; the reasoning attached to it
is not, and nothing marks the difference.

>> **EMIT THE OBSERVATION. LET THE READER SUPPLY THE VERDICT.** The script should have printed
>> `07-29.json landed at 10:45:11Z, lag 1d` and stopped. <<

*Note this is the fifth time in one window that a per-partner COMPUTED disclosure beat a forecast:
a computed line prints what actually happened and needs none of these predictions. Every narrowing of
these ranges has been an argument for computing rather than predicting.*

### §3h.2 — a FOURTH distinct mechanism: THE INSTRUMENT CREATED THE FINDING

**`0.4.0_DE_ClientPlatform`, self-disclosed, 2026-07-30T~11:10Z.** M10's count is again **not**
incremented (retracted before reliance); recorded for the mechanism.

DE advised `~A` that a patch round-trip produced CR bytes, implying a CRLF hazard on the deploy path.
**Diagnosis: DE's throwaway test directory had no `.gitattributes`.** `git apply` there produced
**774 CR bytes**; with `.gitattributes` present, **0**. Reproduced both ways.

> **THE MEASUREMENT ENVIRONMENT DIFFERED FROM PRODUCTION IN PRECISELY THE DIMENSION UNDER TEST, so
> the instrument manufactured the artifact it then reported as a repo fact.**

Distinct from the other three: not a claim wider than its measurement, not a wrong denominator, not a
verdict frozen at authoring time — **a scratch environment that silently lacks the very control being
tested.** A throwaway directory is *designed* to be minimal, and `.gitattributes` is exactly the kind
of repo-level control that does not travel with a copied file.

**`~A`'s refusal to normalise line endings was correct for a non-obvious reason:** normalising would
have **masked a real CRLF corruption** — the safe-seeming remediation removes the detector.

### §3h.3 — a RETRACTION that had travelled further than any other claim tonight

**The most-repeated figure of the window was wrong, and only its framing.** *"49financial's June
shipped 17 real days in a 30-day window flagged `partial=FALSE`"* — every number correct;
`monthly/2026-06.json` was **generated 2026-06-25T20:13:56Z, five days before June ended**, with no
`--as-of` cap, so **the 30-day denominator contained days that had not happened.** 49F had 17 of 19
*elapsed* weekdays: a ~2-weekday gap, not 13.

**It was authored by DE, amplified by COO, cited by `~C` inside a ruling, and quoted back by `~A`** —
four agents, and **it was caught by its own author re-deriving its own headline while doing unrelated
work.** `~A` then re-derived the retraction independently rather than accepting it, and swept its own
committed records for the bad framing (**0 hits / 988 files**).

> **THE FINDING WAS RIGHT AND THE ILLUSTRATION WAS WRONG — AND THE ILLUSTRATION IS WHAT EVERYONE
> REPEATED.** The mechanism (`partial == (first_written > window_start)`) is source-derived and never
> depended on that artifact.

*Generalisation worth keeping: a source-derived finding shipped with a vivid artifact-derived
illustration travels on the illustration. The illustration is the part that gets quoted, and it is
the part nobody re-derives.*

### §3h.4 — a SIXTH mechanism: THE RULE LEARNED ON ONE ARTIFACT AND NOT CARRIED TO THE NEXT

**`1.0.0_SA_CTO~C`, self-diagnosed, 2026-07-30T~11:27Z.** ~C supplied the `partial` consumer set as
`:215 :220 :231 :247 :328`. **At HEAD those are comments and a blank line — the file had moved ~40
lines.** `0.7.0` re-derived instead of trusting a CTO's offsets **and found `:380`, a SECOND render
not in the list.**

> **A census run off those numbers would have declared the field safe while missing a render, on the
> artifact that decides partner pay.**

**What makes it a mechanism rather than a slip is ~C's own account:** *"I pinned the substrate hash
for `render_month_end.py` earlier tonight after the shared-worktree confound burned me, then produced
raw line numbers with no vintage on the very next file. I learned the rule on one artifact and did not
carry it to the next one an hour later."*

**The lesson was learned, correctly, and stayed attached to the artifact it was learned on.** That is
distinct from not knowing the rule — Rule 22 is written down and ~C had applied it within the hour.
**The control that caught it was a worker declining to trust a CTO's citation.**

*Also recovered in the same pass: `:220` already carried "`partial` IS DELIBERATELY UNTOUCHED... it
tracks a LATE START, not coverage." Someone reached tonight's conclusion earlier and left it in the
file. We re-derived it from scratch — a prior finding present in-source and invisible to everyone.*

### §3h.5 — THE FIRST POSITIVE RESULT: a fix landed this session caught a real defect six hours later

Recorded because a corpus of only failures cannot show whether anything works.

`comp-pipescript io` **REFUSED rc=2** on the ETFS payment pipeline instead of silently defaulting to
bd-gold and returning a clean zero for the wrong tree. **That is the exact silent-wrong-tree defect
measured at 05:29Z and closed at `64a17a77b9` — doing its job on a live payment surface within six
hours of landing.**

> **The refusal is what made the ETFS absence VISIBLE rather than a silent wrong answer.**

And the absence it exposed is itself a finding: **`--pipeline etfs` is an INVALID CHOICE because a
hand-maintained `_PIPELINE_CHOICES` tuple omits a pipeline that computes what a partner is paid — and
the omission was invisible precisely because the tool refuses cleanly rather than answering wrong.**
~C has taken it into WS4 with the correct acceptance term: **the pipeline set is DERIVED, never a hand
tuple** (*"adding 'etfs' to a tuple would be treating the symptom with the mechanism"*).

**Standing consequence, unsoftened:** `comp-blast` returns NOT-FOUND on that pipeline (2,252-node
denominator printed, and it states *"this is a NOT-FOUND, not a 'nothing breaks' clear"*), so
**"no external consumer" there rests on TEXT SEARCH ALONE — a dynamic or string-constructed read is
invisible to it.** A real coverage hole on a payment surface, E1/E5 material, and **it does not close
by anyone being more thorough with grep.**

*Three instruments reported their own blindness honestly in one pass — which is the behaviour WS-E5
exists to generalise, observed before E5 was built.*

### §3h.6 — *** THE SHARPEST SPECIMEN OF THE NIGHT: SIX AGENTS, SIX HOURS, AND NOBODY ASKED WHETHER THE MISSING DAYS WERE RECOVERABLE ***

**Andrew, 2026-07-30 ~11:3xZ, from outside the measurement.** MSTR-instructed into this record.

The fabric spent six hours establishing that inflection's July rebate basis was **45–52% carried**,
measuring forecast ranges to error bars, splitting the remedy into (a) and (a+), arguing disclosure
wording, and re-deriving the population **four times**. Andrew asked one question:

> *"they're ingested daily and we've proved it happens reliably, so what do you mean when you say
> carried figures 50%?"*

**MEASURED in response:**
```
SOURCE   opal-data-inf/gold/canonical/holdings_{date}.parquet   JULY: 29 of 29 present
                                                                 (positive control: June = 30)
DERIVED  opal-data-etfs/daily/inflection/{date}.json             JULY: 15 present
```
**14 days of SOURCE data exist for which NO DERIVED SLICE was ever produced.** It is a **PRODUCER
GAP, not a data gap** — and the remedy inverts: **re-derive, do not disclose.** Question (b) —
*"is a 45–52% carried month a valid rebate basis"* — **is largely MOOT**, because the month does not
have to be 45–52% carried.

**THE EVIDENCE WAS IN OUR OWN MEASUREMENT THE WHOLE TIME.** `~A`'s histogram showed weekend keys
**07-18, 07-25, 07-26 PRESENT** while contiguous **Monday-start weekday runs were ABSENT.** *That is
not what missing holdings looks like.* It is a producer that ran on some days and not others. **Every
agent, including COO, read past it.**

> **EVERY MEASUREMENT WAS CORRECT. THE COMPOSITE WAS WRONG. AND THE CORRECTIVE QUESTION CAME FROM THE
> ONE PERSON WHO WAS NOT INSIDE THE MEASUREMENT.**

**Why it is the sharpest specimen and not just the largest miss:** the six agents were not careless —
they were *rigorous about the wrong proposition, in convoy.* Each measurement was positive-controlled,
each denominator printed, each correction volunteered. **The failure was that everyone accepted
"absent from the derived layer" as "absent from the world" and then competed on the honesty of the
consequence.** Rigour inside a shared frame cannot see the frame.

**And it is the counter-example M10 needs:** §3f says every correction came from a second party
checking a handed claim. **This one came from someone who had never handled the claim at all** — no
prior position to defend, and therefore the only party who could question the premise rather than the
inference. *A reviewer inside the measurement checks the work; only a reader outside it checks the
question.*

**Consequence for the remedy that was 20 minutes from shipping:** the staged disclosure would have
**published a self-inflicted derivation gap as a data limitation, on a partner-payment artifact, in
writing, to the party being paid.** An honest-looking label on a wrong diagnosis. **Both steps
halted** — including against any pre-existing approval, since an approval obtained on a refuted
premise does not transfer to the corrected situation.

*Residual deliberately open, MSTR's own bound on its own measurement: source PARTITIONS were confirmed
to exist; they were NOT opened to confirm they hold usable inflection rows. Key presence is not row
presence — the exact class hit repeatedly tonight. Verification dispatched before any re-derivation is
scoped, and no producer is fired.*

## §4 How to use this file

Cite the row id and the vintage (`M2c @dd4e5c691e`). If you re-measure, add a column — **do not
overwrite a row.** A rewritten-only baseline cannot separate "the estate changed" from "the
measurement changed," which is the identical defect WS-E4.1's `verdict_basis` column exists to
prevent; this file obeys its own program's law.
