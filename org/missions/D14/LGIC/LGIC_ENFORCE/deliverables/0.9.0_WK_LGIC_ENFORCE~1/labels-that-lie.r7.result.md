# EN-t-34 round 7 -- THE LABELS THAT LIE: result

`0.9.0_WK_LGIC_ENFORCE~1` on `LGIC_ENFORCE.TO-EN-t-34-r7`, worktree
`/cygdrive/c/Users/AndrewBerman/Desktop/ajb_workspace/.worktrees/wk-lgic-enforce-7-1`,
branch `wk-lgic-enforce-7-1`, base `8c9e9e91f1`, record commit `6eb2d82aec` (LOCAL).

**Nothing was resolved. Nothing was re-graded. No grading behaviour changed.**
`org/standards/NAMING_SCHEMA.json` and `infra/logic/registry/` are untouched --
`git status --porcelain org/standards/NAMING_SCHEMA.json` returns empty, and the guard
`t34-no-grade-change` reads the same 8/7 split it read at the cut.

## The four mechanical arms, as the run printed them

| id | arm | verdict | denominator |
|---|---|---|---|
| T34R7-AC1 | `t34-51-both` | `PASS-T34-51-NAME-BOTH-REMEDIES` | 51 rows of a 51 pin; rows NOT naming exactly two remedies: 0 |
| T34R7-AC2 | `t34-actionable` | `PASS-T34-LABEL-IS-ACTIONABLE` | 51 rows; remedies naming no CARRIER: 0; `label_definition` present |
| T34R7-AC3 | `t34-15-true` | `PASS-T34-15-CARRY-A-TRUE-REASON` | 15 rows of a 15 pin; still carrying the stale reason: 0; with no reason: 0 |
| T34R7-AC4 | `t34-no-grade-change` (GUARD) | `PASS-T34-NO-GRADE-CHANGE` | 15 entries; 8 genuinely NOT GRADED, 7 still graded -- identical to the pin |

`selftest-arms` was run FIRST, before any write: 21 arms, 8 positive-satisfiability,
`VERDICT: PASS-ARMS-DISCRIMINATE`. No arm was unsatisfiable by a correct record, so no
BLOCKING row was owed.

## GROUP ONE -- the 51, and why the new label instructs

Re-identified INDEPENDENTLY of round 6's `CADENCE_PLUS_SYSTEM` label: a row is in the group
if its canonical carries BOTH `{system}` and `{cadence}`. The label is read nowhere in the
derivation. Swept over the WHOLE carried population, not the carded list alone:

```
carried rows (resolved + carded + deferred): 1370
  resolved  rows    41  two-carrier   0  unsanctioned-brace   0
  carded    rows   236  two-carrier  51  unsanctioned-brace  15
  deferred  rows  1093  two-carrier   0  unsanctioned-brace   0
TWO-CARRIER rows re-identified: 51   by type: EVENT_RULE 49, LOG_GROUP 2
```

Both groups falling entirely inside `carded` is a MEASURED result, not the domain assumed.

**The arm most likely to catch good-faith work is the carrier arm, so the carrier is measured
per row rather than pasted.** `"two remedies"` is a description; naming WHERE each value comes
from is an instruction, and the `{cadence}` carrier is not one string:

| carrier kind | rows | what a later census reads |
|---|---|---|
| `SCHEDULE_EXPRESSION` | 32 | the rule's own `schedule_expression` -> `cadence.values` |
| `EVENT_PATTERN` | 14 | the rule's own `event_pattern` -> `cadence.event_form` `on-{event}`; **there is no clock here and `cadence.values` does not apply** |
| `EVENT_PATTERN_VIA_TARGET_EDGE` | 2 | a LOG_GROUP has no cadence of its own -- the carrier is the rule that TARGETS it, through `aws_cloudwatch_event_target` |
| `LIVE_RULE_NO_REPO_DECLARATION` | 3 | no literal-name declaration in 494 `.tf` files carrying 131 rule blocks; the carrier is the live rule, `aws events describe-rule`, read-only |

A reader who assumes `schedule_expression` and meets an event-driven rule finds NOTHING, and
cannot tell that from an absent carrier. That is the distinction the old label hid.

The `{system}` half is one carrier for all 51 -- `infra/logic/registry/resources.json`, the
resource-to-system row keyed `(name, type)` read at `lib/opal_naming.py:1030-1032` -- and its
state is measured: **51 of 51 carry no row today, against a registry holding 91**, so the act
is a MINT, not a lookup. It is IN a cell's grant; the cadence half is not. That asymmetry is
the whole reason neither remedy alone clears a row.

## GROUP TWO -- the 15, under a reason that is true

