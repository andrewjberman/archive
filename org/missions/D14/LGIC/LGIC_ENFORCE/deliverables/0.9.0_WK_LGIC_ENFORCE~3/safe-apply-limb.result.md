# safe-apply-limb.result -- LGIC_ENFORCE.TO-EN-t-2 (cell EN-t-2, PRD candidate E8 second half)

**Worker:** `0.9.0_WK_LGIC_ENFORCE~3`.
- **This run (the re-run):** worktree `.worktrees/wk-lgic-enforce-1-3-t2r`, branch `wk-lgic-enforce-1-3-t2r`, cut from
  CLOUD @`9a05002d39`. That base carries the build drain @`aef1822de4` and the checker fix @`c30637c49c` (issuer row
  `LGIC_ENFORCE-S10`).
- **The build:** commit `7691b6bc82` (first run, branch `wk-lgic-enforce-1-3-t2`). This run edits neither the limb nor the
  stage. `git diff --stat 7691b6bc82 HEAD` over `.tools/naming-apply-gate.py`, `.tools/safe-apply.sh` and `controls/` is
  empty at `9a05002d39`.

**Standing: all three criteria PASS by output on this run, and the order is flipped `complete`.** The first run's
T2-AC1 and T2-AC2 failed in the checker before `.tools/safe-apply.sh` ran (rows W3-S5 and W3-S6). The issuer fixed the
checker @`c30637c49c` and recorded the disarm as row S10.

## 1. What landed (at 7691b6bc82, unchanged)

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

## 3. The criteria (this run, 2026-09-15 ~06:02Z, at 9a05002d39)

Each was run as `cd C:/Users/AndrewBerman/Desktop/ajb_workspace/.worktrees/wk-lgic-enforce-1-3-t2r && timeout 120 python
org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/2.0.0_SA_COO~G/fixed_inputs/check_en.py <sub>`. The outputs below are
verbatim, with CR removed. The checker's first line prints a tail of safe-apply's output, cut mid-path by the checker itself.

| id | output (verbatim) | exit | verdict |
|---|---|---|---|
| T2-AC1 | `rc=6  terraform called: False  uts/tests/t2/bad_tree: 1 .tf file(s), 1 resource-name attribute(s): 1 graded, 0 expression(s) not graded before plan (0 module-produced)` / `[naming-apply-gate] NAMING-GATE: REFUSE 1 graded` / `safe-apply: BLOCKED by the naming limb (LGIC_ENFORCE DEC-6, ENFORCE mode, rc=1). Nothing was planned or applied.` / `VERDICT: PASS-REFUSED-BEFORE-PLAN` | 0 | PASS |
| T2-AC2 | `rc=3  terraform called: True  ables/2.0.0_SA_COO~G/fixed_inputs/tests/t2/good_tree.` / `[tombstone-gate] BLOCKED (rc=3): cannot parse the plan JSON -- Expecting value: line 1 column 1 (char 0)` / `[tombstone-gate]   Render it with: terraform show -json <planfile>` / `safe-apply: TOMBSTONE GATE BLOCKED this apply (rc=3). Nothing was applied.` / `VERDICT: PASS-STAGE-PASSES` | 0 | PASS |
| T2-AC3 | `LINES: halt gate 72  naming gate 81  tag-authz 116` / `VERDICT: PASS-STAGE-ORDER` | 0 | PASS |

- **T2-AC1, denominator 1 of 1 tree (`tests/t2/bad_tree`):** 1 `.tf` file, 1 resource-name attribute, 1 graded, 0
  expressions. The stage exited 6 and the stub terraform was not called.
- **T2-AC2, denominator 1 of 1 tree (`tests/t2/good_tree`):** the stage passed and the stub terraform was called.
  - The `rc=3` comes later, from the tombstone gate: the stub terraform writes no plan JSON.
  - That gate runs after the plan, so it is downstream of this cell's stage. The checker's assertion is "terraform called",
    and it held.
- **T2-AC3, denominator: three first-match line numbers in `.tools/safe-apply.sh`:** 72 < 81 < 116.

**The first run, kept on the record** (at 7691b6bc82, before the checker fix):
- T2-AC1 printed `rc=1  terraform called: False  <3>WSL (9 - Relay) ERROR: ...` then `VERDICT: FAIL-NOT-REFUSED-BEFORE-PLAN`.
- T2-AC2 printed the same WSL line then `VERDICT: FAIL-GOOD-TREE-BLOCKED`.
- Rows W3-S5 (a bare `bash` resolved to the WSL launcher) and W3-S6 (the halt checkpoint could not resolve identity in a
  worktree). Row S10 is the issuer's disarm: `run_bash()` goes through `.tools/git_bash_resolver.py`, and a synthetic
  session file is removed in a `finally` block.

## 4. Controls (not criteria; first run, at 7691b6bc82)

- **The stage, through the checker's own assertions** (`controls/t2_controls.py all`). It makes two disclosed
  substitutions: Git Bash for `bash`, and a pass-through halt library in a `.scratch` copy of safe-apply.sh.

  | variant | arm | observed |
  |---|---|---|
  | this build | refuse | rc 6, terraform not called, `VERDICT: PASS-REFUSED-BEFORE-PLAN` |
  | this build | pass | terraform called, `VERDICT: PASS-STAGE-PASSES` |
  | this build | warn (enforce unset) | terraform called, rc 0 |
  | mutant: 39aae459ed's safe-apply.sh, no stage | refuse | terraform called, `FAIL-NOT-REFUSED-BEFORE-PLAN` |
  | mutant | pass | `FAIL-GOOD-TREE-BLOCKED` |

  So the stage is what decides both assertions. Row S10's negative arm also covers the fixed checker: in EN-f-1's
  worktree, which has no naming stage, it reads FAIL on both.
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

The first run filed five rows. This run filed none.

| id | class | hazard | what |
|---|---|---|---|
| W3-S5 | BLOCKING | ARMED (2.0.0_SA_COO~G); disarmed by the issuer, row S10 | the checker's bare `bash` is the WSL launcher on this box |
| W3-S6 | BLOCKING | ARMED (2.0.0_SA_COO~G); disarmed by the issuer, row S10 | the halt checkpoint cannot name a principal in a worker worktree |
| W3-S7 | OBSERVATION | INERT | `BadQueueName` RAISES: no canonical form exists; this limb refuses a RAISE once enforcing, the commit limb warns |
| W3-S8 | OBSERVATION | ARMED (2.0.0_SA_COO~G) | no NEW/EXISTING at apply; one switch; 57 of 78 roots refused under ENFORCE |
| W3-S9 | OBSERVATION | INERT | 118 of 1266 name attributes are expressions, not graded before plan |

## 6. Not claimed

- Anything live. Every safe-apply run used the checker's stub terraform, and the enforce file stays absent.
- That a real plan passes the gates after the stage. T2-AC2's run stopped at the tombstone gate, because the stub writes
  no plan JSON.
- The significance of any row. Each row records form only.
