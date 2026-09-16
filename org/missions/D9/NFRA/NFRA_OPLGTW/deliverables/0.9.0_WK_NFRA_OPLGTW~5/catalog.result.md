# NFRA_OPLGTW.TO-OG-k-1 -- the authorized catalog and the assumed-role credential adapter

Worker `0.9.0_WK_NFRA_OPLGTW~5`, worktree `/c/tmp/wk-oplgtw-1-5c`, branch `wk-nfra_oplgtw-1-5c`.
COLD START on a PARKED worktree: a previous worker's uncommitted drafts (`app/integrations/base.py`
modified, `app/integrations/schwab/{aws_roles.py,catalog.py}` and
`tests/test_schwab_catalog.py` untracked) were read, every criterion re-run from scratch by this
worker, and kept -- no prior run counted as evidence.

Code commit: `6a77fbc7ef` (LOCAL on `wk-nfra_oplgtw-1-5c`).

## Bar

- HEAD `wk-nfra_oplgtw-1-5c`, base `f4c7184f6d`. `test -d org && test -d .tools` -> `TREE-OK`.
- OG-z-1 (`f4c7184f6d`), OG-c-1 (`1f03a3f209`) and OG-d-1 (`8d8b221ee6`) confirmed ancestors of HEAD
  by `git merge-base --is-ancestor`.
- Surprise channel: highest existing `W5` id was `S2` in both this worktree and the shared tree
  (`/c/Users/AndrewBerman/Desktop/ajb_workspace`) before this order; this order's row is `S3`.

## Acceptance (17 of 17 PASS by output)

Each test prints its own denominators with `capsys` disabled; the full pytest output for every
criterion is in this worker's `.scratch/ac0<n>.log` (not committed -- `.scratch/` is gitignored and
never a deliverable). Summary, one line each, `rc` and the deciding pytest line:

| id | test | rc | deciding line |
|---|---|---|---|
| OGK1-AC1 | test_ogk1_ac01 | 0 | `1 passed in 2.64s` |
| OGK1-AC2 | test_ogk1_ac02 | 0 | `1 passed in 3.16s` |
| OGK1-AC3 | test_ogk1_ac03 | 0 | `1 passed in 1.84s` |
| OGK1-AC4 | test_ogk1_ac04 | 0 | `1 passed in 1.82s` |
| OGK1-AC5 | test_ogk1_ac05 | 0 | `1 passed in 3.19s` |
| OGK1-AC6 | test_ogk1_ac06 | 0 | `1 passed in 2.53s` |
| OGK1-AC7 | test_ogk1_ac07 | 0 | `1 passed in 1.79s` |
| OGK1-AC8 | test_ogk1_ac08 | 0 | `1 passed in 1.87s` |
| OGK1-AC9 | test_ogk1_ac09 | 0 | `1 passed in 1.66s` |
| OGK1-AC10 | test_ogk1_ac10 | 0 | `1 passed in 1.52s` |
| OGK1-AC11 | test_ogk1_ac11 | 0 | `1 passed in 3.00s` |
| OGK1-AC12 | test_ogk1_ac12 | 0 | `1 passed in 3.10s` |
| OGK1-AC13 | test_ogk1_ac13 | 0 | `1 passed in 1.79s` |
| OGK1-AC14 | test_ogk1_ac14 | 0 | `1 passed in 2.61s` |
| OGK1-AC15 | test_ogk1_ac15 | 0 | `1 passed in 2.65s` |
| OGK1-AC16 | test_ogk1_ac16 | 0 | `1 passed in 2.70s` |
| OGK1-AC17 | test_ogk1_ac17 | 0 | `1 passed in 3.60s` |

Full module together (post-mutant-revert regression + determinism check): `17 passed in 24.25s`.

## Controls

**Mutant.** Two mutants, each applied to the tracked file with the Edit tool, run against the
one criterion it targets, then reverted (confirmed by `git diff --stat` returning empty) before
the next test ran:

