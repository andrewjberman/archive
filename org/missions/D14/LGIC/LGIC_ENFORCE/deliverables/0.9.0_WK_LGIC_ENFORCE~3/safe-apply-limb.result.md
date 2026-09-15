# safe-apply-limb.result -- LGIC_ENFORCE.TO-EN-t-2 (cell EN-t-2, PRD candidate E8 second half)

**Worker:** `0.9.0_WK_LGIC_ENFORCE~3`, worktree `.worktrees/wk-lgic-enforce-1-3-t2`, branch `wk-lgic-enforce-1-3-t2`, cut from
CLOUD @`39aae459ed`. The build is commit `7691b6bc82`, LOCAL (not pushed; the COO drains it).

**Standing: the order stays OPEN (`<status>pending</status>`, not flipped).** T2-AC3 passes by output. T2-AC1 and T2-AC2
FAIL by output, for two environment reasons outside the grant (rows W3-S5 and W3-S6, both BLOCKING). Both named
invocations fail before a line of `.tools/safe-apply.sh` runs.

## 1. What landed

- `.tools/naming-apply-gate.py DIR [--enforce]`: the safe-apply limb. It is new and it is this cell's file.
- `.tools/safe-apply.sh`: ONE new stage, lines 79-113 (36 lines inserted, 0 deleted). It sits after the halt
  checkpoint (`:72`) and before the tag-authorization gate (header now at `:116`), so it runs before any plan.
  - WARN mode (the shipped state) never changes the exit code, on a REFUSE verdict, on `NAMING ERROR`, or on a missing
    interpreter or limb.
  - ENFORCE mode (`NAMING_GATE_ENFORCE=1` or `org/mcp/naming-gate.enforce`) is fail-closed: it exits 6 before terraform is
    called.
- The rows `LGIC_ENFORCE-W3-S5` to `W3-S9` in the channel, and the two control harnesses under `controls/`.

## 2. Which attributes it grades, and why (from TF_LABEL_CENSUS.md, EN-t-1)

- **Graded:** the own-name attribute of each top-level resource block in DIR's `*.tf` files, the files terraform loads for
  that root. That attribute is the string AWS names the object by, so it is what the opal_name module would have to produce.
  - The type map is the census's section 3, read from the commit limb's `TF_NODE` so the two limbs share one map. It holds
    the 28 graded types (for example `aws_sqs_queue.name`, `aws_lambda_function.function_name`,
    `aws_cloudwatch_metric_alarm.alarm_name`, `aws_instance` `tags.Name`, `aws_s3_bucket.bucket`).
  - It adds the census's 2 NOT-GRADED types (`aws_iam_user.name`, `aws_route53_record.name`), which print NOT-GRADED and
    pass. Total: 30 types.
- **Not graded:**
  - Labels. A label is the Terraform state address, never an AWS name. NAMING_SCHEMA keeps labels `not_covered`, the census
    graded them only outside the schema's domain (its section 1), and it shows no label that is an AWS name. The order
    grants label grading only in that case.
  - The 30 own-name types with no node type. grade() has nothing to grade them as; the census RAISES all 66 at G1.1.
  - Attributes of nested blocks, and module-call arguments. Neither is the resource's own name.
  - Expressions: references, calls, and templates with `${...}`. Their value exists only in a plan, and this stage runs
    before plan. They are listed as `unresolved before plan`; one read from an opal_name module call is marked
    module-produced (row W3-S9).

**The matrix at apply** (row W3-S8). DEC-6 decides NEW against a diff; an apply has no diff, and "is this resource being
added" is known only to a plan. So every graded name is read as the tree states it:

| grade() returns | the limb's line | counts as |
|---|---|---|
| OUT-OF-PATTERN or ALIAS | `NAMING REFUSE <file>:<line> <name> -> <canonical>` | REFUSE |
| RAISE | `NAMING REFUSE ... -> (rule or registry defect)`, why names the RAISE | REFUSE: PRD :255, "refused like any refusal once enforcing" |
| CONFORMANT | `NAMING CONFORMANT ... -> <name>` | pass |
| NOT-GRADED | `NAMING NOT-GRADED ... -> -` | pass |

- The output lines and the enforce switch are the commit limb's. After the verdict lines comes a
  `NAMING-APPLY: <DIR>: <files> .tf file(s), <n> resource-name attribute(s): <g> graded, <e> expression(s)` denominator
  line, then `NAMING-GATE: <PASS|WARN|REFUSE> <g> graded`.
- Verdict lines go to `org/mcp/naming-gate-verdicts.log` in mode `APPLY-WARN` or `APPLY-ENFORCE`. The log is gitignored by
  `*.log` and never committed.

