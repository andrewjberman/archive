# NEVER-WIDEN, COO HALF -- the Cottonwood account-return landing function to the cloud (IRPT_DASHBD rounds 120 to 126, workstream B-49F): ONE new Terraform root, SEVEN new resources, ONE explicit first event, then explicit catch-up events

**Signer:** 2.0.0_SA_COO~D2. **Status:** SIGNED (REVISION 2). **Date:** 2026-10-15 ~14:0xZ.
**Revision 2 supersedes revision 1 (sha256 `c63702ade4df...`, signed @f1321ee057, now VOID):** revision 1 described a function with no pyarrow layer (row `IRPT_DASHBD-D2-S84`); `DB-b-259` (merged @54e4a0036a) adds the layer and the packet's pins, live state and conditions are updated. This half is re-signed on the new bytes below.
**Bound to the packet's bytes:** [NEVER_WIDEN_PACKET_COTTONWOOD_ACCOUNT_RETURN_DAILY_LANDING.md](file:///C:/dev/ajb_workspace/org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~D2/NEVER_WIDEN_PACKET_COTTONWOOD_ACCOUNT_RETURN_DAILY_LANDING.md)
(repo-relative `org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~D2/NEVER_WIDEN_PACKET_COTTONWOOD_ACCOUNT_RETURN_DAILY_LANDING.md`), sha256 `a1b080c5fe065f90f4ad356c95301e59437637e95ce40afade93726eeaa392df`
(computed by this seat on the file; 15,377 bytes). A packet whose bytes differ is not covered. **The other half:** 1.0.0_SA_CTO~DELL2, who also decides the packet's three questions (section 9). **Nothing is applied and no event is invoked until both halves are SIGNED on this sha256.**

## 1. What this half covers

Three acts, in order. (1) The bundle build of `irpt-cot-account-return-daily-lambda` and ONE `safe-apply` of `infra/aws/terraform/investor-reporting/account-return-daily/` by `0.7.0_AE_CloudOps~DB2`, plan exactly 7 add / 0 change / 0 destroy on the seven named addresses, anything else STOPS. (2) ONE synchronous event `{"day": "2026-07-10"}`. (3) Only after (2)'s after-read passes: explicit `days` events of at most 25 trading days each, naming only days after 2026-07-10 and at or before the newest silver partition, one after-read each. Nothing else: the schedule stays DISABLED through all three; no day at or before 2026-06-22; no delete; no other root.

## 2. What this seat measured and re-ran, and what it did not

- **Live state, read by this seat (read-only):** function, execution role, schedule and artifact key ABSENT; the Cottonwood gold prefix holds 3,325 partitions, 2013-04-03 to 2026-06-22 (LIST); the Cottonwood bucket policy's `role/*-cot-*` admission (the new role names match) and its restricted-prefix denies (the crm bronze prefix only); the silver bucket policy (no principal deny).
- **Re-run by this seat on the landed tree:** the three round-127 criteria (`DB127-1-AC1..AC3`: the layer's data source and `layers` line, the live layer and sibling reads, and the pyarrow import check against the layer's zip), the five round-126 criteria (`DB126-1-AC1..AC3`, `DB126-2-AC1..AC2`), the three guard and floor criteria of round 125 and the root's HCL and additive-root criteria of round 123 (`DB123-3-AC1`, `AC2`): PASS. **`DB123-3-AC3` (the round-123 facts record) now FAILS on the landed tree:** it hashes `lambda.tf` as it stood before `DB-b-257` changed the memory line, so its hash is stale by design; it is superseded by `DB126-1-AC1` and `DB126-1-AC3`, which grade the file as it now stands. The build-only package was built three times (a scratch reference, the worker's tree, the checker's own run) with one sha256.
- **Read line by line by this seat:** the root's `iam.tf` statements, `lambda.tf`, `schedule.tf`; the adapter's `write_day` (a LIST first; two puts, data then manifest).
- **NOT done by anyone:** a `terraform plan`; any invocation of the function; its memory on python3.12 (the 654.5 MB peak was measured on python3.14 on Windows, row `W210-S2`).

## 3. Writers of the changed property, counted: N = 1 rule in scope, 3 entry paths, 1 writer outside the pair

One rule in this pair writes the Cottonwood `account_return_daily` prefix (`write_day`), entered by a `day` event, a `days` event and the DISABLED schedule. The history partitions came from an operator path this pair neither uses nor changes and this seat cannot exclude (packet section 5).

## 4. Blast radius, and the limits this half signs under

- Act 1 changes no served value and writes no object. Acts 2 and 3 each add new partitions in an occupied prefix, never replacing one (the guard LISTs the day first and refuses on either key). **Branch C is signed on:** a death between the two puts leaves a data object without its manifest, which the guard then blocks from re-running; its remedy is a listed-key delete with Andrew's word.
- **Honest limits, signed on:** no plan has ever run; the python3.12 memory is unmeasured and Act 2's `Max Memory Used` is the first reading (above 717 MB, the next change is the one memory line, and Act 3 does not start); whether the roles can read the silver objects is read first at Act 2.
- **Not covered:** enabling the schedule; any day at or before 2026-06-22; any change to the history partitions; any portal reader of the new partitions; a change to the 49 Financial roots.

## 5. Both branches

Branch A: the event writes one partition and the after-read records memory, duration, counts and the `source` words. Branch B: the guard refuses, the silver presence hold returns the day held, or the day is before the floor, and nothing is written. Branch C: the half partition above. Branch D: out of memory or time before the puts, nothing written.

## 6. Conditions of this half

0. **Act 1 step 0 (the CTO's added condition, msg 8287):** read the layer `irpt-performance-native-layer` live and confirm it carries pyarrow for python3.12 and is the version the sibling runs, else STOP. 1. **Ledger first,** bound to the packet's sha256 (`irpt-dashbd-cottonwood-account-return-daily-20261015`; legs git, build, terraform, event, catch-up); `.open_deploys/` read across every live worktree with the denominator printed. 2. **Live state re-read at the moment of the apply** and equal to the packet's section 3, else STOP. 3. **The plan read first:** exactly 7/0/0 on the seven addresses, else STOP; the build line equal to the packet's sha256 or STOP. 4. **Each event only after the previous leg's after-read is recorded in the ledger.** 5. **No `update-function-code`, no bare `terraform apply`, no schedule change, no wildcard delete.** 6. **The applier is an AE seat the gates admit, not a worker.**

## 7. The questions, from this seat (the CTO's half decides them)

1. **Acts 2 and 3 in this pair:** ACCEPT as written; the guard, the floor and the one-after-read-per-event rule bound each step, and a separate word per event adds waits without adding a check.
2. **python3.14 versus python3.12:** ACCEPT 1,024 MB with the first event's `Max Memory Used` as the reading and the one-line raise as the remedy.
3. **The operator writer:** ACCEPT; the guard is the protection and the pair does not touch that path.

-- 2.0.0_SA_COO~D2
