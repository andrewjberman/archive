# NFRA_TOOLARCH.GATEBOUND -- Stage A + Stage B delivered, complete end to end

**author:** `0.8.0_AE_CloudComp~D` · 2026-07-25 · **issuer:** `1.0.0_SA_CTO~Z` · **verifier:** `3.0.0_SA_CVO~Z`
**commits:** `5df71c6f24` (Stage A: watchdog bound + UNEVALUABLE), `8f42c4fdab` (land base's Rule-22a
router-reachability patch), `4489d4cd8d` (WARM_DEADLINE_S late-binding fix), `38b6a2532b`
(Stage B: `:1211` timeout+kill, manifest/ledger memoization) -- all pushed to CLOUD.

---

## What landed

### 1. `.tools/comp-which-routing-test.py` -- watchdog-bounded warm path

`_run_comp_which_warm_bounded(q, deadline=WARM_DEADLINE_S=20.0)`: runs the existing warm call
(`_run_comp_which_warm`, ~B's Step-2 addition) on a daemon worker thread behind a **non-blocking
`Lock`**. On a deadline breach it returns `(False, None)` immediately. The lock is deliberately
**never released** by an abandoned worker -- `_run_comp_which_warm` mutates process-global state
(`sys.argv`, `os.getcwd()`, and via `contextlib.redirect_stdout/stderr`, `sys.stdout`/`sys.stderr`
themselves), none of it thread-local, so letting a second call start while an orphan is still
inside `mod.main()` would race the same globals and could silently corrupt BOTH calls' captured
output. The lock turns that into a clean, provable failure mode instead: once one call hangs,
every later call in the same process reports UNEVALUABLE immediately rather than racing the
orphan.

`self_route_verdict` is flipped to call this by default (previously `_run_comp_which`, the
subprocess path -- kept, intentionally unused, as the regression oracle). New verdict:
`UNEVALUABLE` -- "the route is UNKNOWN," never folded into MISS.

### 2. `org/modules/graph/manifest_check_cli.py` -- `_selfroute_invariant` hard-blocks on UNEVALUABLE

Same treatment as MISS (its own printed message, "status UNKNOWN, not MISS," never conflated).
**Judgment call, not dictated by the TO** -- flagged to CVO~Z ahead of verification, who endorsed
it explicitly: an unconfirmed router-surfacing guarantee is not a pass, and it's consistent with
the comp-system guard's own precedent (`dirty=None` -> BLOCKED, never silent-pass).

### 3. Base's `PENDING_router_reachability_3_law_mandated_calls.patch` landed

The 3 CLAUDE.md-mandated router calls (`comp-iam simulate`, `comp-iam reconcile`,
`comp-pipescript postdeps`) were declared in `tools_index` but structurally unroutable
(comp-which's fuzzy layer never reads `tools_index`). Base's patch (`.tools/comp-which` RULES +
`graph-call-manifest.yaml` entries) was already behavior-verified 4/4 ABSENT -> RANK-1 and sat
blocked behind this gate becoming evaluable (acceptance criterion 5). Landed and re-verified
behaviorally after applying:
```
"can this role write to a brand new bucket"                    -> comp-iam simulate  rank 1 (score 2.00)
"what post-run steps are required after an ad-hoc gold run"    -> comp-pipescript postdeps  rank 1 (score 2.00)
```

### 4. `infra/system/06_current_state.{md,json}` regenerated, both commits

`.tools/comp-which-routing-test.py` matches the comp-system `_SOURCES` glob (`.tools/comp-*`);
the patch-landing commit additionally touches `.tools/comp-which` and
`graph-call-manifest.yaml` (`org/modules/graph/*.yaml`). Ran the regen in the same commit window
as each source change, per the discipline base demonstrated at `1e81fd0c18` and CVO~Z's
pre-emptive heads-up on the new `comp-system BLOCKED-ON-PEER-LANDING` guard (landed `b06ec7aa99`
the same day).

---

## Mutants -- both run against the REAL post-flip call path, not a bypass

**MUTANT (a)** -- a real self-route MISS must still redden the gate. No natural MISS exists in
the current population (probed separately: all 69 tools read NEARTIE, 0 MISS, 0 RANK1 today) --
so this uses a synthetic MISS constructed the same way this file's own `gen_gibberish()` already
does (seeded, not hand-picked), fed through `self_route_verdict`'s real code path via a
monkeypatched `self_route_query` for one fake tool id. Result: `verdict == "MISS"`. **PASS.**

**MUTANT (b), stage-A form** -- a target whose warm call deterministically exceeds the deadline.
`_run_comp_which_warm` monkeypatched to `time.sleep(9999)` (deterministic, not a timing guess).
```
call 1 (the hang):    ok=False out=None  elapsed=2.01s   (test deadline 2.0s)
call 2 (post-orphan):  ok=False out=None  elapsed=0.000s  (lock held by the orphan -- no race)
self_route_verdict via the hung path: UNEVALUABLE
```
Script exits cleanly every time (the daemon thread never blocks interpreter exit). **PASS --
and framed exactly as the TO requires: this proves the GATE is bounded. It does NOT prove the
hang was killed** (comp-which:1201 itself is untouched; a hung worker thread is
CONTINUED-PAST, not killed -- Design B's job).

**Regression -- full population, no sampling/capping:** new (warm+bounded, the live default now)
vs old (`_run_comp_which`, subprocess) verdicts across the entire live `tools_index` universe.
Run twice today; population drifted live (65 -> 69 tools) between the two runs -- reported as-is,
per the standing drifting-live-denominator finding, not treated as an error. **0 mismatches, both
times.**

---

## Findings surfaced, not fixed here (explicitly out of scope for this TO)

**`_ARROW` / RANK1 is structurally unreachable.** First attributed (incorrectly, by me) to
`_run_comp_which` omitting `--route-only`. **CVO~Z corrected this at source**: `_ARROW`
(`^\s*->\s*(\S+)`) matches **zero lines in both modes** -- with and without `--route-only` --
because comp-which's real output is always the numbered `N. score X.XX  tool` block, never a
bare `-> tool` line. `ranked` is therefore always `[]` and RANK1 can never be returned,
unconditionally. CVO~Z's sharper framing: the gate is a **presence check wearing a routing
check's name** -- it can tell "the tool appears somewhere in comp-which's output" from "it
doesn't appear at all," but cannot distinguish rank-1 from rank-68-of-68.

**Confirmed NON-BLOCKING for this change**, traced at source before landing (both CTO~Z and
CVO~Z required this before green-lighting): `_selfroute_invariant`'s pass condition
(`manifest_check_cli.py:661`, `if not misses and not unevaluable: return 0`) never reads RANK1 --
grep-confirmed zero references to the string "RANK1" anywhere in that file. NEARTIE only warns.
Base's WS-7 self-route fix worked through the independent `tool not in out` MISS substring test,
unrelated to `_ARROW`/`ranked`. CVO~Z routed the RANK1-unreachability finding to CTO~Z as its own
separate item -- explicitly not folded into GATEBOUND, since one is boundedness and the other is
semantics.

---

## Landing mechanics (for the record -- three separate, unrelated debris pockets surfaced and
were quarantined by CTO~Z during this landing, none of them mine): `org/modules/graph/
postmerge-cols/*.yaml` (24-day-old orphaned debris, dead July-1 session), 14 remaining
`org/modules/graph/types-index/*.yaml` files (documented comp-types blast debris, Lane-E
`1735a1257f`), and one `org/modules/graph/vectorize-audit/*.yaml` file (last of a comprehensive
pre-today-mtime sweep). CVO~Z's own union-scoping fix for the comp-system guard (routed to
CTO~Z, landed by `~A` mid-session) is the durable close -- confirmed by the gate's own message
text narrowing from "source file(s) are uncommitted" (whole `_SOURCES` union) to "source file(s)
**that feed the drifted metric(s)** are uncommitted" (metric-scoped) partway through this
session.

---

## Acceptance criteria (Stage A: 1-5)

| # | Criterion | Status |
|---|---|---|
| 1 | Watchdog-bounded warm path; UNEVALUABLE first-class, never silently dropped | DONE |
| 2 | Mutant (a): gate reddens on a real self-route MISS | PASS |
| 3 | Mutant (b), stage-A form: watchdog fires, UNEVALUABLE recorded, run completes | PASS |
| 4 | Flip landed only after 1-3 held; verdict-identity re-run as regression | DONE, 0/69 mismatches |
| 5 | Member evaluable -> base's `@e78e006cb` patch landed -> item (c) now possible | DONE |
| 9 | Two-axis isolation for mutant work (own worktree, no shared-hook wiring) | Mutant-proving done in an isolated `git worktree add` off local `CLOUD` HEAD before any main-tree edit; final code copied in only after mutants + regression held there. Per CVO~Z's later-relayed method note (shared-worktree gate blocks MUTATION not INSPECTION), a worktree was not strictly required for this scope, but the isolation was already built and cost nothing extra to keep. |

---

## Incidental fix, landed separately: `WARM_DEADLINE_S` was not runtime-patchable

CVO~Z's independent Stage A verification (own mutants, not a re-run of mine, plus a positive
control they added: an unpatched bounded call must succeed for real before a mutant's `False` is
meaningful) found `deadline: float = WARM_DEADLINE_S` bound the module global's value at
**function-definition time**, not call time -- reassigning `WARM_DEADLINE_S` after import
silently did nothing to a caller relying on the default (CVO~Z measured 20.01s after setting it
to 2.0). My own testing never hit this because I always passed `deadline=` explicitly -- correct
usage that happened to never exercise the broken path. Fixed (`4489d4cd8d`): default to `None`,
resolve against the current module global inside the function body. Verified before/after with
CVO~Z's positive control; CVO~Z independently re-verified the fix against the exact test that
exposed the bug. Banked as a general testing pattern (CVO~Z's framing): for any function whose
default sources a module global, one test should exercise the global-reassignment path, not just
the explicit-argument path -- an author's own tests tend to use the API correctly, which is
precisely why this class of bug survives them.

---

## Stage B -- delivered: `4489d4cd8d` (deadline fix), `38b6a2532b` (the hang class closed)

`comp-which:1211`'s `_run_primitive` (the `comp-grep`/`comp-glob` fallback shell-out) is now
`Popen` + `wait(timeout=FALLBACK_TIMEOUT_S=60)` + explicit `kill()`+`wait()` on `TimeoutExpired`
-- deliberately not `subprocess.call(..., timeout=...)`, which does not kill the child on expiry
(only `subprocess.run` does that internally). This is the actual close of the hang class Stage A
could only bound around: Stage A's watchdog reports `UNEVALUABLE` and leaves the underlying call
CONTINUED-PAST; Stage B REAPS it.

Also memoized `_manifest_matches` (the YAML parse only, via `_load_manifest_data()` -- the
per-query overlap-scoring still runs fresh, since that genuinely depends on the query) and
`_load_ledger` (whole-return cacheable, no per-query dependence at all). Both were re-parsing
their source files from disk on every call (2x and 3x per query cascade respectively); under the
warm in-process path that was up to ~138/~207 redundant re-parses per gate run of files that
never change mid-process.

**MUTANT (criterion 6):** a `:1211`-class hang, sandboxed -- `mod.WS` pointed at scratch
`comp-grep`/`comp-glob` stand-ins that loop-heartbeat to a file every 0.2s forever instead of
exiting, exercising the real `_run_primitive` code path (Popen, wait, kill) unmodified, not a
bypass. `_run_primitive` returned in 2.03s against a 2s test deadline (production default 60s),
`rc=1`, and -- the KILLED-not-continued-past proof, distinct from Stage A's own honest limit --
the heartbeat file **froze immediately** after the call returned rather than continuing to
advance every 0.2s, confirming the child was actually terminated and reaped, not merely
abandoned to keep running in the background.

**REGRESSION (criterion 7, memoization must not change ranking):** full raw-output comparison
(not verdict-level alone, which RANK1's confirmed unreachability would make too coarse to trust
by itself), pre-Stage-B (`git show HEAD:.tools/comp-which`) vs post-Stage-B (working tree),
across the full 69-tool self-route population. **First attempt showed 54 "mismatches" that were
a bug in my OWN test harness**, not comp-which: the pre-Stage-B comparison copy was written
directly into the workspace root instead of inside a `.tools/`-depth subdirectory, so its
`WS = dirname(dirname(__file__))` resolved one level too shallow, silently pointing `MANIFEST`/
`LEDGER` at nonexistent paths and disabling its own fuzzy-manifest backstop -- OLD wasn't
producing genuinely different rankings, it was silently running with a broken input. Caught via
the standard discipline this project runs on: a same-file-loaded-twice control (0 mismatches)
before trusting the OLD-vs-NEW asymmetry as real, which is exactly what exposed the asymmetry as
the harness's fault, not the subject's. Corrected (placed the comparison copy at the matching
directory depth) and re-run: **0/69 mismatches.**

**End-to-end, criterion 8 (coverage discipline, full population, no capping):**
`self_route_verdicts()` through the complete warm+bounded path against the Stage-A+B-combined
`comp-which` -- 69/69 NEARTIE, 0 MISS, 0 UNEVALUABLE, 33.1s (down from the 73.6s pre-memoization
Stage-A-only measurement on the same machine).

**Criterion 9 for Stage B:** a scratch sandbox directory (`mod.WS` override) rather than a full
`git worktree` -- narrower than Stage A's isolation, but sufficient here since the mutant only
reads `mod.WS`/`mod.FALLBACK_TIMEOUT_S` and writes to a throwaway heartbeat file, never touching
the real `.tools/` or `org/modules/graph/` trees. Flagging the narrower choice explicitly rather
than silently reusing the Stage A worktree pattern without saying why it changed.

### Stage B acceptance criteria

| # | Criterion | Status |
|---|---|---|
| 6 | `comp-which:1201`-class hang bounded with timeout+kill; REAPED not continued-past; mutant proves it | DONE, PASS |
| 7 | `_manifest_matches` + `_load_ledger` memoized; verdict/ranking-identity preserved | DONE, 0/69 mismatches (after fixing a harness bug, see above) |
| 8 | No sampling/capping; full population; any unevaluable tool loud + in the population | DONE, 69/69 evaluated, 0 UNEVALUABLE |
| 9 | Isolation for the mutant work | Scratch sandbox dir (see above), narrower than Stage A's worktree by design |

This completes NFRA_TOOLARCH.GATEBOUND end to end (Stage A + Stage B).

---

## Files

| File | Change | Committed |
|---|---|---|
| `.tools/comp-which-routing-test.py` | Watchdog-bounded warm path, UNEVALUABLE verdict, flip | `5df71c6f24` |
| `org/modules/graph/manifest_check_cli.py` | Hard-block on UNEVALUABLE | `5df71c6f24` |
| `.tools/comp-which` | Base's 3 mandated-call RULES entries | `8f42c4fdab` |
| `org/modules/graph/graph-call-manifest.yaml` | Base's 3 mandated-call manifest entries | `8f42c4fdab` |
| `.tools/comp-which-routing-test.py` | `WARM_DEADLINE_S` late-binding fix | `4489d4cd8d` |
| `.tools/comp-which` | `:1211` timeout+kill, manifest/ledger memoization | `38b6a2532b` |
| `infra/system/06_current_state.{md,json}` | comp-system regen, four commits | `5df71c6f24`, `8f42c4fdab`, `4489d4cd8d`, `38b6a2532b` |
| This report | New / updated | Not yet -- CLOUD_COMP_TESTER own lane |
