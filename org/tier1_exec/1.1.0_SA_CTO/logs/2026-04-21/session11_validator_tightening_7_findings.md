# Session 11 — Validator tightening pass, 7 findings

**Date:** 2026-04-21
**Agent:** 1.1.0_SA_CTO
**Principal:** Andrew
**Predecessor:** session10 (hardcore audit, commit `04f85f18`) — closed 3 unwired-guard gaps.
**Trigger:** GPT validator review of session10 audit artifact returned 7 open findings.

## Objective

The session10 audit declared "architectural integrity verified." A follow-up
validator pass (GPT) found the audit itself was incomplete across 7 axes —
some mechanical (untracked artifact, missing schema fields), some substantive
(authoritative-path split, mock-judge contamination, silently-broken cache
key, incomplete compare, insertion-order selector attribution).

Close every one with code-level evidence. The session10 "verified" claim was
too strong; this session restores it.

## Validator findings + resolutions

| # | Severity | Finding | Resolution | Evidence |
|---|----------|---------|------------|----------|
| 1 | CRITICAL | `comp-learns-run.sh` default path is `comp.framework.run` legacy loop, not ratchet. Operators silently run the wrong eval model. | Quarantined — bare invocation exits 2 with message; `--once` (ratchet) or `--legacy` (old loop, deprecated) now required. | `comp/bin/comp-learns-run.sh` quarantine block; live check: bare invocation exits 2. |
| 2 | CRITICAL | `iterate._main` always used `GoldAwareMockJudge`. Scorecard + experiment_log don't record judge identity, so "kept iter 6" at primary_metric=1.2439 is indistinguishable from real eval. | Added `--judge mock\|real` CLI; `real` selects `AnthropicJudge` (requires `ANTHROPIC_API_KEY`). `Scorecard.judge_model_id` surfaces in output + experiment_log `extra.judge_model_id`. Mock mode prints DEMO-ONLY warning. | `comp/loop/ratchet.py::_main`; live scorecard `13254d0_909ea79f.json` shows `"judge_model_id": "gold-aware-mock"`. |
| 3 | CRITICAL | Cache-key `source_hash` computed from `target_root / "compiler.py"` where `target_root = target_dir/_repo/target`. Actual compiler at `target_dir/compiler.py`. `_source_hash()` silently returned `"no-compiler"`. | Added `compiler_py_path: Optional[Path]` kwarg to `iterate()`; `_main` passes `target_dir/compiler.py`. In-memory compiler_fn tests (no path) still use the `"no-compiler"` fallback. | `comp/loop/ratchet.py::iterate` lines 215-220; live run wrote 57 new cache entries — prior entries keyed under `"no-compiler"` are now orphaned, proving the fix takes effect. |
| 4 | HIGH | Champion compare used only `primary_metric`. `Verdict.TIED` updated `champion.json` anyway. `tiebreak_structural` + `tiebreak_loc_delta` helpers in `primary.py` were unused. | Implemented full three-key compare in `iterate()`: `primary_metric → structural_f1 → -compiler_loc`. TIED no longer updates champion. `_save_champion` now writes `structural_f1` + `compiler_loc`. | `comp/loop/ratchet.py::iterate._compare`; live iter 8 with same compiler as iter 7 correctly returned `verdict=tied`, champion unchanged, `delta=0.0 loc_delta=0`. |
| 5 | HIGH | `ab.run` used `max(per_selector.items(), key=lift)`. On ties, Python returns first inserted — `random` (default selector order). Scorecards logged misleading `best_selector="random"`. | Replaced with `sorted(items, key=(-lift, name))`. Alphabetical tie-break → `centrality < keyword < random`, so structured selector wins attribution at ceiling. Added `DownstreamAB.tied_at_best: bool` flag for honest readers. | `comp/bench/ab.py::run`; live scorecard shows `best_selector="centrality"` + `tied_at_best=true` (was `"random"` pre-fix). |
| 6 | MEDIUM | Session10 referenced `protocol_briefing_comp_learns_target_execution.md` as authoritative, but the file was `??` (untracked) — no stable hash for audit. | Committed at `64eee063`. | `git log` shows commit 64eee063. |
| 7 | MEDIUM | `ExperimentEntry` schema missing `delta` + `loc_delta` fields (architecture §7.4 line 700). | Added both fields with sensible defaults; `iterate()` writes `delta = cand.pm - champ.pm` and `loc_delta = cand_loc - champ_loc`. | `comp/loop/experiment_log.py`; live iter 8 entry: `"delta": 0.0, "loc_delta": 0`. |

## Live end-to-end verification

```text
$ comp/bin/comp-learns-run.sh httpx --once
[comp-learns-run] --once mode: single ratchet iteration for target=httpx (judge=mock)
[ratchet] target=httpx iter=7 compiler_sha=13254d0
[ratchet] target_version=909ea79f63e9c016... judge=mock model=gold-aware-mock
[ratchet] WARNING: mock judge -- selector lifts are DEMO-ONLY, not real A/B signal
[ratchet] verdict=kept primary_metric=1.2439
```

