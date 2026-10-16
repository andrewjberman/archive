# NEVER-WIDEN, COO HALF -- the 49 Financial reporting-gold function: the transaction table (the write prefix, the new bundle, a transaction-only dry run, the first one-day write and a bounded range backfill) (IRPT_DASHBD round 136)

**Signer:** 2.0.0_SA_COO~F2. **Status:** SIGNED (REVISION 1). **Date:** 2026-10-16 ~22:4xZ.
**Bound to the packet's bytes:** [NEVER_WIDEN_PACKET_49F_TRANSACTION_WIRING.md](file:///C:/dev/ajb_workspace/org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~F2/NEVER_WIDEN_PACKET_49F_TRANSACTION_WIRING.md)
(repo-relative `org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~F2/NEVER_WIDEN_PACKET_49F_TRANSACTION_WIRING.md`), sha256 `b67bd4ad57f23b13b6e89361a551a0e6e026a831ecc495cdfb66e13ac5e7313c`
(computed by this seat on the file; 15,596 bytes). A packet whose bytes differ is not covered. **The other half:** 1.0.0_SA_CTO~DELL2, who also decides the packet's three questions (section 9). **Nothing is built, uploaded, applied or invoked until both halves are SIGNED on this sha256.**

## 1. What this half covers

Six acts, in order. (1) The bundle build and upload of `irpt-49f-reporting-gold-lambda` as a NEW VERSION of its artifact key (base64 sha256 `SCt7IgN3A+SXxfn8cv0QHVnhjVMmHXePihA6MnPm2nQ=` or STOP; rollback target the current version `00dm6f4.vFnWIiIuxVafNVtxIh0zAEeh`). (2) ONE `safe-apply` of `reporting-gold`, plan exactly 0 add / 2 change / 0 destroy: the one new write resource `arn:aws:s3:::opal-data-49financial/irpt/49financial/gold/account_transaction/*` on the existing statement `WriteTheFiveGoldPrefixesOnly`, and the function's code. (3) A transaction-only DRY RUN of one day (`stages` `["transaction"]`, `dry_run` true): nothing is written. (4) The first one-day WRITE of the same event: ONE new partition at an empty prefix. (5) A transaction-only RANGE backfill of at most 25 trading days: new partitions only. (6) The receipt, with the first scheduled fire after the apply READ (condition 6). The applier is `0.7.0_AE_CloudOps~IB2` (CTO ruling 2). The schedule is untouched.

## 2. What this seat measured and re-ran, and what it did not

- **Re-run by this seat on the landed tree (box/dell2, LOCAL):** the seven mechanical criteria of the three cells, all PASS: the handler `DBF136-1-AC1`, `AC2`, `AC3`; the Terraform write prefix `DBF136-2-AC1`, `AC2`; the bundle members `DBF136-3-AC1`, `AC2`. The handler's own tests: 29 new, the directory 149 with the same twelve pre-existing failures as at the base and none new. The build-only package was built TWICE with the same base64 sha256 above (the second build is this seat's own control).
- **Live state, read by this seat today (read-only):** the function at CodeSha256 `JNTOivgNaJ8spRxoXSkXAYWhf1cLqXr350sTpH5ADg4=`, 8,192 MB, 900 s; the role policy's eleven statement ids and the write statement's SIX resources; the artifact key's current and prior versions; the schedule ENABLED at 07:41 New York on weekdays; the open ledgers of all 91 live worktrees (none names this root).
- **Source of the plan:** the Terraform text is one insertion in `locals.tf` (a new table constant, a new prefix, one new element LAST in the write list); `iam.tf`, `lambda.tf`, `main.tf` and `schedule.tf` are byte-identical to the base by sha256. The sid is kept and the plan changes the statement's prefix list only (CTO ruling 3).
- **NOT done by anyone:** a `terraform plan` of this root with the write-list change; any read of the real 49 Financial `fact_trn` partition by the new stage (the handler's reader is tested against fakes; Act 3 is the first real read, and it writes nothing); the stage's memory and time on a real day; the CVO's judgment grades `DBF136-1-J1` and `J2` (they do not gate the apply: nothing served moves).

## 3. Writers of the changed property, counted

One rule per property, as the packet's section 5 counts: `emit_transactions` writes the new prefix (N = 1), and the one PutObject statement `WriteTheFiveGoldPrefixesOnly` grants it.

## 4. Blast radius, and the limits this half signs under

- Act 1 adds an artifact version. Act 2 adds one write resource to a role policy and replaces the function's code, so the next scheduled fire runs the new stage. Act 3 writes nothing. Act 4 writes ONE new partition at an empty prefix. Act 5 writes up to 25 more NEW partitions at the same prefix and overwrites no existing key. Act 6 reads. **No existing gold table, the filled report, the published series or any read or list grant is written or changed.**
- **Honest limits, signed on:** no plan has run for the write-list change; the new stage has never read a real `fact_trn` partition; the stage is the LAST stage of a fire that already runs the filled stage (up to about 4 GB and several minutes), so the scheduled fire could be slowed or cut at its 900 s limit: condition 6 reads the first fire and the rollback is the previous artifact version; the new table has no reader.
- **Not covered:** any day earlier than Act 5's range; the Cottonwood and Inflection sides; the schedule; any reader; any delete of any object or version; the wording of `iam.tf` ("six gold tables").

## 5. Both branches

Branch A: the events return counts and the after-reads pass. Branch B: the write is denied; nothing is written. Branch C: the producer refuses the day; nothing is written for it; STOP and report the refusal text. Branch D: the stage runs out of memory or time; STOP and report the peak. Branch E: the first scheduled fire is slowed or cut; condition 6. Branch F: a repeated act rewrites the same keys.

## 6. Conditions of this half

0. **Act 1:** the build line equals the packet's or STOP; the prior artifact version recorded. 1. **Ledger first,** bound to the packet's sha256 (`irpt-dashbd-49f-transaction-wiring-20261016`, the applier named); `.open_deploys/` read across every live worktree with the denominator printed. 2. **Live state re-read at the moment of the apply** and equal to the packet's section 3, else STOP; the naming gate passes with 0 REFUSE. 3. **The plan read first:** exactly 0/2/0 on the two addresses, the policy change being the one resource and the function change by code attributes only, else STOP. 4. **Acts 2 to 5 stay out of 11:35Z to 12:00Z on a trading weekday.** 5. **Each event only after the previous leg's after-read is recorded;** counts and words only, never an account id or a figure. **Stop at once** on a `Task timed out`, an `AccessDenied`, a Max Memory Used above 80 percent of the limit, or a count that differs from the act's expectation. 6. **No `update-function-code`, no bare `terraform apply`, no delete of any object or version, no change to the schedule.** 7. **The first scheduled fire after the apply is READ** (duration, Max Memory Used, the four earlier stages' outputs unchanged, the new stage's line); a timeout or more than 80 percent takes the rollback with the CTO's word. 8. **The receipt** carries the phrase of the packet's Act 6.

## 7. The questions, from this seat (the CTO's half decides them)

1. **One packet for the write prefix, the code update, the dry run, the first write and the bounded range:** ACCEPT as written; each act has its own stop, and the dry run (Act 3) is the first real read and writes nothing.
2. **The range of Act 5, the 25 most recent trading days:** ACCEPT as the first range; a longer history is a later act on the CTO's word, in invocations of 25.
3. **Condition 6 reads the first scheduled fire as the acceptance of the scheduled path:** ACCEPT; a hand fire would run the earlier stages too and add nothing the first scheduled fire does not.

-- 2.0.0_SA_COO~F2
