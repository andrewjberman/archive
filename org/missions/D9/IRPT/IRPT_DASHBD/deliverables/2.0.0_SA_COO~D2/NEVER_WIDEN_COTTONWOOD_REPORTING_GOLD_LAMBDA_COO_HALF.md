# NEVER-WIDEN, COO HALF -- the Cottonwood report-build function to the cloud (IRPT_DASHBD rounds 131 to 137, workstream B-49F): ONE new Terraform root, SEVEN new resources, a dry-run event, then the backfill of the filled report values

**Signer:** 2.0.0_SA_COO~D2. **Status:** SIGNED (REVISION 1). **Date:** 2026-10-15 ~19:1xZ.
**Bound to the packet's bytes:** [NEVER_WIDEN_PACKET_COTTONWOOD_REPORTING_GOLD_LAMBDA.md](file:///C:/dev/ajb_workspace/org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~D2/NEVER_WIDEN_PACKET_COTTONWOOD_REPORTING_GOLD_LAMBDA.md)
(repo-relative `org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~D2/NEVER_WIDEN_PACKET_COTTONWOOD_REPORTING_GOLD_LAMBDA.md`), sha256 `cc5e87ff22e6d17c77749b275f631fbd9fbc2f198e0dc39407e0fbbb2b31865f`
(computed by this seat on the file; 15,395 bytes). A packet whose bytes differ is not covered. **The other half:** 1.0.0_SA_CTO~DELL2, who also decides the packet's three questions (section 9). **Nothing is applied and no event is invoked until both halves are SIGNED on this sha256.**

## 1. What this half covers

Four acts, in order. (1) The bundle build of `irpt-cot-reporting-gold-lambda` and ONE `safe-apply` of `infra/aws/terraform/investor-reporting/reporting-gold-iso/` by `0.7.0_AE_CloudOps~DB2`, plan exactly 7 add / 0 change / 0 destroy on the seven named addresses, anything else STOPS. (2) ONE synchronous DRY-RUN event `{"day": "2026-10-14", "dry_run": true}`: it writes and chains nothing. (3) Only after (2) passes: ONE synchronous `{}` event, which builds the oldest owed day and chains at most 10 days. (4) Only after (3)'s after-read: further `{}` events, one at a time, until `NOTHING_OWED`. The schedule stays DISABLED throughout.

## 2. What this seat measured and re-ran, and what it did not

- **Live state, read by this seat (read-only):** function, both roles, schedule, log group and artifact key ABSENT; the filled prefix in `opal-data-cottonwood` EMPTY (0 objects); the layer at version 1 on python3.12, the sibling function on the same version; `account_dim` through 2026-10-14; `account_return_daily/date=2026-10-14/` with both objects.
- **Re-run by this seat on the landed tree (`d6bc5ecbee` and later):** the round-133 root criteria (`DB133-1-AC1..AC3`: the root's HCL, naming, layer and imports, the source-map entry and entry pins) PASS; the round-135 criteria (`DB135-1-AC1..AC3`, which include every clause of round 131 in their probe) PASS; the round-137 criteria (`DB137-1-AC1..AC3`: the unreported-day statement, 33 handler tests) PASS. **Two older criteria are RED on purpose and disclosed:** `DB131-1-AC2` and `DB131-1-AC3` fail because round 131's fixture holds no `manifest.json` and the round-135 contract guard (row `D2-S92`) now refuses a returns partition that names no contract; round 135's probe is the superset that replaced them (the worker's row `IRPT_DASHBD-D2-W217-S2`).
- **Read line by line by this seat:** `iam.tf` (the seven statements), `lambda.tf`, `schedule.tf`, `locals.tf`; the handler's `lambda_handler`, `build_day`, `owed_days` and `chain_next` (a failed day does not stop the chain; a dry run neither writes nor chains; a landed day is a no-op; `build_day` is the only writer and makes one `put_object` per day).
- **NOT done by anyone:** a `terraform plan`; any invocation of the function; its memory on python3.12 (the local peak of 408 MB is python 3 on Windows).

## 3. Writers of the changed property, counted: N = 1 rule, 4 entry paths

One rule writes the Cottonwood `filled_report_values` prefix (`build_day`), entered by a `day` event, a `{}` event, the chain's self-invoke and the DISABLED schedule. The prefix is empty, so no existing object can be replaced; the 49 Financial reporting-gold root writes another firm's bucket (packet section 5).

## 4. Blast radius, and the limits this half signs under

- Act 1 changes no served value and writes no object. Act 2 writes nothing. Acts 3 and 4 add objects to an EMPTY prefix, one per trading day, each created once (the no-overwrite `head_object`); the three source-absent days are never filled.
- **Honest limits, signed on:** no plan has ever run; the python3.12 memory is unmeasured and Act 2's `Max Memory Used` is the first reading (above 717 MB, Act 3 does not start and the next change is the one memory line); the role's reads of every input are first read at Act 2; the backfill builds every day on the newest `account_dim` households.
- **Not covered:** enabling the schedule; any change to an input table or to the 49 Financial roots; any portal reader of the new partitions; a sidecar of any kind; the report's wording of the unreported-day statement.

## 5. Both branches

Branch A: the event returns counts and the statement; the after-read records memory, duration and the object count. Branch B: a refused or landed day writes nothing and the chain goes on. Branch C does not arise (one object per day). Branch D: out of memory or time before the put, nothing is written. Branch E: a broken chain resumes at the oldest owed day on the next `{}` event.

## 6. Conditions of this half

0. **Act 1 step 0:** read the layer `irpt-performance-native-layer` live, confirm it carries pyarrow for python3.12 and is the version the sibling runs, else STOP. 1. **Ledger first,** bound to the packet's sha256 (`irpt-dashbd-cottonwood-reporting-gold-20261015`; legs git, build, terraform, dry run, backfill); `.open_deploys/` read across every live worktree with the denominator printed. 2. **Live state re-read at the moment of the apply** and equal to the packet's section 3, else STOP. 3. **The plan read first:** exactly 7/0/0 on the seven addresses, else STOP; the build line equal to the packet's `NGt2VnH3GioITy+bGudgPiiSGCluX7wvz3MGb3nR6Es=` or STOP. 4. **Each event only after the previous leg's after-read is recorded in the ledger;** stop at once on a `Max Memory Used` above 717 MB, a timeout, an `AccessDenied`, or a skipped day other than the three absent days and 2026-07-10. 5. **No `update-function-code`, no bare `terraform apply`, no schedule change, no wildcard delete.** 6. **The applier is an AE seat the gates admit, not a worker.** 7. **The receipt** to `1.0.0_SA_CTO~DELL1` through `0.0.0_AB_MSTR~DELL2` after Act 2 passes (packet section 8, item 6).

## 7. The questions, from this seat (the CTO's half decides them)

1. **A dry run first, then the backfill, in this pair:** ACCEPT as written; the dry run proves the load and the role's reads before any object exists, and the stop conditions bound each real event.
2. **python3.12 memory:** ACCEPT 1,024 MB with the dry run's `Max Memory Used` as the first reading and the one-line raise as the remedy.
3. **Newest `account_dim` households for every backfilled day:** ACCEPT for the backfill; it is the handler's design and the local feasibility run measured it (220 households, 854 accounts).

-- 2.0.0_SA_COO~D2
