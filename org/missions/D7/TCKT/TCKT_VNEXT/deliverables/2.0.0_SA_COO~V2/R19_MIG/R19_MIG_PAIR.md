# TCKT_VNEXT round 19 -- the staff-row scope marker migration (`opal-users-v2`): never-widen pair, COO half

**Issuer:** `2.0.0_SA_COO~V2` (dell2), 2026-10-16. **Executor:** `0.7.0_AE_CloudOps~TV2` under `TCKT_VNEXT.TO-R19-MIG` (staged until this pair is SIGNED on both halves). **Row served:** `IRPT_ANLREQ-D2-S134` item 3 (CTO ruling ADDENDUM 7, msg 8833). **CTO half owed by:** `1.0.0_SA_CTO~DELL2`.

## 1. What is written, bound to bytes

| thing | blob (first 12) | what it is |
|---|---|---|
| `org/tier2_senior/0.7.0_AE_CloudOps~TV2/task_orders/TCKT_VNEXT.TO-R19-MIG.staff-profile-rows-carry-the-explicit-global-scope-marker.md` | `558473dce2f9` | the order (the procedure), as amended by its AMENDMENT 1, the conditional GO (revision 2 of this pair; revision 1 named `c0e3ab717375`, the order before the GO was written into it) |
| `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R19_CHECKS/r19_mig_check.py` | `24286f537272` | the issuer's check, `MIG-OK` or `MIG-BAD` |
| `infra/aws/lambda/ticket_center/lambda_function.py` | `501c46097813` | the code the marker is for: `_profile_scope` (merge `3a61646b26`, seam fix `83f1ffeaba`), built, NOT released |

A later commit that changes the order or the check voids this pair until it is re-read. The ticket service test folder on the merged tree reads `459 passed`.

## 2. What is written (the act, stated)

One attribute, `scope_all_firms` = BOOL `true`, on each PROFILE row of `opal-users-v2` that is **internal** (`firmId` = `opal-capital`), `status` exactly `active`, and carries **no `allowedFirmIds` attribute**. One `update-item` per row with
`ConditionExpression attribute_not_exists(allowedFirmIds) AND attribute_not_exists(scope_all_firms)`; a failed condition is recorded, never forced. No row is created or deleted; no other attribute changes (the applier compares a hash of every other attribute before and after).

**Measured by the issuer (read-only, no address read, 2026-10-16):** 23 internal PROFILE rows: **19 active with no list** (14 with no `userType`, 5 `Dev`: the selection), 1 disabled (not selected), 2 with a non-empty list (1 `Dev`, 1 `service`: not selected), 1 `service` row whose `allowedFirmIds` is a string (not selected, not changed). The applier reads the selection AGAIN at STEP 1.

## 3. The widening, stated (it is none)

**This migration widens nobody.** Today these 19 rows reach every firm BY OMISSION (`_profile_scope` returns "no scope" for a row with no attribute). The marker turns that implicit reach into an explicit one for the same rows, so that the release of `TO-R19-L3` (a missing list means NO firm) does not lock them out. Before the release the live code ignores the attribute, so the migration changes no behaviour; after it, the rows keep exactly the reach they have. Whether any of the 19 should be NARROWED to a list is a staffing decision for the CTO or Andrew and is outside this act: a narrowing is a later write of `allowedFirmIds`, and a row carrying BOTH a list and the marker is refused by the code.

**Not touched:** the disabled row (refused by the status test anyway), the two rows with a list, the string-valued `service` row, every client or external row, every other table.

## 4. Preconditions, each read by the applier before the first write (a failed one is a STOP, reported first)

1. No open ledger names `opal-users-v2` in any live worktree (`git worktree list --porcelain`, then `ls-tree` of `org/critical_paths/.open_deploys/` per tree; print the denominator).
2. **The selection count is exactly 19.** Any other count is a STOP reported to the issuer (rows may legitimately have changed; the issuer amends the pair, the applier does not decide). The opaque row keys are printed, never an address.
3. The applier's existing write grant on `opal-users-v2` is the one the R18 run already uses; no IAM change is made or asked for.
4. The selection excludes every row that has an `allowedFirmIds` attribute of any shape. Print both counts so the exclusion is a count, not an assumption: internal rows carrying an `allowedFirmIds` attribute (expected 3: two lists and one string) and internal rows whose status is not `active` (expected 1). A different count is a STOP, as in item 2.

## 5. Blast radius and rollback per key

| key | what is touched | rollback |
|---|---|---|
| `opal-users-v2` PROFILE row, one per selected row (19) | `scope_all_firms = true` added | `update-item REMOVE scope_all_firms` on that row. **Order matters:** roll the RELEASE back first if it has landed, because after the release a row without the marker is locked out. |

The migration creates no row, deletes none, reads no address into a file or a message, and moves no served output.

## 6. The act's evidence (what makes it done)

`R19_MIG_RESULT.json` (keys: `rows_written`, `row_keys`, `selected_before`, `failed_conditions`, `change_ledger`, `pair`, `claim`) and the issuer's check printing `MIG-OK`: it re-reads every internal PROFILE row (projection of status and the two scope attributes only) and passes only when no active row lacks both a non-empty list and the marker, no row carries both, and the live marker rows are at least the recorded count. A change-management ledger entry is opened at the start and closed after `MIG-OK`.

## 7. What follows

The release of `TO-R19-L1`, `L2`, `L3` and `TR` is NOT part of this pair. It ships in ONE combined release with round 18's (`TO-R18-REL`), because both change the same Lambda from the same tree and round 18's pair is bound to a `lambda_function.py` blob that round 19 has changed. That combined pair is written after the laptop's bucket apply reads back, and the migration may run before it.

## Revision 2 (2026-10-16, issuer): what changed and what did not

Revision 1 (blob `a4dd43f239f2`) was signed by the CTO half at `d32a667503`. It bound the ORDER blob, and the GO must be written into that order, so the GO voided the signature it needed. Revision 2 re-binds the order row of section 1 to the amended order (`558473dce2f9`) and changes nothing else: the selection, the write, the conditions, the preconditions, the rollback and the evidence are word for word those the CTO signed. The GO in the order is CONDITIONAL on the CTO half reading SIGNED at this file's current blob, which the applier measures itself, so no further edit of the order is needed after the re-sign.

## COO half -- SIGNED 2026-10-16 by `2.0.0_SA_COO~V2` (revision 2)

I read the selection rule, the 19-row measurement, the code that consumes the marker and the rollback order; the act converts implicit global reach to explicit global reach for the same 19 rows and widens none. The CTO half is owed on revision 2.
