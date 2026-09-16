# LGIC_ENFORCE.TO-EN-x-1-r2 -- fwd2-one-carrier -- RESULT

`0.9.0_WK_LGIC_ENFORCE~4`, cell `EN-x-1`, round 2. Branch `wk-lgic-enforce-2e-4`, base CLOUD @7377655ef7.

## Verdict

**3 of 3 mechanical criteria PASS by output.** Proof instance VALID, `proof-of-spec-check` rc 0.
`<status>` flipped to `complete` in the same commit as this file and the instance.

| criterion | invocation subcommand | deciding line | rc |
|---|---|---|---|
| `X1R-AC1` | `x1r-one-hand-edit` | `VERDICT: PASS-ONE-HAND-EDIT` | 0 |
| `X1R-AC2` | `x1r-name-moved` | `VERDICT: PASS-NAME-MOVED` | 0 |
| `X1R-AC3` | `x1r-fence-moved` | `VERDICT: PASS-FENCE-MOVED` | 0 |

Each was run as
`cd /c/Users/AndrewBerman/Desktop/ajb_workspace/.worktrees/wk-lgic-enforce-2e-4 && timeout 120 python org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/2.0.0_SA_COO~G/fixed_inputs/r2/check_en_r2.py <sub>`,
the checker pinned at `5e908a49292663ac196cae7a29334a6d0e288cae`.

## What the cell answered

Round 1 produced a `before` and NO `after`: `org/standards/NAMING_SCHEMA.json` `firm_forms` was a SECOND carrier of
49financial's short form and the validator refused the registry edit (row `LGIC_ENFORCE-W1-S19`). `NAMING_SCHEMA.json`
v1.9 removed it. This round ran the same edit and `python lib/opal_naming.py validate` returned **rc 0, 0 refusals**,
so RULING ONE now holds mechanically: the registry row is the one home of the form.

ONE hand edit -- `infra/logic/registry/scopes.json`, `49financial` `"short"` `49f` -> `f49` -- moved:

- the resource's NAME, `advi-49f-fwd2-exercise-queue` -> `advi-f49-fwd2-exercise-queue`, read from the two plan JSONs;
- the firm's FENCE PATTERN in the generated locals, `role/*-49f-*` -> `role/*-f49-*`;
- and, in the `after` plan, `aws_s3_bucket_policy.opal_data_49financial` from no-op to **`update`** -- the live fence.
  That third movement is the half round 1 could not reach. It is not a criterion; it is the evidence behind them.

`before` `3d119a4bc3802739be30df330400b283fdd2743f`, `after` `dd4de95e584c90db0691754dc25dd82d64f1c3d6`, both on the
scratch branch `prac-lgic-enforce-x1-r2`.

## Controls

- **Mutant, 3 of 3 fired.** One arm per criterion, each running the shipped limb against a mutated record with only the
  checker's in-memory `REC_X1` redirected: `FAIL-NOT-ONE-HAND-EDIT`, `FAIL-NAME-DID-NOT-MOVE`, `FAIL-FENCE-DID-NOT-MOVE`,
  all rc 1, each paired with a positive control on the real record that returned the PASS verdict. `fixed_inputs/` read
  clean afterwards.
- **Determinism STABLE.** Three invocations run twice, 3 of 3 identical; and a third time after the practice worktree
  was removed, still 3 of 3 PASS -- every read is from the object database, not from a checkout.
- **Negative arm at base.** All three limbs read `EXERCISE_FWD2_R2.md`, which does not exist at @7377655ef7
  (`git show` rc 128). With the record absent every limb says `FAIL-NO-X1-RECORD`, so no criterion here was already
  satisfied before the cell ran.

## Bounds honoured

**Nothing was applied.** No `apply` verb, no `safe-apply`. Two read-only `plan -lock=false` runs against the real S3
backend, `show -json` on each. `terraform init` took `hashicorp/aws v5.100.0` from the local plugin cache -- the version
the lock already pins -- so nothing was fetched off Opal infrastructure.

The slot branch carries **records only**: this file, the proof instance, `EXERCISE_FWD2_R2.md`, the two plan JSONs and
one surprise row. The `.tf`, the registry edit and the ten regenerated carriers are on the scratch branch, which is
never pushed and never merged. Its worktree was removed clean; the branch stays in place at `dd4de95e58`.

## Row filed

`LGIC_ENFORCE-W4-S3` (OBSERVATION, INERT) -- `terraform init` did NOT rewrite the tracked `.terraform.lock.hcl` on
`shared-infra`, against the briefing's expectation. Its id is `W4-S3` and not `W4-S1` because slot 4 already held two
rows from round 1; the channel was re-read at write time.
