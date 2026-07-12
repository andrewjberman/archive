# NFRA_LIVELEARN -- Standup Brief

**From:** 0.8.0_AE_CloudComp (tool-owner: the wire `comp_tool_health.py` + the TH-A probe `compproof/tool_probe.py`)
**To:** 1.0.0_SA_CTO (project standup + PRD ownership + arch gates)
**Date:** 2026-07-12 | **Ground vintage:** @ 5b222a6e5 / working-tree

## Andrew-direct instruction (verbatim)

> "create a dedicated project for finalizing this. NFRA_LIVELEARN. PRD should cover the build and validation
> end to end through a few cycles which can be done over the session."

"this" = the mechanical+holistic tool-quality learning loop -- the EFFECTIVE quality-sensor landed under your
3-PRD keystone (NFRA_TOOLPASS.md CYCLE-29/30). I own the two components, so this is the technical
what-needs-to-happen; the PRD authorship, project standup (docs/architecture is ANY_CTO-gated), and per-cycle
gate are yours.

## What is already TRUE (grounded, OBSERVED)

1. **SENSOR live-by-default.** `comp_tool_health.main()` reads `compproof/effective_feed.json` by default
   (`comp_tool_health.py:757-758`); the wire is a PURE REDUCER (`_effective_to_bool:367`, `load_effective_feed:383`)
   -- it reads the produced `effective`, never computes it. VOID/unknown stays EXPLICIT, never a silent False (`:380`).
2. **Loop validated end-to-end on real tools.** `classify_full:127` flips KEEP<->FIX purely on the EFFECTIVE axis
   (`:159`/`:168`, the load-bearing FIX); `--self-test` check (9) exercises that flip on a LIVE pending-KEEP tool.
3. **4 of ~63 tools quality-scored** (`effective_feed.json`): comp-which=no, comp-freshness=no (-> FIX);
   comp-iam=yes, comp-aws=yes (-> KEEP). Each `effective` cites an EXERCISED `oracle_run` (FP-R0 reach corollary),
   oracle grounded OTHER than the tool (frozen-vs-fresh S3 content, simulate-principal-policy, hardcoded-garbage class).
4. **Sovereign-safe by construction.** `tool_corpus.assert_sovereign_safe:233` fails the corpus LOAD on ANY held
   bd/schwab target (run argv, scratch uri, or IAM ARN). Scratch is fixed-key OVERWRITE at
   `s3://opal-data-inf/_toolprobe_scratch/` -- write, never delete (respects the S3-delete human-confirmation rule).

## The 3 gaps that make it NOT yet "finalized" (why the PRD exists)

- **G1 -- REFRESH not wired.** `ensure_fresh()` EXISTS (`tool_probe.py:775`: reuse-if-<=7d-else-run-then-read;
  your consumption-driven trigger, 2026-07-06) but **no consumer calls it**. The wire reads the committed JSON
  directly (`:757-758`), so a consumer reading a >7d feed gets STALE effective data with no refresh and no
  staleness banner. Design intent is fresh-when-consumed; today it is a static snapshot. (Zero cron BY DESIGN --
  confirmed: `grep tool_probe|effective_feed` across `infra/aws/terraform` + `.tools` + `.github` = 0 hits.)
- **G2 -- COVERAGE 4/~63.** The other ~59 tools read KEEP?/FIX?/RETIRE? (pending EFFECTIVE) on the 2 live axes
  only. Honest, but the quality sensor actually SEES only 4 tools.
- **G3 -- LOOP-CLOSURE not yet demonstrated.** No tool has gone FIX -> (fix applied) -> re-probe -> KEEP in the
  live feed. comp-freshness is the natural closer but is HELD until post-07-14 (cot-clarity + fresh dry-run), so
  closure must not depend on it (or that one AC defers).

## Proposed shape -- a few build+validation CYCLES, each doable this session

Each cycle is self-contained and leaves a `NFRA_TOOLPASS.md` CYCLE entry (continues the CYCLE-30 ledger):

- **CYCLE A (REFRESH wire) -- closes G1.** Wire `ensure_fresh` (or a feed-age staleness banner + `--refresh`)
  into `comp-tool-health` / `comp-learns-status` so the read is fresh-when-consumed. Validate: aged feed ->
  consumer re-runs (or loudly flags); fresh feed -> reuse. Small, high-leverage, no live-estate risk.
- **CYCLE B (COVERAGE batch 1).** Author class-representative probes for ~6-10 more tools (isolation-gated,
  sovereign-safe, inf scratch), exercise live, emit `effective_feed`, verify each verdict via the flip-test +
  a positive control. First real coverage jump.
- **CYCLE C (COVERAGE batch 2 + CLOSURE) -- closes G3.** Another batch, AND demonstrate one full loop closure
  (FIX -> fix -> re-probe -> KEEP). Candidate: the comp-freshness partition-key defect-b (`23a7be2a1`) if
  unblocked; else a smaller in-lane tool whose fix is same-session.
- **(Optional CYCLE D).** Coverage to a target %; ARCH RULING on the standing refresh cadence
  (consumption-driven vs a scheduled sweep) -- your call, it is an architecture decision, not mine.

## Acceptance criteria (end-to-end validated + running)

- **AC1 fresh-when-consumed:** a stale feed triggers refresh-or-loud-flag before a verdict is read (G1, exercised).
- **AC2 coverage:** >= N tools carry an EXERCISED `effective` (propose N >= 15 this session), each w/ a positive control.
- **AC3 flip integrity:** every newly-scored tool: `effective=no -> FIX`, `effective=yes -> KEEP` in the LIVE query
  (not merely `--self-test`).
- **AC4 loop closes once:** >= 1 tool demonstrated FIX -> fix -> re-probe -> KEEP in the live feed.
- **AC5 honesty rails hold:** unknown never silent-False; every `effective=yes` cites an exercised `oracle_run`;
  the sovereign LOAD-assert is green on every run.

## Scope / guards (non-negotiable)

Sovereign: inf/cot/mdpf ONLY -- never bd/schwab/49F (`assert_sovereign_safe` enforces at load). No vendor APIs.
S3 = overwrite-only, no delete. Every exercise isolation-gated (author != solver != judge; sealed answer stripped
from the tool payload -- `strip_gate:86`).

## Division of labor

- **You (1.0.0_SA_CTO):** own the PRD + project standup + the arch ruling on refresh cadence (G1); gate each cycle diff.
- **Me (0.8.0_AE_CloudComp):** build + exercise every cycle in my lane (`org/modules/graph/compproof` + the wire),
  report each diff for your gate. I can start CYCLE A immediately on your GO.
- **CVO (optional):** negative-control audit on the flip-tests / coverage probes (a second pair of eyes, as on the
  keystone).

Everything above is one-step-from-ready; the only thing gating CYCLE A is your standup + GO.
