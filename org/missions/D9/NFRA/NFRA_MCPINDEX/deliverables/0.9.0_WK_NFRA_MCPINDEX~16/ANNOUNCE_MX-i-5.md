# ANNOUNCE_MX-i-5 -- PHASE A result (worker 0.9.0_WK_NFRA_MCPINDEX~16)

**Nothing was applied and nothing was changed.** No Terraform edit, no plan file, no ledger. Phase B does not start on this result.

## Proof table (per DOCUMENT, per STEP; full tables in `DEAD_PROOF_MX-i-5.md`)

Predicate (issuer ruling ~06:2xZ): a document with ANY step that writes since LAST_NON_FAILING is LIVE. LAST_NON_FAILING is 2026-06-22 in all 4 (S3 log-object grain, latest version per key).

| rule | SSM grain (N=21) | log grain FIRST_FAILING / LAST_NON_FAILING | step 3 download writes | step 4 merge writes since 2026-06-22 (own window: silver + manifest) | last row-bearing own silver write | VERDICT |
|---|---|---|---|---|---|---|
| bd-allocation-pipeline-trigger | Failed 21 of 21, log FAIL 21 of 21 | 2026-06-23 / 2026-06-22 | 0 | 9 + 4 = 13 (none after 2026-07-03T22:00:50Z) | 2026-07-02 (6,828 rows) | LIVE |
| bd-realized-pipeline-trigger | Failed 21 of 21, log FAIL 21 of 21 | 2026-04-22 / 2026-06-22 | 0 | 35 + 31 = 66 | 2026-09-28 (11,298 rows) | LIVE |
| bd-transaction-pipeline-trigger | Failed 21 of 21, log FAIL 21 of 21 | 2026-02-21 / 2026-06-22 | 0 | 35 + 31 = 66 | 2026-07-17 (3,696 rows); zero-row since | LIVE |
| bd-unrealized-pipeline-trigger | Failed 21 of 21, log FAIL 21 of 21 | 2026-04-22 / 2026-06-22 | 0 | 277 + 50 = 327 | 2026-07-02 (103,080 rows); zero-row since | LIVE |

In all 4, every one of the 70 dated logs after 2026-06-22 records `Download exit code: 1` and `Merge exit code: 0`. The download is dead; the merge runs and writes.

Attribution is INFERRED from time of day (bronze producer lands 00:00-01:30Z; the leg fires 21:38-22:00Z), not from a principal.

## The plan's resource list

0 to add, 0 to change, 0 to destroy. **No rule is proposed for DISABLED.** AC2's "4 to change" and AC3's "OUTPUT_SINCE_LAST_NON_FAILING: 0" cannot be met as written; row `NFRA_MCPINDEX-Z-W16-S1` records the measurement.

## For the issuer's ruling (not decided here)

- allocation: no own-window write of any kind for 88 days (last 2026-07-03T22:00:50Z). It reads LIVE only because the window starts at 2026-06-22.
- unrealized: own-window writes since 2026-07-02 are zero-row partitions (six stale keys, rewritten daily) and its manifest.
- Either is a candidate for a narrower rule if the issuer rules zero-row and state-file writes are not "live output". A plan for a subset is one Terraform edit and one `terraform plan` away; it was not prepared because the order forbids disabling a leg that is not proven dead.

## Rollback

Nothing to roll back. If the issuer later disables a subset, the rollback per rule is: set that rule's `state` back to `"ENABLED"` in `infra/aws/terraform/bd-pipeline/eventbridge.tf`, then `safe-apply`.

## Negative control

`bd-asset-dim-pipeline-trigger` ENABLED, untouched.
