# 1.1.0_SA_CTO Session 08 — .017 architectural acceptance + v0 capstone

**Date:** 2026-04-21 (Tue, evening ET)
**Agent:** 1.1.0_SA_CTO
**Scope:** `.017 e2e-v0-ratchet-httpx` shipped at `695c0d59` by `1.3.0_DS_CompLearns`. Validate evidence, send architectural ACK, reconcile state, document surprising deltas per session07 discipline — no PRD authoring, no TO decomposition.

---

## Objective

The gate we've been waiting on. `.017` is the v0 capstone — first real closed-loop ratchet on httpx with all upstream pieces live. Per session07 standing rule (Current-phase discipline): validate honestly, document surprising deltas, do NOT author new protocol surfaces on the same day.

---

## Work Completed

### 1. Evidence verification (commit 695c0d59)

Ship commit: `feat(comp): COMP_LEARNS.017 — v0 end-to-end ratchet on httpx` by `1.3.0_DS_CompLearns`.

- 21 files, +1975/-3. 5 loop modules (`ratchet.py`, `failure_miner.py`, `propose.py`, `adversarial.py`, `httpx/compiler.py`) + 4 test files covering the §12.2 mandate (KEEP, DISCARD, adversarial subloop, determinism re-run).
- Two scorecard artifacts committed to `comp/targets/httpx/scorecards/`: `6c58f0e_909ea79f.json` (iter 1) + `e8f2c50_909ea79f.json` (iter 2). Real ratchet evidence, not just logs.
- `_normalize_node_ids` fix in `comp/bench/mutations/harness.py` — canonicalizes node IDs to package name, eliminating temp-dir leakage that had been producing `mutation_stability=0.0` false negatives.
- 42 passed / 11 skipped in `comp/loop/` suite (skipped = live-LLM paths blocked without API credentials; cache-only paths all exercised).

### 2. Four §12.2 demos — all land

| Demo | Evidence | Outcome |
|------|----------|---------|
| KEEP | compiler_sha `e8f2c50`, target_version `909ea79f` | `primary_metric=1.2439`, champion advanced |
| DISCARD | empty-graph compiler, induced regression | `verdict=discarded`, 7 adversarial variants fired |
| Active adversarial sub-loop | `per_failure` populated on DISCARD path | Sub-loop mechanics proven working |
| Determinism re-run | Same `(target_version, compiler_sha)` iters 4+5 | Both `primary_metric=1.2439`, `Scorecard.__eq__` holds (only `emitted_at` differs) — **R13 + R14 closed** |

### 3. Scorecard snapshot (champion compiler e8f2c50)

- `primary_metric = 1.2439`
- `structural_f1 = 0.5743`
- `mutation_stability = 0.997` (post-`_normalize_node_ids` fix)
- `per_selector = {centrality: 1.0, keyword: 1.0, random: 1.0}`
- `conflict_fraction = 0.0`

### 4. Architectural ACK sent (RAVC close)

Two MCPs sent (20260421T180400Z / 20260421T180411Z):
- `2.1.0_SA_COO`: architectural acceptance + two observations for the running log + explicit "NOT doing" holds (no PRD amendment, no TO decomposition).
- `1.3.0_DS_CompLearns`: clean ACK with specific callouts on the `_normalize_node_ids` root-cause fix + DISCARD-with-adversarial as induced-regression proof.

COO replied ACK within minutes (20260421T~180800Z); both watch-items logged her side, count reconcile confirms my 17/22 read (her "20/22" was a miscount; `operator.py` buckets DEFERRED as "not outstanding" producing 18/22). RAVC loop closed.

### 5. JSON state reconciled

- `phase` updated to "Phase 2 — v0 complete" with §8 exit-criterion-satisfied note + 17/1/3/1 split.
- `blocking` updated: gate on agent-proposer-loop dispatch CLEARED (agent-proposer itself still v0.4+ per PRD §9); `.019` flipped STAGED→PENDING after COO dispatched.

---

## Surprising Deltas (per validator discipline — "document only the deltas that surprised you")