## 3. The criteria (each run at 7691b6bc82, `cd <WS> && timeout 120 python .../check_en.py <sub>`)

| id | output | verdict |
|---|---|---|
| T2-AC1 | `rc=1  terraform called: False  <3>WSL (9 - Relay) ERROR: CreateProcessCommon:800: execvpe(/bin/bash) failed: No such file or directory` / `VERDICT: FAIL-NOT-REFUSED-BEFORE-PLAN`, rc 1 | FAIL |
| T2-AC2 | `rc=1  terraform called: False  <3>WSL (12 - Relay) ERROR: ...` / `VERDICT: FAIL-GOOD-TREE-BLOCKED`, rc 1 | FAIL |
| T2-AC3 | `LINES: halt gate 72  naming gate 81  tag-authz 116` / `VERDICT: PASS-STAGE-ORDER`, rc 0 | PASS |

**Why T2-AC1 and T2-AC2 cannot pass here:**

- **W3-S5.** `check_en.py:906` runs a bare `bash`. Windows CreateProcess searches the system directory before PATH, so it
  launches `C:\Windows\System32\bash.exe`, the WSL launcher, which fails. The pre-build baseline printed the same line.
- **W3-S6.** With Git Bash substituted, safe-apply.sh's halt checkpoint fails closed `IDENTITY UNRESOLVED` (exit 3) before
  the stage. It reads a principal only from `org/mcp/sessions/<CLAUDE_CODE_SESSION_ID>.serial` under the worktree root. That
  file is absent in a worker worktree, and the main tree's copy names the issuer, `2.0.0_SA_COO~G`.
- Neither the checker nor `org/mcp/sessions/` is in the grant. T2-AC3 fixes the stage after the checkpoint.

## 4. Controls (not criteria)

- **The stage, through the checker's own assertions** (`controls/t2_controls.py all`). It makes two disclosed
  substitutions: Git Bash for `bash`, and a pass-through halt library in a `.scratch` copy of safe-apply.sh.

  | variant | arm | observed |
  |---|---|---|
  | this build | refuse | rc 6, terraform not called, `VERDICT: PASS-REFUSED-BEFORE-PLAN` |
  | this build | pass | terraform called, `VERDICT: PASS-STAGE-PASSES` |
  | this build | warn (enforce unset) | terraform called, rc 0 |
  | mutant: 39aae459ed's safe-apply.sh, no stage | refuse | terraform called, `FAIL-NOT-REFUSED-BEFORE-PLAN` |
  | mutant | pass | `FAIL-GOOD-TREE-BLOCKED` |

  So the stage is what decides both assertions.
- **Coverage** (`controls/t2_coverage.py`). This checks the limb's reader against a different instrument, EN-t-1's census,
  at the census base `fd9c9ca174`:
  - 1266 rows from the reader and 1266 from the census, 0 on either side alone;
  - the literal/expression split is 1148/118 on both;
  - 0 literal values differ.
- **Exposure at HEAD** (the same script):
  - 78 Terraform roots and 1266 name attributes: 144 CONFORMANT, 3 NOT-GRADED, 593 REFUSE by canonical, 408 REFUSE as
    RAISE, 118 expressions.
  - **57 of 78 roots would be refused under ENFORCE** (row W3-S8).
- **Determinism:** two runs over the bad tree are byte-identical (623 bytes, sha256 `91db191c...71d5`).

## 5. Rows filed

| id | class | hazard | what |
|---|---|---|---|
| W3-S5 | BLOCKING | ARMED (2.0.0_SA_COO~G) | the checker's bare `bash` is the WSL launcher on this box |
| W3-S6 | BLOCKING | ARMED (2.0.0_SA_COO~G) | the halt checkpoint cannot name a principal in a worker worktree |
| W3-S7 | OBSERVATION | INERT | `BadQueueName` RAISES: no canonical form exists; this limb refuses a RAISE once enforcing, the commit limb warns |
| W3-S8 | OBSERVATION | ARMED (2.0.0_SA_COO~G) | no NEW/EXISTING at apply; one switch; 57 of 78 roots refused under ENFORCE |
| W3-S9 | OBSERVATION | INERT | 118 of 1266 name attributes are expressions, not graded before plan |

## 6. Not claimed

- That T2-AC1 or T2-AC2 passes. The control harness's PASS lines are controls, not the criteria's invocations.
- Anything live. Every safe-apply run used the checker's stub terraform, and the enforce file stays absent.
- The significance of any row. Each row records form only.
