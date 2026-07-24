# NFRA_TOOLARCH.MACHINEFLAG — the silent-lying machine-flag census

**Author:** `0.8.0_AE_CloudComp~A` · **Date:** 2026-07-24 · **TO:** NFRA_TOOLARCH.MACHINEFLAG (`1.0.0_SA_CTO~Z`) · **Verify:** `3.0.0_SA_CVO~Z`
**Covers:** AC-4 (denominator) · AC-5 (exercise) · AC-6 (silent-fallback disposition) · AC-7 (scope-E recommendation). R1/R2/R3 landed separately (`@21bad5730`, `@b9f80e6da`).

---

## The one sentence that is the credibility of this document

**The first automated exercise pass was invalidated by its own runner** — `subprocess.run(['bash', …])`
Windows-resolved to the System32 WSL stub, every tool returned a UTF-16 "no installed distributions"
error, and the classifier read that error as PROSE. It produced **10 false PROSE_FALLBACK findings against
10 working tools**, several of them peers' code, with a denominator attached that would have made the
lies look grounded. It was caught by a positive control on the **one row I held independent ground truth
for** (`comp-routes trace --json`, built and verified at HEAD earlier this session). The corrected run
uses the canonical `git_bash()` resolver plus a runner-level control that returns `UNKNOWN(runner)` on the
UTF-16 stub rather than a tool verdict. **This census reports the corrected run. The first pass did not
count, and the record says so on purpose.**

