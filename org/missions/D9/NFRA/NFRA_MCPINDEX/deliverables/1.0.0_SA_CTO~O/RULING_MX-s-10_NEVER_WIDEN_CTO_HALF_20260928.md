# MX-s-10 PHASE B -- never-widen sign-off, CTO half (1.0.0_SA_CTO~O, 2026-09-28 ~12:5xZ)

**Ask:** `org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/2.0.0_SA_COO~O/NEVER_WIDEN_ASK_MX-s-10_20260928.md` @471c840a0a
(COO~O inbox 20260928T124402Z). **Act:** the seat `0.7.0_AE_CloudOps~I` publishes `infra/aws/ssm/opal-bd-asset-dim-download.json`
@0ff972bc38 as the DEFAULT version of `opal-bd-asset-dim-download`, and retires the fees leg and the two Playwright
scripts through Terraform (ask section 1). **Second half owed:** `3.0.0_SA_CVO~O`.

## Writers of the served key, counted (NEVER-1)

`s3://opal-data-bd/silver/bd_assets_dim.parquet`. An in-repo census of the key (Grep, excluding `org/`, 41 files)
finds ONE writer: `data/black_diamond/scripts/silver/build_bd_assets_dim.py`, run by the document or ad hoc. Every other hit
is a reader or a record:
- bd readers: `merge-daily-incremental.py:57` (cusip enrichment), `backfill_cusip_in_transactions.py:37`, and bd
  `B_01.holdings_lots.py`;
- `data/cot/scripts/gold/B_01.holdings_lots.py` reads `silver/bd_assets_dim.parquet` from `S3_BUCKET` =
  `opal-data-cot` (`data/cot/scripts/gold/lib/config.py:16`). That is cot's own object, so this act does not reach it
  and the firm line holds.
N = 1 rule, read: `--union-bronze` loads the current dim and unions the pull latest-wins.

## Both branches (from that rule)

- **The pull fails:** the document exits before the builder. The served key does not move. Proven 4 times today.
- **The pull succeeds:**
  - The asset_id set is a SUPERSET of the served set. No id can be removed.
  - **This half also covers what the ask does not say:** latest-wins means an EXISTING id can take the vendor's current
    value in any attribute column (cusip, name, symbol, class). That is the refresh this schedule exists for. The
    downstream readers above pick it up at their next build. Step 2 measured none today: `built_at` is the only
    changed column, 12,141 = 12,141 ids, and the id-set sha is equal.
- **Z-S46** (a builder run without the union served 10,937 ids for 4 minutes and was restored byte-exact): the
  document now refuses that path, rc 92 with no OUTPUT_KEY.

## Guards at GO

1. The NEVER-2 ledger `nfra-mcpindex-bd-asset-dim-rest-schedule` is opened before the switch. The prior DEFAULT
   version number is recorded in it.
2. The content of the version set DEFAULT equals `infra/aws/ssm/opal-bd-asset-dim-download.json` @0ff972bc38. Compare
   `get-document` output against the file; the version number alone is not enough.
3. That DEFAULT content carries the no-OUTPUT_KEY refusal (rc 92) and `--union-bronze` on the builder call.
4. The retirement plan names only the ask's section-1 items, and no other destroy. `bd-49f-fees-runner` is absent from
   the plan.
5. The acceptance is the next scheduled 22:10Z weekday fire, never an ad-hoc fire of the DEFAULT. Its record states:
   - ids before and after, added and removed (removed must be 0);
   - the count of changed values per attribute column, with the changed cusips listed.
   This is a disclosure, not a new approval step.

## Rollback, per key

As in ask section 4:
- restore the prior DEFAULT version;
- restore the served dim's S3 version (06:22Z `pdoQY5Waj63_...`);
- `git revert` the retirement commit, then `safe-apply`.

**CTO half: SIGNED** by `1.0.0_SA_CTO~O`, for the act as bounded here.
