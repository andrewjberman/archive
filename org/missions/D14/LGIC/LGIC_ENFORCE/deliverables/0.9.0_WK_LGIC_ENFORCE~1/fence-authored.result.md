# LGIC_ENFORCE.TO-EN-f-1 -- the fence, authored: result

**Worker:** `0.9.0_WK_LGIC_ENFORCE~1`, worktree `.worktrees/wk-lgic-enforce-1-1-f1`, branch `wk-lgic-enforce-1-1-f1`,
base CLOUD @`39aae459ed`. **Cell:** `EN-f-1` (PRD candidate E5, first half; DEC-4). **Nothing was applied.**

**Status: the order stays OPEN.** F1-AC4 reads FAIL by its output: the checker's `aws` read cannot start on this
box (row `LGIC_ENFORCE-W1-S16`). F1-AC1, F1-AC2, F1-AC3 and F1-AC5 PASS by output. F1-J1 is 3.0.0_SA_CVO's, at L9.

## What landed

| Commit | What |
|---|---|
| `080e1b97c6` | The authored change (ledger leg L1): `exemptions.json` rows, module output, the Deny, the probe roles, rows W1-S13..S15 |
| `887cf01419` | The ledger entry and sentinel (OPEN, L1 closed), `FENCE_PRIOR_POLICY.json`, `fence_plan.json`, `FENCE_PLAN.md` |
| next commit | Rows W1-S16 and W1-S17 |
| the commit after | This result file and the proof instance |

- **`infra/logic/registry/exemptions.json`.** 16 rows under `opal-data-49financial`, one for each principal of
  that bucket in `FENCE_WRITER_CENSUS.md` (16 of 16). `fence_patterns("49financial")` matches none of them.
  - Each row has `reason`, drawn from the census grant and token basis.
  - Each row has `signoff_ref`, naming the ledger entry and its two SIGNOFF lines.
  - Each row has `arn`, the census ARN (row W1-S15).
  - `validate` reads OK at registry@`ba5318901b937130`.
- **`infra/aws/terraform/modules/opal_name/`.** `generated_locals.tf` and `tests/vectors.json` are regenerated
  at the new registry hash; only their header lines change. `main.tf` adds output `fence_exemption_arns`, read from
  `exemptions.json` with `file()` and `jsondecode()`, because `generate()` renders no exemptions local (row W1-S13).
  The module tests pass: `terraform test` 37 of 37, no `data "external"`.
- **`shared-infra/s3-49financial.tf`.** The four typed patterns of `DenyForeignFirmPrincipals` are replaced by an
  `ArnNotLike` over `concat(module.opal_name.fence_patterns["49financial"], module.opal_name.fence_exemption_arns[<bucket>])`.
  A `REPLACED` notice follows the old comment, and `module "opal_name"` is declared beside the policy. The
  LGIC_NAMING notice (`:16-20`) and the read-logging block are untouched.
- **`shared-infra/lgic-enforce-fence-probes.tf`.** Three roles, each named by module `opal_name`, with the system
  held at `mdpf` and only the scope varied:
  - `mdpf-49f-fenceprobe-role`
  - `mdpf-cot-fenceprobe-role`
  - `mdpf-fenceprobe-role`

  Each has one inline policy, GetObject and ListBucket on `opal-data-49financial` only, and trusts this
  account's root.
- **The plan.** Read-only, `plan -lock=false`, as `user/Andrew_Berman`: `Plan: 6 to add, 1 to change, 0 to
  destroy`. 7 of 238 resource changes are not no-op. The plan's `before` policy equals `FENCE_PRIOR_POLICY.json`.
  The `after` policy holds 17 ArnNotLike values: 1 derived pattern and the 16 exemption ARNs.
- **The ledger.** `lgic-enforce-fence-49financial` is OPEN with legs L1..L4, and L1 is closed with `080e1b97c6`.
  The entry and its sentinel are committed. Two blank SIGNOFF slots are left for `1.0.0_SA_CTO` and
  `2.0.0_SA_COO~G`; the tool's next re-render erases them (row W1-S17).
- **`FENCE_PLAN.md`.** The sign-off packet:
  - the blast radius (7 resources);
  - every principal whose access changes, partitioned by denied-before and denied-after;
  - the rollback for each touched resource;
  - four branches.

## Criteria (outputs verbatim in the proof instance)

| id | verdict | deciding line |
|---|---|---|
| F1-AC1 | PASS-by-output | `WRITERS OF opal-data-49financial: 16  COVERED: 16  UNCOVERED: []` |
| F1-AC2 | PASS-by-output | `DENY REGION FOUND: True  TYPED ARN LITERALS: []` |
| F1-AC3 | PASS-by-output | `CHANGES: {('create', 'aws_iam_role'): 3, ('create', 'aws_iam_role_policy'): 3, ('update', 'aws_s3_bucket_policy'): 1} ... OTHER: []` |
| F1-AC4 | **FAIL** | `PRIOR == LIVE (read now): False  NOT RUNNABLE: [WinError 2] The system cannot find the file specified` |
| F1-AC5 | PASS-by-output | `STATUS: OPEN  LEGS: ['L1', 'L2', 'L3', 'L4']  L1 PROOF COMMIT EXISTS: True` |
| F1-J1 | RECORDED (judgment) | graded by 3.0.0_SA_CVO at L9 |

F1-AC4's FAIL is the instrument's. The same comparison through the `.tools/aws` shim read the file byte-equal
(428 bytes) to the live policy at 2026-09-15T04:18:57Z, and a negative control read unequal. That supports the
record. It is not the criterion's output, and the order is not flipped on it.

## Rows filed

| Row | Class and hazard | Subject |
|---|---|---|
| W1-S13 | OBSERVATION, INERT | Exemptions reach the policy through a module local, not a generated local |
| W1-S14 | OBSERVATION, ARMED (2.0.0_SA_COO~G) | 7 generated views outside the grant carry the old registry hash; header-only, measured |
| W1-S15 | OBSERVATION, INERT | Rows carry `arn`, because the checker keys by name and the policy needs the true ARN |
| W1-S16 | BLOCKING, ARMED (2.0.0_SA_COO~G) | F1-AC4's `aws` cannot start from Python on this box |
| W1-S17 | OBSERVATION, ARMED (2.0.0_SA_COO~G) | The ledger tool's re-render erases the SIGNOFF slots |

## Not claimed

- Nothing was applied, and no principal was probed.
- The access partition in `FENCE_PLAN.md` is over the census population and the plan. It is not a sweep of every
  IAM principal.
- The naming gate (WARN mode) printed REFUSE verdicts on three probe-file lines: the `"49f"`/`"cot"` map keys, and
  the inline policy name `fenceprobe-read-opal-data-49financial`. It printed OUT-OF-PATTERN on the `"49financial"`
  index in the Deny. None blocked, and they are left as authored, because the probe file is removed at L4.