Iter 7 scorecard (extracted fields):

```json
{
  "compiler_sha": "13254d0",
  "judge_model_id": "gold-aware-mock",
  "compiler_loc": 34,
  "best_selector": "centrality",
  "tied_at_best": true,
  "primary_metric": 1.2439089035347553
}
```

Iter 8 re-run (same compiler):

```json
{"iter": 8, "verdict": "tied", "delta": 0.0, "loc_delta": 0,
 "extra": {"best_selector": "centrality", "tied_at_best": true,
           "fork_reason": "", "judge_model_id": "gold-aware-mock"}}
```

Champion unchanged (iter 7 is authoritative). Bare invocation:

```text
$ comp/bin/comp-learns-run.sh httpx; echo exit=$?
ERROR: bare `comp-learns-run.sh <target>` is ambiguous. [...]
exit=2
```

## Tests

`pytest comp/ --ignore=comp/targets/httpx/_repo` — **328 passed**.

No test additions needed this session: scorecard serialization round-trip was
already covered, existing selector/fork tests still pass under the new tie-
break logic (they use single-winner configurations). Backward-compat defaults
on new fields mean pre-existing scorecards and experiment_log entries still
deserialize.

## Files changed

Code:
- `comp/bench/scorecard.py` — `DownstreamAB.tied_at_best`, `Scorecard.judge_model_id`, `Scorecard.compiler_loc`, serialization.
- `comp/bench/ab.py` — deterministic sorted tie-break.
- `comp/loop/ratchet.py` — `compiler_py_path` kwarg, `_compiler_loc` helper, `_save_champion` F1+LoC, full three-key compare, `Verdict.TIED` no-update, `judge_model_id` propagation, `--judge` CLI, delta+loc_delta logging.
- `comp/loop/experiment_log.py` — `delta` + `loc_delta` fields + serialization.
- `comp/bin/comp-learns-run.sh` — quarantine block, `--legacy` opt-in, `--judge` flag propagation.

Live-run artifacts (demo-only, flagged in-file via `judge_model_id`):
- `comp/targets/httpx/scorecards/13254d0_909ea79f.json` (new)
- `comp/targets/httpx/champion.json` (updated — now carries F1 + LoC)
- `comp/targets/httpx/experiment_log.jsonl` (2 new entries, iter 7 + 8)

Audit-artifact commit (earlier this session):
- `org/tier1_exec/1.1.0_SA_CTO/logs/2026-04-21/protocol_briefing_comp_learns_target_execution.md` committed at `64eee063`.

## Decisions + non-decisions

**Decision: tie-break is alphabetical, not structured-preference-weighted.**
Alphabetical by selector name gives `centrality < keyword < random` which
happens to match structured-over-random preference, but the reasoning is
"deterministic + simple" not "weighted toward structure." If a future selector
name violates this coincidence (e.g. `z_structured`), we revisit with a named
ordering.

**Decision: `compiler_py_path` is optional kwarg, not required positional.**
Tests use in-memory `compiler_fn` callables with no file. Keeping the param
optional with None default preserves test backward-compat; the `"no-compiler"`
fallback is explicitly safe for those tests and is not reached by `_main`.

**Non-decision: multi-iter ratchet driver.** Validator #1 suggested either
flipping default to ratchet or quarantining legacy. I chose quarantine because
the ratchet only has `iterate()` (single iter) — a looping driver with kill
switch + budget + plateau is a separate PRD. Quarantine closes the "silently
wrong path" hole without blocking that future PRD.

**Non-decision: backfill iter 1-6 experiment_log with delta/loc_delta.**
Those entries are pre-fix, pre-schema. Leaving them at default 0.0/0 is
honest — they predate the schema and shouldn't pretend otherwise. Iter 7+
use the new schema.

## Residual gaps (acknowledged, out of scope)

1. **No real-judge iteration has ever run.** `--judge real` is wired but
   untested end-to-end. First real run will surface provider-rate-limit and
   answer-format gaps that the mock hides.
2. **Champion F1 + LoC for iter 1-6** weren't recorded; iter 7 won KEEP on
   the F1 tiebreaker against a phantom `champ_f1=0.0, champ_loc=0` champion.
   Transient; iter 8 with recorded F1/LoC returned TIED correctly.
3. **LoC counting is line-count, not non-blank non-comment.** Fine for
   relative-delta tiebreaker but won't match other LoC tools.

## What the validator should now see

- Every CRITICAL finding closed with code + live-run evidence.
- Every HIGH finding closed with behavior change visible in iter-7/iter-8
  diff of scorecard + experiment_log.
- Both MEDIUM findings closed (commit hash + schema fields).
- Session10's "verified" claim was overreach. Session11 replaces it with
  verified-on-7-axes plus an explicit residual-gaps list.

## Compiler tools used

None this session — changes are all within `comp/` package boundary; no blast
radius into Lambda/EC2/portal. `grep`/`Read` only.
