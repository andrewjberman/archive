# FE-s-43 RESULT -- the L7->L8 receiving route binds the governing order

Order: `IRPT_FNTEND.TO-FE-s-43` | Worker: `0.9.0_WK_IRPT_FNTEND~4` | Branch: `wk-irpt_fntend-7-4-fe-s-43` from CLOUD `4d11c008c2`
Ruling: `1.0.0_SA_CTO` RULING AA (round-6 analysis @4713211d87 s.3), on row `IRPT_FNTEND-W4-S14` as graduated by `3.0.0_SA_CVO` (C-S90).

## What changed (commit `e21a8c6116`)

`.tools/receiving-check.py`
- **The binding.** The proof-of-spec route takes `--governing-order <order>`. It hands the order to
  `proof-of-spec-check.py` as `--governing-order <absolute path>`. The path is made absolute because the checker
  resolves a relative path against ITS OWN tree, not the caller's cwd.
- **NOT-BOUND.** A proof-of-spec instance received with no order returns `NOT-BOUND` and runs nothing. It is never
  `ACCEPT`, and it is never a verdict the instance's own `decomp_ref.to_ref` steered. The run exits rc 1 on `HAND BACK`
  or `NOT-BOUND`.
- **Scope.** `BOUND_TOOLS` names the only route that takes the order. No other route's argv-builder is ever handed
  it: PRD, addendum, task order, surprise rows and register row are unchanged, and `--self-test`'s BINDING-SCOPE arm
  shows 6 of 6.
- **The reporter wraps and never truncates** (row `IRPT_FNTEND-W4-S17`). The cut printed `line[:150]`, so FE-s-28's path
  fell off the binding violation. A wrapped continuation carries a `:` gutter, because the checker indents its own
  lines and a `|` continuation read the same as an indented line.
- **Self-test.** Three binding controls were added: NOT-BOUND runs nothing; the argv form; no other route moves.

`.tools/tests/test_receiving_binding.py` (new). FE-s-29's real close is committed in two scratch indexes that borrow
this repository's objects. The two differ ONLY in the instance's `to_ref` bytes. Every file the battery inspects is
read as a committed blob (RULING AC). The binding is tested through the CLI and through `run_one`.

## Criteria (final runs at `e21a8c6116`; AC8 at `e21a8c6116`)

| id | deciding output | verdict |
|---|---|---|
| F43-AC1 | `[to-pipeline-gate --self-test] RESULT: 0 arm(s) failed of 72` (rc 0) | PASS-by-output |
| F43-AC2 | `RESULT: 42 of 42 arm(s) behaved` (rc 0) | PASS-by-output |
| F43-AC3 | `DOCTORED to_ref, BOUND THROUGH THE RECEIVING ROUTE: HAND BACK` | PASS-by-output |
| F43-AC4 | `THE HAND-BACK NAMES BOTH PATHS: yes` | PASS-by-output |
| F43-AC5 | `UNBOUND INSTANCE THROUGH THE RECEIVING ROUTE: NOT-BOUND` | PASS-by-output |
| F43-AC6 | `POSITIVE CONTROL, FE-s-29 AS COMMITTED, BOUND: ACCEPT` | PASS-by-output |
| F43-AC7 | `EVERY OTHER ROUTE UNCHANGED: 5 of 5` | PASS-by-output |
| F43-AC8 | `EVERY .tools BATTERY THAT CALLS EITHER TOOL: 13 of 13 green` (64 files under .tools/tests/, 14 name either tool, the runner excluded) | PASS-by-output |
| F43-AC9 | judgment, graded at L9 by `3.0.0_SA_CVO` | RECORDED |

Beyond the criteria, the doctored close's binding violation is the checker's ONLY violation, so the hand-back is the
binding's and not a PENDING sentinel. The mutant control: the cut's route (@`edac45e48c`) ACCEPTS the same doctored
instance. That ACCEPT is the steered verdict the ruling exists for.

## THE CHANGE `.claude/skills/canonical-flow/SKILL.md` NEEDS (for that skill's owner; row `IRPT_FNTEND-W4-S16`)

This order names the skill NOT YOURS, so it is not edited here. There are three edits, all in Step 3b, citing lines @4d11c008c2:

1. In the bash block at `:352-354`, add a second line:
   ```bash
   .tools/receiving-check.py <instance.proof_of_spec.json> --governing-order <the task order it closes>   # L7 -> L8
   ```
2. In the verdict table, after the `HAND BACK` row (`:373`), add:
   `| NOT-BOUND | a proof-of-spec instance was handed over WITHOUT the order it closes. Nothing ran -- its own to_ref would have steered the verdict. Re-run with --governing-order <that order>; never build on it. |`
3. At `:368`, change `THE THREE VERDICTS` to `THE FOUR VERDICTS`.

## Consumers and scope

- **Callers.** No script calls `receiving-check`. Two scoped reads of `*.py/*.sh/*.ps1` found none: `.tools/` has only
  the tool itself and a comment at `prd-manifest-gate.py:161`, and `org/tier1_exec/3.0.0_SA_CVO/` has 0. The CVO's
  intake and audit scripts call `proof-of-spec-check.py` directly (row W4-S14), and that seat binds its own.
- **Census bound.** `comp-find` page 2 of the workspace census hit its bound (rc 143). The two scoped reads above are
  the census of the callers that matter.
- **Shared order.** One call binds one order. Several instances handed over with it are each refused by the checker
  if their `to_ref` or `to_id` names another order.
- **Checker wording.** The checker's violation says "the order being flipped" on this route too. That wording is the
  checker's (FE-s-44 may change the checker this round), and this cell did not touch it.