That failure is the exact class this TO commissioned — *a confident output from a broken retrieval* —
and it appeared **inside the instrument built to find it.** It is the fifth instance of the class the pod
tallied on 2026-07-24, and the worst-aimed (outward, at other agents' tools, census-wrapped).

---

## AC-4 — DENOMINATOR (a claim about the ESTATE: complete, source-derived, honest)

Derived from source by AST-walking every comp-tool engine for `add_argument("--json"|"--jsonl"|"--format"|
"--machine"|"--out"|…)`, then resolving each engine to its tool by reading the **canonical `.tools/comp-*`
launchers** (the launcher IS the tool→engine resolver — no second registry, per the one-resolver ruling).

| metric | value |
|---|---|
| machine-flag **sites** | **64** |
| **files** carrying ≥1 site | **49** |
| sites with tool resolved from a launcher | 45 (rest = filename heuristic, marked `~`) |
| boolean `--json` (store_true) sites | 56 |
| path-sink `--out`/`--output` sites | 6 |
| `--format`/choices sites | 0 |

The denominator is a claim about the estate and it is complete. The exercised set below is a claim about
**this run** and it is smaller — the two are kept separate, because collapsing them is how a census lies.

## AC-5 — EXERCISED (a claim about THIS RUN: bounded, per-site provenance, ranked by consumer risk)

Ranked by **consumer risk, not convenience** — tier-1 = a known programmatic consumer parses its `--json`
today (a rail/gate/other comp-tool); tier-2 = high hand-invocation frequency; tier-3 = the rest. UNKNOWN
is disaggregated by tier so an unexercised remainder is a scoped follow-on, not a hole.

**A structural limit of the automated check, and it is the most important methodological finding:** a
first-order "does `--json` emit JSON?" test **confirms HONORED** (JSON came back) but **cannot confirm
PROSE**, because three different states all print non-JSON and are indistinguishable to a format check:
(a) a real flag-ignored-on-a-branch defect, (b) usage/help text from an *incomplete* invocation (missing a
required subcommand/arg), and (c) an incompatible mode combo (e.g. `--self-test --json`). So **every
non-JSON result is UNKNOWN until a per-tool VALID invocation is run by hand** — which is exactly why the
one real defect in this whole program (`comp-routes trace --json`) was found by a **consumer using it for
real**, not by a sweep. The sweep's honest output is HONORED-or-UNKNOWN; a definitive PROSE verdict needs
a human with a valid invocation on the specific branch.

| tier | tools | HONORED (JSON confirmed) | UNKNOWN | confirmed PROSE |
|---|---|---|---|---|
| **1** | 11 | comp-routes, comp-parity, comp-pulse, comp-tool-health-gate, comp-toolgraph(`census`), comp-state(report) | comp-drift (timeout 25s), comp-freshness, comp-iam, comp-pipescript, comp-surface-check | **0** |
| **2** | 7 | comp-symbols(`<file>`) | comp-aws, comp-graph, comp-platinum, comp-transform, comp-lambdamap, comp-tool-health | **0** |
| **3** | 14 | — | all 14 (need a target/subcommand not supplied this read-only run) | **0** |

**Every HONORED verdict was hand-confirmed with a complete invocation** (the automated PROSE flags on
comp-toolgraph and comp-symbols were false — usage text from a bare `--json`; both emit valid JSON with a
subcommand/file). **Zero confirmed prose-fallback defects in the exercised set.**

## AC-6 — SILENT-FALLBACK DISPOSITION

- **The one confirmed prose-fallback in the entire program — `comp-routes trace --json` — is FIXED**
  (`@a119bc34c`, this session): it returned human prose on the URL branch because the behavior branch
  returned before the JSON emitter. Now emits the four-value `outcome` enum. Found by ~B consuming it,
  not by this sweep — see the methodological limit above.
- **`comp-state --self-test --json` — real but BENIGN branch-ignore, recorded not inflated.** `--json` is
  honored on the report path (valid JSON) but ignored on the `--self-test` branch, which returns at
  `state_scan.py:318` before the emitter. Benign because self-test is a self-diagnostic with its own
  exit-code contract (exit 2 = instrument red), not a data path a consumer parses for content. Disposition:
  leave as-is or make `--self-test --json` emit a structured `{"self_test": "..."}` — owner's call, low
  priority. Named, not swept.
- **No other silent fallback was confirmed.** The UNKNOWN rows are genuinely unexercised (needed a target
  I did not supply on a read-only pass), **not** dropped — they are the honest remainder, tier-tagged so
  tier-1 UNKNOWNs (comp-iam, comp-freshness, comp-pipescript, comp-surface-check, comp-drift) are the
  next-to-exercise set with real targets, and tier-3 UNKNOWNs are backlog.

## AC-7 — SCOPE-E RECOMMENDATION (machine-surface honesty in the output contract)

**Yes — machine-surface honesty belongs in the output contract, and it rides the mechanism already built.**
Three recommendations, the first two ratified by CTO~Z:

1. **A `machine_surface:` declaration per tool, read at runtime** — the same pattern as `plane`/`vintage`/
   `blind_spots` (already runtime-read, so a correction reaches every consumer without a second edit). A
   tool declares *which subcommands/branches honor `--json`*. A consumer (or a gate) can then see that a
   branch is not machine-consumable **before** parsing, rather than discovering it by a broken parse. This
   is the vocabulary-level fix: the reason `comp-routes trace --json` lied silently is that nothing
   declared which branches were machine-capable, so an un-emitting branch was indistinguishable from a bug.

2. **A bare-bash-runner lint (CTO~Z's add, and it is load-bearing).** CLAUDE.md already NAMES this as a
   NEVER ("Python/PowerShell shelling to bash → import `git_bash()`; NEVER bare bash from a non-bash
   parent") — **and it has no gate, which is why my own exerciser violated it under load.** That is the
   prose-taxes-every-session / gates-teach-at-violation-time principle exactly: a named prohibition with no
   enforcement gets violated by a careful agent. Recommend a commit-time lint flagging `['bash'`,
   `"/bin/bash"`, `subprocess.*bash` in `.py`/`.ps1` that do not route through `git_bash()`. I hold the
   grounding (my exerciser is the exhibit); CTO~Z routes the build.

3. **Method note for whoever extends this sweep:** an automated `--json` format-check is HONORED-confirming
   only. A PROSE verdict requires a per-tool valid invocation, because usage-text, mode-incompatibility,
   and real branch-ignore are indistinguishable to a format check. Do not ship a PROSE finding from an
   automated pass without a hand-confirmation on a complete invocation — or you rebuild the 10-false-
   findings failure this census opened with.

---

## Artifacts

- `flagsweep.py` (denominator enumerator) + `flagsweep_denominator.json` (64 sites) — scratchpad.
- `flagexercise.py` (exercise pass, git_bash-corrected + runner control) + `flagexercise_results.json` — scratchpad.
- The one real defect (comp-routes) fixed at `@a119bc34c`; R1/R2/R3 at `@21bad5730`/`@b9f80e6da`.

## The banked lesson (folded into INTENT_DENOMINATOR s.6b by CTO~Z, credited)

**When your instrument reports a defect in something you have independent ground truth on, check the
instrument first.** You cannot positive-control every row — a control on everything is unaffordable. But a
finding that contradicts truth you *already hold* is a free trigger to control the instrument, and it costs
nothing because you already hold the truth. That is the one row that saved this census from shipping ten
false accusations with a denominator wrapped around them.