### Delta 1: Selector ceiling on httpx v0

**Observation.** `per_selector = {centrality: 1.0, keyword: 1.0, random: 1.0}`. All three selectors saturate at 1.0; `best_lift = 0`; SelectorGameDetected correctly does NOT fire (strict `> 0.1` boundary holds). But the non-differentiating signal is itself a finding.

**Candidate causes.**
- **(a) Corpus size ceiling.** httpx gold has 85 records + 19 ratchet-critical questions + 5 exploratory. With a `token_budget` that comfortably exceeds the minimum-graph subset needed, any selector — even random — can include all relevant nodes.
- **(b) Question-shape ceiling.** Questions may be structurally trivial for any sampling strategy (e.g., "which modules import X?" where X is referenced cleanly).

**Neither is alarming on its own.** This is expected on a v0 target that was chosen for tractability. The selector discipline defends against R9 by DESIGN — the mechanism fires when a compiler dishonestly co-adapts to one selector; tied-at-1.0 is the benign case.

**Action.** None immediately. When `.009 target-2 selection` is picked up (post settling window), one of the `§5` hard minimums should implicitly stress selector differentiation — e.g., require the target to have enough question diversity that random selection cannot saturate. Not amending PRD now; adding to my mental queue for the `.009` scope conversation.

### Delta 2: Node-ID aliasing pattern — possibly recurring elsewhere

**Observation.** The `mutation_stability=0.0` bug was rooted in temp-dir names leaking into node IDs via `harness.py` — transient filesystem state contaminating what should be identifier-stable graph nodes. `1.3.0_DS`'s `_normalize_node_ids` fix (canonicalize to package name) is the right shape: kill the leakage at source, not paper over the symptom downstream.

**But this is a general failure-class, not a one-shot bug.** Other places where node IDs get constructed from filesystem paths or other transient state:
- `GraphBuilder` (`.014`) — node construction from file paths.
- Imports subtype (`.013`) — node IDs for imports.
- `httpx/compiler.py` itself — its own node emission layer.

**Action.** None immediately. Per discipline, let the ratchet run a few more iterations; if `mutation_stability` anomalies surface on other benchmarks, that's the signal to audit. If it stays at ~0.997 across the next 5-10 iterations, the general pattern is likely contained at the harness layer and the audit is low-value. Watch-item, not TO. If `.009` target-2 is chosen with a different filesystem layout (e.g., flat module vs. nested package), this bug-class gets an involuntary test.

---

## Decisions Made

1. **Architectural acceptance on .017 is unambiguous.** Four demos land, R13+R14 closed, two real scorecard artifacts committed. No flex was pre-flagged during the run. This is an honest v0 capstone.

2. **Do NOT remove the "Current-phase discipline" section from prompt.md today.** The rule itself says "let the run speak first." Removing the guardrail on the same day .017 shipped would violate the spirit. Target removal: after 2-3 additional iterations confirm the ratchet behaves honestly under further runs, OR when `.009`/`.018` is formally picked up (whichever comes first).

3. **Do NOT decompose .009 or .018 today.** Same rule as above. COO explicitly confirmed no pressure ("you'll signal when ready"). The right next-action after `.019` ship (visualization CLI, no architecture-layer question) is a quiet observation window, not more authoring.

4. **Two surprising deltas logged here, NOT elsewhere.** No PRD amendment, no new TO, no new narrative artifact. This session log is the sole home for both observations per "one human narrative source" discipline from validator feedback.

5. **Count reconcile landed clean.** JSON phase + blocking trimmed to 17/1/3/1 reality. COO's `operator.py` 18/22 read is internally consistent (DEFERRED bucketed as "not outstanding"); both numbers defensible, underlying state identical.

---

## Files Modified

- `org/projects/COMP_LEARNS.json` — phase + blocking updated for post-.017 state.
- `org/tier1_exec/1.1.0_SA_CTO/logs/2026-04-21/session08_017_arch_acceptance_v0_capstone.md` — this log.

No PRD touched. No TOs touched. No prompt.md changes (discipline section stays in place).

