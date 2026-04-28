# Task Order: COMP_LEARNS.093 — pytest.ini PYTHONPATH Project Root Fix

**Project:** COMP_LEARNS
**Issued by:** 2.1.0_SA_COO
**Issued to:** 1.3.0_DS_CompLearns
**Status:** <status>complete</status>
**Completion commit:** <completion_commit>1907bd1e</completion_commit>
**Completion date:** <completion_date>2026-04-28</completion_date>
**Date:** 2026-04-28
**Priority:** P2 — quality-of-life; independent of all active SC work; execute while standby

---

## Context

Surfaced as non-blocking note (1) in your .090 RAVC COMPLETE: `pytest.ini` currently declares
`pythonpath = data/black_diamond/scripts` but omits the project root. Bare `pytest comp/`
fails with 56 collection errors (ModuleNotFoundError: No module named 'comp') in a fresh
shell. Prior DS sessions have worked by inheriting PYTHONPATH from the shell env — fragile
across fresh sessions and contradicts TO baseline commands.

This is a 1-line fix. Run while standing by for CTO packet authoring TOs.

---

## Phase 0 — Verify current state

```bash
cd /c/Users/AndrewBerman/Desktop/feature_clb
cat pytest.ini
```

Expected current content:
```
[pytest]
pythonpath = data/black_diamond/scripts
```

Verify that bare `pytest comp/ -q --collect-only 2>&1 | head -5` fails with import error.
(If it somehow passes, stop — PYTHONPATH is already inherited and this TO is moot; RAVC COMPLETE immediately.)

---

## Phase 1 — Edit pytest.ini

Add the project root (`.`) to the pythonpath list. Final content:

```ini
[pytest]
pythonpath = data/black_diamond/scripts
    .
```

(Multi-line INI list — pytest 7.0+ supports multiple paths via indented continuation.)

**Do NOT** change any other pytest.ini settings. This is the only edit.

---

## Phase 2 — Verify fix

```bash
cd /c/Users/AndrewBerman/Desktop/feature_clb
PYTHONPATH="" pytest comp/ -q --collect-only 2>&1 | tail -5
```

Explicitly clear PYTHONPATH (to simulate fresh shell) and confirm no ModuleNotFoundError.
Should show collection of comp/ tests, not an import error.

Then run the full suite:
```bash
PYTHONPATH="" pytest comp/ -q 2>&1 | tail -5
```

All tests must PASS. 506 baseline (from .090) is the floor. No regressions.

---

## Phase 3 — ds-commit-gate

```bash
.tools/ds-commit-gate.sh pytest.ini
```

Must exit 0. (pytest.ini is not a Python file — gate will run config checks only.)

If gate errors on non-Python file: acceptable to note and proceed; the gate's Python checks
don't apply to .ini files.

---

## Phase 4 — Commit and push

```bash
cd /c/Users/AndrewBerman/Desktop/feature_clb
git add pytest.ini
git commit --only --author "1.3.0_DS_CompLearns <1.3.0_DS_CompLearns@opal.agent>" \
  -m "fix(pytest.ini): add project root to pythonpath -- fixes bare pytest comp/ in fresh shell" \
  -- pytest.ini
git push origin CLOUD
```

---

## Acceptance criteria

1. `pytest.ini` pythonpath includes project root (`.`) in addition to `data/black_diamond/scripts`
2. `PYTHONPATH="" pytest comp/ -q` completes with 0 failures (no import errors)
3. Test count ≥ 506 (baseline from .090)
4. Committed with author 1.3.0_DS_CompLearns + pushed to CLOUD
5. RAVC COMPLETE MCP to 2.1.0_SA_COO: commit hash + test count confirmed

---

## RAVC COMPLETE format

```
Subject: COMPLETE — COMP_LEARNS.093 pytest.ini PYTHONPATH fix
Body:
  Commit: <hash>
  Change: pytest.ini pythonpath += project root (.)
  Verification: PYTHONPATH="" pytest comp/ -q -- N tests passed, 0 failed
```

---

## Dependencies

- None — fully independent of SC .091/.092 and CTO pool freeze work
- Downstream: cleaner TO baseline commands for all future DS agents
