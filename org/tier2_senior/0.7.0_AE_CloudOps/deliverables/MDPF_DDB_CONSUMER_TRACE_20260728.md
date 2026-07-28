# `opal-assets-daily-aua` -- DDB-row-side CONSUMER TRACE (the severity gate)

**archetype:** TRACE
**Author:** 0.7.0_AE_CloudOps | **Measured:** 2026-07-28T~2145Z | Read-only, zero writes.
**GO:** CTO 214356Z. **Plane:** DDB-row-side ONLY. `0.2.0_DT` holds the S3-object-side census --
different instrument, different plane, no overlap.

## ANSWER

> **No live EXTERNAL consumer of the ETF cohorts on the DDB plane.** The only component that reads
> this table is **the emitter itself**, reading its own history to run a guard. The one consumer
> previously treated as a floor is **DORMANT CODE that is never invoked**, and the role it would run
> under **has no DynamoDB access at all.**

**Therefore, on this plane, `$522,484,735.05` of T-16 staleness reaches nothing.** Severity is
**internal-only HERE** -- and see the bound at the end, because that is not the whole answer.

---

## DENOMINATOR AND PREDICATES (six, each stated with what it can and cannot see)

**P1 -- literal table-name sweep, whole parent repo** (`comp-grep "opal-assets-daily-aua"`):
**2 code-bearing references** (rest are docs/PRDs/audit logs):
```
infra/aws/lambda/opal-assets/opal-assets-daily-emitter/lambda_function.py:62   TABLE_NAME  <- WRITER
data/mdpf/scripts/gold/dim_mdpf_aggregate_aua_timeseries.py:330                DDB_AUA_TABLE
```

**P2 -- the second reference is DORMANT, not a consumer.**
`load_ddb_0824_custody_history()` (`:334-358`) is **defined and never invoked.** Its only other
mention is a comment at `:822` -- *"retained for that alignment harness"* -- and the production path
one line later calls a different function entirely:
```
:823   custody_map = load_rps_custody_history(dates)      <- what actually runs (S3 silver, not DDB)
```
**A reader nothing calls is not a consumer.** CTO flagged this as the known floor; measured, the
floor is **zero**.

**P3 -- env propagation (TF):** exactly one Lambda receives the table name.
`emitter.tf:184  TABLE_NAME = aws_dynamodb_table.opal_assets_daily.name`. No other function is told
the table exists.

**P4 -- grants in the `opal-assets` TF root:** one statement, `WriteOpalAssetsDaily` (emitter role).

**P5 -- APPLIED truth on the runner that would host P2's code.** `dim_mdpf_aggregate_aua_timeseries.py`
IS Stage 6's REVAMP producer (`mdpf-daily-dispatch.sh:142`), so it runs on `mdpf-daily-runner`:
```
mdpf-daily-runner-ec2-role: 20 inline Sids, occurrences of "dynamodb" = 0
                            attached managed: AmazonSSMManagedInstanceCore only
simulate-principal-policy  dynamodb:Scan on the table  -> implicitDeny
POSITIVE CONTROL           s3:PutObject on its platinum prefix -> allowed
```
**The role cannot read the table.** This *corroborates* P2 rather than contradicting it: the code path
is dead, so the missing grant has never been felt. **Had the harness ever been switched on, it would
have AccessDenied on an unguarded `ddb.scan()` in a `while True` (`:348-358`, no try/except).**
Recorded as a latent trap for whoever activates it.

**P6 -- the two-hop `resource().Table()` class CLAUDE.md 22a names as historically invisible.**
Swept `infra/aws/lambda` + `data`: **10+ Lambdas use the shape, none name this table.** The one
two-hop consumer of *this* table is **the emitter itself**:
```
lambda_function.py:900   _ddb.Table(TABLE_NAME).query(IndexName="cohort_history", ...)
```

---

## WHAT THAT `:900` READ IS -- the table is NOT write-only, and this matters

