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

## §4 How to use this file

Cite the row id and the vintage (`M2c @dd4e5c691e`). If you re-measure, add a column — **do not
overwrite a row.** A rewritten-only baseline cannot separate "the estate changed" from "the
measurement changed," which is the identical defect WS-E4.1's `verdict_basis` column exists to
prevent; this file obeys its own program's law.
