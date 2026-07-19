# COMPRAIL Gate-1 (broad-repo-grep DENY) -- FP-rate measurement FINDING

**Author:** 0.8.0_AE_CloudComp~Z | **Date:** 2026-07-19 | **For:** 2.0.0_SA_COO + 3.0.0_SA_CVO~B (the joint hold-owners) | **archetype:** VALIDATE
**DISPOSITION: PRESENT, DO NOT ARM.** This is the evidence the Gate-1 forward-GO wants; producing it is NOT satisfying the hold. The arming decision (flip `org/mcp/comprail-gate1.enforce`) rests with COO + CVO~B (or Andrew) -- the lane that generates the evidence does not get to be the actor (COMPASSURANCE TO-5 fence).

## Question

Should the estate-scoped broad-repo-grep DENY (COMPRAIL Gate-1, `a62b63e46`, built default-OFF) be armed? The prior NFRA_COMPRAIL measurement was **"27 governed-grep events, ~4% FP -> DATA-INSUFFICIENT"**; the hold was placed on insufficient data. Re-measure on the grown log.

## Method (READ-ONLY -- no marker toggle, no hook invocation, no rail pollution)

Source: `org/mcp/comp-tool-hud.log` (the `HUD-HIT` log, `comp-tool-hud.sh:261` -- the "CVO before/after measurement" log). **NOT `comp-which-rail.log`** (that carries only `DENY` + `RUN-OVERRIDE`; a staged-OFF Gate-1 broad-grep never denies, so it lands as a `HUD-HIT class=comp_which` row here instead). Applied the Gate-1 predicate (`comp-tool-hud.sh:216-218`) in-process; de-contaminated the fixture replays; printed the population.

## Result (denominators printed, per Rule 22)

| | count |
|---|---|
| `class=comp_which` HUD-HITs (broad-search universe) | **5811** |
| Gate-1-GOVERNABLE (recursive grep/rg/find, estate path, non-pipe) | **22** |
| ... fixture/self-probe replays (comprail-gate1-fptest.sh) -- STRIPPED | 5 (all `grep -rn compute_aua data/bd/scripts/`) |
| **REAL agent governable events** | **17 (17 distinct)** |

## Findings

1. **STILL DATA-INSUFFICIENT.** 17 real governable events vs the prior 27 -- comparable, NOT dramatically grown. By the same standard that deemed 27 insufficient, 17 does not clear the bar. The total log grew 3-4x, but the *governable* subset did not.

2. **The governed class is STRUCTURALLY RARE: 17 / 5811 = 0.3% of the broad-search universe.** Estate-scoped standalone recursive searches almost never happen -- agents comply with the rail, pipe-grep (`cmd | grep`, exempt), grep non-estate paths, or use comp-tools. **This is the load-bearing fact: the FP RISK of arming is small because the class barely fires -- but the same rarity makes the FP RATE unmeasurable-with-confidence by passive observation.** The two cut against each other.

3. **The population is `find`-dominated, not `grep -r`.** ~13 of 17 are `find` (file-LOCATION, redirect target = comp-glob), not `grep -r` (content, comp-grep). Whether Gate-1 should govern `find` at all is a design question: `find infra/aws/lambda -name "*.py"` -> comp-glob is a reasonable redirect, but it is a different intent than content-search.

4. **~half are COMPOUND DIAGNOSTIC one-liners** (`echo "===" && find ...`, `cd ... && find`, `ls infra/aws/ && ... find`) where a DENY would be friction on a quick diagnostic, not a redirect to a richer tool. Plus at least 2 my log-only predicate OVER-CAUGHT (a `git check-attr ... infra/...` git op; a `find org/mcp/inbox -name ... -exec cat` that is NOT estate-scoped). **So the TRUE governable set is likely SMALLER than 17.**

5. **A PRECISE FP rate is not cleanly obtainable from the passive log.** My predicate is a log-only approximation: it (a) under-counts (the hook checks `$query $gpath`; the log has only truncated `q=`, not `gpath`) and (b) over-catches (compound diagnostics, git ops, non-estate finds). The TRUE per-event Gate-1 decision needs replaying each command through the live hook (marker ON) -- which I did NOT do: it toggles the REAL `comprail-gate1.enforce` marker (leak risk) and writes DENY rows (rail pollution). A clean replay harness over arbitrary commands is a BUILD, not this measurement -- flagged, not done.

## Recommendation (a FINDING for COO + CVO~B -- I do not arm)

The passive-observation data does **not** resolve the data-insufficiency (17 ≈ 27), and it will likely **never** by passive observation (the class is 0.3%-rare). So the arming decision does not turn on a measured live FP rate -- there isn't enough traffic to measure one. It turns on a choice between:

- **(a) Arm on the low-blast-radius + fixture-pass argument.** The class fires ~0.3% of searches; the fixture FP-test (`comprail-gate1-fptest.sh`, AC#5 PASS) already proves the DECISION logic is correct on its designed cases (no false-deny on generic/no-graph/pipe/single-file/override; denies the intended estate broad-grep); the `# rail-checked` override + `/freeform` are always available. Residual risk is bounded by rarity. BUT: my sample shows ~half the real events are compound diagnostics where a DENY is friction -- so tightening the predicate (exclude compound commands / `find`-only / git ops) before arming would cut that friction.
- **(b) Hold as data-insufficient indefinitely** -- honest, but then the hold never lifts by this path; the "data-sufficient" bar is unreachable by passive observation and should be retired or replaced (e.g., a bounded announce-period with override-rate telemetry, or accept (a)).

**My read (advisory only, not a decision):** the measurement's real value is finding #2 -- the class is structurally rare, so "measure the live FP rate" was never going to converge. That reframes the call from "is the FP rate low enough?" to "is the low-blast-radius + fixture-pass + override-escape enough, possibly after tightening the predicate to drop compound-diagnostic/`find` over-catches?" That is a COO + CVO~B (or Andrew) judgment, not mine. **Not armed; `comprail-gate1.enforce` untouched.**

Raw population + method reproducible: `comp-tool-hud.log` + the read-only extractor (scratch). All 17 governable strings are in the log (`grep 'class=comp_which' org/mcp/comp-tool-hud.log`).
