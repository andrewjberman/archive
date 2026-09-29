# CARD -- row W2-S6: 8 probe fixtures in the production table `gateway-access-state-table`

For Andrew's confirmation. **Nothing was deleted.** A delete in a production store needs his word; this card only prepares it.
Prepared by 0.9.0_WK_NFRA_OPLGTW~13 under OG-h-1 item F.

## What was read

One read-only `dynamodb scan`, region us-east-1, `--projection-expression "pk, sk"` (no other attribute was requested or printed), 2026-09-29.

- Items scanned (the denominator): **203** (`Count` 203, `ScannedCount` 203, no `LastEvaluatedKey`, so the scan is complete).
- Items whose pk contains `probe-og-`: **8**.
- Items that are not probe fixtures: **195** -- count only, keys not listed.
- Reconciliation: 8 matches the 8 items recorded on 2026-09-18. One `describe-table` read (an extra call beyond the Scan) returned `ItemCount` 198 for the same table; DynamoDB refreshes that figure only about every six hours, so the scan count is the one to trust.

## The 8 probe items (literal pk / sk)

| # | pk | sk |
|---|---|---|
| 1 | `POLICY#probe-og-i1-20260916T000402023004Z` | `AUDIT#0001` |
| 2 | `POLICY#probe-og-i1-20260916T000402023004Z` | `AUDIT#0002` |
| 3 | `POLICY#probe-og-i1-20260916T000402023004Z` | `PROFILE` |
| 4 | `POLICY#probe-og-i1-20260916T000658709747Z-race` | `AUDIT#0001` |
| 5 | `POLICY#probe-og-i1-20260916T000658709747Z-race` | `PROFILE` |
| 6 | `POLICY#probe-og-i1-20260916T000705463912Z-ttl` | `AUDIT#0001` |
| 7 | `POLICY#probe-og-i1-20260916T000705463912Z-ttl` | `PROFILE` |
| 8 | `RUNTIME#probe-og-i5-20260917T140533Z` | `AC9` |

## The exact delete command per key (NOT run)

Each removes one item by its full primary key. `attribute_exists(pk)` makes a re-run a no-op error instead of a silent success on an absent key.

```
.tools/aws dynamodb delete-item --region us-east-1 --table-name gateway-access-state-table --key '{"pk":{"S":"POLICY#probe-og-i1-20260916T000402023004Z"},"sk":{"S":"AUDIT#0001"}}' --condition-expression 'attribute_exists(pk)'
.tools/aws dynamodb delete-item --region us-east-1 --table-name gateway-access-state-table --key '{"pk":{"S":"POLICY#probe-og-i1-20260916T000402023004Z"},"sk":{"S":"AUDIT#0002"}}' --condition-expression 'attribute_exists(pk)'
.tools/aws dynamodb delete-item --region us-east-1 --table-name gateway-access-state-table --key '{"pk":{"S":"POLICY#probe-og-i1-20260916T000402023004Z"},"sk":{"S":"PROFILE"}}' --condition-expression 'attribute_exists(pk)'
.tools/aws dynamodb delete-item --region us-east-1 --table-name gateway-access-state-table --key '{"pk":{"S":"POLICY#probe-og-i1-20260916T000658709747Z-race"},"sk":{"S":"AUDIT#0001"}}' --condition-expression 'attribute_exists(pk)'
.tools/aws dynamodb delete-item --region us-east-1 --table-name gateway-access-state-table --key '{"pk":{"S":"POLICY#probe-og-i1-20260916T000658709747Z-race"},"sk":{"S":"PROFILE"}}' --condition-expression 'attribute_exists(pk)'
.tools/aws dynamodb delete-item --region us-east-1 --table-name gateway-access-state-table --key '{"pk":{"S":"POLICY#probe-og-i1-20260916T000705463912Z-ttl"},"sk":{"S":"AUDIT#0001"}}' --condition-expression 'attribute_exists(pk)'
.tools/aws dynamodb delete-item --region us-east-1 --table-name gateway-access-state-table --key '{"pk":{"S":"POLICY#probe-og-i1-20260916T000705463912Z-ttl"},"sk":{"S":"PROFILE"}}' --condition-expression 'attribute_exists(pk)'
.tools/aws dynamodb delete-item --region us-east-1 --table-name gateway-access-state-table --key '{"pk":{"S":"RUNTIME#probe-og-i5-20260917T140533Z"},"sk":{"S":"AC9"}}' --condition-expression 'attribute_exists(pk)'
```

## What Andrew is approving

- Blast radius: exactly these 8 items, by full key. No `pk` prefix delete, no scan-and-delete.
- Rollback: none by command. The items are synthetic round-1 probe fixtures (`probe-og-i1-*` policy, audit and profile rows; `probe-og-i5-*` runtime row); if one were needed again the probe that wrote it is re-run. No point-in-time-recovery state was read.
- The command runs under `Andrew_Berman`; the Gateway role is not involved.