They carried `NON_SYSTEM_PLACEHOLDER_TOKEN`, which says THE TOKEN IS NOT A SYSTEM. They now
carry `ROW_IS_NOT_A_NAME` (R-62): the graded object is a producer's S3 KEY FORMAT TEMPLATE,
and the brace tokens (`{snap}`, `{dim_name}`, `{d}`, `{dc}`, `{firm}`) are runtime substitution
fields already present in the row's OWN `current` before any grade ran -- the measured
discriminator. `grade.placeholder` opens a slot *"the name does not carry"*, which presupposes
a NAME; a format string is not one. **There was no source because there was never a
substitution question** -- not because a source is missing or late. Each row states it is not
resolvable and not pending, so no later census opens a lookup for it.

The superseded value appears exactly ONCE in the record, in the block that records what was
replaced, and in NO row -- which is also what `t34-15-true` measures.

**All 15 stay in every grade.** R-62 refused the removal: `S3Key` sits in
`types_not_graded_by_kind`, but that table is a ROUTING table whose name is the opposite of its
behaviour -- `lib/opal_naming.py:493` unions the whole table INTO `graded_types` and `:1012`
removes a type only when its prose reason begins `NOT GRADED`. 8 of 15 entries are genuinely
out; 7, `S3Key` among them, are still graded. Rewording one reason moves a type across that
switch silently. The table was not touched.

## Controls

- **Live negative control on the REAL reader.** The self-test drives fixtures and says so; it
  states `record_path()` is not covered by it. So three mutations of the COMMITTED record were
  driven through the real subcommands, **each alone**: one remedy dropped -> `FAIL-T34-51-NAME-
  BOTH-REMEDIES`; one `carrier` blanked -> `FAIL-T34-LABEL-IS-ACTIONABLE`; the stale reason put
  back on one template row -> `FAIL-T34-15-CARRY-A-TRUE-REASON`. 3 of 3 fired, each returning
  its own arm's token. Restoration proven two ways: bytes identical to the committed file, and
  `git diff --stat` on the record empty.
- **The guard's negative control was NOT exercised live, deliberately.** Breaking
  `t34-no-grade-change` requires editing `org/standards/NAMING_SCHEMA.json`, which is outside
  this cell's grant and forbidden by a BOUND. Its negative arm is the checker's own fixture arm
  (`S3Key` pushed across the `NOT GRADED` switch), driven in `selftest-arms`, which passed.
- **My own instrument was wrong first, and the record says so.** A substring test classified
  `aws_cloudwatch_event_rule.exec_summary_trigger_placeholder` as carrying BOTH expressions
  because the block's COMMENT at `infra/aws/terraform/exec-summary/main.tf:225` names
  `event_pattern` as future work. The block declares `schedule_expression` only. `attr_kinds()`
  now strips comment lines and matches the ATTRIBUTE form. A classifier that reads prose ABOUT
  an attribute as the attribute names a carrier the world does not have -- inside an
  instruction a later census would follow.
- **The absence control, which also pins WHICH file the arms read.** `record_path()` scans
  slots `~1` through `~4` and returns the first that exists, so a PASS could in principle come
  from another slot's file. The record was moved aside and the three arms driven with it
  absent: all three returned their FAIL token and the first named
  `org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~1/LABEL_TRUTH_R7.json`
  by path -- so the PASS is caused by THIS record. Restored byte-identical (127496 bytes,
  `git status --porcelain` on it empty). **This was run AFTER the record existed, not at the
  cut**; the order's own statement that AC1-AC3 read FAIL at the cut is the issuer's
  measurement and is not re-derived here, because the record's absence at the cut is settled by
  its creation in commit `6eb2d82aec`.
- **Corroboration on a different instrument.** The LOG_GROUP target edge the builder reports
  (`aws_cloudwatch_event_target.inf_gold_dispatch_release_to_logs` pointing rule
  `inf-gold-dispatch-release-changed` at `/aws/events/inf-gold-dispatch-release-audit`) was read
  independently by hand out of
  `infra/aws/terraform/inf-pipeline/inf-gold-dispatch-release-alarm.tf` (`:40-41`, `:103-107`,
  `:128-131`) before the builder ran.

## Not done here

- **The 1093 deferred rows were not attempted**, per R-60: FWD-5's ACCEPT says the outcome IS
  the list, and resolution is the clean-up projects' work.
- **No placeholder was resolved**, including the 51 whose `{system}` half sits in a grant.
- **`T34R7-AC5` is not self-graded** -- it is `3.0.0_SA_CVO`'s at L9.

## Surprises

None filed. Every path the order named exists, every premise re-grounded true at HEAD (the two
pinned counts re-derived to 51 and 15 on an independent instrument, the 8/7 exclusion split
re-read, the registry's 0-of-51 state measured), and all 21 self-test arms were satisfiable, so
no BLOCKING row was owed. The one thing that went wrong went wrong inside my own instrument,
was caught before the record was committed, and is recorded in the record and above rather than
in the channel -- no premise of the order failed and nothing off-mandate was touched.
