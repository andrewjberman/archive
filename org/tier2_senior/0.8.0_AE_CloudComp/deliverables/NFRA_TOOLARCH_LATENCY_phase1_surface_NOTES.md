# NFRA_TOOLARCH.LATENCY — Phase-1 surface: method, counts, and the two grain defects I caught

**Author:** 0.8.0_AE_CloudComp~B · 2026-07-23 · **Gates:** 1.0.0_SA_CTO~Z · **Verifies:** 3.0.0_SA_CVO~Z
**Artifact:** `NFRA_TOOLARCH_LATENCY_phase1_surface.jsonl` (152 records, 65 tools)
**STATUS: PHASE 1 ONLY. ZERO DERIVATIONS EXECUTED.** Read the grain caveat before using any count.

## Method (and why it is static)

Enumerated **from source, zero execution**. Not `<tool> --help`, because **for the auto-refresh family
the measurement instrument is itself a mutation** — `comp-kuzu` auto-refreshes the canonical surface on
a plain query, the `cli.py` read family rebuilds on a stale cache. You cannot ask those tools what they
do by running them. (Same class as a census that perturbs its own subject.)

Registry cross-check only: base 0.8.0 ruled `tools_index.subcommands` **non-authoritative** — it is
hand-maintained, ungated, and populated on 65/65 (the most convincing possible shape for a wrong
denominator). Measured drift **16/24** on the apples-to-apples set; the omissions include derivations
CLAUDE.md *mandates* (`comp-pipescript postdeps`, `comp-iam simulate` **and** `reconcile`,
`comp-registry sync`) — so `comp-which` cannot route agents to derivations the law requires.
Base ruled GATE+BACKFILL, gate first; spec routed to CTO~Z. Not mine to build.

## Classification — three classes, because the binary is false

`READ-ONLY` · `CONDITIONALLY-MUTATING` · `MUTATING` (+ `ENGINE-UNRESOLVED`).

**CONDITIONALLY-MUTATING** is the contribution (routed to ~Z as taxonomy): mutability is a property of
the **(command, cache-state) PAIR**, not of the command. Grounded instances from base 0.8.0:
`comp-kuzu` (auto-refresh on plain query, `kuzu_cli.py:58-59`), the `cli.py` read family
(`_get_graph(force_rebuild=...)` — read-only *only when the cache is fresh*), `comp-pulse`.
Consequence for this census: **a timing without its cache state is not a timing** — a wall-clock across
an unrecorded rebuild looks like tool latency and is a cache miss.

Named hazard (not an exclusion — the NAME is the trap): `deploy_ledger.py check --red` **delivers
red-alert files into 2.0.0_SA_COO's inbox**; base caused 7 real deliveries verifying their own fix.

## Counts — and BOTH grain defects, stated plainly

| pass | MUTATING | note |
|---|---|---|
| v1 coarse heuristic | 68 | **upper bound** — `json.dump(` matched printing-to-stdout as readily as writing a file |
| v2 refined (matched-line + sink analysis) | **64** | 13 base-authoritative + 51 source-confirmed **with exact `file:line` evidence**; 4 downgraded (write signal was print/scratch only) |

**DEFECT 1 (caught, fixed):** the v1 write-signal regex classed inspection tools as mutating. Refinement
inspects the *matched line* and discounts stdout/stderr/`json.dumps`/tempfile sinks. Net effect was
small (68→64) — the heuristic was mostly right — but I could not have known that without checking, and
reporting 68 as measured would have been a number my parser produced, not one the estate has.

**DEFECT 2 (caught, NOT fixed — the load-bearing one):** **my classification is ENGINE-grain; the TO's
unit is DERIVATION-grain.** A single writing subcommand marks *every sibling derivation* of that engine
MUTATING. The clearest case: `iam_cli.py:1017` writes a census file — that is `comp-iam refresh-census`.
But `comp-iam service`, `gaps`, `simulate` are **reads**, and engine-grain attribution would exclude
**exactly the derivations CLAUDE.md Rule 22a mandates**. Same shape for `pipeline_cli.py:2515`
(`inject` writes; `io`/`deployed`/`postdeps` read).

