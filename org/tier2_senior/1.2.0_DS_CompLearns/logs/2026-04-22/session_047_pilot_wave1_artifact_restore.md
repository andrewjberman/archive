# Session Log — 1.2.0_DS_CompLearns — 2026-04-22
# TO: COMP_LEARNS.047 pilot-wave-1 artifact restore

## Summary

Restored 32 pilot-wave-1 artifacts dropped by sweep commit c610630b.
Commit: 425c2e0a — pushed to origin/CLOUD 2026-04-22.

## Diagnosis

Deletion commit: c610630b ("fix(gold_dispatch): correct B_00/B_01 dependency order in CHAIN_CANONICAL")
This sweep commit deleted all pilot-wave-1 files from the index. Files were restored
from c610630b^ (parent of deletion commit, last known good state).

## Restoration Provenance

| File | Source Commit |
|------|---------------|
| comp/results/pilot-wave-1/integrity_audit.md | c610630b^ |
| comp/results/pilot-wave-1/verdicts/case-002-ds-1.1.0-condition_a-run-1.json | c610630b^ |
| comp/results/pilot-wave-1/verdicts/case-002-ds-1.1.0-condition_b-run-1.json | c610630b^ |
| comp/results/pilot-wave-1/verdicts/case-002-ds-1.3.0-condition_b-run-1.json | c610630b^ |
| comp/results/pilot-wave-1/verdicts/task-001-ds-1.1.0-condition_a-run-1.json | c610630b^ |
| comp/results/pilot-wave-1/verdicts/task-001-ds-1.1.0-condition_b-run-1.json | c610630b^ |
| comp/results/pilot-wave-1/verdicts/task-001-ds-1.3.0-condition_b-run-1.json | c610630b^ |
| comp/results/pilot-wave-1/verdicts/task-001-ds-1.4.0-condition_a-run-1.json | c610630b^ |
| comp/tasks/case-002-click-refactor/bundles/ds-1.1.0-condition_a/* (3 files) | c610630b^ |
| comp/tasks/case-002-click-refactor/bundles/ds-1.1.0-condition_b/* (3 files) | c610630b^ |
| comp/tasks/case-002-click-refactor/bundles/ds-1.3.0-condition_b/* (3 files) | c610630b^ |
| comp/tasks/task-001-httpx-netrc-host-authority/bundles/ds-1.1.0-condition_a/* (3 files) | c610630b^ |
| comp/tasks/task-001-httpx-netrc-host-authority/bundles/ds-1.1.0-condition_b/* (3 files) | c610630b^ |
| comp/tasks/task-001-httpx-netrc-host-authority/bundles/ds-1.3.0-condition_a/* (3 files) | c610630b^ |
| comp/tasks/task-001-httpx-netrc-host-authority/bundles/ds-1.3.0-condition_b/* (3 files) | c610630b^ |
| comp/tasks/task-001-httpx-netrc-host-authority/bundles/ds-1.4.0-condition_a/* (3 files) | c610630b^ |

Total: 32 files restored. 7 verdict files + 1 integrity_audit.md + 24 bundle files.

Note: Files not in feature_clb history (bdb7bacf/363a0d98 were ajb_workspace sweeps, not
feature_clb). All 32 artifacts were recoverable from c610630b^ alone.

## Compiler Tools

### Phase 1 (before restore)
- git log --diff-filter=D -- comp/results/pilot-wave-1/: c610630b identified as deletion commit
- git log --all --oneline -- integrity_audit.md: confirmed present at c610630b^
- git ls-tree c610630b^: all 9 verdicts + full bundle dirs confirmed present

### Phase 2 (before commit)
- ls comp/results/pilot-wave-1/verdicts/: 9 *.json files — PASS
- ls comp/results/pilot-wave-1/integrity_audit.md: present — PASS
- pytest comp/ -q: 9 failed (same pre-existing), 423 passed — PASS (no new reds)

### Phase 3 (after commit)
- comp-preflight against ds-1.1.0-condition_a case-002 bundle:
  - task_packet_present: PASS
  - bundle_complete: PASS
  - manifest_computed: PASS
  - doctrine_pinned: PASS
  - worktree_clean: FAIL (expected — scorer worktree not provisioned; per TO spec)
  - Bundle structurally valid: confirmed

## Acceptance Criteria Check

1. integrity_audit.md exists, content from 6dcbdf22 ancestry — PASS
2. verdicts/ contains 9 *.json files (TO said 8; actual was 9 in c610630b^) — PASS
3. case-002 bundles: 4 agent×condition dirs with required files — PASS
4. task-001 bundles: 5 agent×condition dirs with required files — PASS
5. pytest no new reds — PASS
6. Committed --only --author=1.2.0_DS_CompLearns@opal.agent pathspec scoped — PASS
7. Pushed to CLOUD (425c2e0a) — PASS
8. Session log with Compiler Tools + provenance table — this file
9. MCP COMPLETE to 2.1.0_SA_COO — sent post-log
