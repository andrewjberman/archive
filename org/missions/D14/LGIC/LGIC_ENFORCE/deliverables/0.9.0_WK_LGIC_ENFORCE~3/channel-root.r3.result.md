# Result -- LGIC_ENFORCE.TO-EN-i-3-r3 (proof-of-spec-check resolves a cited row from the INSTANCE's checkout, LGIC_NAMING-S21)

Assignee: `0.9.0_WK_LGIC_ENFORCE~3` | Worktree: `wk-lgic-enforce-3-3` | Artifact commit: PENDING-THIS-COMMIT (rides this same commit)

## What changed

One file: `.tools/proof-of-spec-check.py`. THE DEFECT: `_channel_row_ids(code)` globbed `WORKSPACE`
(`Path(__file__).resolve().parent.parent` -- this SCRIPT's own checkout) unconditionally, so a checker
running from one checkout but graded against an instance whose `surprises` row is committed only in a
DIFFERENT checkout (a linked worktree, a side branch) read that row as absent, even though it was
committed in the GRADED tree.

THE FIX:

- New `_instance_checkout_root(inst_path)` walks up from `inst_path` to the nearest ancestor carrying a
  `.git` entry (a directory in a main checkout, a FILE in a linked worktree -- `.exists()` covers both),
  and returns that as the root. Falls back to `WORKSPACE` when `inst_path` is `None` or no `.git` is
  found above it, so a caller that never passes `inst_path` is byte-identical to before.
- `_channel_row_ids(code, root=None)` grows an optional `root` parameter (default `WORKSPACE`, the
  pre-existing behaviour).
- `surprises_check(..., inst_path=None)` grows an optional `inst_path` parameter, used ONLY when
  `row_ids` is not injected by the caller (the self-test's existing arms A-L inject `row_ids` directly and
  never touch this path).
- `main()` now calls `surprises_check(inst, inst_path=Path(args[0]))`, mirroring the pattern
  `artifact_resolution_check` already uses for the same argument (`:2300`/`:2305`).

Every other limb (`_governing_is_tree`/`_resolve_governing_to`, alignment, artifact-resolution,
invocation-alignment, count-bar, drives, binding) is untouched, per BOUNDS ("Change only the
channel-resolution root").

New self-test arm **M** (`_channel_root_arm`, inside `_self_test()`): builds a throwaway repo (a `.git`
marker dir plus a planted channel row for project `NFRA_TESTPROJ`, absent from this script's own
checkout -- premise-checked via `_channel_row_ids` before asserting), then calls `surprises_check`
directly with `inst_path` pointed inside that throwaway repo and `row_ids` left uninjected, so
`_instance_checkout_root` + `_channel_row_ids` genuinely run. Asserts the row resolves (`0 violations`,
frame says `1 resolve to a channel row`).

## Acceptance

| id | invocation | expect | result |
|---|---|---|---|
| I3R3-AC1 | `check_en_r3.py i3-channel-root` | `PASS-I3-ROOTED-AT-INSTANCE-CHECKOUT` | PASS |
| I3R3-AC2 | `proof-of-spec-check.py --self-test` | `RESULT: ([0-9]+) of \1 arm(s) behaved` | PASS (`45 of 45`) |

Both criteria PASS by output, re-run twice each, byte-identical stdout+stderr both times (determinism,
below).

## Controls

**Mutant** (load-bearing check): a scratch copy of the fixed script (`.scratch/mutant_proof_of_spec_check.py`,
committed bytes never touched) with the ONE fix line reverted --
`_channel_row_ids(code, _instance_checkout_root(inst_path))` back to the pre-fix `_channel_row_ids(code)`
(root argument dropped). Run through the fixed input's own `i3-channel-root` arm against the mutant path:
verdict flips from `PASS-I3-ROOTED-AT-INSTANCE-CHECKOUT` to `FAIL-I3-ROOTED-AT-SCRIPT-CHECKOUT` (rc 0 -> 1),
frame's `resolve to a channel row` count drops from 1 to 0 -- FIRED-AS-EXPECTED.

**Determinism:** both AC1's and AC2's invocations run twice back-to-back on the identical tree; captured
stdout+stderr diffed byte-for-byte, empty diff both pairs (`.scratch/ac1_run{1,2}.log`,
`.scratch/ac2_run{1,2}.log`) -- STABLE.

## Proof of spec

`org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~3/LGIC_ENFORCE.TO-EN-i-3-r3.channel-root.proof_of_spec.json`,
validated with
`python .tools/proof-of-spec-check.py <instance> I3R3-AC1,I3R3-AC2 --governing-order org/missions/D14/LGIC/LGIC_ENFORCE/task-orders/LGIC_ENFORCE.TO-EN-i-3-r3.channel-root.md`
before the `complete` flip.