- M1 (`catalog.py` `membership_findings`, per-object master check at the line reading
  `if key_master != master:`): changed to `if False and key_master != master:`. Expected: AC7's
  "another master" arm stops rejecting. Observed: `test_ogk1_ac07` FAILED --
  `AssertionError: assert 'incomplete' == 'rejected'` (`- rejected` / `+ incomplete`). Reverted;
  `test_ogk1_ac07` returned to `1 passed in 2.81s`.
  (A first attempt mutated the marker/closure-level master check in the same function instead;
  AC7 stayed GREEN because the per-object key-parse check below it independently catches the
  fixture's foreign-master arm -- a real redundancy, not a control defect. Recorded here rather
  than silently discarded: the SECOND, correctly-targeted mutant is the one that fires.)
- M2 (`aws_roles.py` `role_configs`, the ExternalId-reuse refusal): changed
  `if configs[READER].external_id == configs[CATALOG].external_id:` to
  `if False and configs[READER].external_id == configs[CATALOG].external_id:`. Expected: AC1's
  "one ExternalId reused" refusal arm stops raising. Observed: `test_ogk1_ac01` FAILED --
  `Failed: DID NOT RAISE <class 'app.integrations.schwab.aws_roles.RoleConfigError'>`. Reverted;
  `test_ogk1_ac01` returned to `1 passed in 2.26s`.

Status: **FIRED-AS-EXPECTED** (both mutants fired on their target test; both reverts left the
tracked files byte-identical to the pre-mutant state, confirmed by an empty `git diff --stat`).

**Determinism.** Every criterion ran once standalone (table above) and the whole module ran
again together in one process after both mutants were reverted: `17 passed in 24.25s`, matching
the 17 individual passes with no new failure. AC8's persistence test and AC9's immutability test
depend only on the moto DynamoDB emulator's own conditional-write semantics (not on wall-clock
timing), and AC11/AC14's window arithmetic runs off the fixture's fixed `CLOCK` constant, not the
real clock. Status: **STABLE**.

## Declared exclusions

- **Deploy.** Nothing deploys (order bound). `.venv-og` and `.scratch/` are not committed.
- **A full-suite regression run of every other gateway test module in one process.** The box is
  heavily loaded (~96% CPU per hand-off); tests ran one module or one test at a time. As a bounded
  sanity check on the bound "Existing AuthKind values and their integrations keep their behaviour"
  (base.py gained a new enum member), `test_min_tier_gate.py` (3 passed) and
  `test_data_entitlement_guard.py` (12 passed) were run standalone, both clean. A whole-suite run
  was not attempted; not a criterion of this order.
- **Schwab object reads.** None: OGK1 is offline-only against moto; no Schwab object is read at
  any point (order bound).

## Surprise filed

`NFRA_OPLGTW-W5-S3` (OBSERVATION, INERT): the hand-off names
`tests/test_identity_scope.py::test_scoped_deny_by_default` as "the known red test" that "fails at
the cut base", with an instruction never to edit it or `identity_tool_allowlist.txt`. Neither file
carries any change in this worktree (both clean at HEAD `f4c7184f6d`), and the test PASSES
(`1 passed in 0.07s`). Filed and disposed as a form-only mismatch; no criterion of this order
reads that test, and no edit was made to either named file.

## Tools

- `.tools/commit-gate.sh` on the four touched `.py` files: `OK: pre-commit gate clean for 4 of 4
  file(s)`.
- `.tools/safe-commit.sh --author "0.9.0_WK_NFRA_OPLGTW~5 <...>" -F <msgfile> --` on the code +
  test files + the surprise-channel row: `6a77fbc7ef` (LOCAL on `wk-nfra_oplgtw-1-5c`), commit-gate
  / naming-gate / to-pipeline-gate / surprise-corpus / surprise-row-gate / missions-tree-check all
  clean in the same run.
