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

## DONE @984d0be0c -- the ad-hoc python->bash callers migrated (COO idle-reallocation 211300Z, Andrew-direct)

Migrated each to `git_bash_resolver.git_bash()` (kept each caller's env-override precedence), commit-gate clean,
and EXERCISED each (imported the module, confirmed the resolver resolves the real Git Bash + the resolved bash
actually RUNS `echo ok` rc=0 -- verify-not-assume). Committed under my author line (these paths ARE AE-permitted
-- my earlier "likely ANY_EXEC" concern was wrong; the gate passed clean, no --force).

| Caller | Was | Now | Exercised |
|---|---|---|---|
| `org/modules/graph/comp_system.py` | already avoids bash (`[sys.executable, kuzu_cli.py]`) | **NO-OP** -- best-practice example, untouched | n/a |
| `org/modules/graph/comp_debt/grounding_lib.py:55` | `shutil.which("bash")` | `git_bash() or shutil.which or "bash"` | `_BASH_EXE`=Git Bash, runs |
| `org/modules/graph/debtscan/summary_corpus.py` (`_kuzu_cmd`) | `shutil.which("bash")` | `git_bash() or shutil.which or "bash"` | interp=Git Bash, runs |
| `org/modules/graph/compproof/tool_probe.py:120` | local hardcoded-list `_git_bash()` | delegates to shared (keeps GIT_BASH env) | `_git_bash()`=Git Bash, runs, delegates=True |

**HONEST FRAMING (Rule-22, don't overclaim):** unlike server.py (a CONFIRMED 12-day live outage), these 3 were
NOT live victims -- `shutil.which("bash")` returns Git Bash on this host's current PATH (measured), so they were
resolving correctly. The migration retires the CONDITIONAL risk (a PATH reorder would flip which() to the WSL
stub) + dedups tool_probe's local resolver. Consolidation-clean, additive. `hook_register_orphan_cleanup.py`
DOCUMENTS the class (names the silent variant) -- left as-is (a documenter, not a broken caller).

**The python->bash WSL-stub class is now CLOSED across the estate's python callers** the victim-scan surfaced:
1 canonical resolver + all callers either migrated, already-safe-by-design, or (server.py) fixed.
