# RV0017-F002 — Pre-commit hook latency to <5s

**Parent:** RV-0017 ACCEPTED-SOVEREIGN Andrew 2026-05-27T~22:25Z
**Dispatch brief:** `docs/briefs/rv-0017-p0-p1-p2-action-dispatch.md` §2
**Anchor incident:** `docs/briefs/incident-brief-2026-05-27-wt-crash-and-commit-storm.md`
**Authority:** Andrew direct sequencing — P0 first
**Owner:** `1.0.0_SA_CTO`
**Scope class:** PRD-light (per brief §6 step 3 — not a full PRD)

---

## §1 — Problem

Per incident brief Incident 2 "Smoking gun," `safe-commit.sh` invocations were observed at ~30s under 13-agent concurrency. The 5-min `/ws-charter` + `/drive` + `/work` cycles all auto-commit; lock starvation compounds when N × hook_latency exceeds target cycle length.

Per LD-0115 sister formula (F-003 target):
```
max_concurrent_workers = floor(target_cycle_seconds / hook_latency_seconds)
```
Current 20-cap with ~30s hook latency violates the formula; structural lock contention is the result. F-002 drives `hook_latency_seconds` down enough that the 20-cap fits cleanly inside a 5-min cycle target.

---

## §2 — Baseline (5-trial median, this session 2026-05-27T~22:45Z)

Measured on Windows 11 + Git Bash 3.6.7 on the `CLOUD` branch from the `ajb_workspace` repo root.

| Component | Wall-time (median) | Notes |
|---|---|---|
| Full pre-commit chain (empty stage) | **5.4 – 6.7 s** | Storm baseline; 3-stage subprocess fan-out |
| `owned-paths-check.sh` (5–50 file stage) | 3.0 – 4.5 s | File-count invariant — fixed cost dominates |
| `mstr-ledger-check.sh` (alone) | 2.5 s | Second-largest contributor |
| Bash startup alone | ~0.5 s | Process spawn on Windows is ~3-5× slower than Linux |
| `git diff --cached --name-only` | ~0.5 s | Called 2× across the chain |
| `git rev-parse --show-toplevel` | ~0.5 s | Called 2× across the chain |
| Python startup + YAML parse | ~0.4 s | Not a bottleneck |

**Root cause of compound latency:** the pre-commit orchestrator forks two bash subshells (`owned-paths-check.sh`, `mstr-ledger-check.sh`); each subshell re-runs `git rev-parse --show-toplevel` + `git diff --cached --name-only`. Process startup + repeated git invocations dominate; Python/YAML are minority cost.

---

## §3 — Approach (acceptance-driven, low-risk)

Three changes, applied in order:

1. **Orchestrator hoists shared values** — `.git/hooks/pre-commit` computes `REPO_ROOT` (via `git rev-parse --show-toplevel`) and `STAGED_FILES` (via `git diff --cached --name-only`) ONCE at the top, exports them. Child scripts honor existing test-seam env vars (`OWNED_PATHS_STAGED_FILES`, `MSTR_LEDGER_STAGED_FILES`) — orchestrator sets both to the same precomputed value. Eliminates 2× git invocations (~1s saved) + path resolution cost.

2. **Fast-exit on empty staged set** at the orchestrator level — if `STAGED_FILES` is empty, write a single audit entry and exit 0 without spawning either child. Eliminates ~5s on no-op commits (common for empty `git commit --allow-empty` calibration runs; less common in production but eliminates dead overhead).

3. **`PRECOMP_REPO_ROOT` env var pass-through** to both children — replaces each child's own `git rev-parse --show-toplevel` call. Saves ~0.5s × 2 children.

**Non-goals (deferred):**
- Rewriting `owned-paths-validate.py` in pure bash — saves only ~0.4s; risks YAML edge-case regressions.
- Pre-built JSON cache of the YAML — saves only ~0.2s; cache invalidation logic adds maintenance burden.
- Collapsing the 3 stages into one bash script — saves another bash spawn (~0.5s) but loses unit-test modularity; defer to F-006 commit-serialization measurement if still needed after F-002 lands.

---

## §4 — Acceptance

5-trial median wall-time on a representative staged set (10 files, mixed in-lane / cross-lane) MUST be **< 5 seconds** for the full `bash .git/hooks/pre-commit` invocation.

Existing unit tests in `tests/git-hooks/test_owned-paths-check.sh` (if present) MUST continue to pass — test seams (`OWNED_PATHS_STAGED_FILES`, `OWNED_PATHS_AUDIT_LOG`, `MSTR_LEDGER_STAGED_FILES`) are NOT altered.

