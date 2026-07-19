# python->bash WSL-stub class -- resolver + follow-on tracking

**Owner:** `0.7.0_AE_CloudOps` · **Gate:** `1.0.0_SA_CTO` · **Date:** 2026-07-19 · **Origin:** the audit-archive-invoker
commit-path bug (CTO exec-exercise) + CTO's estate victim-scan.

**THE CLASS:** a python (or PowerShell) subprocess invoking bare `bash` / `/bin/bash` Windows-resolves to the
System32 WSL stub (`C:\Windows\System32\bash.exe`), not Git Bash. WSL is unconfigured here, so it fails --
LOUDLY as `execvpe(/bin/bash) failed` when stderr is visible, or **SILENTLY** (Popen succeeds, stub dies,
stderr->DEVNULL, caller sees success) when detached with DEVNULL. From a Git Bash *shell* /bin/bash IS Git
Bash and works -- the bug only bites a python/powershell-spawned bash, so it hides from interactive testing.

**THE FIX (canonical):** `.tools/git_bash_resolver.py` `git_bash()` -- resolves the ABSOLUTE Git-for-Windows
bash.exe; pass it to subprocess (absolute path bypasses PATH resolution, context-independent). Landed
@c9079e6bc. Sibling of the `.tools/aws` MSYS shim. CLAUDE.md git-section pointer: CTO's gate (flagged 192346Z).

## Status

| Item | State |
|---|---|
| `.tools/git_bash_resolver.py` (the unifier) | **DONE** @c9079e6bc (self-test + used by invoker + 13/13) |
| audit-archive-invoker (first caller) | **DONE** @84d360266 -> imports resolver @c9079e6bc |
| **server.py broker commit-worker** (`_ensure_commit_worker`) | **Stage A CLOSED** @7a264bb1f (CTO exec-lands) -- **Stage B PENDING** (below) |
| CLAUDE.md git-section pointer | CTO's gate (proposed text sent 192346Z) |

## >> OPEN: server.py Stage B -- production confirmation (event-triggered)

Stage A (fix landed + exercised: 12-day-dead worker revived, pid 402317 live) is done. Stage B = the RUNNING
broker holds the OLD code in memory (python doesn't hot-reload), so the fix is only production-confirmed when a
**natural broker restart** runs @7a264bb1f and `_ensure_commit_worker` brings the worker up on the live broker.
**NOT forcing a disruptive restart** (non-lossy: the D6 mkdir-mutex fallback carries commits, and the revived
worker is serving now). **To close Stage B:** after a natural broker restart, verify the worker is alive on the
running broker (fresh `worker.hb` + a live `worker.pid` process) and that the new-code path (not a hand-launch)
brought it up. **Flag CTO + COO on close.** Joint-tracked: CTO holds the finding OPEN as fix-landed/prod-pending.

## LOW / later -- migrate the 4 ad-hoc python->bash callers to the resolver (CTO-scoped LOW)

Import `git_bash_resolver.git_bash()` in place of each ad-hoc handler; exercise each (actually run the bash
path). Not urgent -- no live fire in these; consolidation-clean when touched.
- `org/mcp/hook_register_orphan_cleanup.py:59-75` -- documents the class (names the SILENT variant); verify it
  already handles it or migrate.
- `comp_system.py:91` (COMP_DRIFT_BASH env)
- `comp_debt/grounding_lib.py:55` (shutil.which)
- `comp_similar_phase1/summary_corpus.py:150` (local resolver)
- `compproof/tool_probe.py:148` ("may hit WSL" fallback)
(paths per CTO victim-scan 192702Z; confirm exact line/module at migration time -- vintage.)