`_previous_value()` backs **`apply_value_repeat_guard`**: if a row claims `fresh` while its value is
**identical to the previous served partition on a trading day**, the emitter **withholds the freshness
claim** (`vintage_state -> missing`) while **serving the value unchanged**.

So **`vintage_state` is EMITTER-DERIVED, not source-passthrough** -- a fact any future reader of this
table needs, and one that changes how its rows should be interpreted.

The guard is deliberately **degrade-on-failure** (`:911-915`): an unreadable history returns `None`,
so the guard "will neither pass nor condemn." **It cannot report a false GREEN or a false RED -- it
simply does not fire.** That is the right shape and worth preserving.

---

## ⚠ DENOMINATOR LIMITS -- stated, not hidden

1. **THE PORTAL IS STRUCTURALLY OUTSIDE MY SWEEP.** The parent repo tracks **1** file under `portal/`
   (the gitlink), so `comp-grep` **cannot see portal contents at all**. I swept `portal/src` (404
   files) directly and found no reference.
   **AND I MUST DISCARD TWO OF MY OWN PROBES:** I also grepped `portal/app` and `portal/lib` and got
   empty -- **neither directory exists.** Those were **broken probes, not evidence**, and counting
   them would have inflated my coverage. *An empty result from a nonexistent path is indistinguishable
   from an empty result from a real one.*
2. **A name-based sweep cannot see a consumer that receives the table name from an env var set in a
   different TF root.** P3/P4 cover the `opal-assets` root only. Not exhaustive across all roots.
3. **This is the DDB plane only.** Per CTO, `0.2.0_DT` holds the S3-object side.

**Per CTO's own caution: a source sweep finding nothing is not proof of no consumer.** Six independent
predicates converging is strong evidence, not proof. **I am reporting evidence, with its bounds.**

---

## ⚠ SEVERITY IS NOT FULLY PRICED BY THIS TRACE -- and saying otherwise would be the error

The DDB rows reach no client surface. **But the ETF numbers also exist as SERVED S3 ARTIFACTS**
(`platinum/mdpf/*`, `json/mdpf/*`), and those are on **DT's plane**. **"No DDB consumer" must NOT be
reported as "the staleness is harmless"** -- it means *this* propagation path is closed, and the
serving question is answered by DT's census, not mine.

---

## LEAD FOR CTO'S QUESTION (3) -- the `_total__partner_aua` zero. HYPOTHESIS, NOT A FINDING.

The emitter already carries the correct doctrine for totals, written in its own source at `:1132-1147`:

> *"**A TOTAL'S VINTAGE IS THE WORST OF ITS CONTRIBUTORS' -- NEVER THE ARTIFACT'S.** This used to read
> mdpf's artifact-level `as_of_date`, which describes the PARTNER data, for a row whose CONTENT is ETF
> data. WRONG SOURCE FOR THE CLAIM."*

The ETF total implements it: `_e_as_of = min(contributor as_of)`, and when contributors are absent it
stamps `missing`/`incomplete` rather than summing a partial book (`:1129`).

**`_total__partner_aua` appears NOT to follow that same doctrine** -- it emitted `0` with a CURRENT
`as_of` while **both** its additive constituents were `missing`. **I have not read the partner-total
code path**, so this is a lead, not a conclusion. **If it holds, the fix already exists in the same
file, one row-type over.**

And note what that comment records about how the earlier version was caught:

> *"MY OWN FALSIFIER WAS STRUCTURALLY BLIND TO IT: it checks `vintage` against `staleness`, and BOTH
> were derived from the same wrong `as_of`, so they agreed perfectly. **A CONSISTENCY CHECK CANNOT
> CATCH A WRONG INPUT.** Caught by ANDREW, on a different axis entirely."*

**Independence of verifiers is not independence of questions** -- already in the estate's own source,
and it is the same lesson six near-misses produced tonight.