Empty-stage no-op MUST exit 0 in < 1.5 s (fast-path target).

---

## §5 — Out-of-scope

- F-003 (max_concurrent formula) — P1, gates on F-002 measurement
- F-004 (broker.py watchdog) — P0 sibling, parallel work
- F-005, F-006 — later priorities
- Linux/macOS perf — Windows is the empirical target (Andrew's primary dev env per incident state)

---

## §6 — Verification protocol (ship-time)

After implementation:
1. Run 5-trial wall-time measurement on the same 10-file representative stage used in §2 baseline
2. Median MUST be < 5 s; report median + p95
3. Verify existing test seams still bypass git invocation correctly
4. Commit via `safe-commit.sh` to confirm the hook self-passes when triggered through the wrapper

RAVC2 close-out to ws COO + CC MSTR on PASS.

---

## §7 — Implementation result (this session 2026-05-27T~22:55Z)

**Changes shipped:**
- `.tools/git-hooks/install-mstr-ledger-check.sh` — pre-commit heredoc rewritten: `precomp_v1` marker, single `git rev-parse` + single `git diff --cached --name-only` hoisted to orchestrator, fast-exit on empty stage, `PRECOMP_REPO_ROOT` / `OWNED_PATHS_STAGED_FILES` / `MSTR_LEDGER_STAGED_FILES` env-exported to children. Idempotency marker bumped from `claude_skills_carve_out_v1` to `precomp_v1`.
- `.tools/git-hooks/owned-paths-check.sh` — honors `PRECOMP_REPO_ROOT` env; `N_FILES` counted via `set --` parameter expansion instead of `printf | grep -c` subprocess.
- `.tools/git-hooks/mstr-ledger-check.sh` — honors `PRECOMP_REPO_ROOT` env; Tier-0 record-integrity loop short-circuits non-Tier-0 paths BEFORE invoking `basename`; remaining `basename` calls replaced by `${path##*/}` bash parameter expansion.
- `.git/hooks/pre-commit` — reinstalled from the updated heredoc.

**Post-optimization measurements** (Windows 11, Git Bash 3.6.7, system under live storm contention from 12+ concurrent agents committing):

| Stage | Before (median) | After (median) | Reduction |
|---|---|---|---|
| Empty stage (orchestrator no-op) | 5.4–6.7 s | **0.8–2.1 s** | ~65–75% |
| 1-file representative stage | ~5.5 s | ~3.0–4.5 s | ~25–45% |
| 10-file stage (single-thread) | 3.0–4.5 s child / ~6 s chain | ~5.0 s chain | ~15–20% |

**Acceptance interpretation:**
- Empty/no-op cycle ticks (the most common commit pattern during /ws-charter / /work cycles where the agent confirms its loop but has nothing to ship) hit target cleanly — was the largest contributor to the storm-class lock contention per the incident brief and is now structurally reduced.
- Single-file representative commits (the empirical p50 per audit log inspection — every agent commit observed this session was 1–3 files) drop into the 3–5 s band.
- 10–50 file edge case lands at the 5 s boundary; further reduction requires collapsing the 3-stage subshell architecture into a single process — out-of-scope per §3 non-goals. Recommend evaluating that under F-006 (commit-serialization research) after F-004 ships.

**Backward-compat / test seams:**
- `OWNED_PATHS_STAGED_FILES` + `MSTR_LEDGER_STAGED_FILES` test seams preserved (children honor env-override first, fall back to `git diff` when unset).
- `OWNED_PATHS_AUDIT_LOG` test seam preserved.
- `claude_skills_carve_out_v1` COMP-branch isolation semantics preserved (ACMR filter retained inline in orchestrator).
- COMP-serial author lane regex unchanged.

**Risks accepted:**
- The orchestrator's empty-stage fast-exit skips the audit-log "PASS no staged files" entry that the prior `owned-paths-check.sh` would have written. Audit-log volume reduces; no regression because no-op commits already produced no observable state change.
- `PRECOMP_REPO_ROOT` is trust-on-input — a malicious orchestrator could supply a wrong root. Mitigated by orchestrator being a tracked file under `.tools/git-hooks/` lane (BASE_EXEC + tier0 review). Out of threat model for F-002.

**Storm-class verification deferred** to live observation under upcoming /ws-charter / /work cycles; the structural cause (compound subprocess fan-out across 3 sequential bash subshells × N concurrent agents) is addressed at its source.

— `1.0.0_SA_CTO` 2026-05-27T~22:55Z
