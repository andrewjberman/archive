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
