# FWD-6 live read after the switch-on (2.0.0_SA_COO~B1, 2026-10-09T08:05:42Z)

Switch commit: 4d2bfc6dfd (org/mcp/naming-place.enforce alone). Probe tree: detached worktree at 1eabd4c1de (switch present), removed after.

## Arm A -- unplaceable NEW schedule irpt-directory-newjob in investor-reporting/directory/schedule.tf, through .tools/safe-commit.sh
```
safe-commit rc=1 (nothing committed)
ERROR: BLOCKED -- the naming limb refused (LGIC_ENFORCE DEC-6, ENFORCE mode). Commit aborted; files unstaged.
  [naming-gate] DENOMINATOR: 1 path(s) in this diff; declaration-tree domain = 1 MINUS EXCLUDED(org/, docs/, run-artifact dirs ^workflows/[^/]+/[^/]+/[0-9]{8}T[0-9]{6}Z-[0-9a-f]{7,40}/) 0 = 1 path(s) [of the excluded, 0 are run artifacts and 0 are org//docs/]
  [naming-gate] COVERAGE: 0 path(s) in the declaration domain the gate could not see (extension outside its graded set and not .gitattributes); 1 seen
  [naming-gate] NAMING REFUSE infra/aws/terraform/investor-reporting/directory/schedule.tf:559 irpt-directory-newjob -> irpt-directory-newjob-daily
  [naming-gate]   why: NEW name the canon places as FIX. Owed: use irpt-directory-newjob-daily; the cadence word "daily" is read from the schedule (cron(50 9 ? * MON-FRI *): once a day on 5 days of the week (a weekday restriction is a calendar)). Build it with name() or edit the literal; nothing else is owed. [grade() said: NEW and OUT-OF-PATTERN as SCHEDULE: REFUSE]
  [naming-gate] NAMING-PLACE: REFUSE 1
  [naming-gate] NAMING-GATE: REFUSE 1 graded
```

## Arm B -- placeable NEW schedule irpt-directory-newjob-daily, same file, through .tools/naming-gate.py --diff <staged> --post-from-index (the call safe-commit makes; no probe commit landed)
```
gate rc=0
DENOMINATOR: 1 path(s) in this diff; declaration-tree domain = 1 MINUS EXCLUDED(org/, docs/, run-artifact dirs ^workflows/[^/]+/[^/]+/[0-9]{8}T[0-9]{6}Z-[0-9a-f]{7,40}/) 0 = 1 path(s) [of the excluded, 0 are run artifacts and 0 are org//docs/]
COVERAGE: 0 path(s) in the declaration domain the gate could not see (extension outside its graded set and not .gitattributes); 1 seen
NAMING CONFORMANT infra/aws/terraform/investor-reporting/directory/schedule.tf:559 irpt-directory-newjob-daily -> irpt-directory-newjob-daily
  why: CONFORMANT as SCHEDULE
NAMING-GATE: PASS 1 graded
```

## Census on the switched trunk (ecf2d1cffb)
```
ALL-ROOTS ok=True roots_total=88 mapped=78 unmapped=10 completed=78 stopped=0 items=2269 right=564 fix=1460 not_asked=222 pattern=23 carded=0 refused=0 hole=0 carded_class_holes=0 source_bucket_holes=0 event_rule_holes=0 unknown_word_holes=0 other_holes=0 stale_hints=0 uncounted=1 counted_at_caller=17
```

The unplaceable count is no longer than the round-9 close (hole=0 then, hole=0 now). Rollback not needed.