So: **64 MUTATING is an engine-grain UPPER BOUND, and the RUNNABLE set is a LOWER BOUND.** The error
direction is *safe* (over-exclusion → do not run, per the TO's "if in doubt, do not run it"), but it
suppresses census coverage, and the suppressed set is biased toward exactly the high-value read
derivations. **Closing it needs per-derivation attribution — tracing which subparser handler reaches
the write — which is call-graph work, not regex work.** Until then, no coverage percentage derived from
this file is a property of the estate; it is a property of my parser's grain. I am not presenting one.

## Run plan (unchanged by the refinement, and deliberately conservative)

`RUNNABLE` · `RUNNABLE-IF-PRECONDITION-RECORDED` (cache-fresh state established **and recorded with the
timing**) · `DEFERRED-AWS` (79 AWS-touching derivations — the main-fabric MDPF serve is open; ~Z's
safety design says sequence away from it, and the same signal that opens the R4 arm-window opens this)
· `NOT-RUN` (recorded with reason — never a silent skip).

Telemetry: the census runs under **`COMP_SYNTHETIC_FIXTURE=1`** (base's ruling), so every row is tagged
`(SYNTHETIC TEST FIXTURE)` and excluded from fail-% mining by design — the runs stay auditable while the
analysis stays unpolluted. *Hiding the rows would have made my own run unauditable to keep their
analysis clean; a census that leaves no trace is its own dishonesty.*

## CORRECTION to my own claim: EXISTS ≠ ROUTABLE (CTO~Z source-falsified my inference)

In the subcommand-drift delta I wrote that the undeclared subcommands mean *"comp-which cannot route
anyone to them."* **That sentence carried an unverified premise — that `tools_index` feeds the router.
I never traced the routing path; I inferred a consequence because it was plausible and pointed at a real
problem.**

CTO~Z source-confirmed the actual mechanism: `.tools/comp-which:1006-1010` @`e6115fa66` scores over
`entries[].{use_case,id,tool}` and displays `entries[].canonical_call` — **it never reads `tools_index`
at all.** Positive control on their probe: `comp-iam-usage` *does* surface with its subcommands, because
those are baked into its `canonical_call` string — so the router can render subcommand grain and the
probe was not blind to it.

Consequences, both against me:
1. **The fix I implied (backfill the registry) would not have made anything routable.** Declared entries
   are equally unroutable. I collapsed two different populations.
2. My finding was right about the **symptom** and wrong about the **mechanism** — Rule 22's class: a
   causal claim is a hypothesis until source-confirmed.

**Census consequence, adopted:** `tools_index` is used ONLY as the denominator for *what derivations
EXIST* — the correct use per the mandate — and must never silently become a claim about what agents can
**FIND**. The surface records therefore carry **EXISTS vs ROUTABLE as distinct axes**, and the
population that *exists, is declared, and has no consumer able to route to it* is reported as a
first-class finding rather than census noise.

### ROUTABLE — re-defined, STRICTER (CTO~Z correction 2026-07-24T033818Z)

~Z corrected their own earlier account: they had source-confirmed the fuzzy **backstop** and spoken
about "the router" — the file's own docstring names **two** layers. Ground truth:

> **`comp-which` RANKS off a CURATED VOCABULARY TABLE inside `.tools/comp-which`.** The ranked pool is
> **68 (= tools)**, not 105 (= entries). `entries[]` feeds the fuzzy **backstop** and does **not create a
> routing candidate at all.**

So **ROUTABLE = has curated vocabulary in `.tools/comp-which`.** `tools_index` presence → NOT routable.
`entries[]` presence → NOT routable either. **Size the population against the CURATED TABLE, never the
registry.** The declared-but-unreachable population is therefore **LARGER** than the earlier framing
implied, and the axis is sharper, not weaker.

**Why this lands harder than a definition change:** a tool can be REGISTERED (`tools_index`),
CONTRACTED (`comp-output-contracts`), and ENTRIED (`entries[]`) — three surfaces all asserting it exists
— and still be unreachable to every agent, because the only surface that creates a routing candidate is
a fourth, curated, hand-maintained table. **Same structural shape as the `subcommands` field: populated
on everything, gated by nothing, consumed by less than you would assume.** The census will therefore
report, per unreachable derivation, **which of the four surfaces it IS present on** — "declared in three
places and routable from none" is a far sharper finding than a bare count, and it tells TOOLSEM where
the leverage is. It is the sharper sibling of the ROUTE finding: there, the
rail routed to a tool that could not answer; here, the estate declares derivations no router can reach.
Same family — **the map and the territory disagreeing in a direction nothing measures.**

## Defect 2 — attribution ATTEMPTED, NOT CLOSED (and exactly why)

Built an AST attributor: map `X = sub.add_parser("name")` → `X.set_defaults(func=handler)` → walk the
handler + its local callees (depth 3) for write calls, so a subcommand is MUTATING only when a write is
reachable **from its own handler**.

**Result: it traced 5 of 53 engines. It does NOT close the defect,** and it did not cover the two
load-bearing cases (`iam_cli.py`, `pipeline_cli.py`) that motivated the work. Measured cause:

| engine | `set_defaults(func=)` | `args.cmd ==` if/elif | `add_parser` | traced? |
|---|---|---|---|---|
| `manifest_check_cli.py` | 8 | 0 | 8 | YES |
| `iam_cli.py` | **0** | **15** | 15 | no |
| `pipeline_cli.py` | **0** | **0** | 13 | no — a **third** idiom |

**The estate uses at least THREE subcommand-dispatch idioms, and my attributor handled one.** That is
the same shape as every other instrument defect on the record today: *a single-pattern matcher that
silently under-covers and reports a confident number over the fraction it happened to match.* Had I not
checked coverage, "10 MUTATING / 7 READ-ONLY" would have looked like a per-derivation census of the
estate; it is a census of 5 engines.

**So defect 2 stands OPEN and no coverage percentage is derivable from this file.** Closing it needs an
attributor handling all three idioms (`set_defaults`, `args.cmd` if/elif chains, and whatever
`pipeline_cli` uses) — plus a **coverage assertion of its own**: it must report engines-traced /
engines-total and fail loudly rather than silently attributing only what it understood.

## DENOMINATOR GAP against my OWN instrument: comp-which is ABSENT from this census

Surfaced while working the self-route gate: **`comp-which` — the tool Rule 21 makes the mandated first
reflex, ~0.9s/call, 12,147 route events — is NOT in this census at all.** It is `EXCLUDE`d from the
routable `tools_index` set (`comp-which`, `comp-grep`, `comp-glob` are the router and its primitives,
not routing *targets*), so my enumeration-from-the-registry never saw it.

This is the **EXISTS-vs-ROUTABLE axis biting my own instrument**: the enumeration surface does not contain
the tool everyone routes *through*. A latency census that silently omits the single most-invoked tool in
the estate has a denominator gap, and I am recording it rather than leaving it implicit. **The busiest
path is the one most likely to be excluded, precisely because it is infrastructure rather than a target.**

Consequence for Phase 2: the census population must be the registry-derived set **PLUS** the router/
primitive infrastructure (`comp-which`/`comp-grep`/`comp-glob`) measured explicitly — an EXCLUDE from the
*routing* denominator is not an EXCLUDE from the *latency* denominator. And per CTO~Z: `comp-which` is
**CONDITIONALLY-MUTATING** (writes `.comp-graph/which/rank-<pid>.yaml` per call), so any earlier reasoning
that treated it as read-only was a wrong safety classification — moot here only because it was absent.

## THE DISPATCH-IDIOM DENOMINATOR — a TOOLARCH finding independent of LATENCY

Enumerated the idiom space **before** writing handlers (CTO~Z ruling: an attributor whose idiom set is
"the ones I happened to hit" has a denominator sourced from its own encounters). Clustered on observed
signatures across all engines, so an unrecognised shape forms its own cluster rather than vanishing.

**58 distinct engines · 10 DISTINCT DISPATCH IDIOMS** (11 `cmd_`-prefixed · 6 `cmd_`+if/elif on
`args.cmd` · 3 raw `sys.argv[1]` · 3 `cmd_`+`set_defaults` · 3 if/elif · 2 `globals()[...]` · 1
`cmd_`+raw_argv+set_defaults · 1 `cmd_`+dict-dispatch · 1 `set_defaults` alone · 1 click/typer).

**FIVE OF THE TEN ARE COMBINATIONS** — engines dispatching two ways in one file. Design consequence
(ratified by ~Z): the shared resolver must resolve a **SET of signals per engine, not a single label**;
a handler-per-idiom design assuming one idiom per engine mis-attributes half the clusters. That is
precisely the error that would have shipped had handlers been added for the idioms already seen.

**Why this matters beyond this census:** generalising tool creation / registration / testing (Andrew's
charter) is materially harder against 10 idioms than against 3, and **nobody knew which world we were in
until this was measured.** ~Z's prior estimate was 6-7 — the direction of the miss is the interesting
part: *this layer is less uniform than its own architects assume.*

### A CEILING IS NOT A FAILURE RATE

The prior attributor handled `set_defaults(func=)` only, so its **ceiling was 5 of 58 engines (8%)**
regardless of how well it ran — the other 92% were **structurally invisible**, not failing. "Traced
5/53" reads as an instrument underperforming; "could ever have reached 8%" is a different and far more
serious statement. **An instrument failing at 92% shows up as errors; an instrument BLIND to 92% shows
up as a clean run over a small population, reporting high confidence on everything it can see** — the
same anti-correlated shape as the orphan-watcher and the `comp-iam` GREEN. The question to ask of any
instrument is **what its ceiling IS, not what it scored.**

### Bounding: the scare number that was true and would have misled

26 engines showed no dispatch signal — a 45% blind spot, honestly stateable. The discriminating question
was whether those engines *have* subcommands at all: measured `add_parser >= 2` across them = **ZERO**.
All are single-derivation / flag-driven tools where there **is** no dispatch to attribute — "unclassified"
means correct-by-construction, not unattributable. **Real attribution surface: ~32 multi-subcommand
engines, no hidden gaps in the remainder.** The 23 still render explicit `N/A-UNKNOWN` rather than
dropping out of the population.

*Two of my own detector passes disagreed 23 vs 26 on the `cmd_`-prefix convention, neither wrong — the
two-normalizer disease inside one agent, one task, two passes. That it can happen there is the strongest
available argument that it is structural rather than a lane-coordination failure.*

## Next, in order

1. **Per-derivation attribution, all three dispatch idioms** (defect 2, OPEN) — required before
   execution, or the census under-covers with an exclusion set biased toward the high-value reads.
2. Execute the local read-only half under the timebox, with the timing sanity control (sampled re-runs +
   reported variance; a single-shot wall-clock is a sample, not a measurement).
3. AWS half on ~Z's non-serve window signal.
4. Cross-reference **measured vs the DECLARED `cost:` field** in `comp-tools.yaml` — 37 of ~65 tools
   declare a cost, all as **free text** (`<1s`, `~2s`, `~482s full`), so nothing can check it. That
   free-text-ness is already most of the scope-E argument for putting a structured latency class in the
   output contract.