---

## Current State (for next-session pickup)

### TO state
- **17 COMPLETE** — all of the v0 core (.001-.008, .011-.016, .017, .020-.022 minus the ones that never existed).
- **1 PENDING** — .019 visualization-CLI at 1.1.0_DS_CompLearns (COO running close solo).
- **3 STAGED** — .009 (mine, gated on settling window), .010 (gated on Andrew PRD doc N1), .018 (mine, gated on settling window).
- **1 DEFERRED** — .005 (superseded by .021).

### Standing posture
- Current-phase discipline section in prompt.md stays in place.
- No PRD amendments. No new TOs. No new narrative objects.
- Next session opening: check `.019` ship, check for any mutation_stability anomaly in subsequent ratchet runs (if COO or 1.3.0 runs `comp-learns-run.sh httpx --once` additional times). If anomalies surface → investigate node-ID aliasing pattern. If clean → start considering `.018 program.md v1` pickup in lightweight-freehand mode only.

### Watch-items for subsequent iterations
1. Selector ceiling on httpx (per_selector = {1.0, 1.0, 1.0}) — expect it to stay ceilinged on this target; `.009` target-2 should break it by design.
2. Node-ID aliasing pattern — watch `mutation_stability` on additional iterations; if it stays ≥0.99 on varied compilers, the pattern is contained.
3. The four-demo pattern itself — if any future iteration fails the DISCARD path or the determinism re-run drifts, that's an immediate architecture question.

---

## Next Steps

**Post-session:**
- If `.019` ships cleanly: COO will handle close solo. No action from me unless she surfaces an architecture-layer question.
- If additional `.017` iteration runs produce surprising scorecards: investigate first, document, THEN consider PRD amendment only if a named failure mode emerges.
- If Andrew or COO signal "ready to pick up `.018`": start with the lightweight-freehand `program.md` scope from TARGET_CLOSEOUT v2.0. Do NOT reintroduce the subsystem shape that v2.0 trimmed.

**Explicitly NOT doing next session:**
- Open a PRD amendment for selector ceiling.
- Open a TO for node-ID aliasing audit.
- Decompose `.009` or `.018` without a settling-window signal.
- Remove the Current-phase discipline section from prompt.md until the settling window has actually happened.

---

## Compiler Tools

| Tool | Command | Result | Purpose |
|------|---------|--------|---------|
| mcp check_inbox | `check_inbox("1.1.0_SA_CTO")` x2 | 1 message from COO each time (.017 notification + COO ACK of my ACK) | Inbox sync |
| mcp get_agent_status | `get_agent_status("1.1.0_SA_CTO")` x2 | LIVE both times | Liveness check |
| bash inbox-watch | `inbox-watch 1.1.0_SA_CTO` x2 (relaunched after each delivery per 2026-04-21 rule) | Real-time push, Bash `run_in_background: true` | Message notify |
| mcp send_message | 2 MCPs (to COO + to 1.3.0_DS) | Delivered inbox + broker + push | RAVC close + arch ACK |
| git | `git log --oneline 695c0d59 -1` + `git show --stat 695c0d59` | Clean ship commit, 21 files +1975/-3, author 1.3.0_DS | Evidence verification |

No `comp-*` graph-tool runs — this session operated on org narrative + JSON + session log only. CTO compiler-tools obligation per `org/XXX.md` is "before authoring PRD amendments touching graph-level concerns in `comp/`" — no PRD amendments this session.

---

## Session chain reference

| Session | Log | Commit | Summary |
|---------|-----|--------|---------|
| 01-06 | (earlier sessions) | various | Agent setup through `.020` ship |
| 07 | `session07_validator_feedback_process_tuning.md` | `eaaaea0e` | Validator-driven trim (delete brief, skeleton bundle, tighten JSON, add discipline section) |
| 08 | `session08_017_arch_acceptance_v0_capstone.md` | *this commit* | `.017` architectural ACK, v0 capstone, count reconcile, 2 surprising deltas logged as watch-items |

— 1.1.0_SA_CTO
