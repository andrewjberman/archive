# NEVER-WIDEN, COO HALF -- the Cottonwood report-build function's code update for the chain cap (IRPT_DASHBD round 141, row IRPT_DASHBD-D2-S95, workstream B-49F)

**Signer:** 2.0.0_SA_COO~D2. **Status:** SIGNED (REVISION 1). **Date:** 2026-10-15 ~22:0xZ.
**Bound to the packet's bytes:** [NEVER_WIDEN_PACKET_COTTONWOOD_REPORTING_GOLD_CODE_UPDATE_CHAIN_CAP.md](file:///C:/dev/ajb_workspace/org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~D2/NEVER_WIDEN_PACKET_COTTONWOOD_REPORTING_GOLD_CODE_UPDATE_CHAIN_CAP.md)
(repo-relative `org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~D2/NEVER_WIDEN_PACKET_COTTONWOOD_REPORTING_GOLD_CODE_UPDATE_CHAIN_CAP.md`), sha256 `0ba134ff507a525437ea18ca93d05f58963505cb8bc0b2454cbff789b044f6ae`
(computed by this seat on the file; 10,230 bytes). A packet whose bytes differ is not covered. **The other half:** 1.0.0_SA_CTO~DELL2, who also decides the packet's three questions (section 9). **Nothing is uploaded or applied until both halves are SIGNED on this sha256.**

## 1. What this half covers

Three acts, in order, by `0.7.0_AE_CloudOps~DB2`. (1) The build-only hash equal to `7FYx8sPkt0I25tZ8POS3HIueH0lJ99aGjppTky9E7DE=`, a member diff against the LIVE artifact that must read exactly one member, `handler.py`, then ONE new version of the existing key. (2) ONE `safe-apply`, plan exactly 0 add / 1 change / 0 destroy on `module.irpt_reporting_gold_iso.aws_lambda_function.this`, the changed attributes exactly `s3_object_version` and `source_code_hash`; read-backs equal to the packet; a post-apply plan with no changes. (3) Three synchronous events that write nothing (`{}`, a dry run of the landed 2026-10-14, and a deliberately refused `chain_left` of 10). The schedule stays DISABLED; the r139 ledger closes after the after-read.

## 2. What this seat measured and re-ran, and what it did not

- **Live state, read by this seat (read-only):** the function's `CodeSha256` `8pQOR3TN3iicEFV53N7Cs0yeensgZhPDd7zEwTZO3Z4=`, 182,268 bytes, last modified 2026-10-15T20:02:24Z; the artifact key holds ONE version; the schedule DISABLED; the filled prefix 65 objects, equal to the printed day list.
- **Re-run by this seat on the landed tree (`24b4b16305` and later):** `DB141-1-AC1..AC3` PASS (the probe drives a whole chain through a fake S3 and a fake lambda client: exactly ten days, the budget one less per hop, a short backlog stopping at its end, an explicit day capped, seven bad budgets refused with zero calls, a dry run chaining nothing), and the earlier rounds' probes (`DB131`, `DB135`, `DB137`, `DB138`) still PASS; `BUILD_ONLY` built here gives the packet's hash. The probe was validated against a scratch reference handler (green) and seven single-fault mutants (all red).
- **Read line by line by this seat:** the handler's `_chain_left`, `chain_next` (the budget in the payload, none left means nothing invoked), `lambda_handler` (validation before any client) and the yang-lambda module (`s3_object_version` and `source_code_hash` from the artifact, so a new artifact version is exactly a 0/1/0 plan).
- **NOT done by anyone:** a `terraform plan` of a code change on this root; a chain under a real backlog on the real runtime (none is owed); the schedule's own event input was not read (it carries no day, so a scheduled fire is an empty event, which the new code bounds).

## 3. Writers of the changed property, counted: N = 1

The function's code is written by `terraform apply` of this root through `safe-apply` reading the artifact's current version. `update-function-code` is forbidden and gated; the artifact's versions are written by `build-and-upload.sh` only.

## 4. Blast radius, and the limits this half signs under

- Act 1 adds one object version to an existing key; Act 2 changes one function's code and nothing else about it; Act 3 writes no object. The filled prefix's 65 objects are not touched by any act; the schedule is DISABLED, so nothing can invoke the function except the applier's three events.
- **Honest limits, signed on:** the plan of a code change on this root has never run; Act 3's refused event errors by design; the cap is proved on the real runtime only for its validation and its empty path, and under a real backlog only in the probe.
- **Not covered:** enabling the schedule; any object write; any change to a role, policy, schedule, layer or memory; deleting the previous artifact version.

## 5. Both branches

Branch A: the diff reads handler.py only, the plan reads 0/1/0 with the two attributes, the events read as stated. Branch B: the diff or the build hash differs, STOP before the upload. Branch C: the plan reads anything else, STOP (the new version is an unreferenced object, the function still runs the old code). Branch D: after the apply, any unexpected error; the previous version stays and the rollback is a new pair.

## 6. Conditions of this half

1. **Ledger:** reuse the open r139 ledger with legs L6 to L9 bound to this packet's sha256; `.open_deploys/` read across every live worktree with the denominator printed; **the gate footprint is copied into the ledger entry before any worktree is removed.** 2. **Live state re-read at the moment of the apply** and equal to the packet's section 3, with `CodeSha256` equal to its live value. 3. **The diff read first:** exactly one member, `handler.py`, else STOP before the upload. 4. **The plan read first:** exactly 0/1/0 on the one address with exactly the two attributes, else STOP. 5. **No `update-function-code`, no bare `terraform apply`, no delete, no schedule change.** 6. **Stop at once** on any error other than Act 3 event (c), a `Max Memory Used` above 717 MB, or any object newer than the apply in the filled prefix. 7. **The AE applier is a seat the gates admit, not a worker.**

## 7. The questions, from this seat (the CTO's half decides them)

1. **A chain under a real backlog is proved in the probe only:** ACCEPT; no backlog exists to run it on, and manufacturing one would mean deleting objects (Andrew's act) or writing a day that was never owed.
2. **A deliberately refused event in Act 3:** ACCEPT; it is the only live proof of the validation and it writes nothing.
3. **This shape as the template for a later handler change:** ACCEPT.

-- 2.0.0_SA_COO~D2
