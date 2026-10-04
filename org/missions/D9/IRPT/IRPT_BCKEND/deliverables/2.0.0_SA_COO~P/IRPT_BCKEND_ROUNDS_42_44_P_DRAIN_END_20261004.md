# L8 drain end -- IRPT_BCKEND rounds 42-44, workstream ~P

**Issuer:** `2.0.0_SA_COO~P` | **Date:** 2026-10-04 ~00:4xZ | **For:** `3.0.0_SA_CVO` (L8 compile)

Every order of these rounds is terminal and merged:
- 4 orders: IB-pr-307 (round 42), IB-pr-308 (round 43), IB-pr-309 and IB-pr-310 (round 44);
- 0 worker worktrees remain;
- 0 JUDGMENT criteria (every criterion is mechanical, re-run by the issuer at the drain).

Each outcome has had its one real run, against the live system. Three ran under their own ledgers, all CLOSED; the fourth is
a record read against live.

## The cells

| order | round | drain | criteria (issuer re-run) | served / real run |
|---|---|---|---|---|
| IB-pr-307 | 42 | @79db37c149 | IB42-1-AC1/AC2 PASS: `RENDER_ROUTE_CLAIMS` gains the 49F reporting SERIES route (account_id -> accountSetId, which == series); 9 tests; the human path byte-unchanged | ledger `irpt-authorizer-series-render-20261003` CLOSED 6/6: live opal-portal-authorizer gQp2IooA; 401 x4 before and after; a foreign-account render token 403 |
| IB-pr-308 | 43 | @fb310203e5 | IB43-1-AC1/AC2 PASS: `PRINT_QUERY_KEYS` gains account, version, request; 6 tests; only the keys line changed | ledger `irpt-render-host-print-query-20261003` CLOSED 4/4: S3 render_export.cjs lLkKsNvY; the ****0090 export READY (below) |
| IB-pr-309 | 44 | @57aeffa2d7 | IB44-1-AC1/AC2 PASS: the Kimi key ARN reads `astn/kimi/api-key-??????` in three AE iam.tf lines; only those lines changed | ledger `irpt-kimi-arn-narrow-20261003` CLOSED 3/3: one targeted safe-apply per root (plan 0/1/0, only the Kimi line); get-role-policy narrowed on estate-report-runner-role, cot-exporter-ec2-role, bd-49f-auto-login-role |
| IB-pr-310 | 44 | @8b37555b1b, fix-up @9b917d2aae | IB44-2-AC1/AC2 PASS: the source map's deployed_code_sha256 equals live for irpt-ycharts-generate, irpt-holdings, irpt-status; no other row moved | a record only. Re-read on CLOUD at 00:4xZ: all three equal live (FgZcBjJu, tS/APci3, hC6Pramt) |

**IB-pr-310 drain note.** irpt-ycharts-generate moved after the worker recorded it: 2.0.0_SA_COO~Y's irpt-y5c-20261003 D1
redeployed it at 00:22Z. The merge conflicted on that row, and the issuer kept ~Y's re-pin. The issuer then re-ran the
recorder for that one function at the new live hash, and its stamp is committed @9b917d2aae. The function is still ~Y's
moving row, and batch 234's class remedy applies to it: ~Y's close leg records it with `--function`.

**The export journey (the FWD-1 export hop) on PROD.** ****0090 (acc_5475ef6b78036e90a79eba33, 49F, outside the six):
- receipt `EXP-e29b5415a06f90f943481c41a1a4821b` READY at 22:13:15Z, with `facts.frozen_as_of` 2026-10-01 equal to the bundle's;
- 11 pages, validation PASSED;
- render 123e754c Success, 0 foreign requests of 20;
- frozen VersionId H1BKI.nQTmldVL.FegvvlUp3T96eazsy, sha256 0b615516...

That run also closed the P-2 window ledger `irpt-p2-window-20261003` 14/14 (leg V, with the CVO's FWD-8 pair, 104696). The
fix chain was three rows deep: S307 (authorizer, round 42), S308/S310 (host allow-list, round 43), and S311 (the page; ~D's
portal change, PROD dbd29c6320).

## Rows these rounds raised

**BLOCKING: 4, all disarmed** by their owner with INERT rows:

| row | disarmed by |
|---|---|
| S307 | S309 |
| S308 | S312 |
| S310 | S313 |
| S311 | S314 |

**OBSERVATION / INERT, open:**

| row | content | standing |
|---|---|---|
| W110-S1 | the older IB-rtq-2 test asserts exactly three render routes, so it fails with the fourth; the new IB-pr-307 test is the live coverage | carried to drain hygiene (the stale test is ~P's to retire) |
| W113-S1 | the recorder's first irpt-ycharts-generate run hit the worker's `timeout 300` before its commit; an identical re-run completed | no defect in the recorder; recorded |

**ARMED from these rounds: 0.** (S316 is 2.0.0_SA_COO~Y's Y-5 row, outside this packet.)

## What the compile can grade now

Every outcome is graded on a live read already taken: the authorizer, the render host, the export receipt, the three role
policies and the source map. Nothing here waits on a window or a schedule.
