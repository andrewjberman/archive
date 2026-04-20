# 0.4.0_DS_ClientPlatform~C — Session Log
**Date:** 2026-04-16
**TO:** COMP_LEARNS.006 — comp/prompts/iter.md per-iteration agent prompt
**Status:** COMPLETE
**Commit:** d8ab1372

---

## Inbox triage (pre-work)

- `20260416T135831Z_0.4.0_DT_ClientPlatform`: FYI on ADVI_49EXEC.004 gate on TO2 — FYI only, TO2 is base-routed. No ~C action.
- All earlier messages (CTO retract, COO GO SL-P1, AE SSM ACK) triaged last context — not ~C scope.

GO received from Andrew 2026-04-16 ~10:00 ET. Flipped COMP_LEARNS.006 staged→pending.

---

## Compiler Tools Mandate Execution

### Phase 1 (before write)

**Step 1:** `cat /tmp/autoresearch_inspect/autoresearch-master/program.md | head -60`

Confirmed Karpathy pattern: prose-procedural, numbered sections, "do X then Y", explicit CAN/CANNOT
boundaries, no meta-loop instructions (loop-forever is the bash driver's job). Used this as the
structural model for iter.md.

**Step 2:** `grep -n "python -m comp.framework.run" comp/bin/comp-learns-run.sh`

Output: line 342 — `python -m comp.framework.run "$TARGET" \ --iter "$iter"`

Confirmed: step 6 in iter.md must use exactly `python -m comp.framework.run $COMP_LEARNS_TARGET --iter $COMP_LEARNS_ITER`.

### Phase 2 (before commit)

**Step 1:** `wc -l comp/prompts/iter.md` → 116 lines. Within ≤120 limit.

**Step 2:** Dry-run against _stub target:
- Set env: `COMP_LEARNS_TARGET=_stub COMP_LEARNS_ITER=1 COMP_LEARNS_WORKTREE=$(pwd)`
- Traced steps 1-3 manually (env read, git log, queries.yaml fallback confirmed for iter 1)
- Ran step 6: `python -m comp.framework.run _stub --iter 1`
- Output: exit 0, FAIL Q002+Q003 surfaced correctly, results.tsv row appended, state.json written
- Dry-run artifacts cleaned (rm results.tsv state.json — untracked, not staged)

Agent follows 7 steps without looping or escalating. Trace valid.

### Phase 3 (after commit)

`comp/prompts/README.md` present. Lists iter.md + driver invocation contract (env vars, restrictions).

---

## Deliverables

### comp/prompts/iter.md (116 lines)

7 sections per wire_contract:
1. Context — env var echo, cd into worktree
2. Read the state — git log + tail results.tsv
3. Pick one failing query — logs/iter_{N-1}.log fallback to queries.yaml for iter 1
4. Propose one edit — compiler.py scope only; explicit CAN/CANNOT list
5. Commit the edit — `--only` constraint, `--author=0.4.0_DS_ClientPlatform~C`, one commit, no amend
6. Re-run harness — `python -m comp.framework.run $COMP_LEARNS_TARGET --iter $COMP_LEARNS_ITER`, exit code semantics, revert protocol for crash
7. Return — explicit DO NOT list (no loop, no push, no human ask)

### comp/prompts/README.md

Index of prompt files + driver invocation contract (env var table, restriction summary).

---

## DO NOT (carry-forward)

- DO NOT act on ADVI_49EXEC.002/TO2 — base-routed, different tilde lane
- DO NOT act on SL-P1 — routed to base/~A per COO GO 13:45Z
- DO NOT act on RA-P2b — HARD GATED on RA-P1b (~D work, no GO yet)
- DO NOT act on RA-P5 — gated on RA-P4 + D_01 canonical cutover

---

## ~C Queue (post-session)

| TO | Status | Gate |
|----|--------|------|
| COMP_LEARNS.006 | COMPLETE (d8ab1372) | — |
| RA-P2b | STAGED | HARD GATE: RA-P1b validator PASS |
| RA-P5 | STAGED | GATE: RA-P4 + D_01 cutover |
