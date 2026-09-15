# LGIC_ENFORCE.TO-EN-f-1 -- the fence, authored: result (re-run)

**Worker:** `0.9.0_WK_LGIC_ENFORCE~1`, worktree `.worktrees/wk-lgic-enforce-1-1-f1r`, branch `wk-lgic-enforce-1-1-f1r`,
base CLOUD @`9a05002d39`. **Cell:** `EN-f-1` (PRD candidate E5, first half; DEC-4). **Nothing was applied.**

**Status: every mechanical criterion PASSES by output on this run.** F1-AC1 through F1-AC5 all read PASS.
F1-J1 is graded by 3.0.0_SA_CVO at L9.

## What this run did

This is a re-run. The cell's work was built by this slot's earlier run and merged at this base (drain
@`07cb65ab63`). That run read F1-AC4 FAIL because its checker launched a bare `aws` (row `LGIC_ENFORCE-W1-S16`).
The checker was fixed at @`c30637c49c` (issuer row `LGIC_ENFORCE-S11`).

This run rebuilt, re-planned, re-opened and closed nothing. It did three things:

- re-ran every criterion from this worktree;
- ran one negative control for F1-AC4, which the earlier run could not run;
- updated this file and the proof instance.

## The artifacts, pinned to the commits that carried them

Each pin below is an ancestor of HEAD `9a05002d39`, checked with `git merge-base --is-ancestor` (positive control:
`HEAD~1` is an ancestor). `git diff --stat <pin> HEAD` over each set is empty, so every artifact is unchanged since
its pin.

| Pin | Artifacts |
|---|---|
| `080e1b97c6` | `infra/logic/registry/exemptions.json`; module `opal_name` `main.tf`, `generated_locals.tf`, `tests/vectors.json`; `shared-infra/s3-49financial.tf`; `shared-infra/lgic-enforce-fence-probes.tf` |
| `887cf01419` | `fence_plan.json`; `FENCE_PRIOR_POLICY.json` (428 bytes); the ledger sentinel; the ledger entry `20260915T0334Z_lgic-enforce-fence-49financial_deploy_completion.md`; `FENCE_PLAN.md` |
| `080e1b97c6`, `103a4348a4` | Rows W1-S13..S15 and W1-S16..S17 in `INVESTIGATION_v1.md` |

## Criteria (outputs verbatim in the proof instance)

| id | verdict | deciding line | rc |
|---|---|---|---|
| F1-AC1 | PASS-by-output | `WRITERS OF opal-data-49financial: 16  COVERED: 16  UNCOVERED: []` | 0 |
| F1-AC2 | PASS-by-output | `DENY REGION FOUND: True  TYPED ARN LITERALS: []` | 0 |
| F1-AC3 | PASS-by-output | `CHANGES: {('create', 'aws_iam_role'): 3, ('create', 'aws_iam_role_policy'): 3, ('update', 'aws_s3_bucket_policy'): 1} ... OTHER: []` | 0 |
| F1-AC4 | PASS-by-output | `PRIOR == LIVE (read now): True` (read 2026-09-15T06:00:15Z..06:00:26Z; again at 06:08:19Z, identical) | 0 |
| F1-AC5 | PASS-by-output | `STATUS: OPEN  LEGS: ['L1', 'L2', 'L3', 'L4']  L1 PROOF COMMIT EXISTS: True` | 0 |
| F1-J1 | RECORDED (judgment) | graded by 3.0.0_SA_CVO at L9; the artifact is `FENCE_PLAN.md`@`887cf01419` | -- |

## F1-AC4's negative control

This control tests whether F1-AC4's PASS could appear if the claim were false.

**Setup.**
- Two scratch directories under `.scratch/mut_prior/`. Each holds only `.tools/git_bash_resolver.py`, `.tools/aws`
  and a copy of `FENCE_PRIOR_POLICY.json`.
- The unchanged fixed `check_en.py` runs `f1-prior` by absolute path, with each directory as its working directory.
- Each run reads the live policy through the shim, read-only.

**Arms.**

| Arm | Change to the copy | Result |
|---|---|---|
| unmutated | none | `PRIOR == LIVE (read now): True`, `PASS-PRIOR-VERBATIM`, rc=0 |
| drop_pattern | `role/opal-assets-mdpf-*` removed from the Deny's `ArnLike` (3 of 4 left) | `PRIOR == LIVE (read now): False`, `FAIL-PRIOR-DIFFERS`, rc=1 |

**Reading.** The unmutated arm rules out an environment failure in the scratch setup. So the drop_pattern FAIL is
a real difference, and the instrument can go non-zero. No fixed input was edited.

## Rows

None filed by this run. Rows W1-S13..S17 are this slot's earlier run's, and they stay in the proof's `surprises`.
The checker fix @`c30637c49c` states that it disarms W1-S16. Its row is not edited.

## Not claimed

- Nothing was applied, and no principal was probed. The fence reaches the live plane only through EN-f-2, after
  gate G-E. That gate is the two SIGNOFF lines, which belong to `1.0.0_SA_CTO` and `2.0.0_SA_COO~G`; they were not
  touched.
- The mutant arms for F1-AC1, AC2, AC3 and AC5 are the earlier run's. They were not re-run here, because the
  artifacts they read are unchanged since their pins (see the pin table).
- The access partition in `FENCE_PLAN.md` covers the census population and the plan. It is not a sweep of every
  IAM principal.
