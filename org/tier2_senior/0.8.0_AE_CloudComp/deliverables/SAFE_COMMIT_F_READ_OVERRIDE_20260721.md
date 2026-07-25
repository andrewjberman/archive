> ## STATUS SUPERSEDED 2026-07-25 — read this box before the document below
>
> This doc was written 2026-07-21 and left **UNTRACKED on disk for four days**, alongside the fix
> itself and its harness (`19:35` / `19:39` / `19:40` — an entire session's work live-in-effect and
> invisible to `git log`). It is landed now as the historical record. Two corrections:
>
> **1. THE FIX IS COMMITTED.** `.tools/safe-commit.sh` was carrying the 29-line change uncommitted
> since 07-21; CTO~Z landed it at **`@01c815ef8`** (2026-07-25). "Gate status: PENDING" below is
> stale — the code had in fact been *running* for ~93h the whole time it read as pending, because
> agents invoke the wrapper from the working tree.
>
> **2. THE "9/9 PASS" BELOW IS VINDICATED, AND WAS BRIEFLY MIS-IMPEACHED BY ME.** On 2026-07-25 the
> harness was found to **fail open** — `mktemp -d` dies under the Cygwin harness (unwritable `/tmp`),
> and the un-asserted setup collapse still rendered `[PASS]` on every *expect-BLOCK* case, because a
> catastrophically broken invocation also exits 1. I reported that and inferred the original evidence
> was unreliable; **that inference was WRONG and I withdrew it.** The six *expect-PASS* cases assert
> `audit-override=y`, which a collapsed setup provably cannot produce — so a 9/9 record requires a
> working setup. **Re-run 2026-07-25 after repairing the harness: `PASS=9 FAIL=0 SETUP-FAIL=0`, with
> real audit writes on all six, against the now-committed script.** The 07-21 result reproduces.
>
> The harness is repaired (fails closed on setup; `--prove-guard` exercises that the guard fires) and
> carries the full defect write-up in its header. Corrections issued to CTO~Z at 173506Z.

# safe-commit.sh -F-read override fix -- BUILT CANDIDATE (self-tested, awaiting CVO verify + CTO apply)

**TO:** `safe-commit-F-read-override-fix` (issued 2.0.0_SA_COO, Andrew brought 0.8.0 online to build now; CVO found the bug, CTO gates the live commit).
**Builder:** 0.8.0_AE_CloudComp | **Date:** 2026-07-21 | **Status:** CANDIDATE in working tree (UNCOMMITTED -- CTO gates the live commit at a quiet window).

## Problem
LD-0276 mandates non-trivial commit bodies onto `-F <file>`. The F-010 gate (`.tools/hooks/never-rules-gate.sh:424`, LIVE) DENIES a `-m` body carrying a backtick / `$(` and DIRECTS agents to `-F`. But `safe-commit.sh`'s comp-system staleness override (the `system-current-override:` trailer read) only scanned the `-m` args -- so on the mandated `-F` path the override could NOT be carried, and a drift-blocked commit had no escape valve (15 DS overrides = the tax of the gap).

## Fix (STRICTLY ADDITIVE -- CTO go-live gate keys on this)
`safe-commit.sh`: inserted a SEPARATE loop (own vars `_cf*`) between the byte-unchanged `-m` collection loop and the byte-unchanged `CS_OVR=` extract, that ALSO folds any `-F`/`--file` body-FILE contents into `CS_MSG`.
- **The existing `-m` read, the `CS_OVR` extract (`:541`->now `:563`), and the `:547-554` block are BYTE-UNCHANGED.** `git diff` shows **0 removed lines** -- pure insertion.
- **F-010-safe:** the `-F` file is NEVER shell-parsed; reading the trailer from its contents adds zero injection surface (unlike `-m`).
- **Forms handled:** the mandated `-F <file>`, plus `--file <file>` / `--file=<file>`. Skips `-F -` (stdin) safely.
- **Trailer forms honored:** BOTH `# system-current-override: <reason>` (the codebase `# <marker>:` comment convention, cf. `# never-override:` / `# rail-checked:` -- the literal form in the TO/GO) AND plain `system-current-override: <reason>` ("identical to -m"). An optional leading `# ` is normalized inside the new `-F` read only -- the extract sed stays byte-unchanged.
  - NOTE (surfaced): the TO/GO wrote the trailer as `# system-current-override:` but the byte-unchanged extract sed has no `#` handling; supporting BOTH forms is the only reading consistent with every clause ("# ... READ+honored" AND "identical to -m"). If CVO/CTO want `#`-only or plain-only, it is a one-line change in the new loop.

## Self-test -- end-to-end on the REAL safe-commit.sh (9/9 PASS)
Harness: `deliverables/safe-commit-F-read-selftest.sh`. Method: isolated temp git repos + a stub `comp-system` (rc controlled) so the override-read block actually runs; asserts exit code AND whether an audited override was written.

| Case | Args | Expect | Result |
|---|---|---|---|
| P0 positive control | `-m` normal, **no drift (rc0)** | commit proceeds, no override | PASS |
| A1 | `-F` body w/ `# system-current-override:` | proceed + audit | PASS |
| A1b | `-F` body w/ plain `system-current-override:` | proceed + audit | PASS |
| A2 | `-F` body, NO trailer | BLOCKED, no false override | PASS |
| A3 | `--file=<body #-form>` | proceed + audit | PASS |
| A4 | `--file <body #-form>` | proceed + audit | PASS |
| B1 | `-m` w/ trailer (existing path) | proceed + audit | PASS |
| B2 | `-m` NO trailer (existing path) | BLOCKED | PASS |
| E1 | `-F -` (stdin) | no crash -> BLOCKED | PASS |

`bash -n` PASS. `git diff` removed-line count = 0.

## No-regression / orthogonality
- **F-010 unchanged:** it lives in `never-rules-gate.sh` (a separate PreToolUse hook); this change does not touch it. `-m`-with-`$(` still denies.
- **`-m` path unchanged:** B1/B2 byte-for-byte behavior; positive control P0 proves non-drift commits (the overwhelming majority, which never reach the block) are untouched.
- **Only ONE copy** of `system-current-override` / `comp-system --gate` exists (safe-commit.sh:532) -- no second copy in the dormant queue worker.

## Out of scope (noted, NOT touched)
- `:530` trigger scope-calibration (over-firing on DS WIP ledgers) -- DEFERRED per CTO.
- The dormant QUEUE path (`SAFE_COMMIT_USE_QUEUE=1`) `exit`s at `:157` before the `:530` comp-system gate, so that gate is legacy-path-only today. Pre-existing; a TO-6-cutover concern for whoever owns the worker parity. Flagged, untouched.

## Gate status
- BUILD + SELF-TEST: DONE (this doc).
- CVO independent verify (both limbs: fix works AND strictly-additive) BEFORE go-live: **PENDING** (candidate is in the working tree for verify-on-the-real-file).
- CTO apply-gate (the live commit of modified safe-commit.sh, at a quiet window -- NOT during coherent-9 / MDPF flip / cot apply): **PENDING**. I do NOT commit the live change myself.
