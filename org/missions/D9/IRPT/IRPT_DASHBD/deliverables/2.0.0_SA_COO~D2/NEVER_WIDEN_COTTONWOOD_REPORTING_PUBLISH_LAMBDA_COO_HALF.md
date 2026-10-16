# NEVER-WIDEN, COO HALF -- the first Cottonwood series publish (IRPT_DASHBD round 147, workstream B-49F + contract): ONE new Terraform root, FOUR new resources, a dry-run event, a one-account upload, then the full upload

**Signer:** 2.0.0_SA_COO~D2. **Status:** SIGNED (REVISION 1). **Date:** 2026-10-16 ~04:3xZ.
**Bound to the packet's bytes:** [NEVER_WIDEN_PACKET_COTTONWOOD_REPORTING_PUBLISH_LAMBDA.md](file:///C:/dev/ajb_workspace/org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~D2/NEVER_WIDEN_PACKET_COTTONWOOD_REPORTING_PUBLISH_LAMBDA.md)
(repo-relative `org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~D2/NEVER_WIDEN_PACKET_COTTONWOOD_REPORTING_PUBLISH_LAMBDA.md`), sha256 `0c9b495ce2f7e347738ad53a643d1f7b19bf48b226258136e84753371cdae463`
(computed by this seat on the file; 14,292 bytes). A packet whose bytes differ is not covered. **The other half:** 1.0.0_SA_CTO~DELL2, who also decides the packet's three questions (section 9). **Nothing is applied and no event is invoked until both halves are SIGNED on this sha256.**

## 1. What this half covers

Four acts, in order. (1) The bundle build of `irpt-cot-reporting-publish-lambda` and ONE `safe-apply` of `infra/aws/terraform/investor-reporting/reporting-publish-iso/` by the AE applier, plan exactly 4 add / 0 change / 0 destroy on the four named addresses, anything else STOPS. (2) ONE synchronous DRY-RUN event `{}`: it writes nothing. (3) Only after (2) passes: ONE synchronous event `{"upload": true, "accounts": ["<one id>"]}`, one account, two objects. (4) Only after (3)'s after-read: ONE synchronous event `{"upload": true}`. No schedule exists.

## 2. What this seat measured and re-ran, and what it did not

- **Live state, read by this seat (read-only):** function, execution role, role policy, log group and artifact key ABSENT; the target prefix `irpt/cottonwood/platinum/reporting/` EMPTY (0 objects, LIST); the platinum tables present are `holdings/` and `holdings_qa/`; the layer at version 1 on python3.12.
- **Re-run by this seat on the landed tree (`220c9c63f3`, tree `8dce40fd77`):** the publisher criteria `DB147-1-AC1..AC3`, the handler criteria `DB147-2-AC1..AC3` and the root criteria `DB147-3-AC1..AC3` PASS in the worker's tree (and `DB147-1-AC2`, `DB147-2-AC1` and `DB147-3-AC1` again on the landed tree), and the series contract criteria `DB146-1-AC1..AC3` PASS. `DB147-3-AC3` read FAIL on the landed trunk only because another seat changed the `irpt-ycharts-generate` entry since the order's base; this seat compared the merge itself: the new entry equals the branch's and every other entry equals the merge's first parent. The round-close check reads MAY-CLOSE.
- **Read line by line by this seat:** `iam.tf` (the five statements), `lambda.tf`, `locals.tf`, `main.tf`; the handler's contract guard, floor, upload switch (`is True`), read-back and summary.
- **NOT done by anyone:** a `terraform plan`; any invocation of the function; its memory on python3.12; the calendar's source on the Lambda.

## 3. Writers of the changed property, counted: N = 1 rule, 1 entry path

One rule writes `irpt/cottonwood/platinum/reporting/` (the handler's `put_object`), entered by a hand invocation only. The prefix is empty, so no existing object can be replaced.

## 4. Blast radius, and the limits this half signs under

- Act 1 changes no served value and writes no object. Act 2 writes nothing. Acts 3 and 4 add objects to an EMPTY prefix: two for one account, then two per published account (at most about 1,958).
- **Honest limits, signed on:** no plan has ever run; the python3.12 memory is unmeasured and Act 2's `Max Memory Used` is the first reading (above 717 MB, Acts 3 and 4 do not start and the next change is the one memory line); the role's reads are first read at Act 2; no reader of the new prefix is established.
- **Not covered:** a schedule; any change to an input table or the 49 Financial roots; any reader; the class object; any delete.

## 5. Both branches

Branch A: the events return counts and the after-reads pass. Branch B: an account refuses, is counted by reason and skipped; refusals above 10 percent stop at Act 2. Branch C: a death between an account's series and manifest leaves a series without its manifest until a re-run, which rewrites both. Branch D: out of memory or time stops further writes. Branch E: a repeated run rewrites the same keys with the same series bytes.

## 6. Conditions of this half

0. **Act 1 step 0:** read the layer live, confirm pyarrow for python3.12 and the version the sibling functions run, else STOP. 1. **Ledger first,** bound to the packet's sha256 (`irpt-dashbd-cottonwood-reporting-publish-20261016`; legs git, build, terraform, dry run, canary, full upload); `.open_deploys/` read across every live worktree with the denominator printed. 2. **Live state re-read at the moment of the apply** and equal to the packet's section 3, else STOP. 3. **The plan read first:** exactly 4/0/0 on the four addresses, else STOP; the build line equal to the packet's `HDgIzQoXMyUNBxeyqgLXcplD1c01QwVsASRoMJbd4hk=` or STOP. 4. **Each event only after the previous leg's after-read is recorded;** counts and words only, never an account id (a hash prefix where a key is named). 5. **No `update-function-code`, no bare `terraform apply`, no delete of any object.** 6. **The receipt** after Act 4 carries the words "NOT a page render" and "no reader of the prefix established".

## 7. The questions, from this seat (the CTO's half decides them)

1. **A one-account canary, then the full upload, in this pair:** ACCEPT as written; the canary checks the contract, the pair, the null income and the size read-back on one account before the rest.
2. **python3.12 memory:** ACCEPT 1,024 MB with the dry run's `Max Memory Used` as the first reading and the one-line raise as the remedy.
3. **Series for every account in the floor-era gold:** ACCEPT; the prefix is new, nothing reads it yet, and the objects are listed-key deletable with Andrew's word.

-- 2.0.0_SA_COO~D2
