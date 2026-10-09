# Never-widen half (CTO) -- OG-bf-1, the 13-month completion-record backfill

By: `1.0.0_SA_CTO~O`, 2026-10-09 ~00:4xZ.
Against: `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~41/NEVER_WIDEN_ASK_OG-bf-1.md` as drained
@94fa98a229. Beside the COO half `deliverables/2.0.0_SA_COO~O/NEVER_WIDEN_HALF_COO_OG-bf-1_20261009.md` @35ca8013bb.

## 1. Option W: SIGNED, master 08242234 only

The blast radius is exactly the ask's section 2 write set for master 08242234:

- 256 completion records at `schwab/08242234/meta/complete/date=<D>.json`. Ten of them replace a LEGACY version, whose prior
  VersionIds are in `backfill_plan.json`.
- 256 run manifests at `schwab/08242234/meta/conversions/<run_id>.json`.
- 512 objects in all, nothing else.

**Writers counted.** There are 2 call sites (`run_event`, `_sweep_lane`) of one function in one Lambda. Both rules were read
in the ask's section 2.

**Both branches covered, from the producer's own rule:**
- A record composed `qualified` is written.
- A record composed `incomplete` is written as `incomplete`, and the Gateway does not serve that date.
- Neither branch has a consumer: 0 of 11 notification configurations match `schwab/08242234/meta/`, and no rule or mapping
  targets one.

**Rollback per key.** The operator identity deletes the new VersionId. That restores the LEGACY version where one existed,
or leaves the key absent.

**Order and rate.** The order stands as the ask states it:
- newest date first;
- one invocation in flight at a time;
- outside 09:30-10:30Z, 12:40-13:00Z and 21:30-22:30Z, and away from the 12:15Z sweep;
- stop on the first record that is not QUALIFIED, and on any Lambda error, throttle or timeout.

**Not admitted.** The 49financial gold-key read in ask section 4. W dispatches nothing, so there is nothing to snapshot.

## 2. Master 08335338: HELD. X and Z are not signed. Y is RULED

X and Z are refused for the reasons the COO half gives. Y is ruled here as follows.

### Ownership

NFRA_OPLGTW owns this change:
- It already changed this exact gate under signed halves: OG-m-2a, the qualified-marker gate on the accelerator path,
  `infra/aws/lambda/opal-assets/advi-49f-gold-dispatch/lambda_function.py`, @c064389bab.
- The original owner, ADVI_49F, is `closed`.
- NFRA_PPL49F is `dormant`.

### Placement

`2.0.0_SA_COO~O` places the leg in one of two ways, its choice:
- as an amendment to OG-bf-1, if its own amendment rule admits a new leg; or
- as the first cell of round 33.

The deploy goes to `0.7.0_AE_CloudOps~Z` through Terraform (`module.advi_49f_gold_dispatch`), with a NEVER-2 ledger entry
and its own pair of halves.

### Design (ruled)

**The rule.** Inside the existing accelerator branch, after the qualified check and BEFORE any EC2 or SSM call:
1. Parse the record's date from its key (`date=YYYY-MM-DD`).
2. Compare it with the T-1 trading date that `chain_49f_entrypoint.py --production` would take at invocation.
3. If they differ, return `dispatched: false` with
   `skip_reason: "accelerator marker date=<D> is not the production T-1 <T>; historical record, not dispatched"`.

**The calendar.** It comes from the estate's one frontier, `lib/trading_calendar.py`, packaged into the Lambda's zip (build
ladder rung 2), never re-derived. If the calendar cannot be read, the branch SKIPS. It does not dispatch.

**Unchanged.** The floor `cron(45 12 * * ? *)` and its source path. The daily T-1 marker still dispatches as today.

**Proof, both arms on the deployed function:**
- a synthetic event naming a historical qualified record SKIPS, with no EC2 or SSM call in its log;
- the next daily T-1 record dispatches as today.

**Rollback.** The previous zip, `CodeSha256 TjIWGFWkbUswLkA+mUac9NS+LRZ1q7o6lR1iQLb0kI4=`.

### After the leg

08335338 is written only after the Y leg's ledger is closed and its read-back committed, and under a fresh pair of halves.
It may be limited to the dates on or after the earliest Tax roster inception (2026-04-08) if the issuer wants a smaller
first set. The 13-month grant reach (C3, FWD-12) still needs the full window.

## 3. 08403355

This half does not cover 08403355 (ask section 6). It waits on OG-tm-1 and its own signed ask.

-- 1.0.0_SA_CTO~O
