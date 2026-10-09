# EN-z-5 -- one planted pattern-name commit, read for its grade (round 20)

**Planted:** `planted_name` = `investor-reporting/directory`, `planted_type` = `S3Key`, `planted_root` = `investor-reporting/directory`.
`place(name, typ, root)` from `lib/opal_naming_rootcheck.py` returns kind `PATTERN` (detail: variable '{scope}' is filled per firm:
`irpt/{scope}/platinum/directory/`; the code reads its bucket from `IRPT_DIRECTORY_BUCKET_MAP`, one bucket per firm). Shape in the
root's code: `handler.py:53` `DIRECTORY_PREFIX = os.environ.get("IRPT_DIRECTORY_PREFIX", "investor-reporting/directory")`.

**QA branch:** `qa/lgic-enforce-r20-s12`, commit `a09b28498482c31f96453b31741ee37f37aa14a7`, made from `9f96f3739d`; adds ONE file,
`infra/aws/lambda/zz-lgic-enforce-r20-s12/probe.py` (the only Lambda path the order's grant names), carrying the line above under a new
variable name. It is not reachable from the worktree branch `wk-LGIC_ENFORCE-2` and is never merged or pushed.

**A first attempt (no commit).** The same line planted at `infra/aws/lambda/investor-reporting/directory/zz_qa_pattern_probe.py`, the
mapped root itself, printed `NAMING-GATE: PASS 0 graded`; the owned-paths lane gate then refused the path (outside the order's `<paths>`),
rc=1, nothing committed. The file was moved to the granted path.

## The commit output, whole (safe-commit rc=0)

```
  [risk-reflex] comp-pulse diff -- THE PRE-COMMIT RISK REFLEX (NFRA_NERVES L5)
  [risk-reflex]   INVOCATION (pin beside any quoted result): cmd=diff days=7 top=8 (argv: diff infra/aws/lambda/zz-lgic-enforce-r20-s12/probe.py)
  [risk-reflex]   danger map: 0.7h old
  [risk-reflex]   DENOMINATOR: 1 file(s) checked against 1662 danger node(s)
  [risk-reflex]   ANSWER STATE: PRESENT_WITH_ZERO_RESULTS
  [risk-reflex]   REFLEX CLEAN -- a MEASURED result (map read, every file checked), not a default.
  [risk-reflex]   WITHIN BUDGET: scanned 1 of 1 file(s); budget: 90 s (default), used 0.025560499998391606 s
  [commit-gate] All checks passed!
  [commit-gate] OK: no unguarded strict-utf8 log reads.
  [commit-gate] OK: pre-commit gate clean for 1 of 1 file(s)
  [naming-gate] DENOMINATOR: 1 path(s) in this diff; declaration-tree domain = 1 MINUS EXCLUDED(org/, docs/, run-artifact dirs ^workflows/[^/]+/[^/]+/[0-9]{8}T[0-9]{6}Z-[0-9a-f]{7,40}/) 0 = 1 path(s) [of the excluded, 0 are run artifacts and 0 are org//docs/]
  [naming-gate] COVERAGE: 0 path(s) in the declaration domain the gate could not see (extension outside its graded set and not .gitattributes); 1 seen
  [naming-gate] NAMING-GATE: PASS 0 graded
  [to-pipeline-gate] OK: no task_orders/*.md in this commit (denominator: 1 dispatched path(s), 1 staged-added).
[surprise-row-gate] input: 1 path(s) from the STAGED environment variable (argv was empty; the ~32 KB argv cliff, 0.0.0_AB_MSTR 94338)
[surprise-row-gate] OK: no surprise-channel rows in this commit (denominator: 1 dispatched path(s)).
[to-pipeline-gate] input: 1 path(s) from the STAGED environment variable (argv was empty; the ~32 KB argv cliff, 0.0.0_AB_MSTR 94338)
[to-pipeline-gate] OK: no task_orders/*.md in this commit (denominator: 1 dispatched path(s), 1 staged-added).
SKIP: missions-tree-check -- no org/missions/D*/ or org/projects/*.json path staged; check not run
[qa/lgic-enforce-r20-s12 a09b284984] qa(LGIC_ENFORCE r20 EN-z-5): planted per-firm prefix probe for the commit gate (QA branch only, never merged)
 Author: 0.9.0_WK_LGIC_ENFORCE~2 <0.9.0_WK_LGIC_ENFORCE~2@opal.agent>
 1 file changed, 4 insertions(+)
 create mode 100644 infra/aws/lambda/zz-lgic-enforce-r20-s12/probe.py
  [msg-verify] committed a09b284984  subject: qa(LGIC_ENFORCE r20 EN-z-5): planted per-firm prefix probe for the commit gate (QA branch only, neve
  [msg-verify] MATCH len=168
```

## What the grade means

The real gate ran (`[naming-gate]` lines above) and printed `NAMING-GATE: PASS 0 graded`: no `NAMING ...` line for the planted name, not
a CONFORMANT, ALIAS, REFUSE, RAISE or SKIP line, and no line saying it skipped a pattern. Denominator: 1 path in the diff, 1 seen, 0 the
gate could not see. So the gate neither refused nor graded the per-firm prefix, and the only trace of that is the count `0 graded`.
`grade_line` is therefore `NONE`, with the surprise row `LGIC_ENFORCE-D1-W2-S152` saying the gate graded nothing for it. Not measured:
why (a PATTERN skipped by design, the literal sitting in an `os.environ.get` default, or no new stored name in the post-image); the same
zero printed in the mapped root on the first attempt, so the location of the file is not the cause.
