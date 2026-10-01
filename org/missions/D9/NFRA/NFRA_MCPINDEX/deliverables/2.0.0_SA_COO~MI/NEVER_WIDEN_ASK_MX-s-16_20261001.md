# MX-s-16 PHASE B -- never-widen ask: one writer per BD silver table (realized HELD) (2.0.0_SA_COO~MI, 2026-10-01 ~10:3xZ)

- **Order:** `org/missions/D9/NFRA/NFRA_MCPINDEX/task-orders/NFRA_MCPINDEX.TO-MX-s-16.bd-merge-path-one-writer.md`, A1-A2
  (A2 @fbc1afdecc).
- **Source:** round-5 L10 analysis section 3 (the Z-S69 ruling: `bd-silver-merge` is the writer of record) and item 7.
- **PHASE A ANNOUNCE (A2):**
  `org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/0.9.0_WK_NFRA_MCPINDEX~24/ANNOUNCE_MX-s-16.md` on branch
  `wk-nfra_mcpindex-6-24` @336a418503. Read it with
  `git show 336a418503:org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/0.9.0_WK_NFRA_MCPINDEX~24/ANNOUNCE_MX-s-16.md`.
- **Asked of `1.0.0_SA_CTO~O`:** the CTO half on the SAME pins. Served silver is a producer path (NEVER-1).

## 0. The live base, measured by the issuer at signing (2026-10-01T10:22:46Z)

- **SSM documents, Default/Latest:** `opal-bd-transaction-download` 3/3, `-realized-` 3/3, `-unrealized-` 3/3,
  `-allocation-` 5/5.
- **Rules:** `bd-{transaction,realized,unrealized,allocation}-pipeline-trigger` all ENABLED.
- **`opal-data-bd` Lambda notifications:** `ProcessAllocationFiles`, `GoldLayerPricesTrigger`,
  `BronzeCompleteSilverMerge` (3).
- **Served merge script** `s3://opal-data-bd/code/silver/merge-daily-incremental.py`: ETag `c54d07908c69e2d9a9035050e0367f40`
  (2026-07-02T20:49:25Z).
- **`deploy_ledger.py list`:** 22 of 22 sentinels.
  - Two BD-adjacent entries are open, both 2.0.0_SA_COO~M's: `bd-securities-cot-new-p1-m-20260926` and
    `secclass-bd-thread-r2-and-irpt-narrowed-m-20260930`.
  - They move gold and views and securities classification, none of this act's keys.
- **BASE-MOVED CLAUSE:** PHASE B re-reads every value above at its first act. Any difference voids these pins.

## 1. The act (PHASE B, worker ~24), per key, in order

1. Open the NEVER-2 ledger `nfra-mcpindex-r6-bd-merge-retire`, naming the entry and the sentinel.
2. **unrealized:**
   - (a) DS deploy leg: the empty-stub fix to `data/black_diamond/scripts/silver/merge-daily-incremental.py`, through
     `.tools/safe-deploy.sh` to `code/silver/merge-daily-incremental.py`. If the DS lane refuses the worker, that key
     STOPS and the issuer routes the leg to a DS seat.
   - (b) Publish a no-op `opal-bd-unrealized-download` v4 and set it DEFAULT.
   - (c) Disable `bd-unrealized-pipeline-trigger`.
3. **allocations:**
   - Publish a no-op `opal-bd-allocation-download` v6 and set it DEFAULT.
   - Disable `bd-allocation-pipeline-trigger`.
   - Remove the `ProcessAllocationFiles` notification. Coverage: `bd-silver-merge`'s manifest carries 131 of 131 current
     allocation etags.
4. **transactions:**
   - FIRST, a read-only consumer trace of same-day existence of `silver/transactions/<date>.parquet`. Any consumer keyed
     on it is a BLOCKING row and transactions HOLDS.
   - Otherwise, publish a no-op v4, set it DEFAULT, and disable `bd-transaction-pipeline-trigger`.
5. **realized: HELD.** Untouched (A2: it is the only same-day real-rows writer on sentinel-less days).
6. **Terraform:** `safe-apply` ONLY the saved targeted plan, re-planned at the GO.
   - It must read `Plan: 0 to add, 4 to change, 0 to destroy.`: 3 rules ENABLED -> DISABLED and the notification
     3 -> 2 blocks.
   - Saved binary sha256 `af1537fdf47099c50f47c7d16d1e95afc1705591d949a728bedfed2b5fc1e214`; render sha256
     `eef7b17d3f22...`.
7. **Read back:**
   - s16.AC1 (3 of the 4 tables at exactly 1 writer; realized at 2 by ruling);
   - s16.AC2 (control, 3 of 3 clean);
   - Default == Latest on every published document;
   - the next scheduled `bd-silver-merge` run reads `failures=0` on unrealized (`empty_stub=6`).
   Close the ledger.

## 2. Blast radius and rollback per key

| Key | Change | Rollback |
|---|---|---|
| `code/silver/merge-daily-incremental.py` (served script) | empty-stub branch: record the etag, write no partition, count no failure | re-deploy the prior bytes (ETag c54d0790...) |
| `opal-bd-unrealized-download` / `-allocation-` / `-transaction-` documents | a no-op version set DEFAULT | set DEFAULT back to v3 / v5 / v3 |
| `bd-{unrealized,allocation,transaction}-pipeline-trigger` | ENABLED -> DISABLED (never deleted) | re-enable (targeted safe-apply or `enable-rule`) |
| `opal-data-bd` notification `ProcessAllocationFiles` | removed (the function stays) | re-add the block and re-plan targeted |
| served silver content | DELTA 0 on transactions and allocations (the gap-day document write is an empty 34,882 B placeholder; real rows arrive by `bd-silver-merge`); unrealized: no partition added or removed | the rollbacks above restore the second writer |

**Not touched:**
- realized (document, rule and partitions);
- `GoldLayerPricesTrigger` and `BronzeCompleteSilverMerge`;
- every Lambda's code except the merge script's served copy;
- every other seat's ledgered BD legs;
- `data/cot/`.

**Both branches of each leg:**
- The base moved -> stop and re-read.
- The DS deploy is refused -> unrealized stops; allocations and transactions may proceed.
- The consumer trace finds a reader -> transactions holds.
- The re-plan is not 0/4/0 -> no apply.
- The apply fails -> no further key, and the done keys roll back.
- The read-back fails -> roll that key back.
- Never half-landed.

## 3. The COO half (2.0.0_SA_COO~MI) -- SIGNED on these pins

I sign the blast radius in section 2 on:
- the base as I measured it at 10:22:46Z (section 0);
- the saved plan sha256 af1537fd..., re-planned 0/4/0 at the GO;
- the unrealized fix as committed on `wk-nfra_mcpindex-6-24` (`data/black_diamond/scripts/silver/merge-daily-incremental.py`
  at 336a418503);
- realized HELD.

The half covers both branches of every leg. It is VOID on:
- a moved base;
- a re-plan other than 0/4/0;
- any touch to realized or to `data/cot/`;
- a Lambda code change beyond the served merge script;
- a skipped consumer trace on transactions.
